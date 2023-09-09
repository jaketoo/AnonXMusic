import time
import requests 
from pyrogram import Client, filters
import asyncio
from AnonXMusic import app
from pyrogram.types import VideoChatEnded, Message
from pytgcalls import PyTgCalls, StreamType
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from AnonXMusic.core.call import Anony
from AnonXMusic.utils.database import *
from pytgcalls.exceptions import (NoActiveGroupCall,TelegramServerError,AlreadyJoinedError)
from datetime import datetime, timedelta
from pyrogram.errors import FloodWait
from pyrogram.raw import types
import random

chat = []

async def get_prayer_times(address, method, school):
    url = f"http://api.aladhan.com/timingsByAddress?address={address}&method={method}&school={school}"
    response = requests.get(url)
    data = response.json()
    return data["data"]["timings"]

async def azan2():
    address = "Cairo"
    method = 4  
    school = 0  
    prayer_times = await get_prayer_times(address, method, school)
    times_message = f"أوقات الصلاة في {address}:\n"
    times_message += f"الفجر: {prayer_times['Fajr']}\n"
    times_message += f"الشروق: {prayer_times['Sunrise']}\n"
    times_message += f"الظهر: {prayer_times['Dhuhr']}\n"
    times_message += f"العصر: {prayer_times['Asr']}\n"
    times_message += f"المغرب: {prayer_times['Maghrib']}\n"
    times_message += f"العشاء: {prayer_times['Isha']}\n"
    await times_message

async def azan(message):

    assistant = await group_assistant(Anony, message.chat.id)
    try:
        await assistant.join_group_call(message.chat.id, AudioPiped("./AnonXMusic/assets/azan.mp3"), stream_type=StreamType().pulse_stream)
        text = "حان الآن موعد الأذان:"
        await message.reply(text)
        await asyncio.sleep(60)
        await assistant.leave_group_call(message.chat.id)
    except NoActiveGroupCall:
        await message.reply("المكالمة الجماعية مغلقة.")
    except AlreadyJoinedError:
        text = "حان الآن موعد الأذان:"
        await message.reply(text)
    await asyncio.sleep(60)
    for i in chat:
        try:
            await app.send_message(i, random.choice(azan2))
        except:
            pass

asyncio.create_task(azan2())
