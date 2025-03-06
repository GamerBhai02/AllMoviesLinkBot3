from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from info import ADMINS, LOG_CHANNEL, USERNAME
from database.users_chats_db import db
from database.ia_filterdb import Media, get_files_db_size
from utils import get_size, temp
from Script import script
from datetime import datetime
import psutil
import time

@Client.on_message(filters.new_chat_members & filters.group)
async def save_group(bot, message):
    check = [u.id for u in message.new_chat_members]
    if temp.ME in check:
        if (str(message.chat.id)).startswith("-100") and not await db.get_chat(message.chat.id):
            total=await bot.get_chat_members_count(message.chat.id)
            user = message.from_user.mention if message.from_user else "Dear" 
            group_link = await message.chat.export_invite_link()
            await bot.send_message(LOG_CHANNEL, script.NEW_GROUP_TXT.format(temp.B_LINK, message.chat.title, message.chat.id, message.chat.username, group_link, total, user), disable_web_page_preview=True)  
            await db.add_chat(message.chat.id, message.chat.title)
            btn = [[
                InlineKeyboardButton('⚡️ 𝗦𝘂𝗽𝗽𝗼𝗿𝘁 ⚡️', url=USERNAME)
            ]]
            reply_markup=InlineKeyboardMarkup(btn)
            await bot.send_message(
                chat_id=message.chat.id,
                text=f"<b>☤ 𝖳𝗁𝖺𝗇𝗄 𝗒𝗈𝗎 𝖿𝗈𝗋 𝖺𝖽𝖽𝗂𝗇𝗀 𝗆𝖾 𝗂𝗇 {message.chat.title}\n\n🤖 𝖣𝗈𝗇'𝗍 𝖿𝗈𝗋𝗀𝖾𝗍 𝗍𝗈 𝗆𝖺𝗄𝖾 𝗆𝖾 𝖺𝖽𝗆𝗂𝗇 🤖\n\n㊝ 𝖨𝖿 𝗒𝗈𝗎 𝗁𝖺𝗏𝖾 𝖺𝗇𝗒 𝖽𝗈𝗎𝖻𝗍 𝗒𝗈𝗎 𝖼𝗅𝖾𝖺𝗋 𝗂𝗍 𝗎𝗌𝗂𝗇𝗀 𝖻𝖾𝗅𝗈𝗐 𝖻𝗎𝗍𝗍𝗈𝗇𝗌 ㊜</b>",
                reply_markup=reply_markup
            )

@Client.on_message(filters.command('leave') & filters.user(ADMINS))
async def leave_a_chat(bot, message):
    r = message.text.split(None)
    if len(message.command) == 1:
        return await message.reply('<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗅𝗂𝗄𝖾 𝗍𝗁𝗂𝗌 `/leave -100******`</b>')
    if len(r) > 2:
        reason = message.text.split(None, 2)[2]
        chat = message.text.split(None, 2)[1]
    else:
        chat = message.command[1]
        reason = "𝖭𝗈 𝗋𝖾𝖺𝗌𝗈𝗇 𝗉𝗋𝗈𝗏𝗂𝖽𝖾𝖽..."
    try:
        chat = int(chat)
    except:
        chat = chat
    try:
        btn = [[
            InlineKeyboardButton('⚡️ 𝗢𝘄𝗻𝗲𝗿 ⚡️', url=USERNAME)
        ]]
        reply_markup=InlineKeyboardMarkup(btn)
        await bot.send_message(
            chat_id=chat,
            text=f'😞 𝖧𝖾𝗅𝗅𝗈 𝖣𝖾𝖺𝗋,\n𝖬𝗒 𝗈𝗐𝗇𝖾𝗋 𝗁𝖺𝗌 𝗍𝗈𝗅𝖽 𝗆𝖾 𝗍𝗈 𝗅𝖾𝖺𝗏𝖾 𝖿𝗋𝗈𝗆 𝗍𝗁𝖾 𝗀𝗋𝗈𝗎𝗉 𝗌𝗈 𝖨 a𝗆 𝗅𝖾𝖺𝗏𝗂𝗇𝗀 😔\n\n🚫 𝖱𝖾𝖺𝗌𝗈𝗇 - <code>{reason}</code>\n\n𝖨𝖿 𝗒𝗈𝗎 𝗇𝖾𝖾𝖽 𝗍𝗈 𝖺𝖽𝖽 𝗆𝖾 𝖺𝗀𝖺𝗂𝗇 𝗍𝗁𝖾𝗇 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 𝗆𝗒 𝗈𝗐𝗇𝖾𝗋 👇',
            reply_markup=reply_markup,
        )
        await bot.leave_chat(chat)
        await db.delete_chat(chat)
        await message.reply(f"<b>𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗅𝖾𝖿𝗍 𝖿𝗋𝗈𝗆 𝗀𝗋𝗈𝗎𝗉 - `{chat}`</b>")
    except Exception as e:
        await message.reply(f'<b>🚫 𝖤𝗋𝗋𝗈𝗋 - `{e}`</b>')

@Client.on_message(filters.command('groups') & filters.user(ADMINS))
async def groups_list(bot, message):
    msg = await message.reply('<b>𝖲𝖾𝖺𝗋𝖼𝗁𝗂𝗇𝗀...</b>')
    chats = await db.get_all_chats()
    out = "𝖦𝗋𝗈𝗎𝗉𝗌 𝗌𝖺𝗏𝖾𝖽 𝗂𝗇 𝗍𝗁𝖾 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾:\n\n"
    count = 1
    async for chat in chats:
        chat_info = await bot.get_chat(chat['id'])
        members_count = chat_info.members_count if chat_info.members_count else "Unknown"
        out += f"<b>{count}. 𝖳𝗂𝗍𝗅𝖾 - `{chat['title']}`\n𝖨𝖣 - `{chat['id']}`\n𝖬𝖾𝗆𝖻𝖾𝗋𝗌 - `{members_count}`</b>"
        out += '\n\n'
        count += 1
    try:
        if count > 1:
            await msg.edit_text(out)
        else:
            await msg.edit_text("<b>𝖭𝗈 𝗀𝗋𝗈𝗎𝗉𝗌 𝖿𝗈𝗎𝗇𝖽</b>")
    except MessageTooLong:
        with open('chats.txt', 'w+') as outfile:
            outfile.write(out)
        await message.reply_document('chats.txt', caption="<b>𝖫𝗂𝗌𝗍 𝗈𝖿 𝖺𝗅𝗅 𝗀𝗋𝗈𝗎𝗉𝗌</b>")

@Client.on_message(filters.command('stats') & filters.user(ADMINS) & filters.incoming)
async def get_ststs(bot, message):
    users = await db.total_users_count()
    groups = await db.total_chat_count()
    size = get_size(await db.get_db_size())
    free = get_size(536870912)
    files = await Media.count_documents()
    db2_size = get_size(await get_files_db_size())
    db2_free = get_size(536870912)
    uptime = time.strftime("%Hh %Mm %Ss", time.gmtime(time.time() - time.time()))
    ram = psutil.virtual_memory().percent
    cpu = psutil.cpu_percent()
    await message.reply_text(script.STATUS_TXT.format(users, groups, size, free, files, db2_size, db2_free, uptime, ram, cpu))
