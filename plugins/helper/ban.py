from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid
from database.users_chats_db import db  
from utils import temp 
from info import *

@Client.on_message(filters.command('ban') & filters.user(ADMINS))
async def ban_a_user(bot, message):
    # https://t.me/JISSHU_BOTS
    if len(message.command) == 1:
        return await message.reply('𝖦𝗂𝗏𝖾 𝗆𝖾 𝖺 𝗎𝗌𝖾𝗋 𝗂𝖽 / 𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "𝖭𝗈 𝗋𝖾𝖺𝗌𝗈𝗇 𝖯𝗋𝗈𝗏𝗂𝖽𝖾𝖽"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("𝖳𝗁𝗂𝗌 𝗂𝗌 𝖺𝗇 𝗂𝗇𝗏𝖺𝗅𝗂𝖽 𝗎𝗌𝖾𝗋, 𝗆𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝖨 𝗁𝖺𝗏𝖾 𝗆𝖾𝗍 𝗁𝗂𝗆 𝖻𝖾𝖿𝗈𝗋𝖾.")
    except IndexError:
        return await message.reply("𝖳𝗁𝗂𝗌 𝗆𝗂𝗀𝗁𝗍 𝖻𝖾 𝖺 𝖼𝗁𝖺𝗇𝗇𝖾𝗅, 𝗆𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝗂𝗍𝗌 𝖺 𝗎𝗌𝖾𝗋.")
    except Exception as e:
        return await message.reply(f'𝖤𝗋𝗋𝗈𝗋 - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if jar['is_banned']:
            return await message.reply(f"{k.mention} 𝗂𝗌 𝖺𝗅𝗋𝖾𝖺𝖽𝗒 𝖻𝖺𝗇𝗇𝖾𝖽\n𝖱𝖾𝖺𝗌𝗈𝗇: {jar['ban_reason']}")
        await db.ban_user(k.id, reason)
        temp.BANNED_USERS.append(k.id)
        await message.reply(f"𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖻𝖺𝗇𝗇𝖾𝖽 {k.mention}")


    
@Client.on_message(filters.command('unban') & filters.user(ADMINS))
async def unban_a_user(bot, message):
    if len(message.command) == 1:
        return await message.reply('𝖦𝗂𝗏𝖾 𝗆𝖾 𝖺 𝗎𝗌𝖾𝗋 𝗂𝖽 / 𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾')
    r = message.text.split(None)
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "𝖭𝗈 𝗋𝖾𝖺𝗌𝗈𝗇 𝖯𝗋𝗈𝗏𝗂𝖽𝖾𝖽"
    try:
        chat = int(chat)
    except:
        pass
    try:
        k = await bot.get_users(chat)
    except PeerIdInvalid:
        return await message.reply("𝖳𝗁𝗂𝗌 𝗂𝗌 𝖺𝗇 𝗂𝗇𝗏𝖺𝗅𝗂𝖽 𝗎𝗌𝖾𝗋, 𝗆𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝖨 𝗁𝖺𝗏𝖾 𝗆𝖾𝗍 𝗁𝗂𝗆 𝖻𝖾𝖿𝗈𝗋𝖾.")
    except IndexError:
        return await message.reply("𝖳𝗁𝗂𝗌 𝗆𝗂𝗀𝗁𝗍 𝖻𝖾 𝖺 𝖼𝗁𝖺𝗇𝗇𝖾𝗅, 𝗆𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝗂𝗍𝗌 𝖺 𝗎𝗌𝖾𝗋.")
    except Exception as e:
        return await message.reply(f'𝖤𝗋𝗋𝗈𝗋 - {e}')
    else:
        jar = await db.get_ban_status(k.id)
        if not jar['is_banned']:
            return await message.reply(f"{k.mention} 𝗂𝗌 𝗇𝗈𝗍 𝗒𝖾𝗍 𝖻𝖺𝗇𝗇𝖾𝖽.")
        await db.remove_ban(k.id)
        temp.BANNED_USERS.remove(k.id)
        await message.reply(f"𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗎𝗇𝖻𝖺𝗇𝗇𝖾𝖽 {k.mention}")
      
