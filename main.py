#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""Simple inline keyboard bot with multiple CallbackQueryHandlers.

This Bot uses the Application class to handle the bot.
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.

"""
import logging
import os
from dotenv import load_dotenv

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

load_dotenv()
token = os.getenv("BOT_TOKEN")
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Stages
START_ROUTES, END_ROUTES = range(2)
# Callback data
ONE, TWO, THREE, FOUR = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    # Get user that sent /start and log his name
    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)
    # Build InlineKeyboard where each button has a displayed text
    # and a string as callback_data
    # The keyboard is a list of button rows, where each row is in turn
    # a list (hence `[[...]]`).
    keyboard = [
        [
            InlineKeyboardButton("NEXT", callback_data=str(ONE)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_html(
        """
What is Harpie Protect?

Harpie is backed with some of the
most trusted name in the crypto
space like <a href="https://crypto.news/opensea-to-protect-buyers-from-unintentional-purchases/" >Open Sea</>, <a href="https://www.theblock.co/amp/post/172978/coinbase-ventures-backs-crypto-firewall-provider-harpies-4-5-million-raise-exclusive" > Coinbase </a> 
Ventures and <a href="https://tokeninsight.com/en/news/on-chain-firewall-provider-harpie-raises-4.5m-in-seed-round-led-by-dragonfly-capital?outputType=amp" >Dragonfly XYZ</a>. 
""",
        reply_markup=reply_markup,
    )
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_ROUTES


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("NEXT", callback_data=str(ONE)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.
    await query.edit_message_text(
        text="Start handler, Choose a route", reply_markup=reply_markup
    )
    return START_ROUTES


async def one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(
                "CREATE A FREE HARPIE ACCOUNT", url="https://harpie-protect.io"
            ),
        ],
        [
            InlineKeyboardButton(
                "JOIN HARPIE COMMUNITY", url="https://t.me/harpie_protect"
            ),
        ],
        [
            InlineKeyboardButton("HARPIE TOKEN?", callback_data=str(THREE)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.effective_chat.send_message(
        text="""
  How Harpie Protects your Wallet.

<a href="https://harpie-protect.io">
Harpie</> is an on-chain fire wall app
created and developed to monitor
your wallets for any suspicious
activity and stop it mid-execution.

It was designed to stop all
unauthorized malicious activities
in your wallet.        
""",
        reply_markup=reply_markup,
        parse_mode="HTML",
    )
    #     await query.edit_message_text(
    #         text="""
    #   How Harpie ProtectS your Wallet.

    # Harpie is an on-chain fire wall app
    # created and developed to monitor
    # your wallets for any suspicious
    # activity and stop it mid-execution.

    # It was designed to stop all
    # unauthorized malicious activities
    # in your wallet.
    # """,
    #         reply_markup=reply_markup,
    #     )
    return START_ROUTES


async def two(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(
                "CREATE A FREE HARPIE ACCOUNT", callback_data=str(ONE)
            ),
        ],
        [
            InlineKeyboardButton("TOKEN", callback_data=str(THREE)),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    #     await query.edit_message_text(
    #         text="""

    # """,

    #         reply_markup=reply_markup,
    #     )
    await update.effective_chat.send_message(
        text="""

""",
        reply_markup=reply_markup,
    )
    return START_ROUTES


async def three(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons. This is the end point of the conversation."""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(
                "CREATE A FREE HARPIE ACCOUNT", url="https://harpit-protect.io"
            ),
        ],
        [
            InlineKeyboardButton(
                "JOIN HARPIE COMMUNITY", url="https://t.me/harpie_protect"
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # await query.edit_message_text(
    #     text="",
    #     reply_markup=reply_markup,
    # )
    await update.effective_chat.send_message(
        text="""
Will Harpie Protect launch a Token?

Harpie Protect might launch a token
with potential crypto partners to
protect their users from crypto theft.
 """,
        reply_markup=reply_markup,
    )
    # Transfer to conversation state `SECOND`
    return END_ROUTES


async def four(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("2", callback_data=str(TWO)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Fourth CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return START_ROUTES


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.ƒf
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(one, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(two, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(three, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(four, pattern="^" + str(FOUR) + "$"),
            ],
            END_ROUTES: [
                CallbackQueryHandler(start_over, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(end, pattern="^" + str(TWO) + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
