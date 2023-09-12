import requests
import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait, ChatAdminRequired, UserAlreadyParticipant, UserNotParticipant
from pyrogram.raw import types
from AnonXMusic import app
import random
from datetime import datetime
import requests
import pytz
from AnonXMusic.core.call import Anony
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped
from AnonXMusic.core.call import Anony
from AnonXMusic.utils.database import *
from pytgcalls.exceptions import NoActiveGroupCall, TelegramServerError, AlreadyJoinedError

tz = pytz.timezone('Africa/Cairo')

chat = []

@app.on_message(filters.text & ~filters.private, group=20)
async def handle_messages(c, msg):
    if msg.text == "تفعيل الأذان":
        if msg.chat.id in chat:
            await msg.reply_text("ℹ️ الأذان مفعل بالفعل.")
        else:
            chat.append(msg.chat.id)
            await msg.reply_text("✅ تم تفعيل الأذان.")
    elif msg.text == "تعطيل الأذان":
        if msg.chat.id in chat:
            chat.remove(msg.chat.id)
            await msg.reply_text("✅ تم تعطيل الأذان.")
        else:
            await msg.reply_text("ℹ️ الأذان معطل بالفعل.")

async def stop_streams():
    for i in chat:
        await Anony.force_stop_stream(i)

async def play_azan(i):
    assistant = await group_assistant(Anony, i)
    file_path = "AnonXMusic/assets/azan.mp3"
    stream = AudioPiped(file_path, audio_parameters=HighQualityAudio())
    
    try:
        await assistant.join_group_call(
            i,
            stream,
            stream_type=StreamType().pulse_stream,
        )
    except NoActiveGroupCall:
        try:
            await Anony.join_assistant(i, i)
        except Exception as e:
            await app.send_message(i, f"{e}")
    except TelegramServerError:
        await app.send_message(i, "حدث خطأ في سيرفرات تليجرام.")
    except AlreadyJoinedError:
        await stop_streams()
        try:
            await assistant.join_group_call(
                i,
                stream,
                stream_type=StreamType().pulse_stream,
            )
        except Exception as e:
            await app.send_message(i, f"{e}")

def get_prayer_time():
    try:
        prayer = requests.get(f"http://api.aladhan.com/timingsByAddress?address=Cairo&method=4&school=0")
        prayer = prayer.json()
        fajr = datetime.strptime(prayer['data']['timings']['Fajr'], '%H:%M').strftime('%I:%M %p')
        dhuhr = datetime.strptime(prayer['data']['timings']['Dhuhr'], '%H:%M').strftime('%I:%M %p')
        asr = datetime.strptime(prayer['data']['timings']['Asr'], '%H:%M').strftime('%I:%M %p')
        maghrib = datetime.strptime(prayer['data']['timings']['Maghrib'], '%H:%M').strftime('%I:%M %p')
        isha = datetime.strptime(prayer['data']['timings']['Isha'], '%H:%M').strftime('%I:%M %p')
        
        current_time = datetime.now(tz).strftime('%I:%M %p')
        if current_time == fajr:
            return "الفجر 🌅"
        elif current_time == dhuhr:
            return "الظهر 🌞"
        elif current_time == asr:
            return "العصر 🌇"
        elif current_time == maghrib:
            return "المغرب 🌆"
        elif current_time == isha:
            return "العشاء 🌙"
    except Exception as e:
       asyncio.sleep(5)
       print(e) 

async def send_prayer_alerts():
    while not await asyncio.sleep(2):
        prayer = get_prayer_time()
        if prayer:
            await stop_streams()
            for i in chat:
                await app.send_message(i, f"حان الآن وقت أذان {prayer}")
                await play_azan(i)
            await asyncio.sleep(174)
            await stop_streams()
