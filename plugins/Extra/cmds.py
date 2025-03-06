import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, BotCommand
from utils import is_check_admin
from Script import script
from info import ADMINS, admin_cmds, cmds


@Client.on_message(filters.command('grp_cmds'))
async def grp_cmds(client, message):
    user_id = message.from_user.id if message.from_user else None
    if not user_id:
        return await message.reply("<b>💔 𝖸𝗈𝗎 𝖺𝗋𝖾 𝖺𝗇𝗈𝗇𝗒𝗆𝗈𝗎𝗌 𝖺𝖽𝗆𝗂𝗇 𝗒𝗈𝗎 𝖼𝖺𝗇'𝗍 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽...</b>")
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<code>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗂𝗇 𝖺 𝗀𝗋𝗈𝗎𝗉.</code>")
    grp_id = message.chat.id
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉</b>')
    #title = message.chat.title
    buttons = [[
                InlineKeyboardButton('❌ 𝗖𝗹𝗼𝘀𝗲 ❌', callback_data='close_data')
            ]]        
    await message.reply_text(
        text=script.GROUP_C_TEXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=enums.ParseMode.HTML
        )
    

@Client.on_message(filters.command("admin_cmds") & filters.user(ADMINS))
async def admin_cmds(client, message):
    buttons = []
    for i in range(0, len(admin_cmds), 2):
        if i + 1 < len(admin_cmds):
            buttons.append([KeyboardButton(vp[i]), KeyboardButton(vp[i + 1])])
        else:
            buttons.append([KeyboardButton(vp[i])])

    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
   
    sent_message = await message.reply(
        "<b>𝖠𝖽𝗆𝗂𝗇 𝖠𝗅𝗅 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌 [𝖺𝗎𝗍𝗈 𝖽𝖾𝗅𝖾𝗍𝖾 2 𝗆𝗂𝗇] 👇</b>",
        reply_markup=reply_markup,
    ) 
    #  2 minutes (120 seconds)
    await asyncio.sleep(120)
    await sent_message.delete()
    await message.delete()


@Client.on_message(filters.command("commands") & filters.user(ADMINS))
async def set_commands(client, message):
    commands = []
    for item in vp:
        for command, description in item.items():
            commands.append(BotCommand(command, description))

    await client.set_bot_commands(commands)
    await message.reply("𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌 𝗌𝖾𝗍 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 ✅ ")
