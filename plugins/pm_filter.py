import asyncio
import re
import math
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from info import * #SUBSCRIPTION, PAYPICS, START_IMG, SETTINGS, URL, STICKERS_IDS,PREMIUM_POINT,MAX_BTN, BIN_CHANNEL, USERNAME, URL, ADMINS,REACTIONS, LANGUAGES, QUALITIES, YEARS, SEASONS, AUTH_CHANNEL, SUPPORT_GROUP, IMDB, IMDB_TEMPLATE, LOG_CHANNEL, LOG_VR_CHANNEL, TUTORIAL, FILE_CAPTION, SHORTENER_WEBSITE, SHORTENER_API, SHORTENER_WEBSITE2, SHORTENER_API2, DELETE_TIME
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto, ChatPermissions, WebAppInfo, InputMediaAnimation, InputMediaPhoto
from pyrogram import Client, filters, enums
from pyrogram.errors import * #FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid, ChatAdminRequired
from utils import temp, get_settings, is_check_admin, get_status, get_size, save_group_settings, is_req_subscribed, get_poster, get_status, get_readable_time , imdb , formate_file_name
from database.users_chats_db import db
from database.ia_filterdb import Media, get_search_results, get_bad_files, get_file_details
import random
lock = asyncio.Lock()
import traceback
from fuzzywuzzy import process
BUTTONS = {}
FILES_ID = {}
CAP = {}

# zishan [
from database.jsreferdb import referdb
from database.config_db import mdb
import logging
from urllib.parse import quote_plus
from Jisshu.util.file_properties import get_name, get_hash, get_media_file_size
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
# ] codes add


@Client.on_message(filters.private & filters.text & filters.incoming)
async def pm_search(client, message):
    await mdb.update_top_messages(message.from_user.id, message.text)
    bot_id = client.me.id
    user_id = message.from_user.id    
 #   if user_id in ADMINS: return
    if str(message.text).startswith('/'):
        return
    if await db.get_pm_search_status(bot_id):
        if 'hindi' in message.text.lower() or 'tamil' in message.text.lower() or 'telugu' in message.text.lower() or 'malayalam' in message.text.lower() or 'kannada' in message.text.lower() or 'english' in message.text.lower() or 'gujarati' in message.text.lower(): 
            return await auto_filter(client, message)
        await auto_filter(client, message)
    else:
        await message.reply_text("<b><i>𝖨 𝖺𝗆 𝗇𝗈𝗍 𝗐𝗈𝗋𝗄𝗂𝗇𝗀 𝗁𝖾𝗋𝖾. 𝖲𝖾𝖺𝗋𝖼𝗁 𝗆𝗈𝗏𝗂𝖾𝗌 𝗂𝗇 𝗈𝗎𝗋 𝗆𝗈𝗏𝗂𝖾 𝗌𝖾𝖺𝗋𝖼𝗁 𝗀𝗋𝗈𝗎𝗉.</i></b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📝 𝖬𝗈𝗏𝗂𝖾 𝖲𝖾𝖺𝗋𝖼𝗁 𝖦𝗋𝗈𝗎𝗉 ", url='https://t.me/+ZUyhAwBNBsU0YjA9')]]))
        
    
@Client.on_message(filters.group & filters.text & filters.incoming)
async def group_search(client, message):
    #await message.react(emoji=random.choice(REACTIONS))
    await mdb.update_top_messages(message.from_user.id, message.text)
    user_id = message.from_user.id if message.from_user else None
    chat_id = message.chat.id
    settings = await get_settings(chat_id)
 
    if message.chat.id == SUPPORT_GROUP :
                if message.text.startswith("/"):
                    return
                files, n_offset, total = await get_search_results(message.text, offset=0)
                if total != 0:
                    link = await db.get_set_grp_links(index=1)
                    msg = await message.reply_text(script.SUPPORT_GRP_MOVIE_TEXT.format(message.from_user.mention(), total), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('𝖦𝖾𝗍 𝖥𝗂𝗅𝖾𝗌 𝖥𝗋𝗈𝗆 𝖧𝖾𝗋𝖾 😉' , url='https://t.me/+ZUyhAwBNBsU0YjA9')]]))
                    await asyncio.sleep(300)
                    return await msg.delete()
                else: return     
    if settings["auto_filter"]:
        if not user_id:
            #await message.reply("<b>🚨 ɪ'ᴍ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ ғᴏʀ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ!</b>")
            return
        
        if 'hindi' in message.text.lower() or 'tamil' in message.text.lower() or 'telugu' in message.text.lower() or 'malayalam' in message.text.lower() or 'kannada' in message.text.lower() or 'english' in message.text.lower() or 'gujarati' in message.text.lower(): 
            return await auto_filter(client, message)

        elif message.text.startswith("/"):
            return
        
        elif re.findall(r'https?://\S+|www\.\S+|t\.me/\S+', message.text):
            if await is_check_admin(client, message.chat.id, message.from_user.id):
                return
            await message.delete()
            return await message.reply("<b>𝖲𝖾𝗇𝖽𝗂𝗇𝗀 𝗅𝗂𝗇𝗄𝗌 𝗂𝗌𝗇'𝗍 𝖺𝗅𝗅𝗈𝗐𝖾𝖽 𝗁𝖾𝗋𝖾 ❌🤞🏻</b>")

        elif '@admin' in message.text.lower() or '@admins' in message.text.lower():
            if await is_check_admin(client, message.chat.id, message.from_user.id):
                return
            admins = []
            async for member in client.get_chat_members(chat_id=message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
                if not member.user.is_bot:
                    admins.append(member.user.id)
                    if member.status == enums.ChatMemberStatus.OWNER:
                        if message.reply_to_message:
                            try:
                                sent_msg = await message.reply_to_message.forward(member.user.id)
                                await sent_msg.reply_text(f"#Attention\n★ 𝖴𝗌𝖾𝗋: {message.from_user.mention}\n★ 𝖦𝗋𝗈𝗎𝗉: {message.chat.title}\n\n★ <a href={message.reply_to_message.link}>𝖦𝗈 𝗍𝗈 𝗆𝖾𝗌𝗌𝖺𝗀𝖾</a>", disable_web_page_preview=True)
                            except:
                                pass
                        else:
                            try:
                                sent_msg = await message.forward(member.user.id)
                                await sent_msg.reply_text(f"#Attention\n★ 𝖴𝗌𝖾𝗋: {message.from_user.mention}\n★ 𝖦𝗋𝗈𝗎𝗉: {message.chat.title}\n\n★ <a href={message.link}>𝖦𝗈 𝗍𝗈 𝗆𝖾𝗌𝗌𝖺𝗀𝖾</a>", disable_web_page_preview=True)
                            except:
                                pass
            hidden_mentions = (f'[\u2064](tg://user?id={user_id})' for user_id in admins)
            await message.reply_text('<code>𝖱𝖾𝗉𝗈𝗋𝗍 𝖲𝖾𝗇𝗍</code>' + ''.join(hidden_mentions))
            return               
        else:
            try: 
                await auto_filter(client, message)
            except Exception as e:
                traceback.print_exc()
                print('𝖿𝗈𝗎𝗇𝖽 𝖾𝗋𝗋 𝗂𝗇 𝗀𝗋𝗉 𝗌𝖾𝖺𝗋𝖼𝗁  :',e)

    else:
        k=await message.reply_text('<b>⚠️ 𝖠𝗎𝗍𝗈 𝖥𝗂𝗅𝗍𝖾𝗋 𝖬𝗈𝖽𝖾 𝗂𝗌 𝖮𝖿𝖿...</b>')
        await asyncio.sleep(10)
        await k.delete()
        try:
            await message.delete()
        except:
            pass

@Client.on_callback_query(filters.regex(r"^reffff"))
async def refercall(bot, query):
    btn = [[
        InlineKeyboardButton('𝖨𝗇𝗏𝗂𝗍𝖾 𝖫𝗂𝗇𝗄', url=f'https://telegram.me/share/url?url=https://t.me/{bot.me.username}?start=reff_{query.from_user.id}&text=Hello%21%20Experience%20a%20bot%20that%20offers%20a%20vast%20library%20of%20unlimited%20movies%20and%20series.%20%F0%9F%98%83'),
        InlineKeyboardButton(f'⏳ {referdb.get_refer_points(query.from_user.id)}', callback_data='ref_point'),
        InlineKeyboardButton('𝖡𝖺𝖼𝗄', callback_data='close_data')
    ]]
    reply_markup = InlineKeyboardMarkup(btn)
    await bot.send_photo(
        chat_id=query.message.chat.id,
        photo="https://graph.org/file/1a2e64aee3d4d10edd930.jpg",
        caption=f'𝖧𝖾𝗋𝖾 𝗂𝗌 𝗒𝗈𝗎𝗋 𝗋𝖾𝖿𝖾𝗋 𝗅𝗂𝗇𝗄:\n\nhttps://t.me/{bot.me.username}?start=reff_{query.from_user.id}\n\n𝖲𝗁𝖺𝗋𝖾 𝗍𝗁𝗂𝗌 𝗅𝗂𝗇𝗄 𝗐𝗂𝗍𝗁 𝗒𝗈𝗎𝗋 𝖿𝗋𝗂𝖾𝗇𝖽𝗌, 𝖤𝖺𝖼𝗁 𝗍𝗂𝗆𝖾 𝗍𝗁𝖾𝗒 𝗃𝗈𝗂𝗇, 𝗒𝗈𝗎 𝗐𝗂𝗅𝗅 𝗀𝖾𝗍 10 𝗋𝖾𝖿𝖾𝗋𝗋𝖺𝗅 𝗉𝗈𝗂𝗇𝗍𝗌 𝖺𝗇𝖽 𝖺𝖿𝗍𝖾𝗋 100 𝗉𝗈𝗂𝗇𝗍𝗌 𝗒𝗈𝗎 𝗐𝗂𝗅𝗅 𝗀𝖾𝗍 1 𝗆𝗈𝗇𝗍𝗁 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝗌𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇.',
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML
    )
    await query.answer()
	


@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = BUTTONS.get(key)
    cap = CAP.get(key)
    if not search:
        await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name),show_alert=True)
        return
    files, n_offset, total = await get_search_results(search, offset=offset)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0
    if not files:
        return
    temp.FILES_ID[key] = files
    batch_ids = files
    temp.FILES_ID[f"{query.message.chat.id}-{query.id}"] = batch_ids
    batch_link = f"batchfiles#{query.message.chat.id}#{query.id}#{query.from_user.id}"
    ads, ads_name, _ = await mdb.get_advirtisment()
    ads_text = ""
    if ads is not None and ads_name is not None:
        ads_url = f"https://t.me/{temp.U_NAME}?start=ads"
        ads_text = f"<a href={ads_url}>{ads_name}</a>"
    js_ads = f"\n━━━━━━━━━━━━━━━━━━\n <b>{ads_text}</b> \n━━━━━━━━━━━━━━━━━━" if ads_text else ""
    settings = await get_settings(query.message.chat.id)
    reqnxt  = query.from_user.id if query.from_user else 0
    temp.CHAT[query.from_user.id] = query.message.chat.id
    #del_msg = f"\n\n<b>⚠️ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀꜰᴛᴇʀ <code>{get_readable_time(DELETE_TIME)}</code> ᴛᴏ ᴀᴠᴏɪᴅ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs</b>" if settings["auto_delete"] else ''
    links = ""
    if settings["link"]:
        btn = []
        for file_num, file in enumerate(files, start=offset+1):
            links += f"""<b>\n\n{file_num}. <a href=https://t.me/{temp.U_NAME}?start=file_{query.message.chat.id}_{file.file_id}>[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}</a></b>"""
    else:
        btn = [[InlineKeyboardButton(text=f"📁 {get_size(file.file_size)}≽ {formate_file_name(file.file_name)}", url=f'https://telegram.dog/{temp.U_NAME}?start=file_{query.message.chat.id}_{file.file_id}'),]
                for file in files
              ]
    btn.insert(0,[
	InlineKeyboardButton("📥 𝖲𝖾𝗇𝖽 𝖠𝗅𝗅 𝖥𝗂𝗅𝖾𝗌 📥", callback_data=batch_link),
        ])
    btn.insert(1, [
        InlineKeyboardButton("𝖰𝗎𝖺𝗅𝗂𝗍𝗒", callback_data=f"qualities#{key}#{offset}#{req}"),
	InlineKeyboardButton("𝖲𝖾𝖺𝗌𝗈𝗇", callback_data=f"seasons#{key}#{offset}#{req}"),
        InlineKeyboardButton("𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾", callback_data=f"languages#{key}#{offset}#{req}")
    ])    

    if 0 < offset <= int(MAX_BTN):
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - int(MAX_BTN)
    if n_offset == 0:

        btn.append(
            [InlineKeyboardButton("⪻ 𝖡𝖺𝖼𝗄", callback_data=f"next_{req}_{key}_{off_set}"),
             InlineKeyboardButton(f"𝖯𝖺𝗀𝖾 {math.ceil(int(offset) / int(MAX_BTN)) + 1} / {math.ceil(total / int(MAX_BTN))}", callback_data="pages")]
        )
    elif off_set is None:
        btn.append(
            [InlineKeyboardButton(f"{math.ceil(int(offset) / int(MAX_BTN)) + 1} / {math.ceil(total / int(MAX_BTN))}", callback_data="pages"),
             InlineKeyboardButton("𝖭𝖾𝗑𝗍 ⪼", callback_data=f"next_{req}_{key}_{n_offset}")])
    else:
        btn.append(
            [
                InlineKeyboardButton("⪻ 𝖡𝖺𝖼𝗄", callback_data=f"next_{req}_{key}_{off_set}"),
                InlineKeyboardButton(f"{math.ceil(int(offset) / int(MAX_BTN)) + 1} / {math.ceil(total / int(MAX_BTN))}", callback_data="pages"),
                InlineKeyboardButton("𝖭𝖾𝗑𝗍 ⪼", callback_data=f"next_{req}_{key}_{n_offset}")
            ],
        )
    if settings["link"]:
        links = ""
        for file_num, file in enumerate(files, start=offset+1):
            links += f"""<b>\n\n{file_num}. <a href=https://t.me/{temp.U_NAME}?start=file_{query.message.chat.id}_{file.file_id}>[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}</a></b>"""
        await query.message.edit_text(cap + links + js_ads, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(btn))
        return        
    try:
        await query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(btn)
        )
    except MessageNotModified:
        pass
    await query.answer()
    
