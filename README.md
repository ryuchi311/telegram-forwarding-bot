# Telegram Message Forwarding Bot

This Telegram bot allows authorized users to forward messages to specified channels with a confirmation step, delay to prevent spam, and progress reporting. The bot supports forwarding text, photo, video, and audio messages. The bot only interacts with users in direct private messages, ignoring messages from groups.

## Features

- **Authorization**: Only specified users can forward messages.
- **Confirmation Step**: Users must confirm before a message is forwarded.
- **Delay**: A 30-second delay before forwarding to prevent spamming.
- **Progress Reporting**: Shows the progress of forwarding and reports the success or failure of each attempt.
- **Logging**: Logs actions and errors for easy monitoring and debugging.
- **Direct Messages Only**: The bot only replies to direct private messages and ignores group messages.

## Prerequisites

- Python 3.8+
- `python-telegram-bot` library
- Telegram bot token

## Setup

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/telegram-forwarding-bot.git
    cd telegram-forwarding-bot
    ```

2. **Create a virtual environment** (optional but recommended):
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install python-telegram-bot
    ```

4. **Configure the bot**:
    - Replace `'YOUR_TOKEN_HERE'` in the code with your actual Telegram bot token.
    - Update `AUTHORIZED_USERNAMES` with the usernames of users who are allowed to forward messages.
    - Update `TARGET_CHANNEL_IDS` with the channel IDs where messages will be forwarded.

## Usage

1. **Run the bot**:
    ```sh
    python bot.py
    ```

2. **Start the bot in your Telegram**:
    - Send `/start` to the bot to see the welcome message.
    - Send any message type (text, photo, video, audio) to the bot.
    - Confirm the forwarding when prompted.

## Code Overview

```python
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import logging
import asyncio
import time
from telegram.error import TimedOut, NetworkError

# Replace 'YOUR_TOKEN_HERE' with your bot's token
TOKEN = 'YOUR_TOKEN_HERE'

# Define the target channel IDs
TARGET_CHANNEL_IDS = ['@testxpbot11', '@testbot']

# List of authorized usernames (without '@')
AUTHORIZED_USERNAMES = ['chicago311', 'username2', 'username3']
