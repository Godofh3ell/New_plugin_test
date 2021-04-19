#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

import logging

import pyrogram
from tobrot import AUTH_CHANNEL, LOGGER
import configparser  # buildin package

import logging

import os

import re

import pyrogram.types as pyrogram

from pyrogram.types import CallbackQuery

from tobrot import LOGGER, OWNER_ID

config = configparser.ConfigParser()

async def rclone_command_fd(client, message):

    """/rclone command"""

    LOGGER.info(

        f"rclone command from chatid:{message.chat.id}, userid:{message.from_user.id}"

    )

    if message.from_user.id == OWNER_ID and message.chat.type == "private":

        config.read("rclone_bak.conf")

        sections = list(config.sections())

        inline_keyboard = []

        for section in sections:

            ikeyboard = [

                pyrogram.InlineKeyboardButton(

                    section, callback_data=(f"rclone_{section}").encode("UTF-8")

                )

            ]

            inline_keyboard.append(ikeyboard)

        config.read("rclone.conf")

        section = config.sections()[0]

        msg_text = f"""Default section of rclone config is: **{section}**\n\n

There are {len(sections)} sections in your rclone.conf file, 

please choose which section you want to use:"""

        ikeyboard = [

            pyrogram.InlineKeyboardButton(

                "‼️ Cancel ‼️", callback_data=(f"rcloneCancel").encode("UTF-8")

            )

        ]

        inline_keyboard.append(ikeyboard)

        reply_markup = pyrogram.InlineKeyboardMarkup(inline_keyboard)

        await message.reply_text(text=msg_text, reply_markup=reply_markup)

    else:

        await message.reply_text("You have no permission!")

        LOGGER.warning(

            f"uid={message.from_user.id} have no permission to edit rclone config!"

        )



async def new_join_f(client, message):
    chat_type = message.chat.type
    if chat_type != "private":
        await message.reply_text(f"Current CHAT ID: <code>{message.chat.id}</code>")
        # leave chat
        await client.leave_chat(chat_id=message.chat.id, delete=True)
    # delete all other messages, except for AUTH_CHANNEL
    await message.delete(revoke=True)


async def help_message_f(client, message):
    # await message.reply_text("no one gonna help you 🤣🤣🤣🤣", quote=True)
    # channel_id = str(AUTH_CHANNEL)[4:]
    # message_id = 99
    # display the /help

    await message.reply_text(
        """join this group for help-- @GbotStoreSupport\n\n And also don't forget to star/fork this repo: <a href="https://github.com/gautamajay52/TorrentLeech-Gdrive">TorrentLeech-Gdrive</a>""",
        disable_web_page_preview=True,
    )
    
    
async def rclone_button_callback(bot, update: CallbackQuery):

    """rclone button callback"""

    if update.data == "rcloneCancel":

        config.read("rclone.conf")

        section = config.sections()[0]

        await update.message.edit_text(

            f"Opration canceled! \n\nThe default section of rclone config is: **{section}**"

        )

        LOGGER.info(

            f"Opration canceled! The default section of rclone config is: {section}"

        )

    else:

        section = update.data.split("_", maxsplit=1)[1]

        with open("rclone.conf", "w", newline="\n", encoding="utf-8") as f:

            config.read("rclone_bak.conf")

            temp = configparser.ConfigParser()

            temp[section] = config[section]

            temp.write(f)

        await update.message.edit_text(

            f"Default rclone config changed to **{section}**"

        )

        LOGGER.info(f"Default rclone config changed to {section}")
