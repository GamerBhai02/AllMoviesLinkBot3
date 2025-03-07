import asyncio
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified
from info import ADMINS, LOG_CHANNEL, CHANNELS
from database.ia_filterdb import save_file
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils import temp, get_readable_time
import time

lock = asyncio.Lock()

@Client.on_callback_query(filters.regex(r'^index'))
async def index_files(bot, query):
    _, ident, chat, lst_msg_id, skip = query.data.split("#")
    if ident == 'yes':
        msg = query.message
        await msg.edit("<b>𝖨𝗇𝖽𝖾𝗑𝗂𝗇𝗀 𝗌𝗍𝖺𝗋𝗍𝖾𝖽...</b>")
        try:
            chat = int(chat)
        except:
            chat = chat
        await index_files_to_db(int(lst_msg_id), chat, msg, bot, int(skip))
    elif ident == 'cancel':
        temp.CANCEL = True
        await query.message.edit("𝖳𝗋𝗒𝗂𝗇𝗀 𝗍𝗈 𝖼𝖺𝗇𝖼𝖾𝗅 𝖨𝗇𝖽𝖾𝗑𝗂𝗇𝗀...")

@Client.on_message(filters.command('index') & filters.private & filters.incoming & filters.user(ADMINS))
async def send_for_index(bot, message):
    if lock.locked():
        return await message.reply('𝖶𝖺𝗂𝗍 𝗎𝗇𝗍𝗂𝗅 𝗉𝗋𝖾𝗏𝗂𝗈𝗎𝗌 𝗉𝗋𝗈𝖼𝖾𝗌𝗌 𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾.')
    i = await message.reply("𝖥𝗈𝗋𝗐𝖺𝗋𝖽 𝗅𝖺𝗌𝗍 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗈𝗋 𝗌𝖾𝗇𝖽 𝗅𝖺𝗌𝗍 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗅𝗂𝗇𝗄.")
    msg = await bot.listen(chat_id=message.chat.id, user_id=message.from_user.id)
    await i.delete()
    if msg.text and msg.text.startswith("https://t.me"):
        try:
            msg_link = msg.text.split("/")
            last_msg_id = int(msg_link[-1])
            chat_id = msg_link[-2]
            if chat_id.isnumeric():
                chat_id = int(("-100" + chat_id))
        except:
            await message.reply('𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗅𝗂𝗇𝗄!')
            return
    elif msg.forward_from_chat and msg.forward_from_chat.type == enums.ChatType.CHANNEL:
        last_msg_id = msg.forward_from_message_id
        chat_id = msg.forward_from_chat.username or msg.forward_from_chat.id
    else:
        await message.reply('𝖳𝗁𝗂𝗌 𝗂𝗌 𝗇𝗈𝗍 𝖿𝗈𝗋𝗐𝖺𝗋𝖽𝖾𝖽 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗈𝗋 𝗅𝗂𝗇𝗄.')
        return
    try:
        chat = await bot.get_chat(chat_id)
    except Exception as e:
        return await message.reply(f'𝖤𝗋𝗋𝗈𝗋𝗌 - {e}')
    if chat.type != enums.ChatType.CHANNEL:
        return await message.reply("𝖨 𝖼𝖺𝗇 𝗂𝗇𝖽𝖾𝗑 𝗈𝗇𝗅𝗒 𝖼𝗁𝖺𝗇𝗇𝖾𝗅𝗌.")
    s = await message.reply("𝖲𝖾𝗇𝖽 𝗌𝗄𝗂𝗉 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗇𝗎𝗆𝖻𝖾𝗋.")
    msg = await bot.listen(chat_id=message.chat.id, user_id=message.from_user.id)
    await s.delete()
    try:
        skip = int(msg.text)
    except:
        return await message.reply("𝖭𝗎𝗆𝖻𝖾𝗋 𝗂𝗌 𝗂𝗇𝗏𝖺𝗅𝗂𝖽.")
    buttons = [[
        InlineKeyboardButton('𝖸𝖾𝗌', callback_data=f'index#yes#{chat_id}#{last_msg_id}#{skip}')
    ],[
        InlineKeyboardButton('𝖢𝗅𝗈𝗌𝖾', callback_data='close_data'),
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    await message.reply(f'𝖣𝗈 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝗂𝗇𝖽𝖾𝗑 {chat.title} 𝖼𝗁𝖺𝗇𝗇𝖾𝗅?\n𝖳𝗈𝗍𝖺𝗅 𝖬𝖾𝗌𝗌𝖺𝗀𝖾𝗌: <code>{last_msg_id}</code>', reply_markup=reply_markup)

@Client.on_message(filters.command('channel'))
async def channel_info(bot, message):
    if message.from_user.id not in ADMINS:
        await message.reply('𝖮𝗇𝗅𝗒 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗈𝗐𝗇𝖾𝗋 𝖼𝖺𝗇 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽... 😑')
        return
    ids = CHANNELS
    if not ids:
        return await message.reply("𝖭𝗈𝗍 𝗌𝖾𝗍 𝖢𝖧𝖠𝖭𝖭𝖤𝖫𝖲")
    text = '**𝖨𝗇𝖽𝖾𝗑𝖾𝖽 𝖢𝗁𝖺𝗇𝗇𝖾𝗅𝗌:**\n\n'
    for id in ids:
        chat = await bot.get_chat(id)
        text += f'{chat.title}\n'
    text += f'\n**𝖳𝗈𝗍𝖺𝗅:** {len(ids)}'
    await message.reply(text)

async def index_files_to_db(lst_msg_id, chat, msg, bot, skip):
    start_time = time.time()
    total_files = 0
    duplicate = 0
    errors = 0
    deleted = 0
    no_media = 0
    unsupported = 0
    current = skip
    
    async with lock:
        try:
            async for message in bot.iter_messages(chat, lst_msg_id, skip):
                time_taken = get_readable_time(time.time()-start_time)
                if temp.CANCEL:
                    temp.CANCEL = False
                    await msg.edit(f"𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖢𝖺𝗇𝖼𝖾𝗅𝗅𝖾𝖽!\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 𝗂𝗇 {time_taken}\n\n𝖲𝖺𝗏𝖾𝖽 <code>{total_files}</code> 𝖿𝗂𝗅𝖾𝗌 𝗍𝗈 𝖣𝖺𝗍𝖺𝖻𝖺𝗌𝖾!\n𝖣𝗎𝗉𝗅𝗂𝖼𝖺𝗍𝖾 𝖥𝗂𝗅𝖾𝗌 𝖲𝗄𝗂𝗉𝗉𝖾𝖽: <code>{duplicate}</code>\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽 𝖬𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝖲𝗄𝗂𝗉𝗉𝖾𝖽: <code>{deleted}</code>\n𝖭𝗈𝗇-𝖬𝖾𝖽𝗂𝖺 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝗌𝗄𝗂𝗉𝗉𝖾𝖽: <code>{no_media + unsupported}</code>\n𝖴𝗇𝗌𝗎𝗉𝗉𝗈𝗋𝗍𝖾𝖽 𝖬𝖾𝖽𝗂𝖺: <code>{unsupported}</code>\n𝖤𝗋𝗋𝗈𝗋𝗌 𝖮𝖼𝖼𝗎𝗋𝗋𝖾𝖽: <code>{errors}</code>")
                    return
                current += 1
                if current % 100 == 0:
                    btn = [[
                        InlineKeyboardButton('𝖢𝖠𝖭𝖢𝖤𝖫', callback_data=f'index#cancel#{chat}#{lst_msg_id}#{skip}')
                    ]]
                    await msg.edit_text(text=f"𝖳𝗈𝗍𝖺𝗅 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝗋𝖾𝖼𝖾𝗂𝗏𝖾𝖽: <code>{current}</code>\n𝖳𝗈𝗍𝖺𝗅 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝗌𝖺𝗏𝖾𝖽: <code>{total_files}</code>\n𝖣𝗎𝗉𝗅𝗂𝖼𝖺𝗍𝖾 𝖥𝗂𝗅𝖾𝗌 𝖲𝗄𝗂𝗉𝗉𝖾𝖽: <code>{duplicate}</code>\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽 𝖬𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝖲𝗄𝗂𝗉𝗉𝖾𝖽: <code>{deleted}</code>\n𝖭𝗈𝗇-𝖬𝖾𝖽𝗂𝖺 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝗌𝗄𝗂𝗉𝗉𝖾𝖽: <code>{no_media + unsupported}</code>\n𝖴𝗇𝗌𝗎𝗉𝗉𝗈𝗋𝗍𝖾𝖽 𝖬𝖾𝖽𝗂𝖺: <code>{unsupported}</code>\n𝖤𝗋𝗋𝗈𝗋𝗌 𝖮𝖼𝖼𝗎𝗋𝗋𝖾𝖽: <code>{errors}</code>", reply_markup=InlineKeyboardMarkup(btn))
                    await asyncio.sleep(2)
                if message.empty:
                    deleted += 1
                    continue
                elif not message.media:
                    no_media += 1
                    continue
                elif message.media not in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
                    unsupported += 1
                    continue
                media = getattr(message, message.media.value, None)
                if not media:
                    unsupported += 1
                    continue
                elif media.mime_type not in ['video/mp4', 'video/x-matroska']:
                    unsupported += 1
                    continue
                media.caption = message.caption
                sts = await save_file(media)
                if sts == 'suc':
                    total_files += 1
                elif sts == 'dup':
                    duplicate += 1
                elif sts == 'err':
                    errors += 1
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except Exception as e:
            await msg.reply(f'𝖨𝗇𝖽𝖾𝗑 𝖼𝖺𝗇𝖼𝖾𝗅𝖾𝖽 𝖽𝗎𝖾 𝗍𝗈 𝖤𝗋𝗋𝗈𝗋 - {e}')
        else:
            time_taken = get_readable_time(time.time()-start_time)
            await msg.edit(f'𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗌𝖺𝗏𝖾𝖽 <code>{total_files}</code> 𝗍𝗈 𝖣𝖺𝗍𝖺𝖻𝖺𝗌𝖾!\n𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 𝗂𝗇 {time_taken}\n\n𝖣𝗎𝗉𝗅𝗂𝖼𝖺𝗍𝖾 𝖥𝗂𝗅𝖾𝗌 𝖲𝗄𝗂𝗉𝗉𝖾𝖽: <code>{duplicate}</code>\n𝖣𝖾𝗅𝖾𝗍𝖾𝖽 𝖬𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝖲𝗄𝗂𝗉𝗉𝖾𝖽: <code>{deleted}</code>\n𝖭𝗈𝗇-𝖬𝖾𝖽𝗂𝖺 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝗌𝗄𝗂𝗉𝗉𝖾𝖽: <code>{no_media + unsupported}</code>\n𝖴𝗇𝗌𝗎𝗉𝗉𝗈𝗋𝗍𝖾𝖽 𝖬𝖾𝖽𝗂𝖺: <code>{unsupported}</code>\n𝖤𝗋𝗋𝗈𝗋𝗌 𝖮𝖼𝖼𝗎𝗋𝗋𝖾𝖽: <code>{errors}</code>')
