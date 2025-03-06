from aiohttp import web
from .route import routes
from asyncio import sleep 
from datetime import datetime
from database.users_chats_db import db
from info import LOG_CHANNEL

async def web_server():
    web_app = web.Application(client_max_size=30000000)
    web_app.add_routes(routes)
    return web_app

async def check_expired_premium(client):
    while 1:
        data = await db.get_expired(datetime.now())
        for user in data:
            user_id = user["id"]
            await db.remove_premium_access(user_id)
            try:
                user = await client.get_users(user_id)
                await client.send_message(
                    chat_id=user_id,
                    text=f"<b>𝖧𝖾𝗒 {user.mention},\n\n𝖸𝗈𝗎𝗋 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝖺𝖼𝖼𝖾𝗌𝗌 𝗁𝖺𝗌 𝖾𝗑𝗉𝗂𝗋𝖾𝖽, 𝗍𝗁𝖺𝗇𝗄 𝗒𝗈𝗎 𝖿𝗈𝗋 𝗎𝗌𝗂𝗇𝗀 𝗈𝗎𝗋 𝗌𝖾𝗋𝗏𝗂𝖼𝖾 😊\n\n𝖨𝖿 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝗍𝖺𝗄𝖾 𝗍𝗁𝖾 𝗉𝗋𝖾𝗆𝗂𝗎𝗆 𝖺𝗀𝖺𝗂𝗇, 𝗍𝗁𝖾𝗇 𝖼𝗅𝗂𝖼𝗄 𝗈𝗇 𝗍𝗁𝖾 /plan 𝖿𝗈𝗋 𝗍𝗁𝖾 𝖽𝖾𝗍𝖺𝗂𝗅𝗌 𝗈𝖿 𝗍𝗁𝖾 𝗉𝗅𝖺𝗇𝗌...</b>"
                )
                await client.send_message(LOG_CHANNEL, text=f"<b>#Premium_Expired\n\n𝖴𝗌𝖾𝗋𝗇𝖺𝗆𝖾: {user.mention}\n𝖴𝗌𝖾𝗋 𝖨𝖽: <code>{user_id}</code>")
            except Exception as e:
                print(e)
            await sleep(0.5)
        await sleep(1)
