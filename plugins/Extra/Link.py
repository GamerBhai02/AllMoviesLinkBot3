# powered by Jisshu_bots and ZISHAN KHAN
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command("link"))
async def generate_link(client, message):
    command_text = message.text.split(maxsplit=1)
    if len(command_text) < 2:
        await message.reply("𝖯𝗅𝖾𝖺𝗌𝖾 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝗍𝗁𝖾 𝗇𝖺𝗆𝖾 𝖿𝗈𝗋 𝗍𝗁𝖾 𝗆𝗈𝗏𝗂𝖾! 𝖤𝗑𝖺𝗆𝗉𝗅𝖾: `/link game of thrones`")
        return
    movie_name = command_text[1].replace(" ", "-")
    link = f"https://telegram.me/AllMoviesLinkBot?start=getfile-{movie_name}"
    
    await message.reply(
        text=f"Here is your link: {link}",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="𝖲𝗁𝖺𝗋𝖾 𝖫𝗂𝗇𝗄", url=f"https://telegram.me/share/url?url={link}")]]
        )
    )
