from pyrogram import Client, filters

OWNER_ID = 6317313711
API_ID = 36845222
API_HASH = "6b145a7819ea1f045e0b89877575530f"
BOT_TOKEN = "8674697438:AAES7ApBlzXGJl8muEemsq4GYbQIhwxunNk"

app = Client("musicbot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("🎵 Nova Music Bot Online")

app.run()