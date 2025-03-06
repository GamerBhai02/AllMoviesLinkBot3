from pyrogram import Client, filters
import datetime
import time
from database.users_chats_db import db
from info import ADMINS
from utils import users_broadcast, groups_broadcast, temp, get_readable_time
import asyncio
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup 

lock = asyncio.Lock()

@Client.on_callback_query(filters.regex(r'^broadcast_cancel'))
async def broadcast_cancel(bot, query):
    _, ident = query.data.split("#")
    if ident == 'users':
        await query.message.edit("𝖳𝗋𝗒𝗂𝗇𝗀 𝗍𝗈 𝖼𝖺𝗇𝖼𝖾𝗅 𝗎𝗌𝖾𝗋𝗌 𝖻𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍𝗂𝗇𝗀...")
        temp.USERS_CANCEL = True
    elif ident == 'groups':
        temp.GROUPS_CANCEL = True
        await query.message.edit("𝖳𝗋𝗒𝗂𝗇𝗀 𝗍𝗈 𝖼𝖺𝗇𝖼𝖾𝗅 𝗀𝗋𝗈𝗎𝗉𝗌 𝖻𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍𝗂𝗇𝗀...")
       
@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_users(bot, message):
    if lock.locked():
        return await message.reply('𝖢𝗎𝗋𝗋𝖾𝗇𝗍𝗅𝗒 𝖻𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝗂𝗌 𝗉𝗋𝗈𝖼𝖾𝗌𝗌𝗂𝗇𝗀, 𝖶𝖺𝗂𝗍 𝖿𝗈𝗋 𝗂𝗍 𝗍𝗈 𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾.')

    msg = await message.ask('<b>𝖣𝗈 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝗉𝗂𝗇 𝗍𝗁𝗂𝗌 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗍𝗈 𝗎𝗌𝖾𝗋𝗌?</b>', reply_markup=ReplyKeyboardMarkup([['Yes', 'No']], one_time_keyboard=True, resize_keyboard=True))
    if msg.text == 'Yes':
        is_pin = True
    elif msg.text == 'No':
        is_pin = False
    else:
        return await msg.edit('𝖶𝗋𝗈𝗇𝗀 𝖱𝖾𝗌𝗉𝗈𝗇𝗌𝖾!')
    await msg.delete()
    users = await db.get_all_users()
    b_msg = message.reply_to_message
    b_sts = await message.reply_text(text='<b>𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍𝗂𝗇𝗀 𝗒𝗈𝗎𝗋 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗍𝗈 𝗎𝗌𝖾𝗋𝗌 ⌛️</b>')
    start_time = time.time()
    total_users = await db.total_users_count()
    done = 0
    blocked = 0
    deleted = 0
    failed = 0
    success = 0

    async with lock:
        async for user in users:
            time_taken = get_readable_time(time.time()-start_time)
            if temp.USERS_CANCEL:
                temp.USERS_CANCEL = False
                await b_sts.edit(f"𝖴𝗌𝖾𝗋𝗌 𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖢𝖺𝗇𝖼𝖾𝗅𝗅𝖾𝖽!\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 𝗂𝗇 {time_taken}\n\n𝖳𝗈𝗍𝖺𝗅 𝖴𝗌𝖾𝗋𝗌: <code>{total_users}</code>\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: <code>{done} / {total_users}</code>\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌: <code>{success}</code>")
                return
            sts = await users_broadcast(int(user['id']), b_msg, is_pin)
            if sts == 'Success':
                success += 1
            elif sts == 'Error':
                failed += 1
            done += 1
            if not done % 20:
                btn = [[
                    InlineKeyboardButton('𝗖𝗔𝗡𝗖𝗘𝗟', callback_data=f'broadcast_cancel#users')
                ]]
                await b_sts.edit(f"𝖴𝗌𝖾𝗋𝗌 𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝗂𝗇 𝗉𝗋𝗈𝗀𝗋𝖾𝗌𝗌...\n\n𝖳𝗈𝗍𝖺𝗅 𝖴𝗌𝖾𝗋𝗌: <code>{total_users}</code>\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: <code>{done} / {total_users}</code>\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌: <code>{success}</code>", reply_markup=InlineKeyboardMarkup(btn))
        await b_sts.edit(f"𝖴𝗌𝖾𝗋𝗌 𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽.\nCompleted in {time_taken}\n\n𝖳𝗈𝗍𝖺𝗅 𝖴𝗌𝖾𝗋𝗌: <code>{total_users}</code>\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: <code>{done} / {total_users}</code>\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌: <code>{success}</code>")

