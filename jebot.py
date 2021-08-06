#    Copyright (c) 2021 Uvindu Bro <https://t.me/UvinduBro_BOTs>
 
#    This program is free software: you can redistribute it and/or modify  
#    it under the terms of the GNU General Public License as published by  
#    the Free Software Foundation, version 3.
# 
#    This program is distributed in the hope that it will be useful, but 
#    WITHOUT ANY WARRANTY; without even the implied warranty of 
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
#    General Public License for more details.

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import time
import aiohttp

# the secret configuration specific things
if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from sample_config import Config

# the Strings used for this "thing"
from translation import Translation

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from helper_utils.chat_base import TRChatBase
from helper_utils.display_progress import progress_for_pyrogram

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from pyrogram import Client, filters
from PIL import Image
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InlineQuery, InputTextMessageContent

if __name__ == "__main__" :
    # create download directory, if not exist
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    plugins = dict(
        root="plugins"
    )
    bot = pyrogram.Client(
        "File Renamer",
        bot_token=Config.TG_BOT_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        plugins=plugins
    )

@bot.on_message(filters.command("start"))
async def start(client, message):
   if message.chat.type == 'private':
       await bot.send_message(
               chat_id=message.chat.id,
               text="""<b>😋𝙷𝚎𝚢, 𝚃𝚑𝚎𝚛𝚎 🔥𝙸 𝙰𝚖 𝙰 𝚃𝚎𝚕𝚎𝚐𝚛𝚊𝚖 𝙵𝚒𝚕𝚎 𝚁𝚎𝚗𝚊𝚖𝚎𝚛 𝙱𝚘𝚝.🌟... 𝙸 𝙰𝚖 𝚊𝚝𝚑𝚞𝚖𝚋𝚗𝚊𝚒𝚕 𝚜𝚞𝚙𝚙𝚘𝚛𝚝𝚒𝚗𝚐.🇱🇰😋 𝚈𝚘𝚞 𝙲𝚊𝚗 𝙰 𝚁𝚎𝚗𝚊𝚖𝚎 𝙰 𝙵𝚒𝚕𝚎𝚜 𝙸𝚗𝚝𝚘 𝙼𝚎.💠🤖"

✳️𝙿𝚘𝚠𝚎𝚛𝚍 𝙱𝚢 @sdprojectupdates 🇱🇰 𝙰𝚗𝚍 𝙼𝚊𝚍𝚎 𝙱𝚢 @Omindas 🔥🔥🌟

👇👇😋Hit 💠help💠 𝚋𝚞𝚝𝚝𝚘𝚗 𝚝𝚘 𝚏𝚒𝚗𝚍 𝚘𝚞𝚝 𝚖𝚘𝚛𝚎 𝚊𝚋𝚘𝚞𝚝 𝚑𝚘𝚠 𝚝𝚘 𝚞𝚜𝚎 𝚖𝚎🤖🇱🇰</b>""",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "💠𝐇𝐞𝐥𝐩💠", callback_data="help"),
                                        InlineKeyboardButton(
                                            "🇱🇰 𝐔𝐩𝐝𝐚𝐭𝐞 𝐂𝐡𝐚𝐧𝐧𝐚𝐥 🇱🇰", url="https://t.me/sdprojectupdates"),
                                 ],[
                                        InlineKeyboardButton(
                                            "🔥 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 🔥", url="https://t.me/omindas")
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html")

@bot.on_message(filters.command("help"))
async def help(client, message):
    if message.chat.type == 'private':   
        await bot.send_message(
               chat_id=message.chat.id,
               text="""<b>𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐓𝐨 𝐇𝐞𝐥𝐩 𝐑𝐨𝐨𝐦!

👉 𝐒𝐞𝐧𝐝 𝐀𝐧𝐲 𝐓𝐡𝐮𝐦𝐛𝐧𝐚𝐢𝐥 𝐓𝐨 𝐌𝐞
[Do <code>/delthumb</code> to delete thumbnail]

👉 𝐓𝐡𝐞 𝐒𝐞𝐧𝐝 𝐚𝐧𝐲 𝐌𝐞𝐝𝐢𝐚 𝐅𝐢𝐥𝐞 𝐭𝐨 𝐦𝐞

👉 Finally reply file with <code>/rename NewFile.extension</code>

~ @omindas</b>""",
    reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "🔙Back🔙", callback_data="start"),
                                        InlineKeyboardButton(
                                            "☢️About☢️", callback_data="about"),
                                  ],[
                                        InlineKeyboardButton(
                                            "😇Source Code😇", url="https://github.com/omindadelshan/File-Renamer-Bot")
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html")

@bot.on_message(filters.command("about"))
async def about(client, message):
    if message.chat.type == 'private':   
        await bot.send_message(
               chat_id=message.chat.id,
               text="""<b>About File Renamer!</b>

<b>📌 Developer🔥:</b> <a href="https://t.me/omindas">Ominda🇱🇰</a>

<b>📌 Support🔥:</b> <a href="https://t.me/sdprojectupdates">Channal Support</a>

<b>📌 Library🔥:</b> <a href="https://github.com/pyrogram/pyrogram">Pyrogram</a>

<b>~ @omindas</b>""",
     reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "🔙Back🔙", callback_data="help"),
                                        InlineKeyboardButton(
                                            "Source Code 📦", url="https://github.com/omindadelshan/File-Renamer-Bot")
                                    ]]
                            ),        
            disable_web_page_preview=True,        
            parse_mode="html")
        