@Client.on_callback_query(filters.regex(r"^seasons#"))
async def seasons_cb_handler(client: Client, query: CallbackQuery):
    _, key, offset, req = query.data.split("#")
    if int(req) != query.from_user.id:
        return await query.answer(script.ALRT_TXT, show_alert=True) 
    btn= []
    for i in range(0, len(SEASONS)-1, 3):
        btn.append([
            InlineKeyboardButton(
                text=SEASONS[i].title(),
                callback_data=f"season_search#{SEASONS[i].lower()}#{key}#0#{offset}#{req}"
            ),
            InlineKeyboardButton(
                text=SEASONS[i+1].title(),
                callback_data=f"season_search#{SEASONS[i+1].lower()}#{key}#0#{offset}#{req}"
            ),
            InlineKeyboardButton(
                text=SEASONS[i+2].title(),
                callback_data=f"season_search#{SEASONS[i+2].lower()}#{key}#0#{offset}#{req}"
            ),
        ])

    btn.append([InlineKeyboardButton(text="⪻ 𝖡𝖺𝖼𝗄 𝗍𝗈 𝗆𝖺𝗂𝗇 𝗉𝖺𝗀𝖾", callback_data=f"next_{req}_{key}_{offset}")])
    await query.message.edit_text("<b>𝖨𝗇 𝗐𝗁𝗂𝖼𝗁 𝖲𝖾𝖺𝗌𝗈𝗇 𝖽𝗈 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍, 𝖼𝗁𝗈𝗈𝗌𝖾 𝖿𝗋𝗈𝗆 𝗁𝖾𝗋𝖾 ↓↓</b>", reply_markup=InlineKeyboardMarkup(btn))
    return

@Client.on_callback_query(filters.regex(r"^season_search#"))
async def season_search(client: Client, query: CallbackQuery):
    _, season, key, offset, orginal_offset, req = query.data.split("#")
    seas = int(season.split(' ' , 1)[1])
    if seas < 10:
        seas = f'S0{seas}'
    else:
        seas = f'S{seas}'
    
    if int(req) != query.from_user.id:
        return await query.answer(script.ALRT_TXT, show_alert=True)	
    offset = int(offset)
    search = BUTTONS.get(key)
    cap = CAP.get(key)
    if not search:
        await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name),show_alert=True)
        return 
    search = search.replace("_", " ")
    files, n_offset, total = await get_search_results(f"{search} {seas}", max_results=int(MAX_BTN), offset=offset)
    files2, n_offset2, total2 = await get_search_results(f"{search} {season}", max_results=int(MAX_BTN), offset=offset)
    total += total2
    try:
        n_offset = int(n_offset)
    except:
        try: 
            n_offset = int(n_offset2)
        except : 
            n_offset = 0
    files = [file for file in files if re.search(seas, file.file_name, re.IGNORECASE)]
    
    if not files:
        files = [file for file in files2 if re.search(season, file.file_name, re.IGNORECASE)]
        if not files:
            await query.answer(f"𝖲𝗈𝗋𝗋𝗒 {season.title()} 𝗇𝗈𝗍 𝖿𝗈𝗎𝗇𝖽 𝖿𝗈𝗋 {search}", show_alert=1)
            return

    batch_ids = files
    temp.FILES_ID[f"{query.message.chat.id}-{query.id}"] = batch_ids
    batch_link = f"batchfiles#{query.message.chat.id}#{query.id}#{query.from_user.id}"
    reqnxt = query.from_user.id if query.from_user else 0
    settings = await get_settings(query.message.chat.id)
    temp.CHAT[query.from_user.id] = query.message.chat.id
    ads, ads_name, _ = await mdb.get_advirtisment()
    ads_text = ""
    if ads is not None and ads_name is not None:
        ads_url = f"https://t.me/{temp.U_NAME}?start=ads"
        ads_text = f"<a href={ads_url}>{ads_name}</a>"
    js_ads = f"\n━━━━━━━━━━━━━━━━━━\n <b>{ads_text}</b> \n━━━━━━━━━━━━━━━━━━" if ads_text else ""
  #  del_msg = f"\n\n<b>⚠️ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀꜰᴛᴇʀ <code>{get_readable_time(DELETE_TIME)}</code> ᴛᴏ ᴀᴠᴏɪᴅ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs</b>" if settings["auto_delete"] else ''
    links = ""
    if settings["link"]:
        btn = []
        for file_num, file in enumerate(files, start=offset+1):
            links += f"""<b>\n\n{file_num}. <a href=https://t.me/{temp.U_NAME}?start=file_{query.message.chat.id}_{file.file_id}>[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}</a></b>"""
    else:
        btn = [[
                InlineKeyboardButton(text=f"🔗 {get_size(file.file_size)}≽ {formate_file_name(file.file_name)}", callback_data=f'cfiles#{reqnxt}#{file.file_id}'),]
                   for file in files
              ]
   
    btn.insert(0,[
	InlineKeyboardButton("📥 𝖲𝖾𝗇𝖽 𝖠𝗅𝗅 𝖥𝗂𝗅𝖾𝗌 📥", callback_data=batch_link),
        ])
    btn.insert(1, [
        InlineKeyboardButton("𝖰𝗎𝖺𝗅𝗂𝗍𝗒", callback_data=f"qualities#{key}#{offset}#{req}"),
	InlineKeyboardButton("𝖲𝖾𝖺𝗌𝗈𝗇", callback_data=f"seasons#{key}#{offset}#{req}"),
        InlineKeyboardButton("𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾", callback_data=f"languages#{key}#{offset}#{req}")
    ])    
    
    if n_offset== '':
        btn.append(
            [InlineKeyboardButton(text="🚸 𝖭𝗈 𝖬𝗈𝗋𝖾 𝖯𝖺𝗀𝖾𝗌 🚸", callback_data="buttons")]
        )
    elif n_offset == 0:
        btn.append(
            [InlineKeyboardButton("⪻ 𝖡𝖺𝖼𝗄", callback_data=f"season_search#{season}#{key}#{offset- int(MAX_BTN)}#{orginal_offset}#{req}"),
             InlineKeyboardButton(f"{math.ceil(offset / int(MAX_BTN)) + 1}/{math.ceil(total / int(MAX_BTN))}", callback_data="pages",),
            ])
    elif offset==0:
        btn.append(
            [InlineKeyboardButton(f"{math.ceil(offset / int(MAX_BTN)) + 1}/{math.ceil(total / int(MAX_BTN))}",callback_data="pages",),
             InlineKeyboardButton("𝖭𝖾𝗑𝗍 ⪼", callback_data=f"season_search#{season}#{key}#{n_offset}#{orginal_offset}#{req}"),])
    else:
        btn.append(
            [InlineKeyboardButton("⪻ 𝖡𝖺𝖼𝗄", callback_data=f"season_search#{season}#{key}#{offset- int(MAX_BTN)}#{orginal_offset}#{req}"),
             InlineKeyboardButton(f"{math.ceil(offset / int(MAX_BTN)) + 1}/{math.ceil(total / int(MAX_BTN))}", callback_data="pages",),
             InlineKeyboardButton("𝖭𝖾𝗑𝗍 ⪼", callback_data=f"season_search#{season}#{key}#{n_offset}#{orginal_offset}#{req}"),])

    btn.append([
        InlineKeyboardButton(text="⪻ 𝖡𝖺𝖼𝗄 𝗍𝗈 𝗆𝖺𝗂𝗇 𝗉𝖺𝗀𝖾", callback_data=f"next_{req}_{key}_{orginal_offset}"),])
    await query.message.edit_text(cap + links + js_ads, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(btn))
    return

@Client.on_callback_query(filters.regex(r"^years#"))
async def years_cb_handler(client: Client, query: CallbackQuery):
    _, key, offset, req = query.data.split("#")
    if int(req) != query.from_user.id:
        return await query.answer(script.ALRT_TXT, show_alert=True)
    btn  = []
    for i in range(0, len(YEARS)-1, 3):
        btn.append([
            InlineKeyboardButton(
                text=YEARS[i].title(),
                callback_data=f"years_search#{YEARS[i].lower()}#{key}#0#{offset}#{req}"
            ),
            InlineKeyboardButton(
                text=YEARS[i+1].title(),
                callback_data=f"years_search#{YEARS[i+1].lower()}#{key}#0#{offset}#{req}"
            ),
            InlineKeyboardButton(
                text=YEARS[i+2].title(),
                callback_data=f"years_search#{YEARS[i+2].lower()}#{key}#0#{offset}#{req}"
            ),
        ])
    
    btn.append([InlineKeyboardButton(text="⪻ 𝖡𝖺𝖼𝗄 𝗍𝗈 𝗆𝖺𝗂𝗇 𝗉𝖺𝗀𝖾", callback_data=f"next_{req}_{key}_{offset}")])
    await query.message.edit_text("<b>𝖨𝗇 𝗐𝗁𝗂𝖼𝗁 𝗒𝖾𝖺𝗋 𝖽𝗈 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍, 𝖼𝗁𝗈𝗈𝗌𝖾 𝖿𝗋𝗈𝗆 𝗁𝖾𝗋𝖾 ↓↓</b>", reply_markup=InlineKeyboardMarkup(btn))
    return

