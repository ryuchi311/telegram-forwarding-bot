# Telegram Forwarding Bot

A Telegram bot that forwards messages, images, videos, and audio to multiple channels. Only authorized users can use the bot for forwarding. The bot also logs errors and notifies the user of specific channels that encounter issues during message forwarding. Built using the `python-telegram-bot` library.

## Features
- Forward text messages, images, videos, and audio to multiple channels.
- Authorization: Only specific users can forward messages.
- Error logging: Logs errors and notifies the user of channels that encounter issues.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.7+
- Telegram Bot Token (You can get this by talking to [BotFather](https://telegram.me/botfather))

### Installing

1. Clone the repository:
    ```sh
    git clone https://github.com/ryuchi311/telegram-forwarding-bot.git
    cd telegram-forwarding-bot
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install python-telegram-bot
    ```

4. Replace `'YOUR_TOKEN_HERE'` with your actual Telegram bot token in the script.

5. Specify the target channels and the authorized username in the script.

### Running the Bot

Run the bot with the following command:
```sh
python bot.py

