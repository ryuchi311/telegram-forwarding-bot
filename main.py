from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
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
