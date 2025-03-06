from datetime import timedelta, datetime
import pytz
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from info import ADMINS, LOG_CHANNEL
from utils import get_seconds
from database.users_chats_db import db
import string
import random

VALID_REDEEM_CODES = {}

def generate_code(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

@Client.on_message(filters.command("add_redeem") & filters.user(ADMINS))
async def add_redeem_code(client, message):
    user_id = message.from_user.id
    if len(message.command) == 3:
        try:
            time = message.command[1]
            num_codes = int(message.command[2])
        except ValueError:
            await message.reply_text("𝖯𝗅𝖾𝖺𝗌𝖾 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝖺 𝗏𝖺𝗅𝗂𝖽 𝗇𝗎𝗆𝖻𝖾𝗋 𝗈𝖿 𝖼𝗈𝖽𝖾𝗌 𝗍𝗈 𝗀𝖾𝗇𝖾𝗋𝖺𝗍𝖾.")
            return

        codes = []
        for _ in range(num_codes):
            code = generate_code()
            VALID_REDEEM_CODES[code] = time
            codes.append(code)

        codes_text = '\n'.join(f"➔ <code>/redeem {code}</code>" for code in codes)
        response_text = f"""
<b>𝖦𝗂𝖿𝗍 𝖢𝗈𝖽𝖾 𝖦𝖾𝗇𝖾𝗋𝖺𝗍𝖾𝖽 ✅
𝖠𝗆𝗈𝗎𝗇𝗍:</b> {num_codes}

{codes_text}
<b>𝖣𝗎𝗋𝖺𝗍𝗂𝗈𝗇:</b> {time}

🔰<u>𝗥𝗲𝗱𝗲𝗲𝗺 𝗜𝗻𝘀𝘁𝗿𝘂𝗰𝘁𝗶𝗼𝗻𝘀</u>🔰
<b>𝖩𝗎𝗌𝗍 𝖼𝗅𝗂𝖼𝗄 𝗍𝗁𝖾 𝖺𝖻𝗈𝗏𝖾 𝖼𝗈𝖽𝖾 𝗍𝗈 𝖼𝗈𝗉𝗒 𝖺𝗇𝖽 𝗍𝗁𝖾𝗇 𝗌𝖾𝗇𝖽 𝗍𝗁𝖺𝗍 𝖼𝗈𝖽𝖾 𝗍𝗈 𝗍𝗁𝖾 𝖡𝗈𝗍, 𝗍𝗁𝖺𝗍'𝗌 𝗂𝗍 🔥</b>"""

        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("♻️ 𝗥𝗲𝗱𝗲𝗲𝗺 𝗛𝗲𝗿𝗲 ♻️", url="http://t.me/AllMoviesLinkBot")],
                [InlineKeyboardButton("❕ 𝗔𝗻𝘆 𝗛𝗲𝗹𝗽 ❕", url="https://t.me/GamerBhai02Bot")]
            ]
        )

        await message.reply_text(response_text, reply_markup=keyboard)
    else:
        await message.reply_text("<b>♻ 𝖴𝗌𝖺𝗀𝖾:\n\n➩ <code>/add_redeem 1min 1</code>,\n➩ <code>/add_redeem 1hour 10</code>,\n➩ <code>/add_redeem 1day 5</code></b>")

