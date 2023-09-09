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

@app.on_message(filters.regex("^اذن$"))
async def strcall(client, message):
    assistant = await group_assistant(Anony, message.chat.id)
    try:
        await assistant.join_group_call(message.chat.id, AudioPiped("AnonXMusic/assets/azan.mp3"), stream_type=StreamType().pulse_stream)
    except NoActiveGroupCall:
        await message.reply(f"الكول مقفول اصلا يصاحبي")
    except TelegramServerError:
        await message.reply(f"ارسل الامر تاني في مشكله في سيرفر التلجرام")
    except AlreadyJoinedError:
        pass