@Client.on_callback_query(filters.regex(r"^years_search#"))
async def year_search(client: Client, query: CallbackQuery):
    _, year, key, offset, orginal_offset, req = query.data.split("#")
    if int(req) != query.from_user.id:
        return await query.answer(script.ALRT_TXT, show_alert=True)	
    offset = int(offset)
    search = BUTTONS.get(key)
    cap = CAP.get(key)
    if not search:
        await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name),show_alert=True)
        return 
    search = search.replace("_", " ")
    files, n_offset, total = await get_search_results(f"{search} {year}", max_results=int(MAX_BTN), offset=offset)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0
    files = [file for file in files if re.search(year, file.file_name, re.IGNORECASE)]
    if not files:
        await query.answer(f"𝖲𝗈𝗋𝗋𝗒 𝗒𝖾𝖺𝗋 {year.title()} 𝗇𝗈𝗍 𝖿𝗈𝗎𝗇𝖽 𝖿𝗈𝗋 {search}", show_alert=1)
        return

    batch_ids = files
    temp.FILES_ID[f"{query.message.chat.id}-{query.id}"] = batch_ids
    batch_link = f"batchfiles#{query.message.chat.id}#{query.id}#{query.from_user.id}"

    reqnxt = query.from_user.id if query.from_user else 0
    settings = await get_settings(query.message.chat.id)
    temp.CHAT[query.from_user.id] = query.message.chat.id
    ads, ads_name, _ = await mdb.get_advirtisment()
    ads_text = ""
    if ads is not None and ads_name is not None:
        ads_url = f"https://t.me/{temp.U_NAME}?start=ads"
        ads_text = f"<a href={ads_url}>{ads_name}</a>"
    js_ads = f"\n━━━━━━━━━━━━━━━━━━\n <b>{ads_text}</b> \n━━━━━━━━━━━━━━━━━━" if ads_text else ""
    #del_msg = f"\n\n<b>⚠️ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀꜰᴛᴇʀ <code>{get_readable_time(DELETE_TIME)}</code> ᴛᴏ ᴀᴠᴏɪᴅ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs</b>" if settings["auto_delete"] else ''
    links = ""
    if settings["link"]:
        btn = []
        for file_num, file in enumerate(files, start=offset+1):
            links += f"""<b>\n\n{file_num}. <a href=https://t.me/{temp.U_NAME}?start=file_{query.message.chat.id}_{file.file_id}>[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}</a></b>"""
    else:
        btn = [[
                InlineKeyboardButton(text=f"🔗 {get_size(file.file_size)}≽ {formate_file_name(file.file_name)}", callback_data=f'cfiles#{reqnxt}#{file.file_id}'),]
                   for file in files
              ]
        
   
    btn.insert(0,[
	InlineKeyboardButton("📥 𝖲𝖾𝗇𝖽 𝖠𝗅𝗅 𝖥𝗂𝗅𝖾𝗌 📥", callback_data=batch_link),
        ])
    btn.insert(1, [
        InlineKeyboardButton("𝖰𝗎𝖺𝗅𝗂𝗍𝗒", callback_data=f"qualities#{key}#{offset}#{req}"),
	InlineKeyboardButton("𝖲𝖾𝖺𝗌𝗈𝗇", callback_data=f"seasons#{key}#{offset}#{req}"),
        InlineKeyboardButton("𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾", callback_data=f"languages#{key}#{offset}#{req}")
    ])    
    
    if n_offset== '':
        btn.append(
            [InlineKeyboardButton(text="🚸 𝖭𝗈 𝖬𝗈𝗋𝖾 𝖯𝖺𝗀𝖾𝗌 🚸", callback_data="buttons")]
        )
    elif n_offset == 0:
        btn.append(
            [InlineKeyboardButton("⪻ 𝖡𝖺𝖼𝗄", callback_data=f"years_search#{year}#{key}#{offset- int(MAX_BTN)}#{orginal_offset}#{req}"),
             InlineKeyboardButton(f"{math.ceil(offset / int(MAX_BTN)) + 1}/{math.ceil(total / int(MAX_BTN))}", callback_data="pages",),
            ])
    elif offset==0:
        btn.append(
            [InlineKeyboardButton(f"{math.ceil(offset / int(MAX_BTN)) + 1}/{math.ceil(total / int(MAX_BTN))}",callback_data="pages",),
             InlineKeyboardButton("𝖭𝖾𝗑𝗍 ⪼", callback_data=f"years_search#{year}#{key}#{n_offset}#{orginal_offset}#{req}"),])
    else:
        btn.append(
            [InlineKeyboardButton("⪻ 𝖡𝖺𝖼𝗄", callback_data=f"years_search#{year}#{key}#{offset- int(MAX_BTN)}#{orginal_offset}#{req}"),
             InlineKeyboardButton(f"{math.ceil(offset / int(MAX_BTN)) + 1}/{math.ceil(total / int(MAX_BTN))}", callback_data="pages",),
             InlineKeyboardButton("𝖭𝖾𝗑𝗍 ⪼", callback_data=f"years_search#{year}#{key}#{n_offset}#{orginal_offset}#{req}"),])

    btn.append([
        InlineKeyboardButton(text="⪻ 𝖡𝖺𝖼𝗄 𝗍𝗈 𝗆𝖺𝗂𝗇 𝗉𝖺𝗀𝖾", callback_data=f"next_{req}_{key}_{orginal_offset}"),])
    await query.message.edit_text(cap + links + js_ads, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(btn))
    return

@Client.on_callback_query(filters.regex(r"^qualities#"))
async def quality_cb_handler(client: Client, query: CallbackQuery):
    _, key, offset, req = query.data.split("#")
    if int(req) != query.from_user.id:
        return await query.answer(script.ALRT_TXT, show_alert=True)
    btn= []
    for i in range(0, len(QUALITIES)-1, 3):
        btn.append([
            InlineKeyboardButton(
                text=QUALITIES[i].title(),
                callback_data=f"quality_search#{QUALITIES[i].lower()}#{key}#0#{offset}#{req}"
            ),
            InlineKeyboardButton(
                text=QUALITIES[i+1].title(),
                callback_data=f"quality_search#{QUALITIES[i+1].lower()}#{key}#0#{offset}#{req}"
            ),
            InlineKeyboardButton(
                text=QUALITIES[i+2].title(),
                callback_data=f"quality_search#{QUALITIES[i+2].lower()}#{key}#0#{offset}#{req}"
            ),
        ])
    btn.append([InlineKeyboardButton(text="⪻ 𝖡𝖺𝖼𝗄 𝗍𝗈 𝗆𝖺𝗂𝗇 𝗉𝖺𝗀𝖾", callback_data=f"next_{req}_{key}_{offset}")])
    await query.message.edit_text("<b>𝖨𝗇 𝗐𝗁𝗂𝖼𝗁 𝗊𝗎𝖺𝗅𝗂𝗍𝗒 𝖽𝗈 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍, 𝖼𝗁𝗈𝗈𝗌𝖾 𝖿𝗋𝗈𝗆 𝗁𝖾𝗋𝖾 ↓↓</b>", reply_markup=InlineKeyboardMarkup(btn))
    return

@Client.on_callback_query(filters.regex(r"^quality_search#"))
async def quality_search(client: Client, query: CallbackQuery):
    _, qul, key, offset, orginal_offset, req = query.data.split("#")
    if int(req) != query.from_user.id:
        return await query.answer(script.ALRT_TXT, show_alert=True)	
    offset = int(offset)
    search = BUTTONS.get(key)
    cap = CAP.get(key)
    if not search:
        await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name),show_alert=True)
        return 
    search = search.replace("_", " ")
    files, n_offset, total = await get_search_results(f"{search} {qul}", max_results=int(MAX_BTN), offset=offset)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0
    files = [file for file in files if re.search(qul, file.file_name, re.IGNORECASE)]
    if not files:
        await query.answer(f"𝖲𝗈𝗋𝗋𝗒 𝖰𝗎𝖺𝗅𝗂𝗍𝗒 {qul.title()} 𝗇𝗈𝗍 𝖿𝗈𝗎𝗇𝖽 𝖿𝗈𝗋 {search}", show_alert=1)
        return

    batch_ids = files
    temp.FILES_ID[f"{query.message.chat.id}-{query.id}"] = batch_ids
    batch_link = f"batchfiles#{query.message.chat.id}#{query.id}#{query.from_user.id}"

    reqnxt = query.from_user.id if query.from_user else 0
    settings = await get_settings(query.message.chat.id)
    temp.CHAT[query.from_user.id] = query.message.chat.id
    ads, ads_name, _ = await mdb.get_advirtisment()
    ads_text = ""
    if ads is not None and ads_name is not None:
        ads_url = f"https://t.me/{temp.U_NAME}?start=ads"
        ads_text = f"<a href={ads_url}>{ads_name}</a>"
    js_ads = f"\n━━━━━━━━━━━━━━━━━━\n <b>{ads_text}</b> \n━━━━━━━━━━━━━━━━━━" if ads_text else ""
  #  del_msg = f"\n\n<b>⚠️ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀꜰᴛᴇʀ <code>{get_readable_time(DELETE_TIME)}</code> ᴛᴏ ᴀᴠᴏɪᴅ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs</b>" if settings["auto_delete"] else ''
    links = ""
    if settings["link"]:
        btn = []
        for file_num, file in enumerate(files, start=offset+1):
            links += f"""<b>\n\n{file_num}. <a href=https://t.me/{temp.U_NAME}?start=file_{query.message.chat.id}_{file.file_id}>[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}</a></b>"""
    else:
        btn = [[
                InlineKeyboardButton(text=f"🔗 {get_size(file.file_size)}≽ {formate_file_name(file.file_name)}", callback_data=f'cfiles#{reqnxt}#{file.file_id}'),]
                   for file in files
              ]
        
 
    btn.insert(0,[
	InlineKeyboardButton("📥 𝖲𝖾𝗇𝖽 𝖠𝗅𝗅 𝖥𝗂𝗅𝖾𝗌 📥", callback_data=batch_link),
        ])
    btn.insert(1, [
        InlineKeyboardButton("𝖰𝗎𝖺𝗅𝗂𝗍𝗒", callback_data=f"qualities#{key}#{offset}#{req}"),
	InlineKeyboardButton("𝖲𝖾𝖺𝗌𝗈𝗇", callback_data=f"seasons#{key}#{offset}#{req}"),
        InlineKeyboardButton("𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾", callback_data=f"languages#{key}#{offset}#{req}"),
    ])    
    if n_offset== '':
        btn.append(
            [InlineKeyboardButton(text="🚸 𝖭𝗈 𝖬𝗈𝗋𝖾 𝖯𝖺𝗀𝖾𝗌 🚸", callback_data="buttons")]
        )
    elif n_offset == 0:
        btn.append(
            [InlineKeyboardButton("⪻ 𝖡𝖺𝖼𝗄", callback_data=f"quality_search#{qul}#{key}#{offset- int(MAX_BTN)}#{orginal_offset}#{req}"),
             InlineKeyboardButton(f"{math.ceil(offset / int(MAX_BTN)) + 1}/{math.ceil(total / int(MAX_BTN))}", callback_data="pages",),
            ])
    elif offset==0:
        btn.append(
            [InlineKeyboardButton(f"{math.ceil(offset / int(MAX_BTN)) + 1}/{math.ceil(total / int(MAX_BTN))}",callback_data="pages",),
             InlineKeyboardButton("𝖭𝖾𝗑𝗍 ⪼", callback_data=f"quality_search#{qul}#{key}#{n_offset}#{orginal_offset}#{req}"),])
    else:
        btn.append(
            [InlineKeyboardButton("⪻ 𝖡𝖺𝖼𝗄", callback_data=f"quality_search#{qul}#{key}#{offset- int(MAX_BTN)}#{orginal_offset}#{req}"),
             InlineKeyboardButton(f"{math.ceil(offset / int(MAX_BTN)) + 1}/{math.ceil(total / int(MAX_BTN))}", callback_data="pages",),
             InlineKeyboardButton("𝖭𝖾𝗑𝗍 ⪼", callback_data=f"quality_search#{qul}#{key}#{n_offset}#{orginal_offset}#{req}"),])

    btn.append([
        InlineKeyboardButton(text="⪻ 𝖡𝖺𝖼𝗄 𝗍𝗈 𝗆𝖺𝗂𝗇 𝗉𝖺𝗀𝖾", callback_data=f"next_{req}_{key}_{orginal_offset}"),])
    await query.message.edit_text(cap + links + js_ads, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(btn))
    return
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex(r"^languages#"))
async def languages_cb_handler(client: Client, query: CallbackQuery):
    _, key, offset, req = query.data.split("#")
    if int(req) != query.from_user.id:
        return await query.answer(script.ALRT_TXT, show_alert=True)
    btn  = []
    for i in range(0, len(LANGUAGES)-1, 2):
        btn.append([
            InlineKeyboardButton(
                text=LANGUAGES[i].title(),
                callback_data=f"lang_search#{LANGUAGES[i].lower()}#{key}#0#{offset}#{req}"
            ),
            InlineKeyboardButton(
                text=LANGUAGES[i+1].title(),
                callback_data=f"lang_search#{LANGUAGES[i+1].lower()}#{key}#0#{offset}#{req}"
            ),
                    ])
    btn.append([InlineKeyboardButton(text="⪻ 𝖡𝖺𝖼𝗄 𝗍𝗈 𝗆𝖺𝗂𝗇 𝗉𝖺𝗀𝖾", callback_data=f"next_{req}_{key}_{offset}")])
    await query.message.edit_text("<b>𝖨𝗇 𝗐𝗁𝗂𝖼𝗁 𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾 𝖽𝗈 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍, 𝖼𝗁𝗈𝗈𝗌𝖾 𝖿𝗋𝗈𝗆 𝗁𝖾𝗋𝖾 ↓↓</b>", reply_markup=InlineKeyboardMarkup(btn))
    return

