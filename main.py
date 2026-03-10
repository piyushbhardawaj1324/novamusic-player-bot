from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types import AudioPiped
import config

# Initialize Bot and Assistant
bot = Client("music_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)
assistant = Client("assistant", api_id=config.API_ID, api_hash=config.API_HASH, session_string=config.SESSION_STRING)

call_py = PyTgCalls(assistant)

@bot.on_message(filters.command("play") & filters.group)
async def play_audio(client, message):
    if len(message.command) < 2:
        return await message.reply("Provide a direct audio link!")
    
    audio_url = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    
    await message.reply(f"🎵 **Playing:** {audio_url}")
    await call_py.start()
    await call_py.play(chat_id, AudioPiped(audio_url))

@bot.on_message(filters.command("stop") & filters.group)
async def stop_audio(client, message):
    await call_py.leave_call(message.chat.id)
    await message.reply("⏹ Stopped streaming.")

async def start_bot():
    await bot.start()
    await assistant.start()
    await idle()

if __name__ == "__main__":
    start_bot()
