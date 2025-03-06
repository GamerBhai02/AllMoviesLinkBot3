import re
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
from database.config_db import mdb

# most search commands
@Client.on_message(filters.command('most'))
async def most(client, message):

    def is_alphanumeric(string):
        return bool(re.match('^[a-zA-Z0-9 ]*$', string))
    
    try:
        limit = int(message.command[1])
    except (IndexError, ValueError):
        limit = 20

    top_messages = await mdb.get_top_messages(limit)

    # Use a set to ensure unique messages (case sensitive).
    seen_messages = set()
    truncated_messages = []

    for msg in top_messages:
        # Check if message already exists in the set (case sensitive)
        if msg.lower() not in seen_messages and is_alphanumeric(msg):
            seen_messages.add(msg.lower())
            
            if len(msg) > 35:
                truncated_messages.append(msg[:35 - 3])
            else:
                truncated_messages.append(msg)

    keyboard = []
    for i in range(0, len(truncated_messages), 2):
        row = truncated_messages[i:i+2]
        keyboard.append(row)
    
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True, placeholder="Most searches of the day")
    m=await message.reply_text("𝗣𝗹𝗲𝗮𝘀𝗲 𝗪𝗮𝗶𝘁, 𝗙𝗲𝘁𝗰𝗵𝗶𝗻𝗴 𝗠𝗼𝘀𝘁 𝗦𝗲𝗮𝗿𝗰𝗵𝗲𝘀 𝗼𝗳 𝗧𝗵𝗲 𝗗𝗮𝘆.")
    await m.edit_text("𝗣𝗹𝗲𝗮𝘀𝗲 𝗪𝗮𝗶𝘁, 𝗙𝗲𝘁𝗰𝗵𝗶𝗻𝗴 𝗠𝗼𝘀𝘁 𝗦𝗲𝗮𝗿𝗰𝗵𝗲𝘀 𝗼𝗳 𝗧𝗵𝗲 𝗗𝗮𝘆..")
    await m.delete()
    await message.reply_text(f"<b>𝖧𝖾𝗋𝖾 𝗂𝗌 𝗍𝗁𝖾 𝖬𝗈𝗌𝗍 𝖲𝖾𝖺𝗋𝖼𝗁𝖾𝗌 𝖫𝗂𝗌𝗍 👇</b>", reply_markup=reply_markup)

    
@Client.on_message(filters.command('mostlist'))
async def trendlist(client, message):
    def is_alphanumeric(string):
        return bool(re.match('^[a-zA-Z0-9 ]*$', string))

    # Set the limit to the default if no argument is provided
    limit = 31

    # Check if an argument is provided and if it's a valid number
    if len(message.command) > 1:
        try:
            limit = int(message.command[1])
        except ValueError:
            await message.reply_text("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝗇𝗎𝗆𝖻𝖾𝗋 𝖿𝗈𝗋𝗆𝖺𝗍.\n𝖯𝗅𝖾𝖺𝗌𝖾 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝖺 𝗏𝖺𝗅𝗂𝖽 𝗇𝗎𝗆𝖻𝖾𝗋 𝖺𝖿𝗍𝖾𝗋 𝗍𝗁𝖾 /trendlist 𝖼𝗈𝗆𝗆𝖺𝗇𝖽.")
            return  # Exit the function if the argument is not a valid integer

    try:
        top_messages = await mdb.get_top_messages(limit)
    except Exception as e:
        await message.reply_text(f"𝖤𝗋𝗋𝗈𝗋 𝗋𝖾𝗍𝗋𝗂𝖾𝗏𝗂𝗇𝗀 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌: {str(e)}")
        return  # Exit the function if there is an error retrieving messages

    if not top_messages:
        await message.reply_text("𝖭𝗈 𝗆𝗈𝗌𝗍 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝖿𝗈𝗎𝗇𝖽.")
        return  # Exit the function if no messages are found

    seen_messages = set()
    truncated_messages = []

    for msg in top_messages:
        if msg.lower() not in seen_messages and is_alphanumeric(msg):
            seen_messages.add(msg.lower())
            
            # Add an ellipsis to indicate the message has been truncated
            truncated_messages.append(msg[:32] + '...' if len(msg) > 35 else msg)

    if not truncated_messages:
        await message.reply_text("𝖭𝗈 𝗏𝖺𝗅𝗂𝖽 𝗆𝗈𝗌𝗍 𝗆𝖾𝗌𝗌𝖺𝗀𝖾𝗌 𝖿𝗈𝗎𝗇𝖽.")
        return  # Exit the function if no valid messages are found

    # Create a formatted text list
    formatted_list = "\n".join([f"{i+1}. <b>{msg}</b>" for i, msg in enumerate(truncated_messages)])

    # Append the additional message at the end
    additional_message = "𝗔𝗹𝗹 𝘁𝗵𝗲 𝗿𝗲𝘀𝘂𝗹𝘁𝘀 𝗮𝗯𝗼𝘃𝗲 𝗰𝗼𝗺𝗲 𝗳𝗿𝗼𝗺 𝘄𝗵𝗮𝘁 𝘂𝘀𝗲𝗿𝘀 𝗵𝗮𝘃𝗲 𝘀𝗲𝗮𝗿𝗰𝗵𝗲𝗱 𝗳𝗼𝗿. 𝗧𝗵𝗲𝘆'𝗿𝗲 𝘀𝗵𝗼𝘄𝗻 𝘁𝗼 𝘆𝗼𝘂 𝗲𝘅𝗮𝗰𝘁𝗹𝘆 𝗮𝘀 𝘁𝗵𝗲𝘆 𝘄𝗲𝗿𝗲 𝘀𝗲𝗮𝗿𝗰𝗵𝗲𝗱, 𝘄𝗶𝘁𝗵𝗼𝘂𝘁 𝗮𝗻𝘆 𝗰𝗵𝗮𝗻𝗴𝗲𝘀 𝗯𝘆 𝘁𝗵𝗲 𝗼𝘄𝗻𝗲𝗿."
    formatted_list += f"\n\n{additional_message}"

    reply_text = f"<b><u>𝖳𝗈𝗉 {len(truncated_messages)} 𝖬𝗈𝗌𝗍 𝖲𝖾𝖺𝗋𝖼𝗁𝖾𝗌 𝖫𝗂𝗌𝗍:</u></b>\n\n{formatted_list}"
    
    await message.reply_text(reply_text)
