import json
import requests
from PIL import Image
from io import BytesIO


def crop_image(image, width_count, height_count, width_offset, height_offset):
    """
    Crops an image based on the specified parameters.

    Parameters:
    image (PIL.Image.Image): The input image to crop.
    width_count (int): The number of images contained width-wise.
    height_count (int): The number of images contained height-wise.
    width_offset (int): The width offset of the output image to be cropped.
    height_offset (int): The height offset of the output image to be cropped.

    Returns:
    cropped_image (PIL.Image.Image): The cropped output image.
    """

    # Calculate the size of each image contained in the original image
    width, height = image.size
    sub_width = width // width_count
    sub_height = height // height_count

    # Calculate the dimensions of the output image to be cropped
    x = width_offset * sub_width
    y = height_offset * sub_height
    w = sub_width
    h = sub_height

    # Crop the image and return the result
    cropped_image = image.crop((x, y, x + w, y + h))
    return cropped_image

if __name__ == '__main__':
    import argparse

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Download card images from Tabletop Simulator saved deck.')
    parser.add_argument('json_path', type=str, help='path to the JSON file containing the saved deck')
    parser.add_argument('output_path', type=str, help='path to the directory where the card images will be saved')
    args = parser.parse_args()

    # Load the input JSON file
    with open(args.json_path, "r") as file:
        data = json.load(file)

    # All the data we care about sits in the first object state
    data = (data["ObjectStates"])[0]

    # Get the CustomDeck object from the JSON
    custom_deck = data["CustomDeck"]

    # Loop through each deck in the CustomDeck object
    for deck_id, deck_info in custom_deck.items():
        # Get the image URL and the crop dimensions from the deck info
        image_url = deck_info["FaceURL"]
        num_width = deck_info["NumWidth"]
        num_height = deck_info["NumHeight"]

        # Download the image from the URL
        response = requests.get(image_url)
        image = Image.open(BytesIO(response.content))

        # Loop through each card in the ContainedObjects array
        for card in data["ContainedObjects"]:
            # Check if the card ID matches the current deck ID
            card_id = card["CardID"]
            if str(card_id)[:3] != str(deck_id):
                continue

            # Calculate the card offset in the deck image
            card_offset = int(str(card_id)[3:])
            card_row = card_offset // num_width
            card_col = card_offset % num_width

            # Calculate the crop dimensions for the card
            width_count = num_width
            height_count = num_height
            width_offset = card_col
            height_offset = card_row
            cropped_image = crop_image(image, width_count, height_count, width_offset, height_offset)

            # Save the cropped image using the card nickname as the file name
            card_nickname = card["Nickname"]
            card_id = card["CardID"]
            filename = f"{args.output_path}/{card_id}_{card_nickname}.jpg"
            cropped_image.save(filename)
