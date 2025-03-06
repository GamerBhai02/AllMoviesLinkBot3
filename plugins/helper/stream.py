from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from info import URL, LOG_CHANNEL
from urllib.parse import quote_plus
from Jisshu.util.file_properties import get_name, get_hash, get_media_file_size
from Jisshu.util.human_readable import humanbytes
import humanize
import random

@Client.on_message(filters.private & filters.command("streams"))
async def stream_start(client, message):
    msg = await client.ask(message.chat.id, "𝖭𝗈𝗐 𝗌𝖾𝗇𝖽 𝗆𝖾 𝗒𝗈𝗎𝗋 𝖿𝗂𝗅𝖾/𝗏𝗂𝖽𝖾𝗈 𝗍𝗈 𝗀𝖾𝗍 𝗌𝗍𝗋𝖾𝖺𝗆 𝖺𝗇𝖽 𝖽𝗈𝗐𝗇𝗅𝗈𝖺𝖽 𝗅𝗂𝗇𝗄")
    if not msg.media:
        return await message.reply("𝖯𝗅𝖾𝖺𝗌𝖾 𝗌𝖾𝗇𝖽 𝗆𝖾 𝗌𝗎𝗉𝗉𝗈𝗋𝗍𝖾𝖽 𝗆𝖾𝖽𝗂𝖺")
    if msg.media in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
        file = getattr(msg, msg.media.value)
        filename = file.file_name
        filesize = humanize.naturalsize(file.file_size) 
        fileid = file.file_id
        user_id = message.from_user.id
        username =  message.from_user.mention 

        log_msg = await client.send_cached_media(
            chat_id=LOG_CHANNEL,
            file_id=fileid,
        )
        fileName = {quote_plus(get_name(log_msg))}
        stream = f"{URL}watch/{str(log_msg.id)}?hash={get_hash(log_msg)}"
        download = f"{URL}{str(log_msg.id)}?hash={get_hash(log_msg)}"
 
        await log_msg.reply_text(
            text=f"•• 𝖫𝗂𝗇𝗄 𝗀𝖾𝗇𝖾𝗋𝖺𝗍𝖾𝖽 𝖿𝗈𝗋 𝖨𝖣 #{user_id} \n•• 𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾: {username} \n\n•• 𝖥𝗂𝗅𝖾 𝗇𝖺𝗆𝖾: {fileName}",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 𝗙𝗮𝘀𝘁 𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 🚀", url=download),  # web download Link
                                                InlineKeyboardButton('🖥️ 𝗪𝗮𝘁𝗰𝗵 𝗢𝗻𝗹𝗶𝗻𝗲 🖥️', url=stream)]])  # web stream Link
        )
        rm=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("𝗦𝘁𝗿𝗲𝗮𝗺 🖥", url=stream),
                    InlineKeyboardButton('𝗗𝗼𝘄𝗻𝗹𝗼𝗮𝗱 📥', url=download)
                ]
            ] 
        )
        msg_text = """<i><u>𝗬𝗼𝘂𝗿 𝗹𝗶𝗻𝗸 𝗴𝗲𝗻𝗲𝗿𝗮𝘁𝗲𝗱!</u></i>\n\n<b>📂 𝖥𝗂𝗅𝖾 𝗇𝖺𝗆𝖾:</b> <i>{}</i>\n\n<b>📦 𝖥𝗂𝗅𝖾 𝗌𝗂𝗓𝖾:</b> <i>{}</i>\n\n<b>📥 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽:</b> <i>{}</i>\n\n<b>🖥 𝖶𝖺𝗍𝖼𝗁:</b> <i>{}</i>\n\n<b>🚸 𝖭𝗈𝗍𝖾: 𝖫𝗂𝗇𝗄 𝗐𝗈𝗇'𝗍 𝖾𝗑𝗉𝗂𝗋𝖾 𝗎𝗇𝗍𝗂𝗅 𝖨 𝖽𝖾𝗅𝖾𝗍𝖾</b>"""

        await message.reply_text(text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(msg)), download, stream), quote=True, disable_web_page_preview=True, reply_markup=rm)
