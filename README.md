# Telegram Message Forwarding Bot

This Telegram bot allows authorized users to forward messages to specified channels with a confirmation step and delay to prevent spam. The bot supports forwarding text, photo, video, and audio messages.

## Features

- **Authorization**: Only specified users can forward messages.
- **Confirmation Step**: Users must confirm before a message is forwarded.
- **Delay**: A 30-second delay before forwarding to prevent spamming.
- **Logging**: Logs actions and errors for easy monitoring and debugging.

## Prerequisites

- Python 3.8+
- `python-telegram-bot` library
- Telegram bot token

## Setup

1. **Clone the repository**:
    ```sh
    git clone https://github.com/ryuchi311/telegram-forwarding-bot.git
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

# Replace 'YOUR_TOKEN_HERE' with your bot's token
TOKEN = 'YOUR_TOKEN_HERE'

# Define the target channel IDs
TARGET_CHANNEL_IDS = ['@testxpbot11', '@testbot']

# List of authorized usernames (without '@')
AUTHORIZED_USERNAMES = ['chicago311', 'username2', 'username3']

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Dictionary to store the last request time per user to prevent multiple instances
last_request_time = {}

async def forward_post(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Check if the user is authorized
    if update.effective_user.username not in AUTHORIZED_USERNAMES:
        await update.message.reply_text('You are not authorized to use this bot for forwarding messages.')
        return

    # Check last request time to prevent multiple instances
    user_id = update.effective_user.id
    current_time = time.time()
    if user_id in last_request_time and current_time - last_request_time[user_id] < 30:
        await update.message.reply_text('You are sending messages too quickly. Please wait a moment before trying again.')
        return
    
    last_request_time[user_id] = current_time

    # Ask for confirmation
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data=f"confirm_forward:{update.message.chat_id}:{update.message.message_id}"),
         InlineKeyboardButton("No", callback_data="cancel_forward")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Do you want to forward this message?', reply_markup=reply_markup)

async def confirm_forward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data.startswith("confirm_forward"):
        _, chat_id, message_id = query.data.split(":")
        
        # Delay forwarding
        await query.edit_message_text(text="Forwarding message in 30 seconds...")
        await asyncio.sleep(30)

        error_channels = []
        for target_channel_id in TARGET_CHANNEL_IDS:
            try:
                # Forward the message to the target channel(s)
                await context.bot.forward_message(chat_id=target_channel_id, from_chat_id=chat_id, message_id=message_id)
            except Exception as e:
                logger.error(f'Failed to forward message to {target_channel_id}: {e}')
                error_channels.append(target_channel_id)
        
        if error_channels:
            await query.message.reply_text(f'Failed to forward message to the following channels: {", ".join(error_channels)}')
        else:
            await query.message.reply_text('Message forwarded successfully!')

async def cancel_forward(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Message forwarding cancelled.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome! Only authorized users can forward messages using this bot.')

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

# Handle different message types
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_post))
app.add_handler(MessageHandler(filters.PHOTO, forward_post))
app.add_handler(MessageHandler(filters.VIDEO, forward_post))
app.add_handler(MessageHandler(filters.AUDIO, forward_post))

# Handle callbacks for confirmation
app.add_handler(CallbackQueryHandler(confirm_forward, pattern="confirm_forward"))
app.add_handler(CallbackQueryHandler(cancel_forward, pattern="cancel_forward"))

app.run_polling()