@Client.on_message(filters.command("redeem"))
async def redeem_code(client, message):
    user_id = message.from_user.id
    if len(message.command) == 2:
        redeem_code = message.command[1]

        if redeem_code in VALID_REDEEM_CODES:
            try:
                time = VALID_REDEEM_CODES.pop(redeem_code)
                user = await client.get_users(user_id)

                try:
                    seconds = await get_seconds(time)
                except Exception as e:
                    await message.reply_text("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝗍𝗂𝗆𝖾 𝖿𝗈𝗋𝗆𝖺𝗍 𝗂𝗇 𝗋𝖾𝖽𝖾𝖾𝗆 𝖼𝗈𝖽𝖾.")
                    return

                if seconds > 0:
                    data = await db.get_user(user_id)
                    current_expiry = data.get("expiry_time") if data else None

                    now_aware = datetime.now(pytz.utc)

                    if current_expiry:
                        current_expiry = current_expiry.replace(tzinfo=pytz.utc)

                    if current_expiry and current_expiry > now_aware:
                        expiry_str_in_ist = current_expiry.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ 𝖤𝗑𝗉𝗂𝗋𝗒 𝖳𝗂𝗆𝖾: %I:%M:%S %p")
                        await message.reply_text(
                            f"🚫 𝖸𝗈𝗎 𝖺𝗅𝗋𝖾𝖺𝖽𝗒 𝗁𝖺𝗏𝖾 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝖺𝖼𝖼𝖾𝗌𝗌, 𝗐𝗁𝗂𝖼𝗁 𝖾𝗑𝗉𝗂𝗋𝖾𝗌 𝗈𝗇 {expiry_str_in_ist}.\n𝖸𝗈𝗎 𝖼𝖺𝗇𝗇𝗈𝗍 𝗋𝖾𝖽𝖾𝖾𝗆 𝖺𝗇𝗈𝗍𝗁𝖾𝗋 𝖼𝗈𝖽𝖾 𝗎𝗇𝗍𝗂𝗅 𝗒𝗈𝗎𝗋 𝖼𝗎𝗋𝗋𝖾𝗇𝗍 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝖾𝗑𝗉𝗂𝗋𝖾𝗌.",
                            disable_web_page_preview=True
                        )
                        return

                    expiry_time = now_aware + timedelta(seconds=seconds)
                    user_data = {"id": user_id, "expiry_time": expiry_time}
                    await db.update_user(user_data)

                    expiry_str_in_ist = expiry_time.astimezone(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y\n⏱️ 𝖤𝗑𝗉𝗂𝗋𝗒 𝖳𝗂𝗆𝖾: %I:%M:%S %p")

                    await message.reply_text(
                        f"𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖺𝖼𝗍𝗂𝗏𝖺𝗍𝖾𝖽 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒!\n\n𝖴𝗌𝖾𝗋: {user.mention}\nUser ID: {user_id}\n𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖠𝖼𝖼𝖾𝗌𝗌: <code>{time}</code>\n\n𝖤𝗑𝗉𝗂𝗋𝗒 𝖣𝖺𝗍𝖾: {expiry_str_in_ist}",
                        disable_web_page_preview=True
                    )

                    await client.send_message(
                        LOG_CHANNEL,
                        text=f"#Redeemed_Premium\n\n👤 𝖴𝗌𝖾𝗋: {user.mention}\n⚡ 𝖴𝗌𝖾𝗋 𝖨𝖣: <code>{user_id}</code>\n⏰ 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖠𝖼𝖼𝖾𝗌𝗌: <code>{time}</code>\n⌛️ 𝖤𝗑𝗉𝗂𝗋𝗒 𝖣𝖺𝗍𝖾: {expiry_str_in_ist}",
                        disable_web_page_preview=True
                    )
                else:
                    await message.reply_text("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝗍𝗂𝗆𝖾 𝖿𝗈𝗋𝗆𝖺𝗍 𝗂𝗇 𝗋𝖾𝖽𝖾𝖾𝗆 𝖼𝗈𝖽𝖾.")
            except Exception as e:
                await message.reply_text(f"𝖠𝗇 𝖾𝗋𝗋𝗈𝗋 𝗈𝖼𝖼𝗎𝗋𝗋𝖾𝖽 𝗐𝗁𝗂𝗅𝖾 𝗋𝖾𝖽𝖾𝖾𝗆𝗂𝗇𝗀 𝗍𝗁𝖾 𝖼𝗈𝖽𝖾: {e}")
        else:
            await message.reply_text("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖱𝖾𝖽𝖾𝖾𝗆 𝖢𝗈𝖽𝖾 𝗈𝗋 𝖤𝗑𝗉𝗂𝗋𝖾𝖽.")
    else:
        await message.reply_text("𝖴𝗌𝖺𝗀𝖾: /redeem <code>")
