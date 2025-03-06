from pyrogram import Client, filters
from utils import temp
from pyrogram.types import Message
from database.users_chats_db import db
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import SUPPORT_CHAT, LOG_CHANNEL

async def banned_users(_, client, message: Message):
    return (
        message.from_user is not None or not message.sender_chat
    ) and message.from_user.id in temp.BANNED_USERS

banned_user = filters.create(banned_users)

async def disabled_chat(_, client, message: Message):
    return message.chat.id in temp.BANNED_CHATS

disabled_group=filters.create(disabled_chat)


#@Client.on_message(filters.private & banned_user & filters.incoming)
#async def ban_reply(bot, message):
#    ban = await db.get_ban_status(message.from_user.id)
#    await message.reply(f'Sorry Dude, You are Banned to use Me. \nBan Reason : {ban["ban_reason"]}')

@Client.on_message(filters.private & banned_user & filters.incoming)
async def ban_reply(bot, message):
    ban = await db.get_ban_status(message.from_user.id)
    username = message.from_user.username or '𝖭𝗈 𝗎𝗌𝖾𝗋𝗇𝖺𝗆𝖾'
    # Send reply to the user
    await message.reply(f'𝖳𝖾𝗅𝖾𝗀𝗋𝖺𝗆 𝗌𝖺𝗒𝗌: [400 PEER_ID_INVALID] - 𝖳𝗁𝖾 𝗉𝖾𝖾𝗋 𝗂𝖽 𝖻𝖾𝗂𝗇𝗀 𝗎𝗌𝖾𝖽 𝗂𝗌 𝗂𝗇𝗏𝖺𝗅𝗂𝖽 𝗈𝗋 𝗇𝗈𝗍 𝗄𝗇𝗈𝗐𝗇 𝗒𝖾𝗍. 𝖬𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝗒𝗈𝗎 𝗆𝖾𝖾𝗍 𝗍𝗁𝖾 𝗉𝖾𝖾𝗋 𝖻𝖾𝖿𝗈𝗋𝖾 𝗂𝗇𝗍𝖾𝗋𝖺𝖼𝗍𝗂𝗇𝗀 𝗐𝗂𝗍𝗁 𝗂𝗍')
    
    # Send message to the log channel
    await bot.send_message(
        LOG_CHANNEL, 
        f"𝖴𝗌𝖾𝗋 𝖨𝖽: {message.from_user.id}\n𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾: @{username} 𝗍𝗋𝗂𝖾𝖽 𝗍𝗈 𝗆𝖾𝗌𝗌𝖺𝗀𝖾, 𝖻𝗎𝗍 𝗍𝗁𝖾𝗒 𝖺𝗋𝖾 𝖻𝖺𝗇𝗇𝖾𝖽.\n𝖡𝖺𝗇 𝖱𝖾𝖺𝗌𝗈𝗇: {ban['ban_reason']}"
    )

@Client.on_message(filters.group & disabled_group & filters.incoming)
async def grp_bd(bot, message):
    buttons = [[
        InlineKeyboardButton('𝗦𝘂𝗽𝗽𝗼𝗿𝘁', url=f'https://t.me/GamerBhai02Bot')
    ]]
    reply_markup=InlineKeyboardMarkup(buttons)
    vazha = await db.get_chat(message.chat.id)
    k = await message.reply(
        text=f"𝖢𝖧𝖠𝖳 𝖭𝖮𝖳 𝖠𝖫𝖫𝖮𝖶𝖤𝖣 🐞\n\n𝖬𝗒 𝖺𝖽𝗆𝗂𝗇𝗌 𝗁𝖺𝗌 𝗋𝖾𝗌𝗍𝗋𝗂𝖼𝗍𝖾𝖽 𝗆𝖾 𝖿𝗋𝗈𝗆 𝗐𝗈𝗋𝗄𝗂𝗇𝗀 𝗁𝖾𝗋𝖾! 𝖨𝖿 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝗄𝗇𝗈𝗐 𝗆𝗈𝗋𝖾 𝖺𝖻𝗈𝗎𝗍 𝗂𝗍 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 𝗌𝗎𝗉𝗉𝗈𝗋𝗍..\n𝖱𝖾𝖺𝗌𝗈𝗇: <code>{vazha['reason']}</code>.",
        reply_markup=reply_markup)
    try:
        await k.pin()
    except:
        pass
    await bot.leave_chat(message.chat.id)
