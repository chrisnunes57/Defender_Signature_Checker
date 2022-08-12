# Defender_Signature_Checker

## Purpose

This tool is used to easily search through Microsoft Defender signature releases to find when changes to detections have been made. 

Example use cases:

  - Search for "SmokeLoader" to see the history of when that detection was added, and when it has been updated
  - Search for "Ransom:" to view all ransomware detections
  - Search for ":" to see the most recent detections published

## Usage

0. Run `pip install -r requirements.txt`
1. Run `scraper.py` in order to download all of the most recent updates
    - This will create a file named `update_data.json`
2. In this same directory, run `searcher.py` and you will be prompted for your search query.

## Future

Eventually I want to expand this with some more features, like searching for an update number, result limiting, etc.