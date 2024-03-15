# Monopoly GO Discord Bot

This Python script is designed to scrape reward links and special event information from the Monopoly GO website and post them to a Discord server.

## Features

- Scrapes the latest reward links and special event information from the Monopoly GO website.
- Formats the scraped data and sends it to specified Discord channels.

## How to Use

1. Replace `'YOUR TOKEN HERE'` in the `TOKEN` variable with your Discord bot token.
2. Replace `00000000` in the `CHANNEL_ID_REWARD` and `CHANNEL_ID_EVENT` variables with the IDs of the Discord channels where you want to post the reward links and special event information, respectively.
3. Run the script.

## Dependencies

- requests
- BeautifulSoup
- json
- datetime
- discord

## Note

This script is intended for educational purposes and should not be used to violate the terms of service of any website or service.