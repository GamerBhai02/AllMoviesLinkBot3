import os
class script(object):
    START_TXT = """<b>𝖧𝖾𝗒 {}, {}\n\n𝖨 𝖠𝗆 𝖺 𝖯𝗈𝗐𝖾𝗋𝖿𝗎𝗅 𝖠𝗎𝗍𝗈 𝖥𝗂𝗅𝗍𝖾𝗋 𝖡𝗈𝗍. 𝖸𝗈𝗎 𝖼𝖺𝗇 𝗎𝗌𝖾 𝗆𝖾 𝗂𝗇 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉 𝗂 𝗐𝗂𝗅𝗅 𝗀𝗂𝗏𝖾 𝗆𝗈𝗏𝗂𝖾𝗌 𝗈𝗋 𝗌𝖾𝗋𝗂𝖾𝗌 𝗂𝗇 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉 𝖺𝗇𝖽 𝗁𝖾𝗋𝖾 𝗍𝗈𝗈 !! 😍\n<blockquote>🌿 𝖬𝖺𝗂𝗇𝗍𝖺𝗂𝗇𝖾𝖽 𝖡𝗒: <a href="https://t.me/GamerBhai02">𝖠𝖻𝗎 𝖳𝖺𝗅𝗁𝖺 𝖠𝗇𝗌𝖺𝗋𝗂�</a></blockquote></b>"""
    
    HELP_TXT = """<b>𝖢𝗅𝗂𝖼𝗄 𝗈𝗇 𝗍𝗁𝖾 𝖻𝗎𝗍𝗍𝗈𝗇𝗌 𝖻𝖾𝗅𝗈𝗐 𝗍𝗈 𝗀𝖾𝗍 𝖽𝗈𝖼𝗎𝗆𝖾𝗇𝗍𝖺𝗍𝗂𝗈𝗇 𝖺𝖻𝗈𝗎𝗍 𝗌𝗉𝖾𝖼𝗂𝖿𝗂𝖼 𝗆𝗈𝖽𝗎𝗅𝖾𝗌..</b>"""
    
    TELE_TXT = """<b>/telegraph - 𝖲𝖾𝗇𝖽 𝗆𝖾 𝗉𝗂𝖼𝗍𝗎𝗋𝖾 𝗈𝗋 𝗏𝗂𝖽𝖾𝗈 𝗎𝗇𝖽𝖾𝗋 (5𝗆𝖻)

𝖭𝗈𝗍𝖾 - 𝗍𝗁𝗂𝗌 𝖼𝗈𝗆𝗆𝖺𝗇𝖽 𝗐𝗈𝗋𝗄 𝗂𝗇 𝖻𝗈𝗍𝗁 𝗀𝗋𝗈𝗎𝗉𝗌 𝖺𝗇𝖽 𝖻𝗈𝗍 𝗉𝗆</b>"""
    FSUB_TXT = """<b>• 𝖠𝖽𝖽 𝗆𝖾 𝗍𝗈 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉 𝖺𝗇𝖽 𝗆𝖺𝗄𝖾 𝗆𝖾 𝖺𝗇 𝖺𝖽𝗆𝗂𝗇 😗
• 𝖬𝖺𝗄𝖾 𝗆𝖾 𝖺𝗇 𝖺𝖽𝗆𝗂𝗇 𝗂𝗇 𝗒𝗈𝗎𝗋 𝗍𝖺𝗋𝗀𝖾𝗍 𝖿𝗈𝗋𝖼𝖾 𝗌𝗎𝖻𝗌𝖼𝗋𝗂𝖻𝖾 𝖼𝗁𝖺𝗇𝗇𝖾𝗅 𝗈𝗋 𝗀𝗋𝗈𝗎𝗉 😉
• 𝖲𝖾𝗇𝖽 /fsub 𝗒𝗈𝗎𝗋_𝗍𝖺𝗋𝗀𝖾𝗍_𝖼𝗁𝖺𝗍_𝗂𝖽
𝖤𝗑: <code>/fsub -100xxxxxx</code>

𝖭𝗈𝗐 𝗂𝗍'𝗌 𝖽𝗈𝗇𝖾. 𝖨 𝗐𝗂𝗅𝗅 𝖼𝗈𝗆𝗉𝖾𝗅 𝗒𝗈𝗎𝗋 𝗎𝗌𝖾𝗋𝗌 𝗍𝗈 𝗃𝗈𝗂𝗇 𝗒𝗈𝗎𝗋 𝖼𝗁𝖺𝗇𝗇𝖾𝗅/𝗀𝗋𝗈𝗎𝗉, 𝖺𝗇𝖽 𝗂 𝗐𝗂𝗅𝗅 𝗇𝗈𝗍 𝗉𝗋𝗈𝗏𝗂𝖽𝖾 𝖺𝗇𝗒 𝖿𝗂𝗅𝖾𝗌 𝗎𝗇𝗍𝗂𝗅 𝗒𝗈𝗎𝗋 𝗎𝗌𝖾𝗋𝗌 𝗃𝗈𝗂𝗇 𝗒𝗈𝗎𝗋 𝗍𝖺𝗋𝗀𝖾𝗍 𝖼𝗁𝖺𝗇𝗇𝖾𝗅.

𝖳𝗈 𝖽𝗂𝗌𝖺𝖻𝗅𝖾 𝖿𝗌𝗎𝖻 𝗂𝗇 𝗒𝗈𝗎𝗋 𝗀𝗋𝗈𝗎𝗉, 𝗌𝗂𝗆𝗉𝗅𝗒 𝗌𝖾𝗇𝖽 <code>/del_fsub</code>

𝖳𝗈 𝖼𝗁𝖾𝖼𝗄 𝗂𝖿 𝖿𝗌𝗎𝖻 𝗂𝗌 𝖼𝗈𝗇𝗇𝖾𝖼𝗍𝖾𝖽 𝗈𝗋 𝗇𝗈𝗍, 𝗎𝗌𝖾 <code>/show_fsub</code></b>"""

    FORCESUB_TEXT="""<b>
𝖨𝗇 𝗈𝗋𝖽𝖾𝗋 𝗍𝗈 𝗀𝖾𝗍 𝗍𝗁𝖾 𝖿𝗂𝗅𝖾 𝗋𝖾𝗊𝗎𝖾𝗌𝗍𝖾𝖽 𝖻𝗒 𝗒𝗈𝗎.

𝖸𝗈𝗎 𝗐𝗂𝗅𝗅 𝗁𝖺𝗏𝖾 𝗍𝗈 𝗃𝗈𝗂𝗇 𝗈𝗎𝗋 𝗈𝖿𝖿𝗂𝖼𝗂𝖺𝗅 𝖼𝗁𝖺𝗇𝗇𝖾𝗅.

𝖥𝗂𝗋𝗌𝗍, 𝖼𝗅𝗂𝖼𝗄 𝗈𝗇 𝗍𝗁𝖾 "𝖩𝗈𝗂𝗇 𝖴𝗉𝖽𝖺𝗍𝖾 𝖢𝗁𝖺𝗇𝗇𝖾𝗅" 𝖻𝗎𝗍𝗍𝗈𝗇, 𝗍𝗁𝖾𝗇, 𝖼𝗅𝗂𝖼𝗄 𝗈𝗇 𝗍𝗁𝖾 "𝖱𝖾𝗊𝗎𝖾𝗌𝗍 𝖳𝗈 𝖩𝗈𝗂𝗇" 𝖻𝗎𝗍𝗍𝗈𝗇.

𝖠𝗍𝖾𝗋 𝗍𝗁𝖺𝗍, 𝗍𝗋𝗒 𝖺𝖼𝖼𝖾𝗌𝗌𝗂𝗇𝗀 𝗍𝗁𝖺𝗍 𝗆𝗈𝗏𝗂𝖾 𝗍𝗁𝖾𝗇, 𝖼𝗅𝗂𝖼𝗄 𝗈𝗇 𝗍𝗁𝖾 "𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇" 𝖻𝗎𝗍𝗍𝗈𝗇.
    </b>"""
    
    TTS_TXT="""
<b>• 𝖲𝖾𝗇𝖽 /tts 𝗍𝗈 𝗎𝗌𝖾 𝗍𝗁𝗂𝗌 𝖿𝖾𝖺𝗍𝗎𝗋𝖾</b>"""

    DISCLAIMER_TXT = """
<b>𝖳𝗁𝗂𝗌 𝗂𝗌 𝖺𝗇 𝗈𝗉𝖾𝗇-𝗌𝗈𝗎𝗋𝖼𝖾 𝗉𝗋𝗈𝗃𝖾𝖼𝗍.

𝖠𝗅𝗅 𝗍𝗁𝖾 𝖿𝗂𝗅𝖾𝗌 𝗂𝗇 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍 𝖺𝗋𝖾 𝖿𝗋𝖾𝖾𝗅𝗒 𝖺𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝗈𝗇 𝗍𝗁𝖾 𝗂𝗇𝗍𝖾𝗋𝗇𝖾𝗍 𝗈𝗋 𝗉𝗈𝗌𝗍𝖾𝖽 𝖻𝗒 𝗌𝗈𝗆𝖾𝖻𝗈𝖽𝗒 𝖾𝗅𝗌𝖾. 𝖩𝗎𝗌𝗍 𝖿𝗈𝗋 𝖾𝖺𝗌𝗒 𝗌𝖾𝖺𝗋𝖼𝗁𝗂𝗇𝗀 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍 𝗂𝗌 𝗂𝗇𝖽𝖾𝗑𝗂𝗇𝗀 𝖿𝗂𝗅𝖾𝗌 𝗐𝗁𝗂𝖼𝗁 𝖺𝗋𝖾 𝖺𝗅𝗋𝖾𝖺𝖽𝗒 𝗎𝗉𝗅𝗈𝖺𝖽𝖾𝖽 𝗈𝗇 𝗍𝖾𝗅𝖾𝗀𝗋𝖺𝗆. 𝖶𝖾 𝗋𝖾𝗌𝗉𝖾𝖼𝗍 𝖺𝗅𝗅 𝗍𝗁𝖾 𝖼𝗈𝗉𝗒𝗋𝗂𝗀𝗁𝗍 𝗅𝖺𝗐𝗌 𝖺𝗇𝖽 𝗐𝗈𝗋𝗄𝗌 𝗂𝗇 𝖼𝗈𝗆𝗉𝗅𝗂𝖺𝗇𝖼𝖾 𝗐𝗂𝗍𝗁 𝖣𝖬𝖢𝖠 𝖺𝗇𝖽 𝖤𝖴𝖢𝖣. 𝖨𝖿 𝖺𝗇𝗒𝗍𝗁𝗂𝗇𝗀 𝗂𝗌 𝖺𝗀𝖺𝗂𝗇𝗌𝗍 𝗅𝖺𝗐, 𝗉𝗅𝖾𝖺𝗌𝖾 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 𝗆𝖾 𝗌𝗈 𝗍𝗁𝖺𝗍 𝗂𝗍 𝖼𝖺𝗇 𝖻𝖾 𝗋𝖾𝗆𝗈𝗏𝖾𝖽 𝖺𝗌𝖺𝗉. 𝖨𝗍 𝗂𝗌 𝖿𝗈𝗋𝖻𝗂𝖽𝖽𝖾𝗇 𝗍𝗈 𝖽𝗈𝗐𝗇𝗅𝗈𝖺𝖽, 𝗌𝗍𝗋𝖾𝖺𝗆, 𝗋𝖾𝗉𝗋𝗈𝖽𝗎𝖼𝖾, 𝗌𝗁𝖺𝗋𝖾 𝗈𝗋 𝖼𝗈𝗇𝗌𝗎𝗆𝖾 𝖼𝗈𝗇𝗍𝖾𝗇𝗍 𝗐𝗂𝗍𝗁𝗈𝗎𝗍 𝖾𝗑𝗉𝗅𝗂𝖼𝗂𝗍 𝗉𝖾𝗋𝗆𝗂𝗌𝗌𝗂𝗈𝗇 𝖿𝗋𝗈𝗆 𝗍𝗁𝖾 𝖼𝗈𝗇𝗍𝖾𝗇𝗍 𝖼𝗋𝖾𝖺𝗍𝗈𝗋 𝗈𝗋 𝗅𝖾𝗀𝖺𝗅 𝖼𝗈𝗉𝗒𝗋𝗂𝗀𝗁𝗍 𝗁𝗈𝗅𝖽𝖾𝗋. 𝖨𝖿 𝗒𝗈𝗎 𝖻𝖾𝗅𝗂𝖾𝗏𝖾 𝗍𝗁𝗂𝗌 𝖻𝗈𝗍 𝗂𝗌 𝗏𝗂𝗈𝗅𝖺𝗍𝗂𝗇𝗀 𝗒𝗈𝗎𝗋 𝗂𝗇𝗍𝖾𝗅𝗅𝖾𝖼𝗍𝗎𝖺𝗅 𝗉𝗋𝗈𝗉𝖾𝗋𝗍𝗒, 𝖼𝗈𝗇𝗍𝖺𝖼𝗍 𝗍𝗁𝖾 𝗋𝖾𝗌𝗉𝖾𝖼𝗍𝗂𝗏𝖾 𝖼𝗁𝖺𝗇𝗇𝖾𝗅𝗌 𝖿𝗈𝗋 𝗋𝖾𝗆𝗈𝗏𝖺𝗅. 𝖳𝗁𝖾 𝖻𝗈𝗍 𝖽𝗈𝖾𝗌 𝗇𝗈𝗍 𝗈𝗐𝗇 𝖺𝗇𝗒 𝗈𝖿 𝗍𝗁𝖾𝗌𝖾 𝖼𝗈𝗇𝗍𝖾𝗇𝗍𝗌, 𝗂𝗍 𝗈𝗇𝗅𝗒 𝗂𝗇𝖽𝖾𝗑𝖾𝗌 𝗍𝗁𝖾 𝖿𝗂𝗅𝖾𝗌 𝖿𝗋𝗈𝗆 𝗍𝖾𝗅𝖾𝗀𝗋𝖺𝗆. 

<blockquote>🌿 𝖬𝖺𝗂𝗇𝗍𝖺𝗂𝗇𝖾𝖽 𝖡𝗒: <a href='https://t.me/GamerBhai02'>𝖠𝖻𝗎 𝖳𝖺𝗅𝗁𝖺 𝖠𝗇𝗌𝖺𝗋𝗂</a></b></blockquote>"""
    

    ABOUT_TEXT = """<blockquote><b>‣ 𝖬𝗒 𝖭𝖺𝗆𝖾: 𝖠𝗅𝗅 𝖬𝗈𝗏𝗂𝖾𝗌 𝖫𝗂𝗇𝗄 𝖡𝗈𝗍\n‣ 𝖢𝗋𝖾𝖺𝗍𝗈𝗋: <a href='https://t.me/GamerBhai02'>𝖬𝗋. 𝖠𝖻𝗎 𝖳𝖺𝗅𝗁𝖺</a>\n‣ 𝖫𝗂𝖻𝗋𝖺𝗋𝗒: 𝖯𝗒𝗋𝗈𝗀𝗋𝖺𝗆\n‣ 𝖫𝖺𝗇𝗀𝗎𝖺𝗀𝖾: 𝖯𝗒𝗍𝗁𝗈𝗇\n‣ 𝖣𝖺𝗍𝖺𝖻𝖺𝗌𝖾: 𝖬𝗈𝗇𝗀𝗈𝖣𝖡\n‣ 𝖧𝗈𝗌𝗍𝗂𝗇𝗀: 𝖯𝗋𝗂𝗏𝖺𝗍𝖾\n‣ 𝖡𝗎𝗂𝗅𝖽 𝖲𝗍𝖺𝗍𝗎𝗌: ᴠ5.0.1 [𝖲𝗍𝖺𝖻𝗅𝖾]</b></blockquote>"""    
    
    SUPPORT_GRP_MOVIE_TEXT = '''<b>𝖧𝖾𝗒 {}

𝖨 𝖿𝗈𝗎𝗇𝖽 {} 𝗋𝖾𝗌𝗎𝗅𝗍𝗌 🎁,
𝖡𝗎𝗍 𝗂 𝖼𝖺𝗇'𝗍 𝗌𝖾𝗇𝖽 𝗁𝖾𝗋𝖾 🤞🏻
𝖯𝗅𝖾𝖺𝗌𝖾 𝗃𝗈𝗂𝗇 𝗈𝗎𝗋 𝗌𝖾𝖺𝗋𝖼𝗁 𝗀𝗋𝗈𝗎𝗉 𝗍𝗈 𝗀𝖾𝗍 ✨</b>'''

    CHANNELS = """
<u>ᴏᴜʀ ᴀʟʟ ɢʀᴏᴜᴘꜱ ᴀɴᴅ ᴄʜᴀɴɴᴇʟꜱ</u> 

▫ ᴀʟʟ ʟᴀᴛᴇꜱᴛ ᴀɴᴅ ᴏʟᴅ ᴍᴏᴠɪᴇꜱ & ꜱᴇʀɪᴇꜱ.
▫ ᴀʟʟ ʟᴀɴɢᴜᴀɢᴇꜱ ᴍᴏᴠɪᴇꜱ ᴀᴠᴀɪʟᴀʙʟᴇ.
▫ ᴀʟᴡᴀʏꜱ ᴀᴅᴍɪɴ ꜱᴜᴘᴘᴏʀᴛ.
▫ 𝟸𝟺x𝟽 ꜱᴇʀᴠɪᴄᴇꜱ ᴀᴠᴀɪʟᴀʙʟᴇ."""

    LOGO = """

BOT WORKING PROPERLY 🔥"""
    
    RESTART_TXT = """
<b>Bᴏᴛ Rᴇsᴛᴀʀᴛᴇᴅ !
> {} 
📅 Dᴀᴛᴇ : <code>{}</code>
⏰ Tɪᴍᴇ : <code>{}</code>
🌐 Tɪᴍᴇᴢᴏɴᴇ : <code>Asia/Kolkata</code>
🛠️ Bᴜɪʟᴅ Sᴛᴀᴛᴜs: <code>v4.2 [ Sᴛᴀʙʟᴇ ]</code>

Bʏ @JISSHU_BOTS</b>"""
        
    
    STATUS_TXT = """<b><u>🗃 ᴅᴀᴛᴀʙᴀsᴇ 1 🗃</u>

» ᴛᴏᴛᴀʟ ᴜsᴇʀs - <code>{}</code>
» ᴛᴏᴛᴀʟ ɢʀᴏᴜᴘs - <code>{}</code>
» ᴜsᴇᴅ sᴛᴏʀᴀɢᴇ - <code>{} / {}</code>

<u>🗳 ᴅᴀᴛᴀʙᴀsᴇ 2 🗳</u></b>

» ᴛᴏᴛᴀʟ ꜰɪʟᴇs - <code>{}</code>
» ᴜsᴇᴅ sᴛᴏʀᴀɢᴇ - <code>{} / {}</code>

<u>🤖 ʙᴏᴛ ᴅᴇᴛᴀɪʟs 🤖</u>

» ᴜᴘᴛɪᴍᴇ - <code>{}</code>
» ʀᴀᴍ - <code>{}%</code>
» ᴄᴘᴜ - <code>{}%</code></b>"""

    NEW_USER_TXT = """<b>#New_User {}

≈ ɪᴅ:- <code>{}</code>
≈ ɴᴀᴍᴇ:- {}</b>"""

    NEW_GROUP_TXT = """#New_Group {}

Group name - {}
Id - <code>{}</code>
Group username - @{}
Group link - {}
Total members - <code>{}</code>
User - {}"""

    REQUEST_TXT = """<b>📜 ᴜꜱᴇʀ - {}
📇 ɪᴅ - <code>{}</code>

🎁 ʀᴇǫᴜᴇꜱᴛ ᴍꜱɢ - <code>{}</code></b>"""  
   
    IMDB_TEMPLATE_TXT = """
<b>ʜᴇʏ {message.from_user.mention}, ʜᴇʀᴇ ɪꜱ ᴛʜᴇ ʀᴇꜱᴜʟᴛꜱ ꜰᴏʀ ʏᴏᴜʀ ǫᴜᴇʀʏ {search}.

🍿 Title: {title}
🎃 Genres: {genres}
📆 Year: {release_date}
⭐ Rating: {rating} / 10</b>
"""

    FILE_CAPTION = """<b>{file_name}\n\n𝖩𝗈𝗂𝗇➥ 「<a href="https://t.me/Jisshu_Originals">𝙅𝙞𝙨𝙨𝙝𝙪 𝙊𝙧𝙞𝙜𝙞𝙣𝙖𝙡𝙨</a>」</b>"""
    

    ALRT_TXT = """ᴊᴀʟᴅɪ ʏᴇʜᴀ sᴇ ʜᴀᴛᴏ !"""

    OLD_ALRT_TXT = """ʏᴏᴜ ᴀʀᴇ ᴜsɪɴɢ ᴍʏ ᴏʟᴅ ᴍᴇssᴀɢᴇs..sᴇɴᴅ ᴀ ɴᴇᴡ ʀᴇǫᴜᴇsᴛ.."""

    NO_RESULT_TXT = """<b>ᴛʜɪs ᴍᴇssᴀɢᴇ ɪs ɴᴏᴛ ʀᴇʟᴇᴀsᴇᴅ ᴏʀ ᴀᴅᴅᴇᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ 🙄</b>"""
    
    I_CUDNT = """🤧 𝗛𝗲𝗹𝗹𝗼 {}

𝗜 𝗰𝗼𝘂𝗹𝗱𝗻'𝘁 𝗳𝗶𝗻𝗱 𝗮𝗻𝘆 𝗺𝗼𝘃𝗶𝗲 𝗼𝗿 𝘀𝗲𝗿𝗶𝗲𝘀 𝗶𝗻 𝘁𝗵𝗮𝘁 𝗻𝗮𝗺𝗲.. 😐"""

    I_CUD_NT = """😑 𝗛𝗲𝗹𝗹𝗼 {}

𝗜 𝗰𝗼𝘂𝗹𝗱𝗻'𝘁 𝗳𝗶𝗻𝗱 𝗮𝗻𝘆𝘁𝗵𝗶𝗻𝗴 𝗿𝗲𝗹𝗮𝘁𝗲𝗱 𝘁𝗼 𝘁𝗵𝗮𝘁 😞... 𝗰𝗵𝗲𝗰𝗸 𝘆𝗼𝘂𝗿 𝘀𝗽𝗲𝗹𝗹𝗶𝗻𝗴."""
    
    CUDNT_FND = """🤧 𝗛𝗲𝗹𝗹𝗼 {}

𝗜 𝗰𝗼𝘂𝗹𝗱𝗻'𝘁 𝗳𝗶𝗻𝗱 𝗮𝗻𝘆𝘁𝗵𝗶𝗻𝗴 𝗿𝗲𝗹𝗮𝘁𝗲𝗱 𝘁𝗼 𝘁𝗵𝗮𝘁 𝗱𝗶𝗱 𝘆𝗼𝘂 𝗺𝗲𝗮𝗻 𝗮𝗻𝘆 𝗼𝗻𝗲 𝗼𝗳 𝘁𝗵𝗲𝘀𝗲 ?? 👇"""
    
    FONT_TXT= """<b>ʏᴏᴜ ᴄᴀɴ ᴜsᴇ ᴛʜɪs ᴍᴏᴅᴇ ᴛᴏ ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ꜰᴏɴᴛs sᴛʏʟᴇ, ᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ʟɪᴋᴇ ᴛʜɪs ꜰᴏʀᴍᴀᴛ

<code>/font hi how are you</code></b>"""
    
    PLAN_TEXT = """<b>ᴡᴇ ᴀʀᴇ ᴘʀᴏᴠɪᴅɪɴɢ ᴘʀᴇᴍɪᴜᴍ ᴀᴛ ᴛʜᴇ ʟᴏᴡᴇsᴛ ᴘʀɪᴄᴇs:
    
1 ʀᴜᴘᴇᴇ ᴘᴇʀ ᴅᴀʏ 👻
29 ʀᴜᴘᴇᴇs ғᴏʀ ᴏɴᴇ ᴍᴏɴᴛʜ 😚
55 ʀᴜᴘᴇᴇs ғᴏʀ ᴛᴡᴏ ᴍᴏɴᴛʜs 😗

ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ʙᴜʏɪɴɢ ↡↡↡
</b>"""
    
    VERIFICATION_TEXT = """<b>👋 ʜᴇʏ {} {},

📌 <u>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪғɪᴇᴅ ᴛᴏᴅᴀʏ, ᴘʟᴇᴀꜱᴇ ᴄʟɪᴄᴋ ᴏɴ ᴠᴇʀɪғʏ & ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇꜱꜱ ғᴏʀ ᴛɪʟʟ ɴᴇxᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ</u>

#ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ:- 1/3 ✓

ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴅɪʀᴇᴄᴛ ғɪʟᴇꜱ ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴꜱ ᴛʜᴇɴ ʙᴜʏ ʙᴏᴛ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ 😊

💶 sᴇɴᴅ /plan ᴛᴏ ʙᴜʏ sᴜʙsᴄʀɪᴘᴛɪᴏɴ</b>"""

    VERIFY_COMPLETE_TEXT = """<b>👋 ʜᴇʏ {},

ʏᴏᴜ ʜᴀᴠᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴛʜᴇ 1st ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ✓

ɴᴏᴡ ʏᴏᴜ ʜᴀᴠᴇ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ꜰᴏʀ ɴᴇxᴛ <code>{}</code></b>"""

    SECOND_VERIFICATION_TEXT = """<b>👋 ʜᴇʏ {} {},

📌 <u>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪꜰɪᴇᴅ, ᴛᴀᴘ ᴏɴ ᴛʜᴇ ᴠᴇʀɪꜰʏ ʟɪɴᴋ ᴀɴᴅ ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ꜰᴏʀ ᴛɪʟʟ ɴᴇxᴛ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ</u>

#ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ:- 2/3

ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴅɪʀᴇᴄᴛ ғɪʟᴇꜱ ᴡɪᴛʜᴏᴜᴛ ᴀɴʏ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴꜱ ᴛʜᴇɴ ʙᴜʏ ʙᴏᴛ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ 😊

💶 sᴇɴᴅ /plan ᴛᴏ ʙᴜʏ sᴜʙsᴄʀɪᴘᴛɪᴏɴ</b>"""

    SECOND_VERIFY_COMPLETE_TEXT = """<b>👋 ʜᴇʏ {},

ʏᴏᴜ ʜᴀᴠᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴛʜᴇ 2nd ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ✓

ɴᴏᴡ ʏᴏᴜ ʜᴀᴠᴇ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ꜰᴏʀ ɴᴇxᴛ <code>{}</code></b>"""

    THIRDT_VERIFICATION_TEXT = """<b>👋 ʜᴇʏ {},
    
📌 <u>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴠᴇʀɪꜰɪᴇᴅ ᴛᴏᴅᴀʏ, ᴛᴀᴘ ᴏɴ ᴛʜᴇ ᴠᴇʀɪꜰʏ ʟɪɴᴋ & ɢᴇᴛ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ꜰᴏʀ ɴᴇxᴛ ꜰᴜʟʟ ᴅᴀʏ.</u>

#ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ:- 3/3

ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴅɪʀᴇᴄᴛ ꜰɪʟᴇs ᴛʜᴇɴ ʏᴏᴜ ᴄᴀɴ ᴛᴀᴋᴇ ᴘʀᴇᴍɪᴜᴍ sᴇʀᴠɪᴄᴇ (ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴠᴇʀɪꜰʏ)</b>"""

    THIRDT_VERIFY_COMPLETE_TEXT= """<b>👋 ʜᴇʏ {},
    
ʏᴏᴜ ʜᴀᴠᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ᴛʜᴇ 3rd ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ✓

ɴᴏᴡ ʏᴏᴜ ʜᴀᴠᴇ ᴜɴʟɪᴍɪᴛᴇᴅ ᴀᴄᴄᴇss ꜰᴏʀ ɴᴇxᴛ ꜰᴜʟʟ ᴅᴀʏ </b>"""

    VERIFIED_LOG_TEXT = """<b><u>☄ ᴜsᴇʀ ᴠᴇʀɪꜰɪᴇᴅ sᴜᴄᴄᴇssꜰᴜʟʟʏ ☄</u>

⚡️ ɴᴀᴍᴇ:- {} [ <code>{}</code> ] 
📆 ᴅᴀᴛᴇ:- <code>{} </code></b>

#verified_{}_completed"""


    MOVIES_UPDATE_TXT = """<b>#𝑵𝒆𝒘_𝑭𝒊𝒍𝒆_𝑨𝒅𝒅𝒆𝒅 ✅
**🍿 Title:** {title}
**🎃 Genres:** {genres}
**📆 Year:** {year}
**⭐ Rating:** {rating} / 10
</b>"""

    PREPLANS_TXT = """<b>👋 ʜᴇʏ {},

<blockquote>🎁 ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇ ʙᴇɴɪꜰɪᴛꜱ:</blockquote>

❏ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋꜱ
❏ ɢᴇᴛ ᴅɪʀᴇᴄᴛ ғɪʟᴇs   
❏ ᴀᴅ-ғʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ 
❏ ʜɪɢʜ-sᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ                         
❏ ᴍᴜʟᴛɪ-ᴘʟᴀʏᴇʀ sᴛʀᴇᴀᴍɪɴɢ ʟɪɴᴋs                           
❏ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs ᴀɴᴅ sᴇʀɪᴇs                                                                        
❏ ꜰᴜʟʟ ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ                              
❏ ʀᴇǫᴜᴇsᴛ ᴡɪʟʟ ʙᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ 𝟷ʜ [ ɪꜰ ᴀᴠᴀɪʟᴀʙʟᴇ ]

⛽️ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ: /myplan
</b>"""    

    PREPLANSS_TXT = """<b>👋 ʜᴇʏ {}
    
<blockquote>🎁 ᴘʀᴇᴍɪᴜᴍ ғᴇᴀᴛᴜʀᴇ ʙᴇɴɪꜰɪᴛꜱ:</blockquote>

❏ ɴᴏ ɴᴇᴇᴅ ᴛᴏ ᴏᴘᴇɴ ʟɪɴᴋꜱ
❏ ɢᴇᴛ ᴅɪʀᴇᴄᴛ ғɪʟᴇs   
❏ ᴀᴅ-ғʀᴇᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ 
❏ ʜɪɢʜ-sᴘᴇᴇᴅ ᴅᴏᴡɴʟᴏᴀᴅ ʟɪɴᴋ                         
❏ ᴍᴜʟᴛɪ-ᴘʟᴀʏᴇʀ sᴛʀᴇᴀᴍɪɴɢ ʟɪɴᴋs                           
❏ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs ᴀɴᴅ sᴇʀɪᴇs                                                                        
❏ ꜰᴜʟʟ ᴀᴅᴍɪɴ sᴜᴘᴘᴏʀᴛ                              
❏ ʀᴇǫᴜᴇsᴛ ᴡɪʟʟ ʙᴇ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ 𝟷ʜ [ ɪꜰ ᴀᴠᴀɪʟᴀʙʟᴇ ]

⛽️ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ: /myplan
</b>"""

    OTHER_TXT = """<b>👋 ʜᴇʏ {},
    
🎁 <u>ᴏᴛʜᴇʀ ᴘʟᴀɴ</u>
⏰ ᴄᴜꜱᴛᴏᴍɪꜱᴇᴅ ᴅᴀʏꜱ
💸 ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴅᴀʏꜱ ʏᴏᴜ ᴄʜᴏᴏꜱᴇ

🏆 ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴀ ɴᴇᴡ ᴘʟᴀɴ ᴀᴘᴀʀᴛ ꜰʀᴏᴍ ᴛʜᴇ ɢɪᴠᴇɴ ᴘʟᴀɴ, ᴛʜᴇɴ ʏᴏᴜ ᴄᴀɴ ᴛᴀʟᴋ ᴛᴏ ᴏᴜʀ <a href='https://t.me/IM_JISSHU'>ᴏᴡɴᴇʀ</a> ᴅɪʀᴇᴄᴛʟʏ ʙʏ ᴄʟɪᴄᴋɪɴɢ ᴏɴ ᴛʜᴇ ᴄᴏɴᴛᴀᴄᴛ ʙᴜᴛᴛᴏɴ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ.
    
👨‍💻 ᴄᴏɴᴛᴀᴄᴛ ᴛʜᴇ ᴏᴡɴᴇʀ ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ᴏᴛʜᴇʀ ᴘʟᴀɴ.

➛ ᴜꜱᴇ /plan ᴛᴏ ꜱᴇᴇ ᴀʟʟ ᴏᴜʀ ᴘʟᴀɴꜱ ᴀᴛ ᴏɴᴄᴇ.
➛ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ ʙʏ ᴜꜱɪɴɢ : /myplan</b>"""

    FREE_TXT = """<b>👋 ʜᴇʏ {}
    
<blockquote>🎖️ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴꜱ :</blockquote>

 ❏ 𝟶𝟷𝟻₹    ➠    𝟶𝟷 ᴡᴇᴇᴋꜱ
 ❏ 𝟶𝟹𝟿₹    ➠    𝟶𝟷 ᴍᴏɴᴛʜ
 ❏ 𝟶𝟽𝟻₹    ➠    𝟶𝟸 ᴍᴏɴᴛʜ
 ❏ 𝟷𝟷𝟶₹    ➠    𝟶𝟹 ᴍᴏɴᴛʜ
 ❏ 𝟷𝟿𝟿₹    ➠    𝟶𝟼 ᴍᴏɴᴛʜ
 ❏ 𝟹𝟼𝟶₹    ➠    𝟷𝟸 ᴍᴏɴᴛʜ

🆔 ᴜᴘɪ ɪᴅ ➩ <code>jishan@fam</code> [ᴛᴀᴘ ᴛᴏ ᴄᴏᴘʏ]
 
⛽️ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴘʟᴀɴ: /myplan

🏷️ <a href='https://t.me/jisshu_Premium_proof'>ᴘʀᴇᴍɪᴜᴍ ᴘʀᴏᴏꜰ</a>

‼️ ᴍᴜsᴛ sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ ᴀғᴛᴇʀ ᴘᴀʏᴍᴇɴᴛ.
‼️ ɢɪᴠᴇ ᴜꜱ ꜱᴏᴍᴇᴛɪᴍᴇ ᴛᴏ ᴀᴅᴅ ʏᴏᴜ ɪɴ ᴘʀᴇᴍɪᴜᴍ ʟɪꜱᴛ.
</b>"""

    ADMIN_CMD_TXT = """<b><blockquote>
-------------User Premium------------
➩ /add_premium {user ID} {Times} - Add a premium user
➩ /remove_premium {user ID} - Remove a premium user
➩ /add_redeem - Generate a redeem code
➩ /premium_users - List all premium users
➩ /refresh - Refresh free trial for users
-------------Update Channel----------
➩ /set_muc {channel ID} - Set the movies update channel
--------------PM Search--------------
➩ /pm_search_on - Enable PM search
➩ /pm_search_off - Disable PM search
--------------Verify ID--------------
➩ /verify_id - Generate a verification ID for group use only
--------------Set Ads----------------
➩ /set_ads {ads name}}#{Times}#{photo URL} - <a href="https://t.me/Jisshu_developer/11">Explain</a>
➩ /del_ads - Delete ads
-------------Top Trending------------
➩ /setlist {Mirzapur, Money Heist} - <a href=https://t.me/Jisshu_developer/10>Explain</a>
➩ /clearlist - Clear all lists
</blockquote></b>"""

    ADMIN_CMD_TXT2 = """<b><blockquote>
--------------Index File--------------
➩ /index - Index all files
--------------Leave Link--------------
➩ /leave {group ID} - Leave the specified group
-------------Send Message-------------
➩ /send {user-name} - Use this command as a reply to any message
----------------Ban User---------------
➩ /ban {user-name} - Ban user 
➩ /unban {user-name} - Unban user
--------------Broadcast--------------
➩ /broadcast - Broadcast a message to all users
➩ /grp_broadcast - Broadcast a message to all connected groups

</blockquote></b>"""
    
    GROUP_TEXT = """<b><blockquote>
 --------------Set Verify-------------
/set_verify {{website link}} {{website api}}
/set_verify_2 {{website link}} {{website api}}
/set_verify_3 {{website link}} {{website api}}
-------------Set Verify Time-----------
/set_time_2 {{seconds}} Sᴇᴛ ᴛʜᴇ sᴇᴄᴏɴᴅ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴛɪᴍᴇ
/set_time_3 {{seconds}} Sᴇᴛ ᴛʜᴇ ᴛʜɪʀᴅ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴛɪᴍᴇ
--------------Verify On Off------------
/verifyoff {{verify.off code}} - off verification <a href="https://t.me/IM_JISSHU">Cᴏɴᴛᴀᴄᴛ</a> ᴛʜᴇ ʙᴏᴛ ᴀᴅᴍɪɴ ғᴏʀ ᴀ ᴠᴇʀɪғʏ.ᴏғғ ᴄᴏᴅᴇ
/verifyon - on verification 
------------Set File Caption-----------
/set_caption - set coustom file caption 
-----------Set Imdb Template-----------
/set_template - set IMDb template <a href="https://t.me/Jisshu_developer/8">Example</a>
--------------Set Tutorial-------------
/set_tutorial - set verification tutorial 
-------------Set Log Channel-----------
--> ᴀᴅᴅ ʟᴏɢ ᴄʜᴀɴɴᴇʟ ʙʏ ᴛʜɪs ꜰᴏʀᴍᴀᴛ & ᴍᴀᴋᴇ sᴜʀᴇ ʙᴏᴛ ɪs ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ʟᴏɢ ᴄʜᴀɴɴᴇʟ 👇

/set_log {{log channel id}}
---------------------------------------
ʏᴏᴜ ᴄᴀɴ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀʟʟ ᴅᴇᴛᴀɪʟs 
ʙʏ /details ᴄᴏᴍᴍᴀɴᴅ
</blockquote>
Aᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴍᴀᴋᴇ ᴍᴇ ᴀᴅᴍɪɴ ᴀɴᴅ ᴜsᴇ ᴀʟʟ ғᴇᴀᴛᴜʀᴇs😇</b>"""

    SOURCE_TXT = """<b>
NOTE:
- ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ʜᴇʀᴇ ◉› :<blockquote><a href="https://t.me/JISSHU_BOTS">𝗝𝗶𝘀𝘀𝗵𝘂-𝗙𝗶𝗹𝘁𝗲𝗿-𝗕𝗼𝘁</a></blockquote>

developer : Mr.Jisshu
</b>""" 
    GROUP_C_TEXT = """<b><blockquote>
 --------------Set Verify-------------
/set_verify {website link} {website api}
/set_verify_2 {website link} {website api}
/set_verify_3 {website link} {website api}
-------------Set Verify Time-----------
/set_time_2 {seconds} Sᴇᴛ ᴛʜᴇ sᴇᴄᴏɴᴅ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴛɪᴍᴇ
/set_time_3 {seconds} Sᴇᴛ ᴛʜᴇ ᴛʜɪʀᴅ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ᴛɪᴍᴇ
--------------Verify On Off------------
/verifyoff {verify.off code} - off verification <a href="https://t.me/IM_JISSHU">Cᴏɴᴛᴀᴄᴛ</a> ᴛʜᴇ ʙᴏᴛ ᴀᴅᴍɪɴ ғᴏʀ ᴀ ᴠᴇʀɪғʏ.ᴏғғ ᴄᴏᴅᴇ
/verifyon - on verification 
------------Set File Caption-----------
/set_caption - set coustom file caption 
-----------Set Imdb Template-----------
/set_template - set IMDb template <a href="https://t.me/Jisshu_developer/8">Example</a>
--------------Set Tutorial-------------
/set_tutorial {tutorial link} - set 1 verification tutorial 
/set_tutorial_2 {tutorial link} - set 2 verification tutorial 
/set_tutorial_3 {tutorial link} - set 3 verification tutorial 
-------------Set Log Channel-----------
--> ᴀᴅᴅ ʟᴏɢ ᴄʜᴀɴɴᴇʟ ʙʏ ᴛʜɪs ꜰᴏʀᴍᴀᴛ & ᴍᴀᴋᴇ sᴜʀᴇ ʙᴏᴛ ɪs ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ʟᴏɢ ᴄʜᴀɴɴᴇʟ 👇

/set_log {log channel id}
---------------------------------------
ʏᴏᴜ ᴄᴀɴ ᴄʜᴇᴄᴋ ʏᴏᴜʀ ᴀʟʟ ᴅᴇᴛᴀɪʟs 
ʙʏ /details ᴄᴏᴍᴍᴀɴᴅ
</blockquote>
Iғ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ ᴅᴏᴜʙᴛs ᴘʟᴇᴀsᴇ <a href="https://t.me/IM_JISSHU">ᴄᴏɴᴛᴀᴄᴛ</a> ᴍʏ <a href="https://t.me/IM_JISSHU">ᴀᴅᴍɪɴ</a></b>"""
