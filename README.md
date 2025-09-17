# Wallet Tracker Bot
[![Ask DeepWiki](https://devin.ai/assets/askdeepwiki.png)](https://deepwiki.com/lucidshaya/Wallet-Tracker-Bot.git)

![Wallet Tracker Screenshot](https://raw.githubusercontent.com/lucidshaya/Wallet-Tracker-Bot/main/photo_2025-09-01_12-23-03.jpg)

## Overview

Wallet Tracker Bot is a simple yet powerful Telegram bot designed to monitor Ethereum wallets. Add any Ethereum address to track its ETH balance and associated tokens. The bot can provide on-demand balance updates or actively monitor wallets and send periodic reports.

This bot uses the Etherscan API to fetch real-time blockchain data.

## Features

*   **Add Wallets:** Add multiple Ethereum addresses to your portfolio.
*   **Check Balance:** Instantly check the ETH and token balances for all your added wallets.
*   **Live Tracking:** Start a monitoring service that sends you updates on your wallet balances every 60 seconds.
*   **Simple Commands:** Easy-to-use commands for a seamless user experience.

## Setup and Installation

Follow these steps to get your own instance of the Wallet Tracker Bot running.

### 1. Prerequisites

*   Python 3.8+
*   A Telegram Bot Token
*   An Etherscan API Key

### 2. Clone the Repository

```bash
git clone https://github.com/lucidshaya/Wallet-Tracker-Bot.git
cd Wallet-Tracker-Bot
```

### 3. Install Dependencies

It's recommended to use a virtual environment.

```bash
# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install the required packages
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory of the project and add your API keys:

```
TELEGRAM_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
ETHERSCAN_API_KEY="YOUR_ETHERSCAN_API_KEY"
```

*   **`TELEGRAM_TOKEN`**: Get this from the [BotFather](https://t.me/botfather) on Telegram.
*   **`ETHERSCAN_API_KEY`**: Create an account on [Etherscan](https://etherscan.io/apis) to get your free API key.

## How to Use

### 1. Run the Bot

Start the bot by running the `bot.py` script:

```bash
python bot.py
```

The bot will start polling for messages on Telegram.

### 2. Interact with the Bot on Telegram

Once the bot is running, you can interact with it using the following commands:

*   `/start`
    *   Displays a welcome message.

*   `/addwallet <eth_address>`
    *   Adds a new Ethereum wallet address to your tracking list.
    *   Example: `/addwallet 0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae`

*   `/balance`
    *   Fetches and displays the current ETH and token balances for all your added wallets.

*   `/track`
    *   Starts the live monitoring service. The bot will send an update for your wallets every 60 seconds.

## Dependencies

*   [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot): The wrapper for interacting with the Telegram Bot API.
*   [httpx](https://www.python-httpx.org/): A modern, asynchronous HTTP client for making API requests.
*   [python-dotenv](https://github.com/theskumar/python-dotenv): For managing environment variables.
