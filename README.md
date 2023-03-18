# Tabletop-Simulator-Deck-Image-Extractor

This is a Python script that extracts card images from a saved deck in Tabletop Simulator (TTS) and saves them as separate image files. The script takes as input a JSON file exported from TTS, and uses the image URLs and deck properties specified in the file to crop out individual card images. The output images are saved to a specified output directory.

# Installation
pip install -r requirements.txt


# Usage

Save the deck you want to export in Tabletop Simulator, to do this:

1. Right click the deck.
2. Click save object.

Saved Object are typically located here in windows: **C:\Users\<your_account_name>\Documents\My Games\Tabletop Simulator\Saves\Saved Objects**

To use the script, run it with the input and output paths as arguments:

**python tts_saved_deck_to_images.py input.json output_directory**

The input file should be a JSON file exported from TTS. The output directory should exist and will be used to save the extracted card images.

Cards are named {card_id}_(card_nickname}.jpg
