import os, requests
import logging
import random
import asyncio
import string
import pytz
from datetime import timedelta
from datetime import datetime as dt
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup , ForceReply, ReplyKeyboardMarkup
from database.ia_filterdb import Media, get_file_details, get_bad_files, unpack_new_file_id
from database.users_chats_db import db
from database.config_db import mdb
from database.topdb import JsTopDB
from database.jsreferdb import referdb
from plugins.pm_filter import auto_filter
from utils import formate_file_name,  get_settings, save_group_settings, is_req_subscribed, get_size, get_shortlink, is_check_admin, get_status, temp, get_readable_time, save_default_settings
import re
import base64
from info import *
import traceback
logger = logging.getLogger(__name__)
movie_series_db = JsTopDB(DATABASE_URI)
verification_ids = {}

# CHECK COMPONENTS FOLDER FOR MORE COMMANDS
@Client.on_message(filters.command("invite") & filters.private & filters.user(ADMINS))
async def invite(client, message):
    toGenInvLink = message.command[1]
    if len(toGenInvLink) != 14:
        return await message.reply("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖼𝗁𝖺𝗍 𝗂𝖽\n𝖠𝖽𝖽 -100 𝖻𝖾𝖿𝗈𝗋𝖾 𝖼𝗁𝖺𝗍 𝗂𝖽 𝗂𝖿 𝗒𝗈𝗎 𝖽𝗂𝖽 𝗇𝗈𝗍 𝖺𝖽𝖽 𝗒𝖾𝗍.") 
    try:
        link = await client.export_chat_invite_link(toGenInvLink)
        await message.reply(link)
    except Exception as e:
        print(f'𝖤𝗋𝗋𝗈𝗋 𝗐𝗁𝗂𝗅𝖾 𝗀𝖾𝗇𝖾𝗋𝖺𝗍𝗂𝗇𝗀 𝗂𝗇𝗏𝗂𝗍𝖾 𝗅𝗂𝗇𝗄 : {e}\n𝖥𝗈𝗋 𝖼𝗁𝖺𝗍:{toGenInvLink}')
        await message.reply(f'𝖤𝗋𝗋𝗈𝗋 𝗐𝗁𝗂𝗅𝖾 𝗀𝖾𝗇𝖾𝗋𝖺𝗍𝗂𝗇𝗀 𝗂𝗇𝗏𝗂𝗍𝖾 𝗅𝗂𝗇𝗄 : {e}\n𝖥𝗈𝗋 𝖼𝗁𝖺𝗍:{toGenInvLink}')


