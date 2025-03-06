from pyrogram import Client, filters , enums
from info import ADMINS
import re
from database.users_chats_db import db

@Client.on_message(filters.command("set_muc") & filters.user(ADMINS))
async def set_muc_id(client, message):
    try:
        id = message.command[1]
        if id and str(id).startswith('-100') and len(str(id)) == 14:
            is_suc = await db.movies_update_channel_id(id)
            if is_suc:
                await message.reply("𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗌𝖾𝗍 𝗆𝗈𝗏𝗂𝖾𝗌 𝗎𝗉𝖽𝖺𝗍𝖾  𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗂𝖽 : " + id)
            else:
                await message.reply("𝖥𝖺𝗂𝗅𝖾𝖽 𝗍𝗈 𝗌𝖾𝗍 𝗆𝗈𝗏𝗂𝖾𝗌 𝗎𝗉𝖽𝖺𝗍𝖾 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗂𝖽 : " + id)
        else:
            await message.reply("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗂𝖽 : " + id)
    except Exception as e:
        print('Err in set_muc_id', e)
        await message.reply("𝖥𝖺𝗂𝗅𝖾𝖽 𝗍𝗈 𝗌𝖾𝗍 𝗆𝗈𝗏𝗂𝖾𝗌 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗂𝖽! 𝖡𝖾𝖼𝖺𝗎𝗌𝖾 : " + str(e))

