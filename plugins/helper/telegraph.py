import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command(["img", "cup", "telegraph"], prefixes="/") & filters.reply)
async def c_upload(client, message: Message):
    reply = message.reply_to_message

    if not reply.media:
        return await message.reply_text("𝖱𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺 𝗆𝖾𝖽𝗂𝖺 𝗍𝗈 𝗎𝗉𝗅𝗈𝖺𝖽 𝗂𝗍 𝗍𝗈 𝖢𝗅𝗈𝗎𝖽.")

    if reply.document and reply.document.file_size > 512 * 1024 * 1024:  # 512 MB
        return await message.reply_text("𝖥𝗂𝗅𝖾 𝗌𝗂𝗓𝖾 𝗅𝗂𝗆𝗂𝗍 𝗂𝗌 512 𝖬𝖡.")

    msg = await message.reply_text("𝖯𝗋𝗈𝖼𝖾𝗌𝗌𝗂𝗇𝗀...")

    try:
        downloaded_media = await reply.download()

        if not downloaded_media:
            return await msg.edit_text("𝖲𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝗐𝖾𝗇𝗍 𝗐𝗋𝗈𝗇𝗀 𝖽𝗎𝗋𝗂𝗇𝗀 𝗆𝗒 𝖽𝗈𝗐𝗇𝗅𝗈𝖺𝖽.")

        with open(downloaded_media, "rb") as f:
            data = f.read()
            resp = requests.post("https://envs.sh", files={"file": data})
            if resp.status_code == 200:
                await msg.edit_text(f"`{resp.text}`")
            else:
                await msg.edit_text("𝖲𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝗐𝖾𝗇𝗍 𝗐𝗋𝗈𝗇𝗀. 𝖯𝗅𝖾𝖺𝗌𝖾 𝗍𝗋𝗒 𝖺𝗀𝖺𝗂𝗇 𝗅𝖺𝗍𝖾𝗋.")

        os.remove(downloaded_media)

    except Exception as e:
        await msg.edit_text(f"𝖤𝗋𝗋𝗈𝗋: {str(e)}")