@Client.on_message(filters.command("start") & filters.incoming)
async def start(client:Client, message):
    await message.react(emoji=random.choice(REACTIONS))
    pm_mode = False
    try:
         data = message.command[1]
         if data.startswith('pm_mode_'):
             pm_mode = True
    except:
        pass
    m = message
    user_id = m.from_user.id
    if len(m.command) == 2 and m.command[1].startswith('notcopy'):
        _, userid, verify_id, file_id = m.command[1].split("_", 3)
        user_id = int(userid)
        grp_id = temp.CHAT.get(user_id, 0)
        settings = await get_settings(grp_id)         
        verify_id_info = await db.get_verify_id_info(user_id, verify_id)
        if not verify_id_info or verify_id_info["verified"]:
            await message.reply("<b>𝖫𝗂𝗇𝗄 𝖤𝗑𝗉𝗂𝗋𝖾𝖽 𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇...</b>")
            return  
        ist_timezone = pytz.timezone('Asia/Kolkata')
        if await db.user_verified(user_id):
            key = "third_time_verified"
        else:
            key = "second_time_verified" if await db.is_user_verified(user_id) else "last_verified"
        current_time = dt.now(tz=ist_timezone)
        result = await db.update_notcopy_user(user_id, {key:current_time})
        await db.update_verify_id_info(user_id, verify_id, {"verified":True})
        if key == "third_time_verified": 
            num = 3 
        else: 
            num =  2 if key == "second_time_verified" else 1 
        if key == "third_time_verified":
            msg = script.THIRDT_VERIFY_COMPLETE_TEXT
        else:
            msg = script.SECOND_VERIFY_COMPLETE_TEXT if key == "second_time_verified" else script.VERIFY_COMPLETE_TEXT
        await client.send_message(settings['log'], script.VERIFIED_LOG_TEXT.format(m.from_user.mention, user_id, dt.now(pytz.timezone('Asia/Kolkata')).strftime('%d %B %Y'), num))
        btn = [[
            InlineKeyboardButton("‼️ 𝗖𝗹𝗶𝗰𝗸 𝗵𝗲𝗿𝗲 𝘁𝗼 𝗚𝗲𝘁 𝗙𝗶𝗹𝗲 ‼️", url=f"https://telegram.me/{temp.U_NAME}?start=file_{grp_id}_{file_id}"),
        ]]
        reply_markup=InlineKeyboardMarkup(btn)
        await m.reply_photo(
            photo=(VERIFY_IMG),
            caption=msg.format(message.from_user.mention, get_readable_time(TWO_VERIFY_GAP)),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return 
        # refer 
    if len(message.command) == 2 and message.command[1].startswith("reff_"):
        try:
            user_id = int(message.command[1].split("_")[1])
        except ValueError:
            await message.reply_text("𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖱𝖾𝖿𝖾𝗋⁉️")
            return
        if user_id == message.from_user.id:
            await message.reply_text("𝖧𝖾𝗒 𝖣𝗎𝖽𝖾, 𝗒𝗈𝗎 𝖼𝖺𝗇𝗇𝗈𝗍 𝗋𝖾𝖿𝖾𝗋 𝗒𝗈𝗎𝗋𝗌𝖾𝗅𝖿⁉️")
            return
        if referdb.is_user_in_list(message.from_user.id):
            await message.reply_text("‼️ 𝖸𝗈𝗎 𝗁𝖺𝗏𝖾 𝖺𝗅𝗋𝖾𝖺𝖽𝗒 𝖻𝖾𝖾𝗇 𝗂𝗇𝗏𝗂𝗍𝖾𝖽 𝗈𝗋 𝗃𝗈𝗂𝗇𝖾𝖽")
            return
        if await db.is_user_exist(message.from_user.id): 
            await message.reply_text("‼️ 𝖸𝗈𝗎 𝗁𝖺𝗏𝖾 𝖺𝗅𝗋𝖾𝖺𝖽𝗒 𝖻𝖾𝖾𝗇 𝗂𝗇𝗏𝗂𝗍𝖾𝖽 𝗈𝗋 𝗃𝗈𝗂𝗇𝖾𝖽")
            return            
        try:
            uss = await client.get_users(user_id)
        except Exception:
            return
        referdb.add_user(message.from_user.id)
        fromuse = referdb.get_refer_points(user_id) + 10
        if fromuse == 100:
            referdb.add_refer_points(user_id, 0) 
            await message.reply_text(f"𝗬𝗼𝘂 𝗵𝗮𝘃𝗲 𝗯𝗲𝗲𝗻 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗶𝗻𝘃𝗶𝘁𝗲𝗱 𝗯𝘆  {uss.mention}!") 
            await client.send_message(user_id, text=f"𝗬𝗼𝘂 𝗵𝗮𝘃𝗲 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗶𝗻𝘃𝗶𝘁𝗲𝗱  {message.from_user.mention}!") 
            await add_premium(client, user_id, uss)
        else:
            referdb.add_refer_points(user_id, fromuse)
            await message.reply_text(f"𝗬𝗼𝘂 𝗵𝗮𝘃𝗲 𝗯𝗲𝗲𝗻 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗶𝗻𝘃𝗶𝘁𝗲𝗱 𝗯𝘆  {uss.mention}!")
            await client.send_message(user_id, f"𝗬𝗼𝘂 𝗵𝗮𝘃𝗲 𝘀𝘂𝗰𝗰𝗲𝘀𝘀𝗳𝘂𝗹𝗹𝘆 𝗶𝗻𝘃𝗶𝘁𝗲𝗱  {message.from_user.mention}!")
        return

    if len(message.command) == 2 and message.command[1].startswith('getfile'):
        searches = message.command[1].split("-", 1)[1] 
        search = searches.replace('-',' ')
        message.text = search 
        await auto_filter(client, message) 
        return

    if len(message.command) == 2 and message.command[1] in ["ads"]:
        msg, _, impression = await mdb.get_advirtisment()
        user = await db.get_user(message.from_user.id)
        seen_ads = user.get("seen_ads", False)
        JISSHU_ADS_LINK = await db.jisshu_get_ads_link()
        buttons = [[
                    InlineKeyboardButton('❌ 𝗖𝗹𝗼𝘀𝗲 ❌', callback_data='close_data')
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        if msg:
            await message.reply_photo(
                photo=JISSHU_ADS_LINK if JISSHU_ADS_LINK else URL,
                caption=msg,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )

            if impression is not None and not seen_ads:
                await mdb.update_advirtisment_impression(int(impression) - 1)
                await db.update_value(message.from_user.id, "seen_ads", True)
        else:
            await message.reply("<b>𝖭𝗈 𝖠𝖽𝗌 𝖥𝗈𝗎𝗇𝖽</b>")

        await mdb.reset_advertisement_if_expired()

        if msg is None and seen_ads:
            await db.update_value(message.from_user.id, "seen_ads", False)
        return
    
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        status = get_status()
        aks=await message.reply_text(f"<b>🔥 𝖸𝖾𝗌 {status},\n𝖧𝗈𝗐 𝖼𝖺𝗇 𝗂 𝗁𝖾𝗅𝗉 𝗒𝗈𝗎??</b>")
        await asyncio.sleep(600)
        await aks.delete()
        await m.delete()
        if (str(message.chat.id)).startswith("-100") and not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            group_link = await message.chat.export_invite_link()
            user = message.from_user.mention if message.from_user else "Dear" 
            await client.send_message(LOG_CHANNEL, script.NEW_GROUP_TXT.format(temp.B_LINK, message.chat.title, message.chat.id, message.chat.username, group_link, total, user))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.NEW_USER_TXT.format(temp.B_LINK, message.from_user.id, message.from_user.mention))
        try: 
         #   refData = message.command[1]
         #   if refData and refData.split("-", 1)[0] == "Jisshu":
         #       Fullref = refData.split("-", 1)
         #       refUserId = int(Fullref[1])
         #       await db.update_point(refUserId)
         #       newPoint = await db.get_point(refUserId)
             if AUTH_CHANNEL and await is_req_subscribed(client, message):
                        buttons = [[
                            InlineKeyboardButton('☆ 𝖠𝖽𝖽 𝖬𝖾 𝗍𝗈 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉 ☆', url=f'http://t.me/{temp.U_NAME}?startgroup=start')
                        ],[
                            InlineKeyboardButton("𝖧𝖾𝗅𝗉 ⚙️", callback_data='features'),
                            InlineKeyboardButton('𝖠𝖻𝗈𝗎𝗍 💌', callback_data=f'about')
                        ],[
                            InlineKeyboardButton('𝖯𝗋𝖾𝗆𝗂𝗎𝗆 🎫', callback_data='seeplans'),
                            InlineKeyboardButton('𝖱𝖾𝖿𝖾𝗋 ⚜️', callback_data="reffff")
                        ],[
                            InlineKeyboardButton('𝖬𝗈𝗌𝗍 𝖲𝖾𝖺𝗋𝖼𝗁𝖾𝖽 🔍', callback_data="mostsearch"),
                            InlineKeyboardButton('𝖳𝗈𝗉 𝖳𝗋𝖾𝗇𝖽𝗂𝗇𝗀 ⚡', callback_data="trending")
                        ]] 
                        reply_markup = InlineKeyboardMarkup(buttons)
                        m=await message.reply_sticker("CAACAgUAAxkBAAEN_ednyS4y5ZzxCHbLREN451YQI__J6gACCBQAAlnpSFb4TrqdAvsUsTYE") 
                        await asyncio.sleep(1)
                        await m.delete()
                        await message.reply_photo(photo=random.choice(START_IMG), caption=script.START_TXT.format(message.from_user.mention, get_status(), message.from_user.id),
                            reply_markup=reply_markup,
                            parse_mode=enums.ParseMode.HTML)
          #      try: 
          #          if newPoint == 0:
          #              await client.send_message(refUserId , script.REF_PREMEUM.format(PREMIUM_POINT))
          #          else: 
          #              await client.send_message(refUserId , script.REF_START.format(message.from_user.mention() , newPoint))
          #      except : pass
        except Exception as e:
            traceback.print_exc()
            pass
    if len(message.command) != 2:
        buttons = [[
                            InlineKeyboardButton('☆ 𝖠𝖽𝖽 𝖬𝖾 𝗍𝗈 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉 ☆', url=f'http://t.me/{temp.U_NAME}?startgroup=start')
                        ],[
                            InlineKeyboardButton("𝖧𝖾𝗅𝗉 ⚙️", callback_data='features'),
                            InlineKeyboardButton('𝖠𝖻𝗈𝗎𝗍 💌', callback_data=f'about')
                        ],[
                            InlineKeyboardButton('𝖯𝗋𝖾𝗆𝗂𝗎𝗆 🎫', callback_data='seeplans'),
                            InlineKeyboardButton('𝖱𝖾𝖿𝖾𝗋 ⚜️', callback_data="reffff")
                        ],[
                            InlineKeyboardButton('𝖬𝗈𝗌𝗍 𝖲𝖾𝖺𝗋𝖼𝗁𝖾𝖽 🔍', callback_data="mostsearch"),
                            InlineKeyboardButton('𝖳𝗈𝗉 𝖳𝗋𝖾𝗇𝖽𝗂𝗇𝗀 ⚡', callback_data="trending")
                        ]] 
        reply_markup = InlineKeyboardMarkup(buttons)
        m=await message.reply_sticker("CAACAgUAAxkBAAEN_ednyS4y5ZzxCHbLREN451YQI__J6gACCBQAAlnpSFb4TrqdAvsUsTYE") 
        await asyncio.sleep(1)
        await m.delete()
        await message.reply_photo(photo=random.choice(START_IMG), caption=script.START_TXT.format(message.from_user.mention, get_status(), message.from_user.id),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    if AUTH_CHANNEL and not await is_req_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL), creates_join_request=True)
        except ChatAdminRequired:
            logger.error("Make Sure Bot Is Admin In Forcesub Channel")
            return
        btn = [[
            InlineKeyboardButton("🎗️ 𝖩𝗈𝗂𝗇 𝖭𝗈𝗐 🎗️", url=invite_link.invite_link)
        ]]

        if message.command[1] != "subscribe":
            
            try:
                chksub_data = message.command[1].replace('pm_mode_', '') if pm_mode else message.command[1]
                kk, grp_id, file_id = chksub_data.split('_', 2)
                pre = 'checksubp' if kk == 'filep' else 'checksub'
                btn.append(
                    [InlineKeyboardButton("♻️ 𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇 ♻️", callback_data=f"checksub#{file_id}#{int(grp_id)}")]
                )
            except (IndexError, ValueError):
                print('IndexError: ', IndexError)
                btn.append(
                    [InlineKeyboardButton("♻️ 𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇 ♻️", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")]
                )
        reply_markup=InlineKeyboardMarkup(btn)
        await client.send_photo(
            chat_id=message.from_user.id,
            photo=FORCESUB_IMG, 
            caption=script.FORCESUB_TEXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
       # await client.send_message(
       #     chat_id=message.from_user.id,
       #     text="<b>🙁 ғɪʀꜱᴛ ᴊᴏɪɴ ᴏᴜʀ ʙᴀᴄᴋᴜᴘ ᴄʜᴀɴɴᴇʟ ᴛʜᴇɴ ʏᴏᴜ ᴡɪʟʟ ɢᴇᴛ ᴍᴏᴠɪᴇ, ᴏᴛʜᴇʀᴡɪꜱᴇ ʏᴏᴜ ᴡɪʟʟ ɴᴏᴛ ɢᴇᴛ ɪᴛ.\n\nᴄʟɪᴄᴋ ᴊᴏɪɴ ɴᴏᴡ ʙᴜᴛᴛᴏɴ 👇</b>",
       #     reply_markup=InlineKeyboardMarkup(btn),
       #     parse_mode=enums.ParseMode.HTML
    #    )
        return

    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
        buttons = [[
            InlineKeyboardButton('☆ 𝖠𝖽𝖽 𝖬𝖾 𝗍𝗈 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉 ☆', url=f'http://t.me/{temp.U_NAME}?startgroup=start')
                        ],[
                            InlineKeyboardButton("𝖧𝖾𝗅𝗉 ⚙️", callback_data='features'),
                            InlineKeyboardButton('𝖠𝖻𝗈𝗎𝗍 💌', callback_data=f'about')
                        ],[
                            InlineKeyboardButton('𝖯𝗋𝖾𝗆𝗂𝗎𝗆 🎫', callback_data='seeplans'),
                            InlineKeyboardButton('𝖱𝖾𝖿𝖾𝗋 ⚜️', callback_data="reffff")
                        ],[
                            InlineKeyboardButton('𝖬𝗈𝗌𝗍 𝖲𝖾𝖺𝗋𝖼𝗁𝖾𝖽 🔍', callback_data="mostsearch"),
                            InlineKeyboardButton('𝖳𝗈𝗉 𝖳𝗋𝖾𝗇𝖽𝗂𝗇𝗀 ⚡', callback_data="trending")
                        ]] 
        reply_markup = InlineKeyboardMarkup(buttons)
        return await message.reply_photo(photo=START_IMG, caption=script.START_TXT.format(message.from_user.mention, get_status(), message.from_user.id),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    if data.startswith('pm_mode_'):
        pm_mode = True
        data = data.replace('pm_mode_', '')
    try:
        pre, grp_id, file_id = data.split('_', 2)
    except:
        pre, grp_id, file_id = "", 0, data

    user_id = m.from_user.id
    if not await db.has_premium_access(user_id):
        grp_id = int(grp_id)
        user_verified = await db.is_user_verified(user_id)
        settings = await get_settings(grp_id , pm_mode=pm_mode)
        is_second_shortener = await db.use_second_shortener(user_id, settings.get('verify_time', TWO_VERIFY_GAP)) 
        is_third_shortener = await db.use_third_shortener(user_id, settings.get('third_verify_time', THREE_VERIFY_GAP))
        if settings.get("is_verify", IS_VERIFY) and not user_verified or is_second_shortener or is_third_shortener:
            verify_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            await db.create_verify_id(user_id, verify_id)
            temp.CHAT[user_id] = grp_id
            verify = await get_shortlink(f"https://telegram.me/{temp.U_NAME}?start=notcopy_{user_id}_{verify_id}_{file_id}", grp_id, is_second_shortener, is_third_shortener , pm_mode=pm_mode)
            if is_third_shortener:
                howtodownload = settings.get('tutorial_3', TUTORIAL_3)
            else:
                howtodownload = settings.get('tutorial_2', TUTORIAL_2) if is_second_shortener else settings.get('tutorial', TUTORIAL)
            buttons = [[
                InlineKeyboardButton(text="✅ 𝖵𝖾𝗋𝗂𝖿𝗒 ✅", url=verify),
                InlineKeyboardButton(text="𝖧𝗈𝗐 𝖳𝗈 𝖵𝖾𝗋𝗂𝖿𝗒 ❓", url=howtodownload)
                ],[
                InlineKeyboardButton(text="😁 𝖡𝗎𝗒 𝖲𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 - 𝖭𝗈 𝖭𝖾𝖾𝖽 𝖳𝗈 𝖵𝖾𝗋𝗂𝖿𝗒 😁", callback_data='seeplans'),
            ]]
            reply_markup=InlineKeyboardMarkup(buttons)
            if await db.user_verified(user_id): 
                msg = script.THIRDT_VERIFICATION_TEXT
            else:            
                msg = script.SECOND_VERIFICATION_TEXT if is_second_shortener else script.VERIFICATION_TEXT
            d = await m.reply_text(
                text=msg.format(message.from_user.mention, get_status()),
                protect_content = False,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
            await asyncio.sleep(300) 
            await d.delete()
            await m.delete()
            return

    if data and data.startswith("allfiles"):
        _, key = data.split("_", 1)
        files = temp.FILES_ID.get(key)
        if not files:
            await message.reply_text("<b>⚠️ 𝖠𝗅𝗅 𝖥𝗂𝗅𝖾𝗌 𝖭𝗈𝗍 𝖥𝗈𝗎𝗇𝖽 ⚠️</b>")
            return
        files_to_delete = []
        for file in files:
            user_id = message.from_user.id 
            grp_id = temp.CHAT.get(user_id)
            settings = await get_settings(grp_id, pm_mode=pm_mode)
            CAPTION = settings['caption']
            f_caption = CAPTION.format(
                file_name=formate_file_name(file.file_name),
                file_size=get_size(file.file_size),
                file_caption=file.caption
            )
            btn = [[
                InlineKeyboardButton("✛ 𝖶𝖺𝗍𝖼𝗁 & 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽 ✛", callback_data=f'stream#{file.file_id}')
            ]]
            toDel = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file.file_id,
                caption=f_caption,
                reply_markup=InlineKeyboardMarkup(btn)
            )
            files_to_delete.append(toDel)

        delCap = "<b>𝖠𝗅𝗅 {} 𝖿𝗂𝗅𝖾𝗌 𝗐𝗂𝗅𝗅 𝖻𝖾 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝖺f𝗍𝖾𝗋 {} 𝗍𝗈 𝖺𝗏𝗈𝗂𝖽 𝖼𝗈𝗉𝗒𝗋𝗂𝗀𝗁𝗍 𝗏𝗂𝗈𝗅𝖺𝗍𝗂𝗈𝗇𝗌!</b>".format(len(files_to_delete), f'{FILE_AUTO_DEL_TIMER / 60} 𝖬𝗂𝗇𝗎𝗍𝖾𝗌' if FILE_AUTO_DEL_TIMER >= 60 else f'{FILE_AUTO_DEL_TIMER} 𝖲𝖾𝖼𝗈𝗇𝖽𝗌')
        afterDelCap = "<b>𝖠𝗅𝗅 {} 𝖿𝗂𝗅𝖾𝗌 𝖺𝗋𝖾 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝖺𝖿𝗍𝖾𝗋 {} 𝗍𝗈 𝖺𝗏𝗈𝗂𝖽 𝖼𝗈𝗉𝗒𝗋𝗂𝗀𝗁𝗍 𝗏𝗂𝗈𝗅𝖺𝗍𝗂𝗈𝗇𝗌!</b>".format(len(files_to_delete), f'{FILE_AUTO_DEL_TIMER / 60} 𝖬𝗂𝗇𝗎𝗍𝖾𝗌' if FILE_AUTO_DEL_TIMER >= 60 else f'{FILE_AUTO_DEL_TIMER} 𝖲𝖾𝖼𝗈𝗇𝖽𝗌')
        replyed = await message.reply(
            delCap
        )
        await asyncio.sleep(FILE_AUTO_DEL_TIMER)
        for file in files_to_delete:
            try:
                await file.delete()
            except:
                pass
        return await replyed.edit(
            afterDelCap,
        )
    if not data:
        return

    files_ = await get_file_details(file_id)           
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        return await message.reply('<b>⚠️ 𝖠𝗅𝗅 𝖥𝗂𝗅𝖾𝗌 𝖭𝗈𝗍 𝖥𝗈𝗎𝗇𝖽 ⚠️</b>')
    files = files_[0]
    settings = await get_settings(grp_id , pm_mode=pm_mode)
    CAPTION = settings['caption']
    f_caption = CAPTION.format(
        file_name = formate_file_name(files.file_name),
        file_size = get_size(files.file_size),
        file_caption=files.caption
    )
    btn = [[
        InlineKeyboardButton("✛ 𝖶𝖺𝗍𝖼𝗁 & 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽 ✛", callback_data=f'stream#{file_id}')
    ]]
    toDel=await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        reply_markup=InlineKeyboardMarkup(btn)
    )
    delCap = "<b>𝖸𝗈𝗎𝗋 𝖿𝗂𝗅𝖾 𝗐𝗂𝗅𝗅 𝖻𝖾 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝖺𝖿𝗍𝖾𝗋 {} 𝗍𝗈 𝖺𝗏𝗈𝗂𝖽 𝖼𝗈𝗉𝗒𝗋𝗂𝗀𝗁𝗍 𝗏𝗂𝗈𝗅𝖺𝗍𝗂𝗈𝗇𝗌!</b>".format(f'{FILE_AUTO_DEL_TIMER / 60} 𝖬𝗂𝗇𝗎𝗍𝖾𝗌' if FILE_AUTO_DEL_TIMER >= 60 else f'{FILE_AUTO_DEL_TIMER} 𝖲𝖾𝖼𝗈𝗇𝖽𝗌')
    afterDelCap = "<b>𝖸𝗈𝗎𝗋 𝖿𝗂𝗅𝖾 𝗂𝗌 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝖺𝖿𝗍𝖾𝗋 {} 𝗍𝗈 𝖺𝗏𝗈𝗂𝖽 𝖼𝗈𝗉𝗒𝗋𝗂𝗀𝗁𝗍 𝗏𝗂𝗈𝗅𝖺𝗍𝗂𝗈𝗇𝗌!</b>".format(f'{FILE_AUTO_DEL_TIMER / 60} 𝖬𝗂𝗇𝗎𝗍𝖾𝗌' if FILE_AUTO_DEL_TIMER >= 60 else f'{FILE_AUTO_DEL_TIMER} 𝖲𝖾𝖼𝗈𝗇𝖽𝗌') 
    replyed = await message.reply(
        delCap,
        reply_to_message_id= toDel.id)
    await asyncio.sleep(FILE_AUTO_DEL_TIMER)
    await toDel.delete()
    return await replyed.edit(afterDelCap)
    

@Client.on_message(filters.command('delete'))
async def delete(bot, message):
    if message.from_user.id not in ADMINS:
        await message.reply('𝖮𝗇𝗅𝗒 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗈𝗐𝗇𝖾𝗋 𝖼𝖺𝗇 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽... 😑')
        return
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("𝖯𝗋𝗈𝖼𝖾𝗌𝗌𝗂𝗇𝗀...⏳", quote=True)
    else:
        await message.reply('𝖱𝖾𝗉𝗅𝗒 𝗍𝗈 𝖿𝗂𝗅𝖾 𝗐𝗂𝗍𝗁 /𝖽𝖾𝗅𝖾𝗍𝖾 𝗐𝗁𝗂𝖼𝗁 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝖽𝖾𝗅𝖾𝗍𝖾', quote=True)
        return
    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('<b>𝖳𝗁𝗂𝗌 𝗂𝗌 𝗇𝗈𝗍 𝗌𝗎𝗉𝗉𝗈𝗋𝗍𝖾𝖽 𝖿𝗂𝗅𝖾 𝖿𝗈𝗋𝗆𝖺𝗍</b>')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)
    result = await Media.collection.delete_one({
        '_id': file_id,
    })
    if result.deleted_count:
        await msg.edit('<b>𝖥𝗂𝗅𝖾 𝗂𝗌 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝖿𝗋𝗈𝗆 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾 💥</b>')
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await Media.collection.delete_many({
            'file_name': file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
            })
        if result.deleted_count:
            await msg.edit('<b>𝖥𝗂𝗅𝖾 𝗂𝗌 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝖿𝗋𝗈𝗆 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾 💥</b>')
        else:
            result = await Media.collection.delete_many({
                'file_name': media.file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit('<b>𝖥𝗂𝗅𝖾 𝗂𝗌 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝖿𝗋𝗈𝗆 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾 💥</b>')
            else:
                await msg.edit('<b>𝖥𝗂𝗅𝖾 𝗇𝗈𝗍 𝖿𝗈𝗎𝗇𝖽 𝗂𝗇 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾</b>')

@Client.on_message(filters.command('deleteall'))
async def delete_all_index(bot, message):
    files = await Media.count_documents()
    if int(files) == 0:
        return await message.reply_text('𝖭𝗈𝗍 𝗁𝖺𝗏𝖾 𝖿𝗂𝗅𝖾𝗌 𝗍𝗈 𝖽𝖾𝗅𝖾𝗍𝖾')
    btn = [[
            InlineKeyboardButton(text="𝖸𝖾𝗌", callback_data="all_files_delete")
        ],[
            InlineKeyboardButton(text="𝖢𝖺𝗇𝖼𝖾𝗅", callback_data="close_data")
        ]]
    if message.from_user.id not in ADMINS:
        await message.reply('𝖮𝗇𝗅𝗒 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗈𝗐𝗇𝖾𝗋 𝖼𝖺𝗇 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽... 😑')
        return
    await message.reply_text('<b>𝖳𝗁𝗂𝗌 𝗐𝗂𝗅𝗅 𝖽𝖾𝗅𝖾𝗍𝖾 𝖺𝗅𝗅 𝗂𝗇𝖽𝖾𝗑𝖾𝖽 𝖿𝗂𝗅𝖾𝗌.\n𝖣𝗈 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝖼𝗈𝗇𝗍𝗂𝗇𝗎𝖾??</b>', reply_markup=InlineKeyboardMarkup(btn))

@Client.on_message(filters.command('settings'))
async def settings(client, message):
    user_id = message.from_user.id if message.from_user else None
    if not user_id:
        return await message.reply("<b>💔 𝖸𝗈𝗎 𝖺𝗋𝖾 𝖺𝗇𝗈𝗇𝗒𝗆𝗈𝗎𝗌 𝖺𝖽𝗆𝗂𝗇 𝗒𝗈𝗎 𝖼𝖺𝗇'𝗍 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽...</b>")
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<code>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉.</code>")
    grp_id = message.chat.id
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉</b>')
    settings = await get_settings(grp_id)
    title = message.chat.title
    if settings is not None:
            buttons = [[
                InlineKeyboardButton('𝖠𝗎𝗍𝗈 𝖥𝗂𝗅𝗍𝖾𝗋', callback_data=f'setgs#auto_filter#{settings["auto_filter"]}#{grp_id}'),
                InlineKeyboardButton('𝖮𝗇 ✓' if settings["auto_filter"] else '𝖮𝖿𝖿 ✗', callback_data=f'setgs#auto_filter#{settings["auto_filter"]}#{grp_id}')
            ],[
                InlineKeyboardButton('𝖨𝖬𝖣𝖡', callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}'),
                InlineKeyboardButton('𝖮𝗇 ✓' if settings["imdb"] else '𝖮𝖿𝖿 ✗', callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}')
            ],[
                InlineKeyboardButton('𝖲𝗉𝖾𝗅𝗅 𝖢𝗁𝖾𝖼𝗄', callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}'),
                InlineKeyboardButton('𝖮𝗇 ✓' if settings["spell_check"] else '𝖮𝖿𝖿 ✗', callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}')
            ],[
                InlineKeyboardButton('𝖠𝗎𝗍𝗈 𝖣𝖾𝗅𝖾𝗍𝖾', callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{grp_id}'),
                InlineKeyboardButton(f'{get_readable_time(DELETE_TIME)}' if settings["auto_delete"] else '𝖮𝖿𝖿 ✗', callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{grp_id}')
            ],[
                InlineKeyboardButton('𝖱𝖾𝗌𝗎𝗅𝗍 𝖬𝗈𝖽𝖾', callback_data=f'setgs#link#{settings["link"]}#{str(grp_id)}'),
                InlineKeyboardButton('⛓ 𝖫𝗂𝗇𝗄' if settings["link"] else '🧲 𝖡𝗎𝗍𝗍𝗈𝗇', callback_data=f'setgs#link#{settings["link"]}#{str(grp_id)}')
            ],[
                InlineKeyboardButton('❌ 𝖢𝗅𝗈𝗌𝖾 ❌', callback_data='close_data')
            ]]
            await message.reply_text(
                text=f"𝖢𝗁𝖺𝗇𝗀𝖾 𝗒𝗈𝗎𝗋 𝗌𝖾𝗍𝗍𝗂𝗇𝗀𝗌 𝖿𝗈𝗋 <b>'{title}'</b> 𝖺𝗌 𝗒𝗈𝗎𝗋 𝗐𝗂𝗌𝗁 ✨",
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.HTML
            )
    else:
        await message.reply_text('<b>𝖲𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝗐𝖾𝗇𝗍 𝗐𝗋𝗈𝗇𝗀</b>')

@Client.on_message(filters.command('set_template'))
async def save_template(client, message):
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉...</b>")
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉</b>')
    try:
        template = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖨𝗇𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾!")    
    await save_group_settings(grp_id, 'template', template)
    await message.reply_text(f"𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖼𝗁𝖺𝗇𝗀𝖾𝖽 𝗍𝖾𝗆𝗉𝗅𝖺𝗍𝖾 𝖿𝗈𝗋 {title} 𝗍𝗈\n\n{template}", disable_web_page_preview=True)
    
@Client.on_message(filters.command("send"))
async def send_msg(bot, message):
    if message.from_user.id not in ADMINS:
        await message.reply('<b>𝖮𝗇𝗅𝗒 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗈𝗐𝗇𝖾𝗋 𝖼𝖺𝗇 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽...</b>')
        return
    if message.reply_to_message:
        target_ids = message.text.split(" ")[1:]
        if not target_ids:
            await message.reply_text("<b>𝖯𝗅𝖾𝖺𝗌𝖾 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝗈𝗇𝖾 𝗈𝗋 𝗆𝗈𝗋𝖾 𝗎𝗌𝖾𝗋 𝗂𝖽𝗌 𝗐𝗂𝗍𝗁 𝖺 𝗌𝗉𝖺𝖼𝖾...</b>")
            return
        out = "\n\n"
        success_count = 0
        try:
            users = await db.get_all_users()
            for target_id in target_ids:
                try:
                    user = await bot.get_users(target_id)
                    out += f"{user.id}\n"
                    await message.reply_to_message.copy(int(user.id))
                    success_count += 1
                except Exception as e:
                    out += f"‼️ 𝖤𝗋𝗋𝗈𝗋 𝗂𝗇 𝗍𝗁𝗂𝗌 𝗂𝖽 - <code>{target_id}</code> <code>{str(e)}</code>\n"
            await message.reply_text(f"<b>✅️ 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗌𝖾𝗇𝗍 𝗍𝗈 `{success_count}` 𝖨𝖣\n<code>{out}</code></b>")
        except Exception as e:
            await message.reply_text(f"<b>‼️ 𝖤𝗋𝗋𝗈𝗋 - <code>{e}</code></b>")
    else:
        await message.reply_text("<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝖺𝗌 𝗋𝖾𝗉𝗅𝗒 𝗍𝗈 𝖺𝗇𝗒 𝗆𝖾𝗌𝗌𝖺𝗀𝖾, 𝖥𝗈𝗋 𝖤𝗀 - <code>/send userid1 userid2</code></b>")

@Client.on_message(filters.regex("#request"))
async def send_request(bot, message):
    try:
        request = message.text.split(" ", 1)[1]
    except:
        await message.reply_text("<b>‼️ 𝖸𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗂𝗌 𝗂𝗇𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾</b>")
        return
    buttons = [[
        InlineKeyboardButton('👀 𝖵𝗂𝖾𝗐 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 👀', url=f"{message.link}")
    ],[
        InlineKeyboardButton('⚙ 𝖲𝗁𝗈𝗐 𝖮𝗉𝗍𝗂𝗈𝗇𝗌 ⚙', callback_data=f'show_options#{message.from_user.id}#{message.id}')
    ]]
    sent_request = await bot.send_message(REQUEST_CHANNEL, script.REQUEST_TXT.format(message.from_user.mention, message.from_user.id, request), reply_markup=InlineKeyboardMarkup(buttons))
    btn = [[
         InlineKeyboardButton('✨ 𝖵𝗂𝖾𝗐 𝖸𝗈𝗎𝗋 𝖱𝖾𝗊𝗎𝖾𝗌𝗍 ✨', url=f"{sent_request.link}")
    ]]
    await message.reply_text("<b>✅ 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗒𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗁𝖺𝗌 𝖻𝖾𝖾𝗇 𝖺𝖽𝖽𝖾𝖽, 𝗉𝗅𝖾𝖺𝗌𝖾 𝗐𝖺𝗂𝗍 𝗌𝗈𝗆𝖾𝗍𝗂𝗆𝖾...</b>", reply_markup=InlineKeyboardMarkup(btn))

@Client.on_message(filters.command("search"))
async def search_files(bot, message):
    if message.from_user.id not in ADMINS:
        await message.reply('𝖮𝗇𝗅𝗒 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗈𝗐𝗇𝖾𝗋 𝖼𝖺𝗇 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽... 😑')
        return
    chat_type = message.chat.type
    if chat_type != enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>𝖧𝖾𝗒 {message.from_user.mention}, 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗐𝗈𝗇'𝗍 𝗐𝗈𝗋𝗄 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉𝗌. 𝖨𝗍 𝗈𝗇𝗅𝗒 𝗐𝗈𝗋𝗄𝗌 𝗂𝗇 𝗆𝗒 𝗉𝗆!</b>")  
    try:
        keyword = message.text.split(" ", 1)[1]
    except IndexError:
        return await message.reply_text(f"<b>𝖧𝖾𝗒 {message.from_user.mention}, 𝗀𝗂𝗏𝖾 𝗆𝖾 𝖺 𝗄𝖾𝗒𝗐𝗈𝗋𝖽 𝖺𝗅𝗈𝗇𝗀 𝗐𝗂𝗍𝗁 𝗍𝗁𝖾 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗍𝗈 𝗌𝖾𝖺𝗋𝖼𝗁 𝖿𝗂𝗅𝖾𝗌.</b>")
    files, total = await get_bad_files(keyword)
    if int(total) == 0:
        await message.reply_text('<i>𝖨 𝖼𝗈𝗎𝗅𝖽 𝗇𝗈𝗍 𝖿𝗂𝗇𝖽 𝖺𝗇𝗒 𝖿𝗂𝗅𝖾𝗌 𝗐𝗂𝗍𝗁 𝗍𝗁𝗂𝗌 𝗄𝖾𝗒𝗐𝗈𝗋𝖽 😐</i>')
        return 
    file_names = "\n\n".join(f"{index + 1}. {item['file_name']}" for index, item in enumerate(files))
    file_data = f"🚫 𝖸𝗈𝗎𝗋 𝗌𝖾𝖺𝗋𝖼𝗁 - '{keyword}':\n\n{file_names}"    
    with open("file_names.txt", "w" , encoding='utf-8') as file:
        file.write(file_data)
    await message.reply_document(
        document="file_names.txt",
        caption=f"<b>♻️ 𝖡𝗒 𝗒𝗈𝗎𝗋 𝗌𝖾𝖺𝗋𝖼𝗁, 𝖨 𝖿𝗈𝗎𝗇𝖽 - <code>{total}</code> 𝖿𝗂𝗅𝖾𝗌</b>",
        parse_mode=enums.ParseMode.HTML
    )
    os.remove("file_names.txt")

@Client.on_message(filters.command("deletefiles"))
async def deletemultiplefiles(bot, message):
    if message.from_user.id not in ADMINS:
        await message.reply('𝖮𝗇𝗅𝗒 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗈𝗐𝗇𝖾𝗋 𝖼𝖺𝗇 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽... 😑')
        return
    chat_type = message.chat.type
    if chat_type != enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>𝖧𝖾𝗒 {message.from_user.mention}, 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗐𝗈𝗇'𝗍 𝗐𝗈𝗋𝗄 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉𝗌. 𝖨𝗍 𝗈𝗇𝗅𝗒 𝗐𝗈𝗋𝗄𝗌 𝗂𝗇 𝗆𝗒 𝗉𝗆!</b>")
    else:
        pass
    try:
        keyword = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text(f"<b>𝖧𝖾𝗒 {message.from_user.mention}, 𝗀𝗂𝗏𝖾 𝗆𝖾 𝖺 𝗄𝖾𝗒𝗐𝗈𝗋𝖽 𝖺𝗅𝗈𝗇𝗀 𝗐𝗂𝗍𝗁 𝗍𝗁𝖾 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗍𝗈 𝖽𝖾𝗅𝖾𝗍𝖾 𝖿𝗂𝗅𝖾𝗌.</b>")
    files, total = await get_bad_files(keyword)
    if int(total) == 0:
        await message.reply_text('<i>𝖨 𝖼𝗈𝗎𝗅𝖽 𝗇𝗈𝗍 𝖿𝗂𝗇𝖽 𝖺𝗇𝗒 𝖿𝗂𝗅𝖾𝗌 𝗐𝗂𝗍𝗁 𝗍𝗁𝗂𝗌 𝗄𝖾𝗒𝗐𝗈𝗋𝖽 😐</i>')
        return 
    btn = [[
       InlineKeyboardButton("𝖸𝖾𝗌, 𝖢𝗈𝗇𝗍𝗂𝗇𝗎𝖾 ✅", callback_data=f"killfilesak#{keyword}")
       ],[
       InlineKeyboardButton("𝖭𝗈, 𝖠𝖻𝗈𝗋𝗍 😢", callback_data="close_data")
    ]]
    await message.reply_text(
        text=f"<b>𝖳𝗈𝗍𝖺𝗅 𝖿𝗂𝗅𝖾𝗌 𝖿𝗈𝗎𝗇𝖽 - <code>{total}</code>\n\n𝖣𝗈 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝖼𝗈𝗇𝗍𝗂𝗇𝗎𝖾?\n\n𝖭𝗈𝗍𝖾:- 𝖳𝗁𝗂𝗌 𝖼𝗈𝗎𝗅𝖽 𝖻𝖾 𝖺 𝖽𝖾𝗌𝗍𝗋𝗎𝖼𝗍𝗂𝗏𝖾 𝖺𝖼𝗍𝗂𝗈𝗇!!</b>",
        reply_markup=InlineKeyboardMarkup(btn),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command("del_file"))
async def delete_files(bot, message):
    if message.from_user.id not in ADMINS:
        await message.reply('𝖮𝗇𝗅𝗒 𝗍𝗁𝖾 𝖻𝗈𝗍 𝗈𝗐𝗇𝖾𝗋 𝖼𝖺𝗇 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽... 😑')
        return
    chat_type = message.chat.type
    if chat_type != enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>𝖧𝖾𝗒 {message.from_user.mention}, 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗐𝗈𝗇'𝗍 𝗐𝗈𝗋𝗄 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉𝗌. 𝖨𝗍 𝗈𝗇𝗅𝗒 𝗐𝗈𝗋𝗄𝗌 𝗂𝗇 𝗆𝗒 𝗉𝗆!</b>")    
    try:
        keywords = message.text.split(" ", 1)[1].split(",")
    except IndexError:
        return await message.reply_text(f"<b>𝖧𝖾𝗒 {message.from_user.mention}, 𝗀𝗂𝗏𝖾 𝗆𝖾 𝗄𝖾𝗒𝗐𝗈𝗋𝖽𝗌 𝗌𝖾𝗉𝖺𝗋𝖺𝗍𝖾𝖽 𝖻𝗒 𝖼𝗈𝗆𝗆𝖺𝗌 𝖺𝗅𝗈𝗇𝗀 𝗐𝗂𝗍𝗁 𝗍𝗁𝖾 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗍𝗈 𝖽𝖾𝗅𝖾𝗍𝖾 𝖿𝗂𝗅𝖾𝗌.</b>")   
    deleted_files_count = 0
    not_found_files = []
    for keyword in keywords:
        result = await Media.collection.delete_many({'file_name': keyword.strip()})
        if result.deleted_count:
            deleted_files_count += 1
        else:
            not_found_files.append(keyword.strip())
    if deleted_files_count > 0:
        await message.reply_text(f'<b>{deleted_files_count} 𝖿𝗂𝗅𝖾𝗌 𝗌𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 𝖿𝗋𝗈𝗆 𝗍𝗁𝖾 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾 💥</b>')
    if not_found_files:
        await message.reply_text(f'<b>𝖥𝗂𝗅𝖾𝗌 𝗇𝗈𝗍 𝖿𝗈𝗎𝗇𝖽 𝗂𝗇 𝗍𝗁𝖾 𝖽𝖺𝗍𝖺𝖻𝖺𝗌𝖾 - <code>{", ".join(not_found_files)}</code></b>')

@Client.on_message(filters.command('set_caption'))
async def save_caption(client, message):
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉</b>')
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉...</b>")
    try:
        caption = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖨𝗇𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾!")
    await save_group_settings(grp_id, 'caption', caption)
    await message.reply_text(f"𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖼𝗁𝖺𝗇𝗀𝖾𝖽 𝖼𝖺𝗉𝗍𝗂𝗈𝗇 𝖿𝗈𝗋 {title} 𝗍𝗈\n\n{caption}", disable_web_page_preview=True) 
    
@Client.on_message(filters.command('set_tutorial'))
async def save_tutorial(client, message):
    grp_id = message.chat.id
    title = message.chat.title
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉...</b>")
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉</b>')
    try:
        tutorial = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("<b>𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖨𝗇𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾!!\n\n𝖴𝗌𝖾 𝗅𝗂𝗄𝖾 𝗍𝗁𝗂𝗌 -</b>\n\n<code>/set_caption https://t.me/Channel_Link</code>")    
    await save_group_settings(grp_id, 'tutorial', tutorial)
    await message.reply_text(f"<b>𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖢𝗁𝖺𝗇𝗀𝖾𝖽 1𝗌𝗍 𝖵𝖾𝗋𝗂𝖿𝗂𝖼𝖺𝗍𝗂𝗈𝗇 𝖳𝗎𝗍𝗈𝗋𝗂𝖺𝗅 𝖥𝗈𝗋 {title} 𝗍𝗈</b>\n\n{tutorial}", disable_web_page_preview=True)

@Client.on_message(filters.command('set_tutorial_2'))
async def set_tutorial_2(client, message):
    grp_id = message.chat.id
    title = message.chat.title
    invite_link = await client.export_chat_invite_link(grp_id)
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉</b>')
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text(f"<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉...\n\nGroup Name: {title}\nGroup ID: {grp_id}\nGroup Invite Link: {invite_link}</b>")
    try:
        tutorial = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("<b>𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖨𝗇𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾!!\n\n𝖴𝗌𝖾 𝗅𝗂𝗄𝖾 𝗍𝗁𝗂𝗌 -</b>\n\n<code>/set_tutorial_2 https://t.me/Channel_Link/2</code>")
    await save_group_settings(grp_id, 'tutorial_2', tutorial)
    await message.reply_text(f"<b>𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖢𝗁𝖺𝗇𝗀𝖾𝖽 2𝗇𝖽 𝖵𝖾𝗋𝗂𝖿𝗂𝖼𝖺𝗍𝗂𝗈𝗇 𝖳𝗎𝗍𝗈𝗋𝗂𝖺𝗅 𝖥𝗈𝗋 {title} 𝗍𝗈</b>\n\n{tutorial}", disable_web_page_preview=True)
    
@Client.on_message(filters.command('set_tutorial_3'))
async def set_tutorial_3(client, message):
    grp_id = message.chat.id
    title = message.chat.title
    invite_link = await client.export_chat_invite_link(grp_id)
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉</b>')
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text(f"<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉...\n\n𝖦𝗋𝗈𝗎𝗉 𝖭𝖺𝗆𝖾: {title}\n𝖦𝗋𝗈𝗎𝗉 𝖨𝖣: {grp_id}\n𝖦𝗋𝗈𝗎𝗉 𝖨𝗇𝗏𝗂𝗍𝖾 𝖫𝗂𝗇𝗄: {invite_link}</b>")
    try:
        tutorial = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("<b>𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖨𝗇𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾!!\n\n𝖴𝗌𝖾 𝗅𝗂𝗄𝖾 𝗍𝗁𝗂𝗌 -</b>\n\n<code>/set_tutorial https://t.me/Channel_Link</code>")
    await save_group_settings(grp_id, 'tutorial_3', tutorial)
    await message.reply_text(f"<b>𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖢𝗁𝖺𝗇𝗀𝖾𝖽 3𝗋𝖽 𝖵𝖾𝗋𝗂𝖿𝗂𝖼𝖺𝗍𝗂𝗈𝗇 𝖳𝗎𝗍𝗈𝗋𝗂𝖺𝗅 𝖥𝗈𝗋 {title} 𝗍𝗈</b>\n\n{tutorial}", disable_web_page_preview=True)

@Client.on_message(filters.command('set_verify'))
async def set_shortner(c, m):
    grp_id = m.chat.id
    chat_type = m.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await m.reply_text("<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉...</b>")
    if not await is_check_admin(c, grp_id, m.from_user.id):
        return await m.reply_text('<b>𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉</b>')        
    if len(m.text.split()) == 1:
        await m.reply("<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗅𝗂𝗄𝖾 𝗍𝗁𝗂𝗌 - \n\n`/set_shortner shortner.site apikey`</b>")
        return        
    sts = await m.reply("<b>♻️ 𝖢𝗁𝖾𝖼𝗄𝗂𝗇𝗀...</b>")
    await asyncio.sleep(1.2)
    await sts.delete()
    try:
        URL = m.command[1]
        API = m.command[2]
        resp = requests.get(f'https://{URL}/api?api={API}&url=https://telegram.dog/GamerBhai02Bot').json()
        if resp['status'] == 'success':
            SHORT_LINK = resp['shortenedUrl']
        await save_group_settings(grp_id, 'shortner', URL)
        await save_group_settings(grp_id, 'api', API)
        await m.reply_text(f"<b><u>✓ 𝖸𝗈𝗎𝗋 𝖲𝗁𝗈𝗋𝗍𝖾𝗇𝖾𝗋 𝗂𝗌 𝖠𝖽𝖽𝖾𝖽 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒</u>\n\n𝖣𝖾𝗆𝗈 - {SHORT_LINK}\n\n𝖲𝗂𝗍𝖾 - `{URL}`\n\n𝖠𝖯𝖨 - `{API}`</b>", quote=True)
        user_id = m.from_user.id
        user_info = f"@{m.from_user.username}" if m.from_user.username else f"{m.from_user.mention}"
        link = (await c.get_chat(m.chat.id)).invite_link
        grp_link = f"[{m.chat.title}]({link})"
        log_message = f"#New_Shortner_Set_For_1st_Verify\n\n𝖭𝖺𝗆𝖾 - {user_info}\n𝖨𝖣 - `{user_id}`\n\n𝖣𝗈𝗆𝖺𝗂𝗇 𝖭𝖺𝗆𝖾 - {URL}\n𝖠𝖯𝖨 - `{API}`\n𝖦𝗋𝗈𝗎𝗉 𝖫𝗂𝗇𝗄 - {grp_link}"
        await c.send_message(LOG_API_CHANNEL, log_message, disable_web_page_preview=True)
    except Exception as e:
        await save_group_settings(grp_id, 'shortner', SHORTENER_WEBSITE)
        await save_group_settings(grp_id, 'api', SHORTENER_API)
        await m.reply_text(f"<b><u>💢 𝖤𝗋𝗋𝗈𝗋 𝗈𝖼𝖼𝗎𝗋𝗋𝖾𝖽!!</u>\n\n𝖠𝗎𝗍𝗈 𝖺𝖽𝖽𝖾𝖽 𝖻𝗈𝗍 𝗈𝗐𝗇𝖾𝗋 𝖽𝖾𝖿𝖺𝗎𝗅𝗍 𝗌𝗁𝗈𝗋𝗍𝖾𝗇𝖾𝗋\n\n𝖨𝖿 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝖼𝗁𝖺𝗇𝗀𝖾 𝗍𝗁𝖾𝗇 𝗎𝗌𝖾 𝖼𝗈𝗋𝗋𝖾𝖼𝗍 𝖿𝗈𝗋𝗆𝖺𝗍 𝗈𝗋 𝖺𝖽𝖽 𝗏𝖺𝗅𝗂𝖽 𝗌𝗁𝗈𝗋𝗍 𝗅𝗂𝗇𝗄 𝖽𝗈𝗆𝖺𝗂𝗇 𝗇𝖺𝗆𝖾 & 𝖠𝗉𝗂\n\n𝖸𝗈𝗎 𝖼𝖺𝗇 𝖺𝗅𝗌𝗈 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 𝗈𝗎𝗋 <a href=https://t.me/GamerBhai02Bot>𝖠𝖽𝗆𝗂𝗇</a> 𝖿𝗈𝗋 𝗌𝗈𝗅𝗏𝗂𝗇𝗀 𝗍𝗁𝗂𝗌 𝗂𝗌𝗌𝗎𝖾...\n\n𝖫𝗂𝗄𝖾 -\n\n`/set_shortner shortener.site apikey`\n\n💔 𝖤𝗋𝗋𝗈𝗋 - <code>{e}</code></b>", quote=True)

@Client.on_message(filters.command('set_verify_2'))
async def set_shortner_2(c, m):
    grp_id = m.chat.id
    chat_type = m.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await m.reply_text("<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉...</b>")
    if not await is_check_admin(c, grp_id, m.from_user.id):
        return await m.reply_text('<b>𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉</b>')
    if len(m.text.split()) == 1:
        await m.reply("<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗅𝗂𝗄𝖾 𝗍𝗁𝗂𝗌 - \n\n`/set_shortner_2 shortener.site apikey`</b>")
        return
    sts = await m.reply("<b>♻️ 𝖢𝗁𝖾𝖼𝗄𝗂𝗇𝗀...</b>")
    await asyncio.sleep(1.2)
    await sts.delete()
    try:
        URL = m.command[1]
        API = m.command[2]
        resp = requests.get(f'https://{URL}/api?api={API}&url=https://telegram.dog/GamerBhai02Bot').json()
        if resp['status'] == 'success':
            SHORT_LINK = resp['shortenedUrl']
        await save_group_settings(grp_id, 'shortner_two', URL)
        await save_group_settings(grp_id, 'api_two', API)
        await m.reply_text(f"<b><u>✅ 𝖸𝗈𝗎𝗋 𝖲𝗁𝗈𝗋𝗍𝖾𝗇𝖾𝗋 𝗂𝗌 𝖠𝖽𝖽𝖾𝖽 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒</u>\n\n𝖣𝖾𝗆𝗈 - {SHORT_LINK}\n\n𝖲𝗂𝗍𝖾 - `{URL}`\n\n𝖠𝖯𝖨 - `{API}`</b>", quote=True)
        user_id = m.from_user.id
        user_info = f"@{m.from_user.username}" if m.from_user.username else f"{m.from_user.mention}"
        link = (await c.get_chat(m.chat.id)).invite_link
        grp_link = f"[{m.chat.title}]({link})"
        log_message = f"#New_Shortner_Set_For_2nd_Verify\n\n𝖭𝖺𝗆𝖾 - {user_info}\n𝖨𝖣 - `{user_id}`\n\n𝖣𝗈𝗆𝖺𝗂𝗇 𝖭𝖺𝗆𝖾 - {URL}\n𝖠𝖯𝖨 - `{API}`\n𝖦𝗋𝗈𝗎𝗉 𝖫𝗂𝗇𝗄 - {grp_link}"
        await c.send_message(LOG_API_CHANNEL, log_message, disable_web_page_preview=True)
    except Exception as e:
        await save_group_settings(grp_id, 'shortner_two', SHORTENER_WEBSITE2)
        await save_group_settings(grp_id, 'api_two', SHORTENER_API2)
        await m.reply_text(f"<b><u>💢 𝖤𝗋𝗋𝗈𝗋 𝗈𝖼𝖼𝗎𝗋𝗋𝖾𝖽!!</u>\n\n𝖠𝗎𝗍𝗈 𝖺𝖽𝖽𝖾𝖽 𝖻𝗈𝗍 𝗈𝗐𝗇𝖾𝗋 𝖽𝖾𝖿𝖺𝗎𝗅𝗍 𝗌𝗁𝗈𝗋𝗍𝖾𝗇𝖾𝗋\n\n𝖨𝖿 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝖼𝗁𝖺𝗇𝗀𝖾 𝗍𝗁𝖾𝗇 𝗎𝗌𝖾 𝖼𝗈𝗋𝗋𝖾𝖼𝗍 𝖿𝗈𝗋𝗆𝖺𝗍 𝗈𝗋 𝖺𝖽𝖽 𝗏𝖺𝗅𝗂𝖽 𝗌𝗁𝗈𝗋𝗍 𝗅𝗂𝗇𝗄 𝖽𝗈𝗆𝖺𝗂𝗇 𝗇𝖺𝗆𝖾 & 𝖠𝗉𝗂\n\n𝖸𝗈𝗎 𝖼𝖺𝗇 𝖺𝗅𝗌𝗈 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 𝗈𝗎𝗋 <a href=https://t.me/Jisshu_support>𝖠𝖽𝗆𝗂𝗇</a> 𝖿𝗈𝗋 𝗌𝗈𝗅𝗏𝗂𝗇𝗀 𝗍𝗁𝗂𝗌 𝗂𝗌𝗌𝗎𝖾...\n\n𝖫𝗂𝗄𝖾 -\n\n`/set_shortner_2 shortener.site apikey`\n\n💔 𝖤𝗋𝗋𝗈𝗋 - <code>{e}</code></b>", quote=True)

@Client.on_message(filters.command('set_verify_3'))
async def set_shortner_3(c, m):
    chat_type = m.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await m.reply_text("<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗂𝗇 𝖸𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉! 𝖭𝗈𝗍 𝗂𝗇 𝖯𝗋𝗂𝗏𝖺𝗍𝖾</b>")
    if len(m.text.split()) == 1:
        return await m.reply("<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗅𝗂𝗄𝖾 𝗍𝗁𝗂𝗌 - \n\n`/set_shortner_3 shortener.site apikey`</b>")
    sts = await m.reply("<b>♻️ 𝖢𝗁𝖾𝖼𝗄𝗂𝗇𝗀...</b>")
    await sts.delete()
    userid = m.from_user.id if m.from_user else None
    if not userid:
        return await m.reply(f"<b>⚠️ 𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝗇 𝖺𝖽𝗆𝗂𝗇 𝗈𝖿 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉</b>")
    grp_id = m.chat.id
    #check if user admin or not
    if not await is_check_admin(c, grp_id, userid):
        return await m.reply_text('<b>𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉</b>')
    if len(m.command) == 1:
        await m.reply_text("<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗍𝗈 𝖺𝖽𝖽 𝖲𝗁𝗈𝗋𝗍𝖾𝗇𝖾𝗋 𝖺𝗇𝖽 𝖠𝗉𝗂\n\n𝖤𝗑 - `/set_shortner_3 shortener.site apikey`</b>", quote=True)
        return
    try:
        URL = m.command[1]
        API = m.command[2]
        resp = requests.get(f'https://{URL}/api?api={API}&url=https://telegram.dog/GamerBhai02Bot').json()
        if resp['status'] == 'success':
            SHORT_LINK = resp['shortenedUrl']
        await save_group_settings(grp_id, 'shortner_three', URL)
        await save_group_settings(grp_id, 'api_three', API)
        await m.reply_text(f"<b><u>✅ 𝖸𝗈𝗎𝗋 𝖲𝗁𝗈𝗋𝗍𝖾𝗇𝖾𝗋 𝗂𝗌 𝖠𝖽𝖽𝖾𝖽 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒</u>\n\n𝖣𝖾𝗆𝗈 - {SHORT_LINK}\n\n𝖲𝗂𝗍𝖾 - `{URL}`\n\n𝖠𝖯𝖨 - `{API}`</b>", quote=True)
        user_id = m.from_user.id
        if m.from_user.username:
            user_info = f"@{m.from_user.username}"
        else:
            user_info = f"{m.from_user.mention}"
        link = (await c.get_chat(m.chat.id)).invite_link
        grp_link = f"[{m.chat.title}]({link})"
        log_message = f"#New_Shortner_Set_For_3rd_Verify\n\n𝖭𝖺𝗆𝖾 - {user_info}\n𝖨𝖣 - `{user_id}`\n\n𝖣𝗈𝗆𝖺𝗂𝗇 𝖭𝖺𝗆𝖾 - {URL}\n𝖠𝖯𝖨 - `{API}`\n𝖦𝗋𝗈𝗎𝗉 𝖫𝗂𝗇𝗄 - {grp_link}"
        await c.send_message(LOG_API_CHANNEL, log_message, disable_web_page_preview=True)
    except Exception as e:
        await save_group_settings(grp_id, 'shortner_three', SHORTENER_WEBSITE3)
        await save_group_settings(grp_id, 'api_three', SHORTENER_API3)
        await m.reply_text(f"<b><u>💢 𝖤𝗋𝗋𝗈𝗋 𝗈𝖼𝖼𝗎𝗋𝗋𝖾𝖽!!</u>\n\n𝖠𝗎𝗍𝗈 𝖺𝖽𝖽𝖾𝖽 𝖻𝗈𝗍 𝗈𝗐𝗇𝖾𝗋 𝖽𝖾𝖿𝖺𝗎𝗅𝗍 𝗌𝗁𝗈𝗋𝗍𝖾𝗇𝖾𝗋\n\n𝖨𝖿 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝖼𝗁𝖺𝗇𝗀𝖾 𝗍𝗁𝖾𝗇 𝗎𝗌𝖾 𝖼𝗈𝗋𝗋𝖾𝖼𝗍 𝖿𝗈𝗋𝗆𝖺𝗍 𝗈𝗋 𝖺𝖽𝖽 𝗏𝖺𝗅𝗂𝖽 𝗌𝗁𝗈𝗋𝗍 𝗅𝗂𝗇𝗄 𝖽𝗈𝗆𝖺𝗂𝗇 𝗇𝖺𝗆𝖾 & 𝖠𝗉𝗂\n\n𝖸𝗈𝗎 𝖼𝖺𝗇 𝖺𝗅𝗌𝗈 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 𝗈𝗎𝗋 <a href=https://t.me/GamerBhai02Bot>𝖠𝖽𝗆𝗂𝗇</a> 𝖿𝗈𝗋 𝗌𝗈𝗅𝗏𝗂𝗇𝗀 𝗍𝗁𝗂𝗌 𝗂𝗌𝗌𝗎𝖾...\n\n𝖫𝗂𝗄𝖾 -\n\n`/set_shortner_3 shortener.site apikey`\n\n💔 𝖤𝗋𝗋𝗈𝗋 - <code>{e}</code></b>", quote=True)
        

@Client.on_message(filters.command('set_log'))
async def set_log(client, message):
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉</b>')
    if len(message.text.split()) == 1:
        await message.reply("<b><u>𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖥𝗈𝗋𝗆𝖺𝗍!!</u>\n\n𝖴𝗌𝖾 𝗅𝗂𝗄𝖾 𝗍𝗁𝗂𝗌 -\n`/log -100xxxxxxxx`</b>")
        return
    sts = await message.reply("<b>♻️ 𝖢𝗁𝖾𝖼𝗄𝗂𝗇𝗀...</b>")
    await asyncio.sleep(1.2)
    await sts.delete()
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉...</b>")
    try:
        log = int(message.text.split(" ", 1)[1])
    except IndexError:
        return await message.reply_text("<b><u>𝖨𝗇𝗏𝖺𝗅𝗂𝖽 𝖥𝗈𝗋𝗆𝖺𝗍!!</u>\n\n𝖴𝗌𝖾 𝗅𝗂𝗄𝖾 𝗍𝗁𝗂𝗌 -\n`/log -100xxxxxxxx`</b>")
    except ValueError:
        return await message.reply_text('<b>𝖬𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝖨𝖣 𝗂𝗌 𝖺𝗇 𝖨𝗇𝗍𝖾𝗀𝖾𝗋...</b>')
    try:
        t = await client.send_message(chat_id=log, text="<b>𝖧𝖾𝗒 𝖶𝗁𝖺𝗍'𝗌 𝖴𝗉!!</b>")
        await asyncio.sleep(3)
        await t.delete()
    except Exception as e:
        return await message.reply_text(f'<b><u>😐 𝖬𝖺𝗄𝖾 𝗌𝗎𝗋𝖾 𝖻𝗈𝗍 𝗂𝗌 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝖺𝗍 𝖼𝗁𝖺𝗇𝗇𝖾𝗅...</u>\n\n💔 𝖤𝗋𝗋𝗈𝗋 - <code>{e}</code></b>')
    await save_group_settings(grp_id, 'log', log)
    await message.reply_text(f"<b>✅ 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝗌𝖾𝗍 𝗒𝗈𝗎𝗋 𝖫𝗈𝗀 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖿𝗈𝗋 {title}\n\n𝖨𝖣 `{log}`</b>", disable_web_page_preview=True)
    user_id = m.from_user.id
    user_info = f"@{m.from_user.username}" if m.from_user.username else f"{m.from_user.mention}"
    link = (await client.get_chat(message.chat.id)).invite_link
    grp_link = f"[{message.chat.title}]({link})"
    log_message = f"#New_Log_Channel_Set\n\n𝖭𝖺𝗆𝖾 - {user_info}\n𝖨𝖣 - `{user_id}`\n\n𝖫𝗈𝗀 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖨𝖣 - `{log}`\n𝖦𝗋𝗈𝗎𝗉 𝖫𝗂𝗇𝗄 - {grp_link}"
    await client.send_message(LOG_API_CHANNEL, log_message, disable_web_page_preview=True)  
    

@Client.on_message(filters.command('details'))
async def all_settings(client, message):
    grp_id = message.chat.id
    title = message.chat.title
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉...</b>")
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉</b>')
    settings = await get_settings(grp_id)
    text = f"""<b><u>⚙️ 𝖸𝗈𝗎𝗋 𝗌𝖾𝗍𝗍𝗂𝗇𝗀𝗌 𝖿𝗈𝗋 -</u> {title}

<u>✅️ 1𝗌𝗍 𝖵𝖾𝗋𝗂𝖿𝗒 𝖲𝗁𝗈𝗋𝗍𝖾𝗇𝖾𝗋 𝖭𝖺𝗆𝖾 / 𝖠𝗉𝗂</u>
𝖭𝖺𝗆𝖾 - `{settings["shortner"]}`
𝖠𝗉𝗂 - `{settings["api"]}`

<u>✅️ 2𝗇𝖽 𝖵𝖾𝗋𝗂𝖿𝗒 𝖲𝗁𝗈𝗋𝗍𝖾𝗇𝖾𝗋 𝖭𝖺𝗆𝖾 / 𝖠𝗉𝗂</u>
𝖭𝖺𝗆𝖾 - `{settings["shortner_two"]}`
𝖠𝗉𝗂 - `{settings["api_two"]}`

<u>✅️ 3𝗋𝖽 𝖵𝖾𝗋𝗂𝖿𝗒 𝖲𝗁𝗈𝗋𝗍𝖾𝗇𝖾𝗋 𝖭𝖺𝗆𝖾 / 𝖠𝗉𝗂</u>
𝖭𝖺𝗆𝖾 - `{settings["shortner_three"]}`
𝖠𝗉𝗂 - `{settings["api_three"]}`

🧭 2𝗇𝖽 𝖵𝖾𝗋𝗂𝖿𝗂𝖼𝖺𝗍𝗂𝗈𝗇 𝖳𝗂𝗆𝖾 - `{settings['verify_time']}`

🧭 3𝗋𝖽 𝖵𝖾𝗋𝗂𝖿𝗂𝖼𝖺𝗍𝗂𝗈𝗇 𝖳𝗂𝗆𝖾 - `{settings['third_verify_time']}`

📝 𝖫𝗈𝗀 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖨𝖣 - `{settings['log']}`

🌀 𝖥𝖲𝗎𝖻 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 𝖨𝖣 - /show_fsub

📍 1𝗌𝗍 𝖳𝗎𝗍𝗈𝗋𝗂𝖺𝗅 𝖫𝗂𝗇𝗄 - {settings['tutorial']}

📍 2𝗇𝖽 𝖳𝗎𝗍𝗈𝗋𝗂𝖺𝗅 𝖫𝗂𝗇𝗄 - {settings['tutorial_2']}

📍 3𝗋𝖽 𝖳𝗎𝗍𝗈𝗋𝗂𝖺𝗅 𝖫𝗂𝗇𝗄 - {settings['tutorial_3']}

🎯 𝖨𝖬𝖣𝖡 𝖳𝖾𝗆𝗉𝗅𝖺𝗍𝖾 - `{settings['template']}`

📂 𝖥𝗂𝗅𝖾 𝖢𝖺𝗉𝗍𝗂𝗈𝗇 - `{settings['caption']}`</b>"""
    
    btn = [[
        InlineKeyboardButton("𝖱𝖾𝗌𝖾𝗍 𝖣𝖺𝗍𝖺", callback_data="reset_grp_data")
    ],[
        InlineKeyboardButton("𝖢𝗅𝗈𝗌𝖾", callback_data="close_data")
    ]]
    reply_markup=InlineKeyboardMarkup(btn)
    dlt=await message.reply_text(text, reply_markup=reply_markup, disable_web_page_preview=True)
    await asyncio.sleep(300)
    await dlt.delete()


@Client.on_message(filters.command('set_time_2'))
async def set_time_2(client, message):
    userid = message.from_user.id if message.from_user else None
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉...</b>")       
    if not userid:
        return await message.reply("<b>ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ...</b>")
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉</b>')
    try:
        time = int(message.text.split(" ", 1)[1])
    except:
        return await message.reply_text("𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖨𝗇𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾!")   
    await save_group_settings(grp_id, 'verify_time', time)
    await message.reply_text(f"Successfully set 1st verify time for {title}\n\nTime is - <code>{time}</code>")

@Client.on_message(filters.command('set_time_3'))
async def set_time_3(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply("<b>ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ...</b>")
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉...</b>")       
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉</b>')
    try:
        time = int(message.text.split(" ", 1)[1])
    except:
        return await message.reply_text("𝖢𝗈𝗆𝗆𝖺𝗇𝖽 𝖨𝗇𝖼𝗈𝗆𝗉𝗅𝖾𝗍𝖾!")   
    await save_group_settings(grp_id, 'third_verify_time', time)
    await message.reply_text(f"Successfully set 1st verify time for {title}\n\nTime is - <code>{time}</code>")


@Client.on_callback_query(filters.regex("mostsearch"))
async def most(client, callback_query):
    def is_alphanumeric(string):
        return bool(re.match('^[a-zA-Z0-9 ]*$', string))
    limit = 20  
    top_messages = await mdb.get_top_messages(limit)
    seen_messages = set()
    truncated_messages = []
    for msg in top_messages:
        msg_lower = msg.lower()
        if msg_lower not in seen_messages and is_alphanumeric(msg):
            seen_messages.add(msg_lower)
            
            if len(msg) > 35:
                truncated_messages.append(msg[:32] + "...")
            else:
                truncated_messages.append(msg)

   
    keyboard = [truncated_messages[i:i+2] for i in range(0, len(truncated_messages), 2)]
    
    reply_markup = ReplyKeyboardMarkup(
        keyboard, 
        one_time_keyboard=True, 
        resize_keyboard=True, 
        placeholder="Most searches of the day"
    )
    
    await callback_query.message.reply_text("<b>Hᴇʀᴇ ɪꜱ ᴛʜᴇ ᴍᴏꜱᴛ ꜱᴇᴀʀᴄʜᴇꜱ ʟɪꜱᴛ 👇</b>", reply_markup=reply_markup)
    await callback_query.answer()


@Client.on_callback_query(filters.regex(r"^trending$"))
async def top(client, query):
    movie_series_names = await movie_series_db.get_movie_series_names(1)
    if not movie_series_names:
        await query.message.reply("Tʜᴇʀᴇ ᴀʀᴇ ɴᴏ ᴍᴏᴠɪᴇ ᴏʀ sᴇʀɪᴇs ɴᴀᴍᴇs ᴀᴠᴀɪʟᴀʙʟᴇ ғᴏʀ ᴛʜᴇ ᴛᴏᴘ sᴇᴀʀᴄʜᴇs.")
        return
    buttons = [movie_series_names[i:i + 2] for i in range(0, len(movie_series_names), 2)]
    spika = ReplyKeyboardMarkup(
        buttons,
        resize_keyboard=True
    )
    await query.message.reply("<b>Here Is The Top Trending List 👇</b>", reply_markup=spika)
    
@Client.on_message(filters.command("refer"))
async def refer(bot, message):
    btn = [[
        InlineKeyboardButton('invite link', url=f'https://telegram.me/share/url?url=https://t.me/{bot.me.username}?start=reff_{message.from_user.id}&text=Hello%21%20Experience%20a%20bot%20that%20offers%20a%20vast%20library%20of%20unlimited%20movies%20and%20series.%20%F0%9F%98%83'),
        InlineKeyboardButton(f'⏳ {referdb.get_refer_points(message.from_user.id)}', callback_data='ref_point'),
        InlineKeyboardButton('Close', callback_data='close_data')
    ]]  
    m=await message.reply_sticker("CAACAgQAAxkBAAEkt_Rl_7138tgHJdEsqSNzO5mPWioZDgACGRAAAudLcFGAbsHU3KNJUx4E")      
    await m.delete()
    reply_markup = InlineKeyboardMarkup(btn)
    await message.reply_photo(
            photo=random.choice(REFER_PICS),
            caption=f'👋Hay {message.from_user.mention},\n\nHᴇʀᴇ ɪꜱ ʏᴏᴜʀ ʀᴇғғᴇʀᴀʟ ʟɪɴᴋ:\nhttps://t.me/{bot.me.username}?start=reff_{message.from_user.id}\n\nShare this link with your friends, Each time they join,  you will get 10 refferal points and after 100 points you will get 1 month premium subscription.',
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.private & filters.command("pm_search_on"))
async def set_pm_search_on(client, message):
    user_id = message.from_user.id
    bot_id = client.me.id
    if user_id not in ADMINS:
        await message.delete()
        return
    
    await db.update_pm_search_status(bot_id, enable=True)
    await message.reply_text("<b><i>✅️ ᴘᴍ ꜱᴇᴀʀᴄʜ ᴇɴᴀʙʟᴇᴅ, ꜰʀᴏᴍ ɴᴏᴡ ᴜꜱᴇʀꜱ ᴀʙʟᴇ ᴛᴏ ꜱᴇᴀʀᴄʜ ᴍᴏᴠɪᴇ ɪɴ ʙᴏᴛ ᴘᴍ.</i></b>")

@Client.on_message(filters.private & filters.command("pm_search_off"))
async def set_pm_search_off(client, message):
    user_id = message.from_user.id
    bot_id = client.me.id
    if user_id not in ADMINS:
        await message.delete()
        return
    
    await db.update_pm_search_status(bot_id, enable=False)
    await message.reply_text("<b><i>❌️ ᴘᴍ ꜱᴇᴀʀᴄʜ ᴅɪꜱᴀʙʟᴇᴅ, ꜰʀᴏᴍ ɴᴏᴡ ɴᴏ ᴏɴᴇ ᴄᴀɴ ᴀʙʟᴇ ᴛᴏ ꜱᴇᴀʀᴄʜ ᴍᴏᴠɪᴇ ɪɴ ʙᴏᴛ ᴘᴍ.</i></b>")


@Client.on_message(filters.private & filters.command("movie_update_on"))
async def set_send_movie_on(client, message):
    user_id = message.from_user.id
    bot_id = client.me.id
    if user_id not in ADMINS:
        await message.delete()
        return    
    await db.update_send_movie_update_status(bot_id, enable=True)
    await message.reply_text("<b><i>✅️ ꜱᴇɴᴅ ᴍᴏᴠɪᴇ ᴜᴘᴅᴀᴛᴇ ᴇɴᴀʙʟᴇᴅ.</i></b>")

@Client.on_message(filters.private & filters.command("movie_update_off"))
async def set_send_movie_update_off(client, message):
    user_id = message.from_user.id
    bot_id = client.me.id
    if user_id not in ADMINS:
        await message.delete()
        return    
    await db.update_send_movie_update_status(bot_id, enable=False)
    await message.reply_text("<b><i>❌️ ꜱᴇɴᴅ ᴍᴏᴠɪᴇ ᴜᴘᴅᴀᴛᴇ ᴅɪꜱᴀʙʟᴇᴅ.</i></b>")
    
@Client.on_message(filters.command("verify_id"))
async def generate_verify_id(bot, message):
    if message.from_user.id not in ADMINS:
        await message.reply('Only the bot Admin can use this command... 😑')
        return
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("This command only works in groups!")
    grpid = message.chat.id   
    if grpid in verification_ids:
        await message.reply_text(f"An active Verify ID already exists for this group: `/verifyoff {verification_ids[grpid]}`")
        return
    
    verify_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    verification_ids[grpid] = verify_id
    await message.reply_text(f"Verify ID: `/verifyoff {verify_id}` (Valid for this group, one-time use)")
    return

@Client.on_message(filters.command("verifyoff"))
async def verifyoff(bot, message):
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("This command only works in groups!")
    
    grpid = message.chat.id
    if not await is_check_admin(bot, grpid, message.from_user.id):  # Changed client to bot
        return await message.reply_text('<b>You are not an admin in this group!</b>')
    
    try:
        input_id = message.command[1]
    except IndexError:
        return await message.reply_text("Please provide the Verify ID along with the command.\nUsage: `/verifyoff {id}`")
    
    if grpid not in verification_ids or verification_ids[grpid] != input_id:
        return await message.reply_text("Invalid Verify ID! Please contact the admin for the correct ID.")
    
    await save_group_settings(grpid, 'is_verify', False)
    del verification_ids[grpid]
    return await message.reply_text("Verification successfully disabled.")


@Client.on_message(filters.command("verifyon"))
async def verifyon(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("This command only works in groups!")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    
    if not await is_check_admin(bot, grpid, message.from_user.id):  # Changed client to bot
        return await message.reply_text('<b>You are not an admin in this group!</b>')
    
    await save_group_settings(grpid, 'is_verify', True)
    return await message.reply_text("Verification successfully enabled.")

@Client.on_message(filters.command("reset_group"))
async def reset_group_command(client, message):
    grp_id = message.chat.id
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗍𝗁𝗂𝗌 𝗀𝗋𝗈𝗎𝗉</b>')
    sts = await message.reply("<b>♻️ ᴄʜᴇᴄᴋɪɴɢ...</b>")
    await asyncio.sleep(1.2)
    await sts.delete()
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<b>𝖴𝗌𝖾 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗂𝗇 𝗀𝗋𝗈𝗎𝗉...</b>")
    btn = [[
        InlineKeyboardButton('🚫 ᴄʟᴏsᴇ 🚫', callback_data='close_data')
    ]]
    reply_markup = InlineKeyboardMarkup(btn)
    await save_default_settings(grp_id)
    await message.reply_text('ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ʀᴇꜱᴇᴛ ɢʀᴏᴜᴘ ꜱᴇᴛᴛɪɴɢꜱ...')
    