@Client.on_callback_query(filters.regex(r"^lang_search#"))
async def lang_search(client: Client, query: CallbackQuery):
    _, lang, key, offset, orginal_offset, req = query.data.split("#")
    lang2 = lang[:3]
    if int(req) != query.from_user.id:
        return await query.answer(script.ALRT_TXT, show_alert=True)	
    offset = int(offset)
    search = BUTTONS.get(key)
    cap = CAP.get(key)
    if not search:
        await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name),show_alert=True)
        return 
    search = search.replace("_", " ")
    files, n_offset, total = await get_search_results(f"{search} {lang}", max_results=int(MAX_BTN), offset=offset)
    files2, n_offset2, total2 = await get_search_results(f"{search} {lang2}", max_results=int(MAX_BTN), offset=offset)
    total += total2
    try:
        n_offset = int(n_offset)
    except:
        try: 
            n_offset = int(n_offset2)
        except : 
            n_offset = 0
    files = [file for file in files if re.search(lang, file.file_name, re.IGNORECASE)]
    if not files:
        files = [file for file in files2 if re.search(lang2, file.file_name, re.IGNORECASE)]
        if not files:
            return await query.answer(f"𝖲𝗈𝗋𝗋𝗒 𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾 {lang.title()} 𝗇𝗈𝗍 𝖿𝗈𝗎𝗇𝖽 𝖿𝗈𝗋 {search}", show_alert=1)

    batch_ids = files
    temp.FILES_ID[f"{query.message.chat.id}-{query.id}"] = batch_ids
    batch_link = f"batchfiles#{query.message.chat.id}#{query.id}#{query.from_user.id}"

    reqnxt = query.from_user.id if query.from_user else 0
    settings = await get_settings(query.message.chat.id)
    group_id = query.message.chat.id
    temp.CHAT[query.from_user.id] = query.message.chat.id
    ads, ads_name, _ = await mdb.get_advirtisment()
    ads_text = ""
    if ads is not None and ads_name is not None:
        ads_url = f"https://t.me/{temp.U_NAME}?start=ads"
        ads_text = f"<a href={ads_url}>{ads_name}</a>"

    js_ads = f"\n━━━━━━━━━━━━━━━━━━\n <b>{ads_text}</b> \n━━━━━━━━━━━━━━━━━━" if ads_text else ""
    #del_msg = f"\n\n<b>⚠️ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀꜰᴛᴇʀ <code>{get_readable_time(DELETE_TIME)}</code> ᴛᴏ ᴀᴠᴏɪᴅ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs</b>" if settings["auto_delete"] else ''
    links = ""
    if settings["link"]:
        btn = []
        for file_num, file in enumerate(files, start=offset+1):
            links += f"""<b>\n\n{file_num}. <a href=https://t.me/{temp.U_NAME}?start=file_{query.message.chat.id}_{file.file_id}>[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}</a></b>"""
    else:
        btn = [[
                InlineKeyboardButton(text=f"🔗 {get_size(file.file_size)}≽ {formate_file_name(file.file_name)}", callback_data=f'cfiles#{reqnxt}#{file.file_id}'),]
                   for file in files
              ]
        

    btn.insert(0,[
	InlineKeyboardButton("📥 𝖲𝖾𝗇𝖽 𝖠𝗅𝗅 𝖥𝗂𝗅𝖾𝗌 📥", callback_data=batch_link),
        ])
    btn.insert(1, [
        InlineKeyboardButton("𝖰𝗎𝖺𝗅𝗂𝗍𝗒", callback_data=f"qualities#{key}#{offset}#{req}"),
	InlineKeyboardButton("𝖲𝖾𝖺𝗌𝗈𝗇", callback_data=f"seasons#{key}#{offset}#{req}"),
        InlineKeyboardButton("𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾", callback_data=f"languages#{key}#{offset}#{req}")
    ])    
    if n_offset== '':
        btn.append(
            [InlineKeyboardButton(text="🚸 𝖭𝗈 𝖬𝗈𝗋𝖾 𝖯𝖺𝗀𝖾𝗌 🚸", callback_data="buttons")]
        )
    elif n_offset == 0:
        btn.append(
            [InlineKeyboardButton("⪻ 𝖡𝖺𝖼𝗄", callback_data=f"lang_search#{lang}#{key}#{offset- int(MAX_BTN)}#{orginal_offset}#{req}"),
             InlineKeyboardButton(f"{math.ceil(offset / int(MAX_BTN)) + 1}/{math.ceil(total / int(MAX_BTN))}", callback_data="pages",),
            ])
    elif offset==0:
        btn.append(
            [InlineKeyboardButton(f"{math.ceil(offset / int(MAX_BTN)) + 1}/{math.ceil(total / int(MAX_BTN))}",callback_data="pages",),
             InlineKeyboardButton("𝖭𝖾𝗑𝗍 ⪼", callback_data=f"lang_search#{lang}#{key}#{n_offset}#{orginal_offset}#{req}"),])
    else:
        btn.append(
            [InlineKeyboardButton("⪻ 𝖡𝖺𝖼𝗄", callback_data=f"lang_search#{lang}#{key}#{offset- int(MAX_BTN)}#{orginal_offset}#{req}"),
             InlineKeyboardButton(f"{math.ceil(offset / int(MAX_BTN)) + 1}/{math.ceil(total / int(MAX_BTN))}", callback_data="pages",),
             InlineKeyboardButton("𝖭𝖾𝗑𝗍 ⪼", callback_data=f"lang_search#{lang}#{key}#{n_offset}#{orginal_offset}#{req}"),])

    btn.append([
        InlineKeyboardButton(text="⪻ 𝖡𝖺𝖼𝗄 𝗍𝗈 𝗆𝖺𝗂𝗇 𝗉𝖺𝗀𝖾", callback_data=f"next_{req}_{key}_{orginal_offset}"),])
    await query.message.edit_text(cap + links + js_ads, disable_web_page_preview=True, parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(btn))
    return
    await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex(r"^spol"))
async def advantage_spoll_choker(bot, query):
    _, id, user = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer(script.ALRT_TXT, show_alert=True)
    movie = await get_poster(id, id=True)
    search = movie.get('title')
    await query.answer('bhai sahab hamare pass nahin Hai')
    files, offset, total_results = await get_search_results(search)
    if files:
        k = (search, files, offset, total_results)
        await auto_filter(bot, query, k)
    else:
        k = await query.message.edit(script.NO_RESULT_TXT)
        await asyncio.sleep(60)
        await k.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

