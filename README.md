# telegram-stars-bot
A bot made with telethon that uses Telegram Stars payments.

# Setup
### Requirements
Make sure you have [Python](https://python.org/downloads) installed.

Now execute this command to install all the packages you need.
```
pip install -r requirements.txt
```
### Config setup

Open the file .env.sample and change `YOUR_API_ID` and `YOUR_API_HASH` with the data that you can find on [my.telegram.org](https://my.telegram.org).

After that change `YOUR_BOT_TOKEN` with the token that you can get with [@BotFather](https://t.me/BotFather).

And now rename the `.env.sample` file to `.env`.

# How to use
After installing all the packages, start the bot by executing this command in the console
```
python main.py
```

# Bot commands
After completing the [setup](https://github.com/RikyPy/telegram-stars-bot?tab=readme-ov-file#setup), you can use the following commands with the bot.

- /start - You can use this command to see if the bot is working, it only sends a greeting.
- /invoice - You can use this command to let the bot send a payment invoice in your chat.
- /refund {transactionId} - If you don't want to lose your stars for testing you can use this command followed by the transaction id you want to refund for getting back your stars.