@bot.on_message(filters.command("rename"))
async def rename(bot, update):
   
    TRChatBase(update.from_user.id, update.text, "rename")
    if (" " in update.text) and (update.reply_to_message is not None):
        cmd, file_name = update.text.split(" ", 1)
        description = Translation.CUSTOM_CAPTION_UL_FILE
        download_location = Config.DOWNLOAD_LOCATION + "/"
        a = await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.DOWNLOAD_START,
            reply_to_message_id=update.message_id
        )
        c_time = time.time()
        the_real_download_location = await bot.download_media(
            message=update.reply_to_message,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(
                Translation.DOWNLOAD_START,
                a,
                c_time
            )
        )
        if the_real_download_location is not None:
            await bot.edit_message_text(
                text=Translation.SAVED_RECVD_DOC_FILE,
                chat_id=update.chat.id,
                message_id=a.message_id
            )
            if "IndianMovie" in the_real_download_location:
                await bot.edit_message_text(
                    text=Translation.RENAME_403_ERR,
                    chat_id=update.chat.id,
                    message_id=a.message_id
                )
                return
            new_file_name = download_location + file_name
            os.rename(the_real_download_location, new_file_name)
            await bot.edit_message_text(
                text=Translation.UPLOAD_START,
                chat_id=update.chat.id,
                message_id=a.message_id
            )
            logger.info(the_real_download_location)
            thumb_image_path = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id) + ".jpg"
            if not os.path.exists(thumb_image_path):
                thumb_image_path = None
            else:
                width = 0
                height = 0
                metadata = extractMetadata(createParser(thumb_image_path))
                if metadata.has("width"):
                    width = metadata.get("width")
                if metadata.has("height"):
                    height = metadata.get("height")
                # resize image
                # ref: https://t.me/PyrogramChat/44663
                # https://stackoverflow.com/a/21669827/4723940
                Image.open(thumb_image_path).convert("RGB").save(thumb_image_path)
                img = Image.open(thumb_image_path)
                # https://stackoverflow.com/a/37631799/4723940
                # img.thumbnail((90, 90))
                img.resize((320, height))
                img.save(thumb_image_path, "JPEG")
                # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
            c_time = time.time()
            await bot.send_document(
                chat_id=update.chat.id,
                document=new_file_name,
                thumb=thumb_image_path,
                caption=description,
                # reply_markup=reply_markup,
                reply_to_message_id=update.reply_to_message.message_id,
                progress=progress_for_pyrogram,
                progress_args=(
                    Translation.UPLOAD_START,
                    a, 
                    c_time
                )
            )
            try:
                os.remove(new_file_name)
                os.remove(thumb_image_path)
            except:
                pass
            await bot.edit_message_text(
                text=Translation.AFTER_SUCCESSFUL_UPLOAD_MSG,
                chat_id=update.chat.id,
                message_id=a.message_id,
                disable_web_page_preview=True
            )
    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text=Translation.REPLY_TO_DOC_FOR_RENAME_FILE,
            reply_to_message_id=update.message_id
        )

@bot.on_callback_query()
async def button(bot, update):
      cb_data = update.data
      if "help" in cb_data:
        await update.message.delete()
        await help(bot, update.message)
      elif "about" in cb_data:
        await update.message.delete()
        await about(bot, update.message)
      elif "start" in cb_data:
        await update.message.delete()
        await start(bot, update.message)

print(
    """
🤗 Bot Started!
👉 Join @sdprojectupdates
"""
)

bot.run()