@Client.on_callback_query(filters.regex(r"^cfiles"))
async def pmfile_cb(client, query):
    _, userid, fileid = query.data.split("#")
    if query.from_user.id != userid:
        await query.answer("𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝖸𝗈𝗎𝗋 𝖮𝗐𝗇!!", show_alert=True)
        return

    await query.answer(f"https://telegram.dog/{temp.U_NAME}?start=file_{query.message.chat.id}_{fileid}")
    return

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "close_data":
        try:
            user = query.message.reply_to_message.from_user.id
        except:
            user = query.from_user.id
        if int(user) != 0 and query.from_user.id != int(user):
            return await query.answer(script.ALRT_TXT, show_alert=True)
        await query.answer("𝖳𝗁𝖺𝗇𝗄𝗌 𝖿𝗈𝗋 𝖼𝗅𝗈𝗌𝗂𝗇𝗀")
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type
        if chat_type == enums.ChatType.PRIVATE:
            await query.message.reply_to_message.delete()
            await query.message.delete()
        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)    

    elif query.data.startswith("checksub"):
        ident, file_id , grp_id = query.data.split("#")
        if grp_id != 'None' or grp_id != '':
            chat_id = grp_id
        else:
            chat_id = query.message.chat.id
        if AUTH_CHANNEL and not await is_req_subscribed(client, query):
            await query.answer("𝖨 𝗅𝗂𝗄𝖾 𝗒𝗈𝗎𝗋 𝗌𝗆𝖺𝗋𝗍𝗇𝖾𝗌𝗌 𝖻𝗎𝗍 𝖽𝗈𝗇'𝗍 𝖻𝖾 𝗈𝗏𝖾𝗋 𝗌𝗆𝖺𝗋𝗍 😒\n𝖥𝗂𝗋𝗌𝗍 𝖩𝗈𝗂𝗇 𝖮𝗎𝗋 𝖴𝗉𝖽𝖺𝗍𝖾𝗌 𝖢𝗁𝖺𝗇𝗇𝖾𝗅 😒", show_alert=True)
            return         
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('𝖭𝗈 𝗌𝗎𝖼𝗁 𝖿𝗂𝗅𝖾 𝖾𝗑𝗂𝗌𝗍𝗌 🚫')
        files = files_[0]
        btn = [[
            InlineKeyboardButton('🎗️ 𝖦𝖾𝗍 𝖸𝗈𝗎𝗋 𝖥𝗂𝗅𝖾 🎗️', url=f'https://t.me/{temp.U_NAME}?start=file_{chat_id}_{file_id}')
        ]]
        reply_markup = InlineKeyboardMarkup(btn)
        return await query.message.edit(text=f'<b>𝖳𝗁𝖺𝗇𝗄𝗌 𝖿𝗈𝗋 𝗃𝗈𝗂𝗇𝗂𝗇𝗀 𝗈𝗎𝗋 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 🔥😗\n𝖦𝖾𝗍 𝖸𝗈𝗎𝗋 𝖥𝗂𝗅𝖾 : {files.file_name[:20]}.. 𝖻𝗒 𝖼𝗅𝗂𝖼𝗄𝗂𝗇𝗀 𝗍𝗁𝖾 𝖻𝗎𝗍𝗍𝗈𝗇 𝖻𝖾𝗅𝗈𝗐 ⚡\n\n𝖬𝖺𝗂𝗇𝗍𝖺𝗂𝗇𝖾𝖽 𝖡𝗒 : @GamerBhai02</b>',reply_markup=reply_markup)

    elif query.data == "give_trial":
        user_id = query.from_user.id
        has_free_trial = await db.check_trial_status(user_id)
        if has_free_trial:
            await query.answer("𝖸𝗈𝗎'𝗏𝖾 𝖺𝗅𝗋𝖾𝖺𝖽𝗒 𝖼𝗅𝖺𝗂𝗆𝖾𝖽 𝗒𝗈𝗎𝗋 𝖿𝗋𝖾𝖾 𝗍𝗋𝗂𝖺𝗅 𝗈𝗇𝖼𝖾!\n\n📌 𝖢𝗁𝖾𝖼𝗄𝗈𝗎𝗍 𝗈𝗎𝗋 𝗉𝗅𝖺𝗇𝗌 𝖻𝗒 : /plan", show_alert=True)
            return
        else:            
            await db.give_free_trial(user_id)
            await query.message.edit_text(
                text="𝖢𝗈𝗇𝗀𝗋𝖺𝗍𝗎𝗅𝖺𝗍𝗂𝗈𝗇𝗌🎉 𝖸𝗈𝗎 𝖼𝖺𝗇 𝗎𝗌𝖾 𝖿𝗋𝖾𝖾 𝗍𝗋𝗂𝖺𝗅 𝖿𝗈𝗋 <u>5 𝗆𝗂𝗇𝗎𝗍𝖾𝗌</u> 𝖿𝗋𝗈𝗆 𝗇𝗈𝗐!\n\n𝖭𝗈𝗐 𝖾𝗑𝗉𝖾𝗋𝗂𝖾𝗇𝖼𝖾 𝗈𝗎𝗋 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝗌𝖾𝗋𝗏𝗂𝖼𝖾 𝖿𝗈𝗋 5 𝗆𝗂𝗇𝗎𝗍𝖾𝗌. 𝖳𝗈 𝖻𝗎𝗒 𝗈𝗎𝗋 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝗌𝖾𝗋𝗏𝗂𝖼𝖾 𝖼𝗅𝗂𝖼𝗄 𝗈𝗇 𝖻𝖾𝗅𝗈𝗐 𝖻𝗎𝗍𝗍𝗈𝗇.",
                disable_web_page_preview=True,                  
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💸 𝖢𝗁𝖾𝖼𝗄𝗈𝗎𝗍 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖯𝗅𝖺𝗇𝗌 💸", callback_data='seeplans')]]))
            await client.send_message(LOG_CHANNEL, text=f"#FREE_TRAIL_CLAIMED\n\n👤 𝖴𝗌𝖾𝗋 𝗇𝖺𝗆𝖾 - {query.from_user.mention}\n⚡ 𝖴𝗌𝖾𝗋 𝖨𝖣 - {user_id}", disable_web_page_preview=True)
            return   
	
    elif query.data.startswith("stream"):
        user_id = query.from_user.id
        file_id = query.data.split('#', 1)[1]
        log_msg = await client.send_cached_media(
        chat_id=LOG_CHANNEL,
        file_id=file_id
        )
        fileName = quote_plus(get_name(log_msg))
        online = f"{URL}watch/{log_msg.id}/{fileName}?hash={get_hash(log_msg)}"
        download = f"{URL}{log_msg.id}/{fileName}?hash={get_hash(log_msg)}"
        btn = [[
            InlineKeyboardButton("𝖶𝖺𝗍𝖼𝗁 𝖮𝗇𝗅𝗂𝗇𝖾", url=online),
            InlineKeyboardButton("𝖥𝖺𝗌𝗍 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽", url=download)
        ],[
            InlineKeyboardButton('❌ 𝖢𝗅𝗈𝗌𝖾 ❌', callback_data='close_data')
	]]
        await query.edit_message_reply_markup(
        reply_markup=InlineKeyboardMarkup(btn)
	)
        username = query.from_user.username
        await log_msg.reply_text(
            text=f"#LinkGenrated\n\n𝖨𝖣 : <code>{user_id}</code>\n𝖴𝗌𝖾𝗋 𝗇𝖺𝗆𝖾 : {username}\n\n𝖥𝗂𝗅𝖾 𝗇𝖺𝗆𝖾 : {fileName}",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🚀 𝖥𝖺𝗌𝗍 𝖣𝗈𝗐𝗇𝗅𝗈𝖺𝖽", url=download),
                    InlineKeyboardButton('𝖶𝖺𝗍𝖼𝗁 𝖮𝗇𝗅𝗂𝗇𝖾 🧿', url=online)
                ]
            ])
	)
	
    elif query.data == "buttons":
        await query.answer("𝖭𝗈 𝖬𝗈𝗋𝖾 𝖯𝖺𝗀𝖾𝗌 😊", show_alert=True)

    elif query.data == "pages":
        await query.answer("𝖳𝗁𝗂𝗌 𝗂𝗌 𝗉𝖺𝗀𝖾𝗌 𝖻𝗎𝗍𝗍𝗈𝗇 😅")

    elif query.data.startswith("lang_art"):
        _, lang = query.data.split("#")
        await query.answer(f"𝖸𝗈𝗎 𝗌𝖾𝗅𝖾𝖼𝗍𝖾𝖽 {lang.title()} 𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾⚡️", show_alert=True)
  
    elif query.data == "start":
        buttons = [[
		InlineKeyboardButton('𝖬𝗈𝗏𝗂𝖾 𝖲𝖾𝖺𝗋𝖼𝗁 𝖦𝗋𝗈𝗎𝗉 🎥', url=f'https://t.me/+ZUyhAwBNBsU0YjA9')
	],[
                InlineKeyboardButton("𝖧𝖾𝗅𝗉 ⚙️", callback_data='features'),
                InlineKeyboardButton('𝖠𝖻𝗈𝗎𝗍 💌', callback_data=f'about')
	],[
                InlineKeyboardButton('𝖯𝗋𝖾𝗆𝗂𝗎𝗆 🎫', callback_data='seeplans'),
                InlineKeyboardButton('𝖱𝖾𝖿𝖾𝗋 ⚜️', callback_data="reffff")
        ],[
                InlineKeyboardButton('𝖬𝗈𝗌𝗍 𝖲𝖾𝖺𝗋𝖼𝗁𝖾𝖽 🔍', callback_data="mostsearch"),
                InlineKeyboardButton('𝖳𝗈𝗉 𝖳𝗋𝖾𝗇𝖽𝗂𝗇𝗀 ⚡', callback_data="trending")
        ],[
                InlineKeyboardButton('☆ 𝖠𝖽𝖽 𝖬𝖾 𝗍𝗈 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉 ☆', url=f'http://t.me/{temp.U_NAME}?startgroup=start')
        ]] 
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, get_status(), query.from_user.id),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )      
    elif query.data == "seeplans":
        btn = [[
            InlineKeyboardButton('🍁 𝗖𝗵𝗲𝗰𝗸 𝗔𝗹𝗹 𝗣𝗹𝗮𝗻𝘀 & 𝗣𝗿𝗶𝗰𝗲𝘀 🍁', callback_data='free')
        ],[
            InlineKeyboardButton('• 𝗖𝗹𝗼𝘀𝗲 •', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(btn)
        #m=await query.message.reply_sticker("CAACAgQAAxkBAAEiLZ9l7VMuTY7QHn4edR6ouHUosQQ9gwACFxIAArzT-FOmYU0gLeJu7x4E") 
        #await m.delete()
        await query.message.reply_photo(
            photo=(SUBSCRIPTION),
            caption=script.PREPLANS_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
	)
    elif query.data == "free":
        buttons = [[
            InlineKeyboardButton('☆📸 𝗦𝗲𝗻𝗱 𝗦𝗰𝗿𝗲𝗲𝗻𝘀𝗵𝗼𝘁 📸☆', url=f'https://t.me/GamerBhai02Bot')
        ],[
            InlineKeyboardButton('💎 𝗖𝘂𝘀𝘁𝗼𝗺 𝗣𝗹𝗮𝗻 💎', callback_data='other')
        ],[
            InlineKeyboardButton('• 𝗕𝗮𝗰𝗸 •', callback_data='broze'),
            InlineKeyboardButton('• 𝗖𝗹𝗼𝘀𝗲 •', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)             
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PAYPICS))
        )
        await query.message.edit_text(
            text=script.FREE_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )   
    #jisshu
    elif query.data == "broze":
       buttons = [[
            InlineKeyboardButton('🍁 𝗖𝗵𝗲𝗰𝗸 𝗔𝗹𝗹 𝗣𝗹𝗮𝗻𝘀 & 𝗣𝗿𝗶𝗰𝗲𝘀 🍁', callback_data='free')
        ], [
            InlineKeyboardButton('• 𝗖𝗹𝗼𝘀𝗲 •', callback_data='close_data')
       ]]
       reply_markup = InlineKeyboardMarkup(buttons)
  
       await query.message.edit_media(
         media=InputMediaPhoto(
            media=SUBSCRIPTION, 
            caption=script.PREPLANSS_TXT.format(query.from_user.mention()),
            parse_mode=enums.ParseMode.HTML
         ),
         reply_markup=reply_markup
       )
        
    elif query.data == "other":
        buttons = [[
            InlineKeyboardButton('☎️ 𝗖𝗼𝗻𝘁𝗮𝗰𝘁 𝗢𝘄𝗻𝗲𝗿 𝗧𝗼 𝗞𝗻𝗼𝘄 𝗠𝗼𝗿𝗲', user_id = ADMINS[0])
        ],[
            InlineKeyboardButton('• 𝗕𝗮𝗰𝗸 •', callback_data='free')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PAYPICS))
        )
        await query.message.edit_text(
            text=script.OTHER_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
	)

    elif query.data == "ref_point":
        await query.answer(f'𝖸𝗈𝗎 𝗁𝖺𝗏𝖾: {referdb.get_refer_points(query.from_user.id)} 𝖱𝖾𝖿𝖾𝗋𝗋𝖺𝗅 𝖯𝗈𝗂𝗇𝗍𝗌.', show_alert=True)

    elif query.data == "verifyon":
        await query.answer(f'𝖮𝗇𝗅𝗒 𝗍𝗁𝖾 𝖻𝗈𝗍 𝖺𝖽𝗆𝗂𝗇 𝖼𝖺𝗇 𝖮𝖭 ✓ 𝗈𝗋 𝖮𝖥𝖥 ✗ 𝗍𝗁𝗂𝗌 𝖿𝖾𝖺𝗍𝗎𝗋𝖾.', show_alert=True)
    
    elif query.data == "features":
        buttons = [[
              InlineKeyboardButton('𝖠𝖽𝗆𝗂𝗇 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌', callback_data='admincmd'),
              InlineKeyboardButton('𝖨𝗆𝖺𝗀𝖾 𝗍𝗈 𝖫𝗂𝗇𝗄', callback_data='telegraph'),
              ], [
              InlineKeyboardButton('𝖥-𝖲𝗎𝖻', callback_data='fsub'),
              InlineKeyboardButton('𝖦𝗋𝗈𝗎𝗉 𝖲𝖾𝗍𝗎𝗉', callback_data='earn')
              ], [
              InlineKeyboardButton('⋞ 𝖡𝖺𝖼𝗄 𝗍𝗈 𝖧𝗈𝗆𝖾', callback_data='start')
              ]]
    
        reply_markup = InlineKeyboardMarkup(buttons)
    
        await query.message.edit_media(
            media=InputMediaPhoto(
            media=random.choice(START_IMG),
            caption=script.HELP_TXT,
            parse_mode=enums.ParseMode.HTML 
            ),
            reply_markup=reply_markup
	)
      #  await query.message.edit_text(
      #      text=script.HELP_TXT,
      #      reply_markup=reply_markup,
       #     parse_mode=enums.ParseMode.HTML
       # )   
        
    elif query.data == "admincmd":
    # If the user isn't an admin, return
      if query.from_user.id not in ADMINS:
        return await query.answer('𝖳𝗁𝗂𝗌 𝗂𝗌 𝗇𝗈𝗍 𝖿𝗈𝗋 𝗒𝗈𝗎!!', show_alert=True)
    
      buttons = [[
	      InlineKeyboardButton('⋞ 𝖡𝖺𝖼𝗄', callback_data='features'),
	      InlineKeyboardButton('𝖭𝖾𝗑𝗍 ⪼', callback_data='admincmd2'),
      ]]
      reply_markup = InlineKeyboardMarkup(buttons)
    
      await client.edit_message_media(
          chat_id=query.message.chat.id,
          message_id=query.message.id,
          media=InputMediaAnimation(
            media="https://envs.sh/wra.mp4",
            caption=script.ADMIN_CMD_TXT,
            parse_mode=enums.ParseMode.HTML
          ),
          reply_markup=reply_markup
          )

    elif query.data == "admincmd2":
       buttons = [[
	      InlineKeyboardButton('⋞ ʙᴀᴄᴋ', callback_data='admincmd')]]
       reply_markup = InlineKeyboardMarkup(buttons)
    
       await client.edit_message_media(
          chat_id=query.message.chat.id,
          message_id=query.message.id,
          media=InputMediaAnimation(
            media="https://envs.sh/wra.mp4",
            caption=script.ADMIN_CMD_TXT2,
            parse_mode=enums.ParseMode.HTML
          ),
          reply_markup=reply_markup
      )
	    
    elif query.data == "fsub":
        #add back button
        buttons = [[
            InlineKeyboardButton('⇆ 𝖠𝖽𝖽 𝖬𝖾 𝗍𝗈 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉 ⇆', url=f'http://t.me/{temp.U_NAME}?startgroup=start')],
            [InlineKeyboardButton('⋞ 𝖡𝖺𝖼𝗄', callback_data='features')]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.FSUB_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == 'about':
        await query.message.edit_text(
            script.ABOUT_TEXT.format(query.from_user.mention(),temp.B_LINK),
            reply_markup = InlineKeyboardMarkup(
                [[
			InlineKeyboardButton('‼️ 𝖣𝗂𝗌𝖼𝗅𝖺𝗂𝗆𝖾𝗋 ‼️', callback_data='disclaimer')
		],[
			InlineKeyboardButton('𝖲𝗈𝗎𝗋𝖼𝖾 𝖢𝗈𝖽𝖾', callback_data='Source')
                ],[
                        InlineKeyboardButton('𝖬𝗒 𝖣𝖾𝗏𝗌 😎',callback_data='mydevelopers')
		],[
			InlineKeyboardButton('⋞ 𝖧𝗈𝗆𝖾', callback_data='start')]]
                ),
            disable_web_page_preview = True
	)
    elif query.data == "mydevelopers":
        await query.answer("𝖬𝖾𝖾𝗍 𝗍𝗁𝖾 𝗆𝗂𝗇𝖽 𝖻𝖾𝗁𝗂𝗇𝖽 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍:\n\n👨‍💻 @GamerBhai02\n\n\n❤️ A big thank you for making me this awesome!", show_alert=True)
 
    elif query.data == "Source":
        buttons = [[
            InlineKeyboardButton('𝖱𝖾𝗉𝗈', url='https://github.com/GamerBhai02/AllMoviesLinkBot')
        ],[
            InlineKeyboardButton('⋞ 𝖡𝖺𝖼𝗄', callback_data='about'),
            InlineKeyboardButton('• 𝖢𝗅𝗈𝗌𝖾 •', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SOURCE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
	)
	
    elif query.data == "disclaimer":
            btn = [[
                    InlineKeyboardButton("📲 𝖢𝗈𝗇𝗍𝖺𝖼𝗍 𝖮𝗐𝗇𝖾𝗋 ", user_id = ADMINS[0])
               ],[
                    InlineKeyboardButton("⇋ 𝖡𝖺𝖼𝗄 ⇋", callback_data="about")
                  ]]
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.DISCLAIMER_TXT),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML 
	    )
    elif query.data == "earn":
       buttons = [[
	      InlineKeyboardButton('⇆ 𝖠𝖽𝖽 𝖬𝖾 𝗍𝗈 𝖸𝗈𝗎𝗋 𝖦𝗋𝗈𝗎𝗉 ⇆', url=f'http://t.me/{temp.U_NAME}?startgroup=start')
       ],[
              InlineKeyboardButton('⋞ 𝖧𝗈𝗆𝖾', callback_data='features'),
              InlineKeyboardButton('𝖲𝗎𝗉𝗉𝗈𝗋𝗍', url=f'https://t.me/GamerBhai02Bot'),
       ]]
       reply_markup = InlineKeyboardMarkup(buttons)
       await client.edit_message_media(
          chat_id=query.message.chat.id,
          message_id=query.message.id,
          media=InputMediaAnimation(
            media="https://envs.sh/wra.mp4",
            caption=script.GROUP_TEXT.format(temp.B_LINK),
            parse_mode=enums.ParseMode.HTML
        ),
        reply_markup=reply_markup
    )
   
    elif query.data == "telegraph":
        buttons = [[
            InlineKeyboardButton('⋞ 𝖡𝖺𝖼𝗄', callback_data='features')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)  
        await query.message.edit_text(
            text=script.TELE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "font":
        buttons = [[
            InlineKeyboardButton('⋞ 𝖡𝖺𝖼𝗄', callback_data='features')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons) 
        await query.message.edit_text(
            text=script.FONT_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
	)
  

    elif query.data == "all_files_delete":
        files = await Media.count_documents()
        await query.answer('𝖣𝖾𝗅𝖾𝗍𝗂𝗇𝗀...')
        await Media.collection.drop()
        await query.message.edit_text(f"𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 {files} 𝖿𝗂𝗅𝖾𝗌")
        
    elif query.data.startswith("killfilesak"):
        ident, keyword = query.data.split("#")
        await query.message.edit_text(f"<b>𝖥𝖾𝗍𝖼𝗁𝗂𝗇𝗀 𝖿𝗂𝗅𝖾𝗌 𝖿𝗈𝗋 𝗒𝗈𝗎𝗋 𝗊𝗎𝖾𝗋𝗒 {keyword} 𝗈𝗇 𝖣𝖡...\n\n𝖯𝗅𝖾𝖺𝗌𝖾 𝗐𝖺𝗂𝗍...</b>")
        files, total = await get_bad_files(keyword)
        await query.message.edit_text(f"<b>𝖥𝗈𝗎𝗇𝖽 {total} 𝖿𝗂𝗅𝖾𝗌 𝖿𝗈𝗋 𝗒𝗈𝗎𝗋 𝗊𝗎𝖾𝗋𝗒 {keyword}!!</b>")
        deleted = 0
        async with lock:
            try:
                for file in files:
                    file_ids = file.file_id
                    file_name = file.file_name
                    result = await Media.collection.delete_one({
                        '_id': file_ids,
                    })
                    if result.deleted_count:
                        print(f'𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 {file_name} 𝖿𝗋𝗈𝗆 𝖣𝖡.')
                    deleted += 1
                    if deleted % 20 == 0:
                        await query.message.edit_text(f"<b>𝖯𝗋𝗈𝖼𝖾𝗌𝗌 𝗌𝗍𝖺𝗋𝗍𝖾𝖽 𝖿𝗈𝗋 𝖽𝖾𝗅𝖾𝗍𝗂𝗇𝗀 𝖿𝗂𝗅𝖾𝗌 𝖿𝗋𝗈𝗆 𝖣𝖡. 𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 {str(deleted)} 𝖿𝗂𝗅𝖾𝗌 𝖿𝗋𝗈𝗆 𝖣𝖡 𝖿𝗈𝗋 𝗒𝗈𝗎𝗋 𝗊𝗎𝖾𝗋𝗒 {keyword} !\n\n𝖯𝗅𝖾𝖺𝗌𝖾 𝗐𝖺𝗂𝗍...</b>")
            except Exception as e:
                print(e)
                await query.message.edit_text(f'𝖤𝗋𝗋𝗈𝗋: {e}')
            else:
                await query.message.edit_text(f"<b>𝖯𝗋𝗈𝖼𝖾𝗌𝗌 𝖢𝗈𝗆𝗉𝗅𝖾𝗍𝖾𝖽 𝖿𝗈𝗋 𝖿𝗂𝗅𝖾 𝖽𝖾𝗅𝖾𝗍𝗂𝗈𝗇!\n\n𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖽𝖾𝗅𝖾𝗍𝖾𝖽 {str(deleted)} 𝖿𝗂𝗅𝖾𝗌 𝖿𝗋𝗈𝗆 𝖣𝖡 𝖿𝗈𝗋 𝗒𝗈𝗎𝗋 𝗊𝗎𝖾𝗋𝗒 {keyword}.</b>")
          
    elif query.data.startswith("reset_grp_data"):
        grp_id = query.message.chat.id
        btn = [[
            InlineKeyboardButton('☕️ 𝖢𝗅𝗈𝗌𝖾 ☕️', callback_data='close_data')
        ]]           
        reply_markup=InlineKeyboardMarkup(btn)
        await save_group_settings(grp_id, 'shortner', SHORTENER_WEBSITE)
        await save_group_settings(grp_id, 'api', SHORTENER_API)
        await save_group_settings(grp_id, 'shortner_two', SHORTENER_WEBSITE2)
        await save_group_settings(grp_id, 'api_two', SHORTENER_API2)
        await save_group_settings(grp_id, 'shortner_three', SHORTENER_WEBSITE3)
        await save_group_settings(grp_id, 'api_three', SHORTENER_API3)
        await save_group_settings(grp_id, 'verify_time', TWO_VERIFY_GAP)
        await save_group_settings(grp_id, 'third_verify_time', THREE_VERIFY_GAP)
        await save_group_settings(grp_id, 'tutorial', TUTORIAL)
        await save_group_settings(grp_id, 'tutorial_2', TUTORIAL_2)
        await save_group_settings(grp_id, 'tutorial_3', TUTORIAL_3)
        await save_group_settings(grp_id, 'template', IMDB_TEMPLATE)
        await save_group_settings(grp_id, 'caption', FILE_CAPTION)
        await save_group_settings(grp_id, 'log', LOG_VR_CHANNEL)
        await query.answer('𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖱𝖾𝗌𝖾𝗍...')
        await query.message.edit_text("<b>𝖲𝗎𝖼𝖼𝖾𝗌𝗌𝖿𝗎𝗅𝗅𝗒 𝖱𝖾𝗌𝖾𝗍 𝖦𝗋𝗈𝗎𝗉 𝖲𝖾𝗍𝗍𝗂𝗇𝗀𝗌...\n\n𝖭𝗈𝗐 𝗌𝖾𝗇𝖽 /details 𝖺𝗀𝖺𝗂𝗇</b>", reply_markup=reply_markup)

    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        userid = query.from_user.id if query.from_user else None
        if not await is_check_admin(client, int(grp_id), userid):
            await query.answer(script.ALRT_TXT, show_alert=True)
            return
        if status == "True":
            await save_group_settings(int(grp_id), set_type, False)
            await query.answer("𝖮𝖿𝖿 ❌")
        else:
            await save_group_settings(int(grp_id), set_type, True)
            await query.answer("𝖮𝗇 ✅")
        settings = await get_settings(int(grp_id))      
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
            reply_markup = InlineKeyboardMarkup(buttons)
            d = await query.message.edit_reply_markup(reply_markup)
            await asyncio.sleep(300)
            await d.delete()
        else:
            await query.message.edit_text("<b>𝖲𝗈𝗆𝖾𝗍𝗁𝗂𝗇𝗀 𝗐𝖾𝗇𝗍 𝗐𝗋𝗈𝗇𝗀</b>")
            
    elif query.data.startswith("show_options"):
        ident, user_id, msg_id = query.data.split("#")
        chnl_id = query.message.chat.id
        userid = query.from_user.id
        buttons = [[
            InlineKeyboardButton("✅️ 𝖠𝖼𝖼𝖾𝗉𝗍 𝗍𝗁𝗂𝗌 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 ✅️", callback_data=f"accept#{user_id}#{msg_id}")
        ],[
            InlineKeyboardButton("🚫 𝖱𝖾𝗃𝖾𝖼𝗍 𝗍𝗁𝗂𝗌 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 🚫", callback_data=f"reject#{user_id}#{msg_id}")
        ]]
        try:
            st = await client.get_chat_member(chnl_id, userid)
            if (st.status == enums.ChatMemberStatus.ADMINISTRATOR) or (st.status == enums.ChatMemberStatus.OWNER):
                await query.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
            elif st.status == enums.ChatMemberStatus.MEMBER:
                await query.answer(script.ALRT_TXT, show_alert=True)
        except pyrogram.errors.exceptions.bad_request_400.UserNotParticipant:
            await query.answer("⚠️ 𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺 𝗆𝖾𝗆𝖻𝖾𝗋 𝗈𝖿 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗇𝗇𝖾𝗅, 𝖿𝗂𝗋𝗌𝗍 𝗃𝗈𝗂𝗇", show_alert=True)

    elif query.data.startswith("reject"):
        ident, user_id, msg_id = query.data.split("#")
        chnl_id = query.message.chat.id
        userid = query.from_user.id
        buttons = [[
            InlineKeyboardButton("✗ 𝖱𝖾𝗃𝖾𝖼𝗍 ✗", callback_data=f"rj_alert#{user_id}")
        ]]
        btn = [[
            InlineKeyboardButton("♻️ 𝖵𝗂𝖾𝗐 𝗌𝗍𝖺𝗍𝗎𝗌 ♻️", url=f"{query.message.link}")
        ]]
        st = await client.get_chat_member(chnl_id, userid)
        if (st.status == enums.ChatMemberStatus.ADMINISTRATOR) or (st.status == enums.ChatMemberStatus.OWNER):
            user = await client.get_users(user_id)
            request = query.message.text
            await query.answer("𝖬𝗌𝗀 𝗌𝖾𝗇𝗍 𝗍𝗈 𝗋𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝗋")
            await query.message.edit_text(f"<s>{request}</s>")
            await query.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
            try:
                await client.send_message(chat_id=user_id, text="<b>𝖲𝗈𝗋𝗋𝗒 𝗒𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗂𝗌 𝗋𝖾𝗃𝖾𝖼𝗍𝖾𝖽 😶</b>", reply_markup=InlineKeyboardMarkup(btn))
            except UserIsBlocked:
                await client.send_message(SUPPORT_GROUP, text=f"<b>💥 𝖧𝖾𝗅𝗅𝗈 {user.mention},\n\n𝖲𝗈𝗋𝗋𝗒 𝗒𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗂𝗌 𝗋𝖾𝗃𝖾𝖼𝗍𝖾𝖽 😶</b>", reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=int(msg_id))
        else:
            await query.answer(script.ALRT_TXT, show_alert=True)

    elif query.data.startswith("accept"):
        ident, user_id, msg_id = query.data.split("#")
        chnl_id = query.message.chat.id
        userid = query.from_user.id
        buttons = [[
            InlineKeyboardButton("😊 𝖠𝗅𝗋𝖾𝖺𝖽𝗒 𝖠𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 😊", callback_data=f"already_available#{user_id}#{msg_id}")
        ],[
            InlineKeyboardButton("‼️ 𝖭𝗈𝗍 𝖠𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 ‼️", callback_data=f"not_available#{user_id}#{msg_id}")
        ],[
            InlineKeyboardButton("🥵 𝖳𝖾𝗅𝗅 𝗆𝖾 𝗒𝖾𝖺𝗋 / 𝗅𝖺𝗇𝗀𝗎𝖺𝗀𝖾 🥵", callback_data=f"year#{user_id}#{msg_id}")
        ],[
            InlineKeyboardButton("🙃 𝖴𝗉𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝗂𝗇 1 𝗁𝗈𝗎𝗋 🙃", callback_data=f"upload_in#{user_id}#{msg_id}")
        ],[
            InlineKeyboardButton("☇ 𝖴𝗉𝗅𝗈𝖺𝖽𝖾𝖽 ☇", callback_data=f"uploaded#{user_id}#{msg_id}")
        ]]
        try:
            st = await client.get_chat_member(chnl_id, userid)
            if (st.status == enums.ChatMemberStatus.ADMINISTRATOR) or (st.status == enums.ChatMemberStatus.OWNER):
                await query.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
            elif st.status == enums.ChatMemberStatus.MEMBER:
                await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name),show_alert=True)
        except pyrogram.errors.exceptions.bad_request_400.UserNotParticipant:
            await query.answer("⚠️ 𝖸𝗈𝗎 𝖺𝗋𝖾 𝗇𝗈𝗍 𝖺 𝗆𝖾𝗆𝖻𝖾𝗋 𝗈𝖿 𝗍𝗁𝗂𝗌 𝖼𝗁𝖺𝗇𝗇𝖾𝗅, 𝖿𝗂𝗋𝗌𝗍 𝗃𝗈𝗂𝗇", show_alert=True)

    elif query.data.startswith("not_available"):
        ident, user_id, msg_id = query.data.split("#")
        chnl_id = query.message.chat.id
        userid = query.from_user.id
        buttons = [[
            InlineKeyboardButton("🚫 𝖭𝗈𝗍 𝖠𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 🚫", callback_data=f"na_alert#{user_id}")
        ]]
        btn = [[
            InlineKeyboardButton("♻️ 𝖵𝗂𝖾𝗐 𝗌𝗍𝖺𝗍𝗎𝗌 ♻️", url=f"{query.message.link}")
        ]]
        st = await client.get_chat_member(chnl_id, userid)
        if (st.status == enums.ChatMemberStatus.ADMINISTRATOR) or (st.status == enums.ChatMemberStatus.OWNER):
            user = await client.get_users(user_id)
            request = query.message.text
            await query.answer("𝖬𝗌𝗀 𝗌𝖾𝗇𝗍 𝗍𝗈 𝗋𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝗋")
            await query.message.edit_text(f"<s>{request}</s>")
            await query.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
            try:
                await client.send_message(chat_id=user_id, text="<b>𝖲𝗈𝗋𝗋𝗒 𝗒𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗂𝗌 𝗇𝗈𝗍 𝖺𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 😢</b>", reply_markup=InlineKeyboardMarkup(btn))
            except UserIsBlocked:
                await client.send_message(SUPPORT_GROUP, text=f"<b>💥 𝖧𝖾𝗅𝗅𝗈 {user.mention},\n\n𝖲𝗈𝗋𝗋𝗒 𝗒𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗂𝗌 𝗇𝗈𝗍 𝖺𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 😢</b>", reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=int(msg_id))
        else:
            await query.answer(script.ALRT_TXT, show_alert=True)

    elif query.data.startswith("uploaded"):
        ident, user_id, msg_id = query.data.split("#")
        chnl_id = query.message.chat.id
        userid = query.from_user.id
        buttons = [[
            InlineKeyboardButton("🙂 𝖴𝗉𝗅𝗈𝖺𝖽𝖾𝖽 🙂", callback_data=f"ul_alert#{user_id}")
        ]]
        btn = [[
            InlineKeyboardButton("♻️ 𝖵𝗂𝖾𝗐 𝗌𝗍𝖺𝗍𝗎𝗌 ♻️", url=f"{query.message.link}")
        ]]
        st = await client.get_chat_member(chnl_id, userid)
        if (st.status == enums.ChatMemberStatus.ADMINISTRATOR) or (st.status == enums.ChatMemberStatus.OWNER):
            user = await client.get_users(user_id)
            request = query.message.text
            await query.answer("𝖬𝗌𝗀 𝗌𝖾𝗇𝗍 𝗍𝗈 𝗋𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝗋")
            await query.message.edit_text(f"<s>{request}</s>")
            await query.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
            try:
                await client.send_message(chat_id=user_id, text="<b>𝖸𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗂𝗌 𝗎𝗉𝗅𝗈𝖺𝖽𝖾𝖽 ☺️</b>", reply_markup=InlineKeyboardMarkup(btn))
            except UserIsBlocked:
                await client.send_message(SUPPORT_GROUP, text=f"<b>💥 𝖧𝖾𝗅𝗅𝗈 {user.mention},\n\n𝖸𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗂𝗌 𝗎𝗉𝗅𝗈𝖺𝖽𝖾𝖽 ☺️</b>", reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=int(msg_id))
        else:
            await query.answer(script.ALRT_TXT, show_alert=True)

    elif query.data.startswith("already_available"):
        ident, user_id, msg_id = query.data.split("#")
        chnl_id = query.message.chat.id
        userid = query.from_user.id
        buttons = [[
            InlineKeyboardButton("🫤 𝖠𝗅𝗋𝖾𝖺𝖽𝗒 𝖠𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 🫤", callback_data=f"aa_alert#{user_id}")
        ]]
        btn = [[
            InlineKeyboardButton("♻️ 𝖵𝗂𝖾𝗐 𝗌𝗍𝖺𝗍𝗎𝗌 ♻️", url=f"{query.message.link}")
        ]]
        st = await client.get_chat_member(chnl_id, userid)
        if (st.status == enums.ChatMemberStatus.ADMINISTRATOR) or (st.status == enums.ChatMemberStatus.OWNER):
            user = await client.get_users(user_id)
            request = query.message.text
            await query.answer("𝖬𝗌𝗀 𝗌𝖾𝗇𝗍 𝗍𝗈 𝗋𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝗋")
            await query.message.edit_text(f"<s>{request}</s>")
            await query.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
            try:
                await client.send_message(chat_id=user_id, text="<b>𝖸𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗂𝗌 𝖺𝗅𝗋𝖾𝖺𝖽𝗒 𝖺𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 😋</b>", reply_markup=InlineKeyboardMarkup(btn))
            except UserIsBlocked:
                await client.send_message(SUPPORT_GROUP, text=f"<b>💥 𝖧𝖾𝗅𝗅𝗈 {user.mention},\n\n𝖸𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗂𝗌 𝖺𝗅𝗋𝖾𝖺𝖽𝗒 𝖺𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 😋</b>", reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=int(msg_id))
        else:
            await query.answer(script.ALRT_TXT, show_alert=True)

    elif query.data.startswith("upload_in"):
        ident, user_id, msg_id = query.data.split("#")
        chnl_id = query.message.chat.id
        userid = query.from_user.id
        buttons = [[
            InlineKeyboardButton("😌 𝖴𝗉𝗅𝗈𝖺𝖽𝗂𝗇𝗀 𝗂𝗇 1 𝗁𝗈𝗎𝗋 😌", callback_data=f"upload_alert#{user_id}")
        ]]
        btn = [[
            InlineKeyboardButton("♻️ 𝖵𝗂𝖾𝗐 𝗌𝗍𝖺𝗍𝗎𝗌 ♻️", url=f"{query.message.link}")
        ]]
        st = await client.get_chat_member(chnl_id, userid)
        if (st.status == enums.ChatMemberStatus.ADMINISTRATOR) or (st.status == enums.ChatMemberStatus.OWNER):
            user = await client.get_users(user_id)
            request = query.message.text
            await query.answer("𝖬𝗌𝗀 𝗌𝖾𝗇𝗍 𝗍𝗈 𝗋𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝗋")
            await query.message.edit_text(f"<s>{request}</s>")
            await query.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
            try:
                await client.send_message(chat_id=user_id, text="<b>𝖸𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗐𝗂𝗅𝗅 𝖻𝖾 𝗎𝗉𝗅𝗈𝖺𝖽𝖾𝖽 𝗂𝗇 1 𝗁𝗈𝗎𝗋 😁</b>", reply_markup=InlineKeyboardMarkup(btn))
            except UserIsBlocked:
                await client.send_message(SUPPORT_GROUP, text=f"<b>💥 𝖧𝖾𝗅𝗅𝗈 {user.mention},\n\n𝖸𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗐𝗂𝗅𝗅 𝖻𝖾 𝗎𝗉𝗅𝗈𝖺𝖽𝖾𝖽 𝗂𝗇 1 𝗁𝗈𝗎𝗋 😁</b>", reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=int(msg_id))
        else:
            await query.answer(script.ALRT_TXT, show_alert=True)

    elif query.data.startswith("year"):
        ident, user_id, msg_id = query.data.split("#")
        chnl_id = query.message.chat.id
        userid = query.from_user.id
        buttons = [[
            InlineKeyboardButton("⚠️ 𝖳𝖾𝗅𝗅 𝗆𝖾 𝗒𝖾𝖺𝗋 / 𝗅𝖺𝗇𝗀𝗎𝖺𝗀𝖾 ⚠️", callback_data=f"yrs_alert#{user_id}")
        ]]
        btn = [[
            InlineKeyboardButton("♻️ 𝖵𝗂𝖾𝗐 𝗌𝗍𝖺𝗍𝗎𝗌 ♻️", url=f"{query.message.link}")
        ]]
        st = await client.get_chat_member(chnl_id, userid)
        if (st.status == enums.ChatMemberStatus.ADMINISTRATOR) or (st.status == enums.ChatMemberStatus.OWNER):
            user = await client.get_users(user_id)
            request = query.message.text
            await query.answer("𝖬𝗌𝗀 𝗌𝖾𝗇𝗍 𝗍𝗈 𝗋𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝗋")
            await query.message.edit_text(f"<s>{request}</s>")
            await query.message.edit_reply_markup(InlineKeyboardMarkup(buttons))
            try:
                await client.send_message(chat_id=user_id, text="<b>𝖡𝗋𝗈 𝗉𝗅𝖾𝖺𝗌𝖾 𝗍𝖾𝗅𝗅 𝗆𝖾 𝗒𝖾𝖺𝗋 𝖺𝗇𝖽 𝗅𝖺𝗇𝗀𝗎𝖺𝗀𝖾, 𝗍𝗁𝖾𝗇 𝗂 𝗐𝗂𝗅𝗅 𝗎𝗉𝗅𝗈𝖺𝖽 😬</b>", reply_markup=InlineKeyboardMarkup(btn))
            except UserIsBlocked:
                await client.send_message(SUPPORT_GROUP, text=f"<b>💥 𝖧𝖾𝗅𝗅𝗈 {user.mention},\n\n𝖡𝗋𝗈 𝗉𝗅𝖾𝖺𝗌𝖾 𝗍𝖾𝗅𝗅 𝗆𝖾 𝗒𝖾𝖺𝗋 𝖺𝗇𝖽 𝗅𝖺𝗇𝗀𝗎𝖺𝗀𝖾, 𝗍𝗁𝖾𝗇 𝗂 𝗐𝗂𝗅𝗅 𝗎𝗉𝗅𝗈𝖺𝖽 😬</b>", reply_markup=InlineKeyboardMarkup(btn), reply_to_message_id=int(msg_id))
        else:
            await query.answer(script.ALRT_TXT, show_alert=True)

    elif query.data.startswith("rj_alert"):
        ident, user_id = query.data.split("#")
        userid = query.from_user.id
        if str(userid) in user_id:
            await query.answer("𝖲𝗈𝗋𝗋𝗒 𝗒𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗂𝗌 𝗋𝖾𝗃𝖾𝖼𝗍𝖾𝖽", show_alert=True)
        else:
            await query.answer(script.ALRT_TXT, show_alert=True)

    elif query.data.startswith("na_alert"):
        ident, user_id = query.data.split("#")
        userid = query.from_user.id
        if str(userid) in user_id:
            await query.answer("𝖲𝗈𝗋𝗋𝗒 𝗒𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗂𝗌 𝖭𝗈𝗍 𝖠𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾", show_alert=True)
        else:
            await query.answer(script.ALRT_TXT, show_alert=True)

    elif query.data.startswith("ul_alert"):
        ident, user_id = query.data.split("#")
        userid = query.from_user.id
        if str(userid) in user_id:
            await query.answer("𝖸𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗂𝗌 𝖴𝗉𝗅𝗈𝖺𝖽𝖾𝖽", show_alert=True)
        else:
            await query.answer(script.ALRT_TXT, show_alert=True)

    elif query.data.startswith("aa_alert"):
        ident, user_id = query.data.split("#")
        userid = query.from_user.id
        if str(userid) in user_id:
            await query.answer("𝖸𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗂𝗌 𝖠𝗅𝗋𝖾𝖺𝖽𝗒 𝖠𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾", show_alert=True)
        else:
            await query.answer(script.ALRT_TXT, show_alert=True)

    elif query.data.startswith("upload_alert"):
        ident, user_id = query.data.split("#")
        userid = query.from_user.id
        if str(userid) in user_id:
            await query.answer("𝖸𝗈𝗎𝗋 𝗋𝖾𝗊𝗎𝖾𝗌𝗍 𝗐𝗂𝗅𝗅 𝖻𝖾 𝗎𝗉𝗅𝗈𝖺𝖽𝖾𝖽 𝗐𝗂𝗍𝗁𝗂𝗇 1 𝗁𝗈𝗎𝗋 😁", show_alert=True)
        else:
            await query.answer(script.ALRT_TXT, show_alert=True)

    elif query.data.startswith("yrs_alert"):
        ident, user_id = query.data.split("#")
        userid = query.from_user.id
        if str(userid) in user_id:
            await query.answer("𝖡𝗋𝗈 𝗉𝗅𝖾𝖺𝗌𝖾 𝗍𝖾𝗅𝗅 𝗆𝖾 𝗒𝖾𝖺𝗋 𝖺𝗇𝖽 𝗅𝖺𝗇𝗀𝗎𝖺𝗀𝖾, 𝗍𝗁𝖾𝗇 𝗂 𝗐𝗂𝗅𝗅 𝗎𝗉𝗅𝗈𝖺𝖽 😬", show_alert=True)
        else:
            await query.answer(script.ALRT_TXT, show_alert=True)

    elif query.data.startswith("batchfiles"):
        ident, group_id, message_id, user = query.data.split("#")
        group_id = int(group_id)
        message_id = int(message_id)
        user = int(user)
        if user != query.from_user.id:
            await query.answer(script.ALRT_TXT, show_alert=True)
            return
        link = f"https://telegram.me/{temp.U_NAME}?start=allfiles_{group_id}-{message_id}"
        await query.answer(url=link)
        return
	    
async def ai_spell_check(wrong_name):
    async def search_movie(wrong_name):
        search_results = imdb.search_movie(wrong_name)
        movie_list = [movie['title'] for movie in search_results]
        return movie_list
    movie_list = await search_movie(wrong_name)
    if not movie_list:
        return
    for _ in range(5):
        closest_match = process.extractOne(wrong_name, movie_list)
        if not closest_match or closest_match[1] <= 80:
            return 
        movie = closest_match[0]
        files, offset, total_results = await get_search_results(movie)
        if files:
            return movie
        movie_list.remove(movie)
    return
async def auto_filter(client, msg, spoll=False , pm_mode = False):
    if not spoll:
        message = msg
        search = message.text
        chat_id = message.chat.id
        settings = await get_settings(chat_id , pm_mode=pm_mode)
        searching_msg = await msg.reply_text(f'🔎 𝖲𝖾𝖺𝗋𝖼𝗁𝗂𝗇𝗀 {search}')
        files, offset, total_results = await get_search_results(search)
        await searching_msg.delete()
        if not files:
            if settings["spell_check"]:
                ai_sts = await msg.reply_text(f'𝖢𝗁𝖾𝖼𝗄𝗂𝗇𝗀 𝗒𝗈𝗎𝗋 𝗌𝗉𝖾𝗅𝗅𝗂𝗇𝗀...')
                is_misspelled = await ai_spell_check(search)
                if is_misspelled:
              #      await ai_sts.edit(f'<b><i>ʏᴏᴜʀ ꜱᴘᴇʟʟɪɴɢ ɪꜱ ᴡʀᴏɴɢ ɴᴏᴡ ᴅᴇᴠɪʟ ꜱᴇᴀʀᴄʜɪɴɢ ᴡɪᴛʜ ᴄᴏʀʀᴇᴄᴛ ꜱᴘᴇʟʟɪɴɢ - <code>{is_misspelled}</code></i></b>')
                    await asyncio.sleep(2)
                    msg.text = is_misspelled
                    await ai_sts.delete()
                    return await auto_filter(client, msg)
                await ai_sts.delete()
                return await advantage_spell_chok(msg)
            return
    else:
        settings = await get_settings(msg.message.chat.id , pm_mode=pm_mode)
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
    req = message.from_user.id if message.from_user else 0
    key = f"{message.chat.id}-{message.id}"
    batch_ids = files
    temp.FILES_ID[f"{message.chat.id}-{message.id}"] = batch_ids
    batch_link = f"batchfiles#{message.chat.id}#{message.id}#{message.from_user.id}"
    temp.CHAT[message.from_user.id] = message.chat.id
    settings = await get_settings(message.chat.id , pm_mode=pm_mode)
    del_msg = f"\n\n<b>⚠️ 𝖳𝗁𝗂𝗌 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗐𝗂𝗅𝗅 𝖠𝗎𝗍𝗈 𝖣𝖾𝗅𝖾𝗍𝖾 𝖺𝖿𝗍𝖾𝗋 <code>{get_readable_time(DELETE_TIME)}</code> 𝗍𝗈 𝖺𝗏𝗈𝗂𝖽 𝖼𝗈𝗉𝗒𝗋𝗂𝗀𝗁𝗍 𝗂𝗌𝗌𝗎𝖾𝗌</b>" if settings["auto_delete"] else ''
    links = ""
    if settings["link"]:
        btn = []
        for file_num, file in enumerate(files, start=1):
            links += f"""<b>\n\n{file_num}. <a href=https://t.me/{temp.U_NAME}?start={"pm_mode_" if pm_mode else ''}file_{ADMINS[0] if pm_mode else message.chat.id}_{file.file_id}>[{get_size(file.file_size)}] {formate_file_name(file.file_name)}</a></b>"""
    else:
        btn = [[InlineKeyboardButton(text=f"🔗 {get_size(file.file_size)}≽ {formate_file_name(file.file_name)}", url=f'https://telegram.dog/{temp.U_NAME}?start=file_{message.chat.id}_{file.file_id}'),]
               for file in files
              ]
    if offset != "":
        if total_results >= MAX_BTN:
            btn.insert(0,[
                InlineKeyboardButton("📥 𝖲𝖾𝗇𝖽 𝖠𝗅𝗅 𝖥𝗂𝗅𝖾𝗌 📥", callback_data=batch_link),
            ])
            btn.insert(1, [
                InlineKeyboardButton("𝖰𝗎𝖺𝗅𝗂𝗍𝗒", callback_data=f"qualities#{key}#{offset}#{req}"),
                InlineKeyboardButton("𝖲𝖾𝖺𝗌𝗈𝗇", callback_data=f"seasons#{key}#{offset}#{req}"),
                InlineKeyboardButton("𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾", callback_data=f"languages#{key}#{offset}#{req}")
            ])            
        else:
            btn.insert(0,[
                InlineKeyboardButton("📥 𝖲𝖾𝗇𝖽 𝖠𝗅𝗅 𝖥𝗂𝗅𝖾𝗌 📥", callback_data=batch_link),
                InlineKeyboardButton("𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾", callback_data=f"languages#{key}#{offset}#{req}")
            ])
            btn.insert(1,[
                InlineKeyboardButton("🚸 𝖭𝗈 𝖬𝗈𝗋𝖾 𝖯𝖺𝗀𝖾𝗌 🚸", user_id=ADMINS[0])
            ])
    else:
        btn.insert(0,[
            InlineKeyboardButton("📥 𝖲𝖾𝗇𝖽 𝖠𝗅𝗅 𝖥𝗂𝗅𝖾𝗌 📥", callback_data=batch_link),
            ])

        btn.insert(1,[
            InlineKeyboardButton("🚸 𝖭𝗈 𝖬𝗈𝗋𝖾 𝖯𝖺𝗀𝖾𝗌 🚸", user_id=ADMINS[0])
        ])
                             
    if spoll:
        m = await msg.message.edit(f"<b><code>{search}</code> 𝗂𝗌 𝖿𝗈𝗎𝗇𝖽 𝗉𝗅𝖾𝖺𝗌𝖾 𝗐𝖺𝗂𝗍 𝖿𝗈𝗋 𝖿𝗂𝗅𝖾𝗌 📫</b>")
        await asyncio.sleep(1.2)
        await m.delete()
    if offset != "":
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        btn.append(
            [InlineKeyboardButton(text=f"1/{math.ceil(int(total_results) / int(MAX_BTN))}", callback_data="pages"),
             InlineKeyboardButton(text="𝖭𝖾𝗑𝗍 ⪼", callback_data=f"next_{req}_{key}_{offset}")]
        )
        key = f"{message.chat.id}-{message.id}"
        BUTTONS[key] = search
        req = message.from_user.id if message.from_user else 0
        try:
            offset = int(offset) 
        except:
            offset = int(MAX_BTN)
        
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    TEMPLATE = settings['template']
    if imdb:
        cap = TEMPLATE.format(
            query=search,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title=imdb['localized_title'],
            kind=imdb['kind'],
            imdb_id=imdb["imdb_id"],
            cast=imdb["cast"],
            runtime=imdb["runtime"],
            countries=imdb["countries"],
            certificates=imdb["certificates"],
            languages=imdb["languages"],
            director=imdb["director"],
            writer=imdb["writer"],
            producer=imdb["producer"],
            composer=imdb["composer"],
            cinematographer=imdb["cinematographer"],
            music_team=imdb["music_team"],
            distributors=imdb["distributors"],
            release_date=imdb['release_date'],
            year=imdb['year'],
            genres=imdb['genres'],
            poster=imdb['poster'],
            plot=imdb['plot'],
            rating=imdb['rating'],
            url=imdb['url'],
            **locals()
        )
    else:
        cap = f"<b>📂 𝖧𝖾𝗋𝖾 𝗂 𝖿𝗈𝗎𝗇𝖽 𝗒𝗈𝗎𝗋 𝗌𝖾𝖺𝗋𝖼𝗁 {search}</b>"

    ads, ads_name, _ = await mdb.get_advirtisment()
    ads_text = ""
    if ads is not None and ads_name is not None:
        ads_url = f"https://t.me/{temp.U_NAME}?start=ads"
        ads_text = f"<a href={ads_url}>{ads_name}</a>"

    js_ads = f"\n━━━━━━━━━━━━━━━━━━\n <b>{ads_text}</b> \n━━━━━━━━━━━━━━━━━━" if ads_text else ""
  #  del_msg = f"\n\n<b>⚠️ 𝖳𝗁𝗂𝗌 𝗆𝖾𝗌𝗌𝖺𝗀𝖾 𝗐𝗂𝗅𝗅 𝖠𝗎𝗍𝗈 𝖣𝖾𝗅𝖾𝗍𝖾 𝖺𝖿𝗍𝖾𝗋 <code>{get_readable_time(DELETE_TIME)}</code> ᴛᴏ ᴀᴠᴏɪᴅ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs</b>" if settings["auto_delete"] else ''
    CAP[key] = cap
    if imdb and imdb.get('poster'):
        try:
            if settings['auto_delete']:
                k = await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024] + links + del_msg, parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(btn))
              #  await delSticker(st)
                await asyncio.sleep(DELETE_TIME)
                await k.delete()
                try:
                    await message.delete()
                except:
                    pass
            else:
                await message.reply_photo(photo=imdb.get('poster'), caption=cap[:1024] + links + js_ads, reply_markup=InlineKeyboardMarkup(btn))                    
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            if settings["auto_delete"]:
                k = await message.reply_photo(photo=poster, caption=cap[:1024] + links + js_ads, parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(btn))
                #await delSticker(st)
                await asyncio.sleep(DELETE_TIME)
                await k.delete()
                try:
                    await message.delete()
                except:
                    pass
            else:
                await message.reply_photo(photo=poster, caption=cap[:1024] + links + js_ads, parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(btn))
        except Exception as e:
            print(e)
            if settings["auto_delete"]:
                #await delSticker(st)
                try:
                    k = await message.reply_text(cap + links + js_ads, parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
                except Exception as e:
                    print("error", e)
                await asyncio.sleep(DELETE_TIME)
                await k.delete()
                try:
                    await message.delete()
                except:
                    pass
            else:
                await message.reply_text(cap + links + js_ads, parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
    else:
        k = await message.reply_text(text=cap + links + js_ads, disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(btn), parse_mode=enums.ParseMode.HTML, reply_to_message_id=message.id)
       # await delSticker(st)
        if settings['auto_delete']:
          #  await delSticker(st)
            await asyncio.sleep(DELETE_TIME)
            await k.delete()
            try:
                await message.delete()
            except:
                pass
    return            
async def advantage_spell_chok(message):
    mv_id = message.id
    search = message.text
    chat_id = message.chat.id
    settings = await get_settings(chat_id)
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", message.text, flags=re.IGNORECASE)
    query = query.strip() + " movie"
    try:
        movies = await get_poster(search, bulk=True)
    except:
        k = await message.reply(script.I_CUDNT.format(message.from_user.mention))
        await asyncio.sleep(60)
        await k.delete()
        try:
            await message.delete()
        except:
            pass
        return
    if not movies:
        google = search.replace(" ", "+")
        button = [[
            InlineKeyboardButton("🔍 𝖢𝗁𝖾𝖼𝗄 𝗌𝗉𝖾𝗅𝗅𝗂𝗇𝗀 𝗈𝗇 𝗀𝗈𝗈𝗀𝗅𝖾 🔍", url=f"https://www.google.com/search?q={google}")
        ]]
        k = await message.reply_text(text=script.I_CUDNT.format(search), reply_markup=InlineKeyboardMarkup(button))
        await asyncio.sleep(120)
        await k.delete()
        try:
            await message.delete()
        except:
            pass
        return
    user = message.from_user.id if message.from_user else 0
    buttons = [[
        InlineKeyboardButton(text=movie.get('title'), callback_data=f"spol#{movie.movieID}#{user}")
    ]
        for movie in movies
    ]
    buttons.append(
        [InlineKeyboardButton(text="🚫 𝖢𝗅𝗈𝗌𝖾 🚫", callback_data='close_data')]
    )
    d = await message.reply_text(text=script.CUDNT_FND.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(buttons), reply_to_message_id=message.id)
    await asyncio.sleep(120)
    await d.delete()
    try:
        await message.delete()
    except:
        pass
