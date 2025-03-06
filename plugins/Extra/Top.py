from pyrogram import Client, filters
from info import ADMINS, DATABASE_URI
from pyrogram.types import ReplyKeyboardMarkup
import asyncio
from database.topdb import JsTopDB

movie_series_db = JsTopDB(DATABASE_URI)
    

# top trending commands
@Client.on_message(filters.command("setlist") & filters.private & filters.user(ADMINS))
async def set_movie_series_names_command(client, message):
  
    try:
        command, *names = message.text.split(maxsplit=1)
    except ValueError:
        await message.reply("𝖯𝗅𝖾𝖺𝗌𝖾 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝖺 𝗅𝗂𝗌𝗍 𝗈𝖿 𝗆𝗈𝗏𝗂𝖾𝗌 𝖺𝗇𝖽 𝗌𝖾𝗋𝗂𝖾𝗌 𝗇𝖺𝗆𝖾𝗌 𝖺𝖿𝗍𝖾𝗋 𝗍𝗁𝖾 𝖼𝗈𝗆𝗆𝖺𝗇𝖽.")
        return

    if not names:
        await message.reply("𝖯𝗅𝖾𝖺𝗌𝖾 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝖺 𝗅𝗂𝗌𝗍 𝗈𝖿 𝗆𝗈𝗏𝗂𝖾𝗌 𝖺𝗇𝖽 𝗌𝖾𝗋𝗂𝖾𝗌 𝗇𝖺𝗆𝖾𝗌 𝖺𝖿𝗍𝖾𝗋 𝗍𝗁𝖾 𝖼𝗈𝗆𝗆𝖺𝗇𝖽.")
        return

    names_string = " ".join(names)

    capitalized_names = ", ".join(" ".join(word.capitalize() for word in name.split()) for name in names_string.split(','))

    await movie_series_db.set_movie_series_names(capitalized_names, 1)

    await message.reply("𝖳𝗁𝖾 𝗅𝗂𝗌𝗍 𝗈𝖿 𝗆𝗈𝗏𝗂𝖾 𝖺𝗇𝖽 𝗌𝖾𝗋𝗂𝖾𝗌 𝗇𝖺𝗆𝖾𝗌 𝖿𝗈𝗋 𝗍𝗁𝖾 𝗌𝗎𝗀𝗀𝖾𝗌𝗍𝗂𝗈𝗇 𝗁𝖺𝗌 𝖻𝖾𝖾𝗇 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗎𝗉𝖽𝖺𝗍𝖾𝖽 ✅")

@Client.on_message(filters.command("trendlist"))
async def get_movie_series_names_command(client, message):
    current_names = await movie_series_db.get_movie_series_names(1)

    if current_names:
        response = "<b><u>𝖢𝗎𝗋𝗋𝖾𝗇𝗍 𝖫𝗂𝗌𝗍 𝗈𝖿 𝖳𝗈𝗉 𝖳𝗋𝖾𝗇𝖽𝗂𝗇𝗀:</u></b>\n"
        for i, name in enumerate(current_names, start=1):
            response += f"{i}. {name}\n"
        await message.reply(response.strip())
    else:
        await message.reply("𝖳𝗁𝖾 𝗅𝗂𝗌𝗍 𝗈𝖿 𝖳𝗈𝗉 𝖳𝗋𝖾𝗇𝖽𝗂𝗇𝗀 𝗂𝗌 𝖾𝗆𝗉𝗍𝗒 ❌")

@Client.on_message(filters.command("clearlist") & filters.private & filters.user(ADMINS))
async def clear_movie_series_names_command(client, message):
    await movie_series_db.clear_movie_series_names(1)
    await message.reply("𝖳𝗁𝖾 𝗍𝗈𝗉 𝗍𝗋𝖾𝗇𝖽𝗂𝗇𝗀 𝗅𝗂𝗌𝗍 𝗁𝖺𝗌 𝖻𝖾𝖾𝗇 𝖼𝗅𝖾𝖺𝗋𝖾𝖽 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 ✅")

@Client.on_message(filters.command("trend"))
async def trending_command(client, message):
  
    movie_series_names = await movie_series_db.get_movie_series_names(1)
    
    if not movie_series_names:
        await message.reply("𝖳𝗁𝖾𝗋𝖾 𝖺𝗋𝖾 𝗇𝗈 𝗆𝗈𝗏𝗂𝖾𝗌 𝗈𝗋 𝗌𝖾𝗋𝗂𝖾𝗌 𝗇𝖺𝗆𝖾𝗌 𝖺𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝖿𝗈𝗋 𝗍𝗁𝖾 𝖳𝗈𝗉 𝖲𝖾𝖺𝗋𝖼𝗁𝖾𝗌.")
        return

    buttons = [movie_series_names[i:i + 2] for i in range(0, len(movie_series_names), 2)]

    spika = ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True
    )
    m=await message.reply_text("𝗣𝗹𝗲𝗮𝘀𝗲 𝗪𝗮𝗶𝘁, 𝗙𝗲𝘁𝗰𝗵𝗶𝗻𝗴 𝗧𝗼𝗽 𝗧𝗿𝗲𝗻𝗱𝗶𝗻𝗴...")
    await m.delete()        
    await message.reply("<b>𝖧𝖾𝗋𝖾 𝗂𝗌 𝗍𝗁𝖾 𝖳𝗈𝗉 𝖳𝗋𝖾𝗇𝖽𝗂𝗇𝗀 𝗅𝗂𝗌𝗍 👇</b>", reply_markup=spika)
