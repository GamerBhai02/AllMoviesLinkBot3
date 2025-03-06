from datetime import timedelta
import pytz
import datetime, time
from Script import script 
from info import ADMINS, LOG_CHANNEL
from utils import get_seconds
from database.users_chats_db import db 
from pyrogram import Client, filters 
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command("add_premium"))
async def give_premium_cmd_handler(client, message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        await message.reply("𝖸𝗈𝗎 𝖽𝗈𝗇'𝗍 𝗁𝖺𝗏𝖾 𝖺𝗇𝗒 𝗉𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽.")
        return
    if len(message.command) == 3:
        user_id = int(message.command[1])  # Convert the user_id to integer
        user = await client.get_users(user_id)
        time = message.command[2]        
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            user_data = {"id": user_id, "expiry_time": expiry_time} 
            await db.update_user(user_data)  # Use the update_user method to update or insert user data
            await message.reply_text(f"𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖺𝖽𝖽𝖾𝖽 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗍𝗈 𝗍𝗁𝖾 𝗎𝗌𝖾𝗋.\n👤 𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾: {user.mention}\n⚡ 𝖴𝗌𝖾𝗋 𝖨𝖣: {user.id}\n⏰ 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖺𝖼𝖼𝖾𝗌𝗌: {time}")
            time_zone = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            current_time = time_zone.strftime("%d-%m-%Y\n⏱️ Joining time: %I:%M:%S %p")            
            expiry = expiry_time   
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ 𝖤𝗑𝗉𝗂𝗋𝗒 𝗍𝗂𝗆𝖾: %I:%M:%S %p")  
            await client.send_message(
                chat_id=user_id,
                text=f"𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖺𝖽𝖽𝖾𝖽 𝗍𝗈 𝗒𝗈𝗎𝗋 𝖺𝖼𝖼𝗈𝗎𝗇𝗍 𝖿𝗈𝗋 {time} 𝖤𝗇𝗃𝗈𝗒 😀\n\n⏳ 𝖩𝗈𝗂𝗇𝗂𝗇𝗀 𝖽𝖺𝗍𝖾: {current_time}\n\n⌛️ 𝖤𝗑𝗉𝗂𝗋𝗒 𝖽𝖺𝗍𝖾: {expiry_str_in_ist}",                
            )
            #user = await client.get_users(user_id)
            await client.send_message(LOG_CHANNEL, text=f"#Added_Premium\n\n👤 𝖴𝗌𝖾𝗋: {user.mention}\n⚡ 𝖴𝗌𝖾𝗋 𝖨𝖣: {user.id}\n⏰ 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖺𝖼𝖼𝖾𝗌𝗌: {time}\n\n⏳ 𝖩𝗈𝗂𝗇𝗂𝗇𝗀 𝖽𝖺𝗍𝖾 : {current_time}\n\n⌛️ 𝖤𝗑𝗉𝗂𝗋𝗒 𝖽𝖺𝗍𝖾: {expiry_str_in_ist}", disable_web_page_preview=True)
                
        else:
            await message.reply_text("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝗍𝗂𝗆𝖾 𝖿𝗈𝗋𝗆𝖺𝗍. 𝖯𝗅𝖾𝖺𝗌𝖾 𝗎𝗌𝖾 '1day for days', '1hour for hours', or '1min for minutes', or '1month for months' or '1year for year'")
    else:
        await message.reply_text("𝖴𝗌𝖺𝗀𝖾: /add_premium user_id time \n\n𝖤𝗑𝖺𝗆𝗉𝗅𝖾 /add_premium 1252789 10day \n\n(e.g. 𝖿𝗈𝗋 𝗍𝗂𝗆𝖾 𝗎𝗇𝗂𝗍𝗌 '1day for days', '1hour for hours', 𝗈𝗋 '1min for minutes', 𝗈𝗋 '1month for months' 𝗈𝗋 '1year for year')")

@Client.on_message(filters.command("myplan"))
async def check_plans_cmd(client, message):
    user = message.from_user.mention
    user_id  = message.from_user.id
    if await db.has_premium_access(user_id):         
        remaining_time = await db.check_remaining_uasge(user_id)             
        days = remaining_time.days
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        formatted_remaining_time = f"{days} 𝖣𝖺𝗒𝗌, {hours} 𝖧𝗈𝗎𝗋𝗌, {minutes} 𝖬𝗂𝗇𝗎𝗍𝖾𝗌, {seconds} 𝖲𝖾𝖼𝗈𝗇𝖽𝗌"
        expiry_time = remaining_time + datetime.datetime.now()
        expiry_date = expiry_time.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y")
        expiry_time = expiry_time.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%I:%M:%S %p")  # Format time in IST (12-hour format)
        await message.reply_text(f"📝 <u>𝖸𝗈𝗎𝗋 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝗌𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 𝖽𝖾𝗍𝖺𝗂𝗅𝗌</u> :\n\n👤 𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾: {user}\n🏷️ 𝖴𝗌𝖾𝗋 𝖨𝖣: <code>{user_id}</code>\n⏱️ 𝖤𝗑𝗉𝗂𝗋𝗒 𝖽𝖺𝗍𝖾: {expiry_date}\n⏱️ 𝖤𝗑𝗉𝗂𝗋𝗒 𝗍𝗂𝗆𝖾 : {expiry_time}\n⏳ 𝖱𝖾𝗆𝖺𝗂𝗇𝗂𝗇𝗀 𝗍𝗂𝗆𝖾: {formatted_remaining_time}")
    else:
        btn = [ 
            [InlineKeyboardButton("𝗚𝗲𝘁 𝗙𝗿𝗲𝗲 𝗧𝗿𝗶𝗮𝗹 𝗳𝗼𝗿 5 𝗠𝗶𝗻𝘂𝘁𝗲𝘀 ☺️", callback_data="give_trial")],
            [InlineKeyboardButton("𝗕𝘂𝘆 𝗦𝘂𝗯𝘀𝗰𝗿𝗶𝗽𝘁𝗶𝗼𝗻 : 𝗥𝗲𝗺𝗼𝘃𝗲 𝗔𝗱𝘀", callback_data="seeplans")],
        ]
        reply_markup = InlineKeyboardMarkup(btn)
        await message.reply_text(f"😔 𝖸𝗈𝗎 𝖽𝗈𝗇'𝗍 𝗁𝖺𝗏𝖾 𝖺𝗇𝗒 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝗌𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇. 𝖨𝖿 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝖻𝗎𝗒 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝖼𝗅𝗂𝖼𝗄 𝗈𝗇 𝖻𝖾𝗅𝗈𝗐 𝖻𝗎𝗍𝗍𝗈𝗇.\n\n𝖳𝗈 𝗎𝗌𝖾 𝗈𝗎𝗋 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝖿𝖾𝖺𝗍𝗎𝗋𝖾𝗌 𝖿𝗈𝗋 5 𝗆𝗂𝗇𝗎𝗍𝖾𝗌 𝖼𝗅𝗂𝖼𝗄 𝗈𝗇 𝖿𝗋𝖾𝖾 𝗍𝗋𝖺𝗂𝗅 𝖻𝗎𝗍𝗍𝗈𝗇.",reply_markup=reply_markup)


@Client.on_message(filters.command("remove_premium"))
async def remove_premium(client, message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        await message.reply_text("𝖸𝗈𝗎 𝖽𝗈𝗇'𝗍 𝗁𝖺𝗏𝖾 𝖺𝗇𝗒 𝗉𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽.")
        return
    if len(message.command) == 2:
        user_id = int(message.command[1])  # Convert the user_id to integer
        user = await client.get_users(user_id)
        if await db.remove_premium_access(user_id):
            await message.reply_text("𝖴𝗌𝖾𝗋 𝗋𝖾𝗆𝗈𝗏𝖾𝖽 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒!")
            await client.send_message(
                chat_id=user_id,
                text=f"<b>ʜᴇʏ {user.mention},\n\n𝖸𝗈𝗎𝗋 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝗉𝗅𝖺𝗇 𝗁𝖺𝗌 𝖻𝖾𝖾𝗇 𝖾𝗑𝗉𝗂𝗋𝖾𝖽.\n\n𝖨𝖿 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝖻𝗎𝗒 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝖺𝗀𝖺𝗂𝗇 𝗍𝗁𝖾𝗇 𝖼𝗅𝗂𝖼𝗄 𝗈𝗇 /plan 𝖳𝗈 𝖼𝗁𝖾𝖼𝗄 𝗈𝗎𝗍 𝗈𝗍𝗁𝖾𝗋 𝗉𝗅𝖺𝗇𝗌.</b>"
            )
        else:
            await message.reply_text("𝖴𝗇𝖺𝖻𝗅𝖾 𝗍𝗈 𝗋𝖾𝗆𝗈𝗏𝖾 𝗎𝗌𝖾𝗋!\n𝖠𝗋𝖾 𝗒𝗈𝗎 𝗌𝗎𝗋𝖾, 𝗂𝗍 𝗐𝖺𝗌 𝖺 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝗎𝗌𝖾𝗋 𝗂𝖽?")
    else:
        await message.reply_text("𝖴𝗌𝖺𝗀𝖾: /remove_premium user_id") 
      

@Client.on_message(filters.command("premium_users"))
async def premium_users_info(client, message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        await message.reply("𝖸𝗈𝗎 𝖽𝗈𝗇'𝗍 𝗁𝖺𝗏𝖾 𝖺𝗇𝗒 𝗉𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽.")
        return

    count = await db.all_premium_users()
    await message.reply(f"👥 𝖳𝗈𝗍𝖺𝗅 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖴𝗌𝖾𝗋𝗌 - {count}\n\n<i>𝖯𝗅𝖾𝖺𝗌𝖾 𝗐𝖺𝗂𝗍, 𝖿𝖾𝗍𝖼𝗁𝗂𝗇𝗀 𝖿𝗎𝗅𝗅 𝗂𝗇𝖿𝗈 𝗈𝖿 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝗎𝗌𝖾𝗋𝗌</i>")

    users = await db.get_all_users()
    new = "📝 <u>𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝗎𝗌𝖾𝗋𝗌 𝗂𝗇𝖿𝗈𝗋𝗆𝖺𝗍𝗂𝗈𝗇</u>:\n\n"
    user_count = 1
    async for user in users:
        data = await db.get_user(user['id'])
        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time")
            expiry_ist = expiry.astimezone(pytz.timezone("Asia/Kolkata"))
            current_time = datetime.datetime.now(pytz.timezone("Asia/Kolkata"))
            
            if current_time > expiry_ist:
                await db.remove_premium_access(user['id'])  # Remove premium access if expired
                continue  # Skip the user if their expiry time has passed
                
            expiry_str_in_ist = expiry_ist.strftime("%d-%m-%Y")
            expiry_time_in_ist = expiry_ist.strftime("%I:%M:%S %p")
            time_left = expiry_ist - current_time
            
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left_str = f"{days} 𝖣𝖺𝗒𝗌, {hours} 𝖧𝗈𝗎𝗋𝗌, {minutes} 𝖬𝗂𝗇𝗎𝗍𝖾𝗌, {seconds} 𝖲𝖾𝖼𝗈𝗇𝖽𝗌"
            
            new += f"{user_count}. {(await client.get_users(user['id'])).mention}\n👤 𝖴𝗌𝖾𝗋 𝖨𝖣: <code>{user['id']}</code>\n⏱️ 𝖤𝗑𝗉𝗂𝗋𝖾𝖽 𝖣𝖺𝗍𝖾: {expiry_str_in_ist}\n⏱️ 𝖤𝗑𝗉𝗂𝗋𝖾𝖽 𝗍𝗂𝗆𝖾: {expiry_time_in_ist}\n⏳ 𝖱𝖾𝗆𝖺𝗂𝗇𝗂𝗇𝗀 𝖳𝗂𝗆𝖾: {time_left_str}\n\n"
            user_count += 1
        else:
            pass
    
    try:
        await message.reply(new)
    except MessageTooLong:
        with open('premium_users_info.txt', 'w+') as outfile:
            outfile.write(new)
        await message.reply_document('premium_users_info.txt', caption="𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝗎𝗌𝖾𝗋𝗌 𝗂𝗇𝖿𝗈𝗋𝗆𝖺𝗍𝗂𝗈𝗇:")

# Free Trail Remove ( Give Credit To - NBBotz )
@Client.on_message(filters.command("refresh"))
async def reset_trial(client, message):
    user_id = message.from_user.id
    if user_id not in ADMINS:
        await message.reply("𝖸𝗈𝗎 𝖽𝗈𝗇'𝗍 𝗁𝖺𝗏𝖾 𝖺𝗇𝗒 𝗉𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽.")
        return

    try:
        if len(message.command) > 1:
            target_user_id = int(message.command[1])
            updated_count = await db.reset_free_trial(target_user_id)
            message_text = f"𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗋𝖾𝗌𝖾𝗍 𝖿𝗋𝖾𝖾 𝗍𝗋𝗂𝖺𝗅 𝖿𝗈𝗋 𝗎𝗌𝖾𝗋𝗌 {target_user_id}." if updated_count else f"𝖴𝗌𝖾𝗋 {target_user_id} 𝗇𝗈𝗍 𝖿𝗈𝗎𝗇𝖽 𝗈𝗋 𝖽𝗂𝖽𝗇'𝗍 𝖼𝗅𝖺𝗂𝗆 𝖿𝗋𝖾𝖾 𝗍𝗋𝗂𝖺𝗅 𝗒𝖾𝗍."
        else:
            updated_count = await db.reset_free_trial()
            message_text = f"𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗋𝖾𝗌𝖾𝗍 𝖿𝗋𝖾𝖾 𝗍𝗋𝗂𝖺𝗅 𝖿𝗈𝗋 {updated_count} 𝗎𝗌𝖾𝗋𝗌."

        await message.reply_text(message_text)
    except Exception as e:
        await message.reply_text(f"𝖠𝗇 𝖾𝗋𝗋𝗈𝗋 𝗈𝖼𝖼𝗎𝗋𝗋𝖾𝖽: {e}")
       

@Client.on_message(filters.command("plan"))
async def plan(client, message):
    user_id = message.from_user.id 
    users = message.from_user.mention 
    btn = [[
	
        InlineKeyboardButton("🍁 𝗖𝗵𝗲𝗰𝗸 𝗔𝗹𝗹 𝗣𝗹𝗮𝗻𝘀 𝗮𝗻𝗱 𝗣𝗿𝗶𝗰𝗲𝘀 🍁", callback_data='free')],[InlineKeyboardButton("❌ 𝗖𝗹𝗼𝘀𝗲 ❌", callback_data="close_data")
    ]]
    await message.reply_photo(photo="https://telegra.ph/file/4963dfeee700078956e76.jpg", caption=script.PREPLANS_TXT.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(btn))
    
