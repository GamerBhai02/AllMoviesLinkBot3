from pyrogram import Client, filters, enums
from datetime import datetime, timedelta
from database.config_db import mdb
from database.users_chats_db import db
from info import ADMINS
import asyncio
import re

@Client.on_message(filters.private & filters.command("set_ads") & filters.user(ADMINS))
async def set_ads(client, message):
    try:
        command_args = message.text.split(maxsplit=1)[1]
        if '#' not in command_args or len(command_args.split('#')) < 3:
            await message.reply_text(f"𝖴𝗌𝖺𝗀𝖾: /set_ads {{ads name}}#{{time}}#{{photo URL}} <a href=https://t.me/Jisshu_developer/9>Explain</a>")
            return

        ads_name, duration_or_impression, url = command_args.split('#', 2)
        ads_name = ads_name.strip()
        url = url.strip()

        if len(ads_name) > 35:
            await message.reply_text(f"𝖠𝖽𝗏𝖾𝗋𝗍𝗂𝗌𝖾𝗆𝖾𝗇𝗍 𝗇𝖺𝗆𝖾 𝗌𝗁𝗈𝗎𝗅𝖽 𝗇𝗈𝗍 𝖾𝗑𝖼𝖾𝖾𝖽 35 𝖼𝗁𝖺𝗋𝖺𝖼𝗍𝖾𝗋𝗌.")
            return

        if not re.match(r'https?://.+', url):
            await message.reply_text(f"𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖴𝖱𝖫 𝖿𝗈𝗋𝗆𝖺𝗍. 𝖴𝗌𝖾 𝖺 𝗏𝖺𝗅𝗂𝖽 𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 𝗅𝗂𝗇𝗄.")
            return

        expiry_date = None
        impression_count = None

        if duration_or_impression[0] == 'd':
           
            duration = duration_or_impression[1:]
            if not duration.isdigit():
                await message.reply_text(f"𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇 𝗆𝗎𝗌𝗍 𝖻𝖾 𝖺 𝗇𝗎𝗆𝖻𝖾𝗋.")
                return
            expiry_date = datetime.now() + timedelta(days=int(duration))
        elif duration_or_impression[0] == 'i':
           
            impression = duration_or_impression[1:]
            if not impression.isdigit():
                await message.reply_text(f"𝖨𝗆𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇 𝖼𝗈𝗎𝗇𝗍 𝗆𝗎𝗌𝗍 𝖻𝖾 𝖺 𝗇𝗎𝗆𝖻𝖾𝗋.")
                return
            impression_count = int(impression)
        else:
            await message.reply_text(f"𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝗉𝗋𝖾𝖿𝗂𝗑. 𝖴𝗌𝖾 'd' 𝖿𝗈𝗋 𝖽𝗎𝗋𝖺𝗍𝗂𝗈𝗇 𝖺𝗇𝖽 'i' 𝖿𝗈𝗋 𝗂𝗆𝗉𝗋𝖾𝗌𝗌𝗂𝗈𝗇 𝖼𝗈𝗎𝗇𝗍.")
            return

        reply = message.reply_to_message
        if not reply:
            await message.reply_text(f"Reply to a message to set it as your advertisement.")
            return
        if not reply.text:
            await message.reply_text(f"Only text messages are supported.")
            return

       
        await mdb.update_advirtisment(reply.text, f"{ads_name}", expiry_date, impression_count)
        await db.jisshu_set_ads_link(url)

        await asyncio.sleep(3)
        _, name, _ = await mdb.get_advirtisment()
        await message.reply_text(f"Advertisement: '{name}' has been set with the stream link: {url}")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")


@Client.on_message(filters.private & filters.command("ads"))
async def ads(_, message):
    try:
        _, name, impression = await mdb.get_advirtisment()
        if not name:
            await message.reply_text(f"No ads set.")
            return
        if impression == 0:
            await message.reply_text(f"Advertisement: '{name}' has expired.")
            return
        await message.reply_text(f"Advertisement: '{name}' has {impression} impressions left.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")


def checkIfLinkIsValid(link):
    if re.match(r'^https?://(?:www\.)?\S+$', link):
        return True
    else:
        return False

@Client.on_message(filters.private & filters.command("del_ads") & filters.user(ADMINS))
async def del_ads(client, message):
    try:
        await mdb.update_advirtisment()
        
        current_link = await db.jisshu_get_ads_link()
        if current_link:
            is_deleted = await db.jisshu_del_ads_link()
            if is_deleted:
                await message.reply(f"Successfully deleted advertisement and ads photo link: {current_link}!")
            else:
                await message.reply("Advertisement reset, but stream link deletion failed. Stream link not found or something went wrong! Check logs")
        else:
            await message.reply("Advertisement reset. ads photo link not found!")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")
