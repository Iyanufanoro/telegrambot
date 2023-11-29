#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ForceReply,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

NEXT, GENDER, LOCATION, BIO = range(4)

INLINE_BUTTONS = [
    [
        InlineKeyboardButton("NEXT", callback_data="aa"),
    ],
    [
        InlineKeyboardButton("NEXT", callback_data="aa"),
    ],
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [["Boy", "Girl", "Other"]]
    await update.message.reply_html(
        """
<b>Example message
What is Harpie Protect?
Harpie is backed with some of the
most trusted name in the crypto
space like Open Sea, Coinbase Ventures
and Dragonfly XYZ.</b>
           """,
        reply_markup=ForceReply(selective=False, input_field_placeholder="something"),
        # reply_markup=InlineKeyboardMarkup(INLINE_BUTTONS),
        disable_web_page_preview=True,
    )
    return GENDER


async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = InlineKeyboardMarkup(INLINE_BUTTONS)
    await update.message.reply_text(
        "ijbiuniubiu,", reply_markup=reply_markup, disable_web_page_preview=True
    )
    # update.message.reply(
    #     text="testing inline", reply_markup=reply_markup, disable_web_page_preview=True
    # )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token("6696488654:AAH_5DORWJ-QNrebjkXGf87wVOg2zk7HaFQ")
        .build()
    )

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            # CommandHandler("skip", skip_location),
        ],
        states={NEXT: [MessageHandler(filters.TEXT, test)]},
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