@Client.on_message(filters.command("grp_broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_group(bot, message):
    msg = await message.ask('<b>𝖣𝗈 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝗉𝗂𝗇 𝗍𝗁𝗂𝗌 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗂𝗇 𝗍𝗁𝖾 𝗀𝗋𝗈𝗎𝗉𝗌?</b>', reply_markup=ReplyKeyboardMarkup([['Yes', 'No']], one_time_keyboard=True, resize_keyboard=True))
    if msg.text == 'Yes':
        is_pin = True
    elif msg.text == 'No':
        is_pin = False
    else:
        return await msg.edit('𝖶𝗋𝗈𝗇𝗀 𝖱𝖾𝗌𝗉𝗈𝗇𝗌𝖾!')
    await msg.delete()
    chats = await db.get_all_chats()
    b_msg = message.reply_to_message
    b_sts = await message.reply_text(text='<b>𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍𝗂𝗇𝗀 𝗒𝗈𝗎𝗋 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗍𝗈 𝗍𝗁𝖾 𝗀𝗋𝗈𝗎𝗉𝗌 ⏳</b>')
    start_time = time.time()
    total_chats = await db.total_chat_count()
    done = 0
    failed = 0
    success = 0
    
    async with lock:
        async for chat in chats:
            time_taken = get_readable_time(time.time()-start_time)
            if temp.GROUPS_CANCEL:
                temp.GROUPS_CANCEL = False
                await b_sts.edit(f"𝖦𝗋𝗈𝗎𝗉𝗌 𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖢𝖺𝗇𝖼𝖾𝗅𝗅𝖾𝖽!\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 𝗂𝗇 {time_taken}\n\n𝖳𝗈𝗍𝖺𝗅 𝖦𝗋𝗈𝗎𝗉𝗌: <code>{total_chats}</code>\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: <code>{done} / {total_chats}</code>\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌: <code>{success}</code>\n𝖥𝖺𝗂𝗅𝖾𝖽: <code>{failed}</code>")
                return
            sts = await groups_broadcast(int(chat['id']), b_msg, is_pin)
            if sts == 'Success':
                success += 1
            elif sts == 'Error':
                failed += 1
            done += 1
            if not done % 20:
                btn = [[
                    InlineKeyboardButton('𝗖𝗔𝗡𝗖𝗘𝗟', callback_data=f'broadcast_cancel#groups')
                ]]
                await b_sts.edit(f"𝖦𝗋𝗈𝗎𝗉𝗌 𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝗂𝗇 𝗉𝗋𝗈𝗀𝗋𝖾𝗌𝗌...\n\n𝖳𝗈𝗍𝖺𝗅 𝖦𝗋𝗈𝗎𝗉𝗌: <code>{total_chats}</code>\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: <code>{done} / {total_chats}</code>\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌: <code>{success}</code>\n𝖥𝖺𝗂𝗅𝖾𝖽: <code>{failed}</code>", reply_markup=InlineKeyboardMarkup(btn))    
        await b_sts.edit(f"𝖦𝗋𝗈𝗎𝗉𝗌 𝖡𝗋𝗈𝖺𝖽𝖼𝖺𝗌𝗍 𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽.\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 𝗂𝗇 {time_taken}\n\n𝖳𝗈𝗍𝖺𝗅 𝖦𝗋𝗈𝗎𝗉𝗌: <code>{total_chats}</code>\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽: <code>{done} / {total_chats}</code>\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌: <code>{success}</code>\n𝖥𝖺𝗂𝗅𝖾𝖽: <code>{failed}</code>")

