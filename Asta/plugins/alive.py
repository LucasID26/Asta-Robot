from pyrogram import filters 
from config import * 
import time 
from datetime import datetime
import requests
import os
import platform
import psutil

from Asta.decorators.info_cmd import info_cmd
from Asta.func.duration import duration
from Asta.func.file_size import file_size 


starttime = datetime.utcnow()

@bot.on_message(filters.command("ping",prefix))
@info_cmd
async def ping(client, m):
  uptime = duration((datetime.utcnow() - starttime).total_seconds())
  start = time.time() 
  msg = await m.reply_text("**0% ▒▒▒▒▒▒▒▒▒▒**")
  end = time.time()
  durasi = round(end - start,3)
  #await msg.edit("**20% ██▒▒▒▒▒▒▒▒**")
  #await msg.edit("**40% ████▒▒▒▒▒▒**")
  #await msg.edit("**60% ██████▒▒▒▒**")
  #await msg.edit("**80% ████████▒▒**")
  await msg.edit("**100% ██████████**")
  owner = (await bot.get_users(own[0])).mention
  await msg.edit(f"""
❏ **PONG!!🏓**
├• **Pinger** ➥ `{durasi} detik`
├• **Server** ➥ `{ping_server()}`
├• **Uptime** ➥ `{uptime}`
└• **Owner :** {owner} <a href='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTz5q_KcP8RQbDQPciRoBSlwKMyBHAKMNN-pg&amp;usqp=CAU'>⁠</a>""")

def ping_server():
  url = os.environ['PING_URL']
  start = time.time()
  response = requests.get(url, timeout=2) 
  end = time.time()
  ping = (end - start) * 1000
  result = f"{ping:.2f} ms."
  return result




@bot.on_message(filters.command("system",prefix))
@info_cmd
async def system(client,m):
  try:
    vid = "BAACAgUAAx0CYPuISgACl3JkJmfdgFPoYwPizz_hs6Dt0ccAAX4AAiMKAAIkczFVCt3L88hIaXoeBA"
    #PLATFORM
    system = platform.uname()
    sistem = system.system
    versi = system.version
    mesin = system.machine
    p_implementasi = platform.python_implementation()
    bit = platform.architecture()
    python_v = platform.python_version()
    uptime = duration((datetime.utcnow() - starttime).total_seconds())
    #DISK
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    msg = f"""
❏ **SYSTEM ⚙**
├• **System** ➥ `{sistem}`
├• **Version** ➥ `{versi}`
├• **Machine** ➥ `{mesin}`
├• **Py_Implemenation** ➥ `{implementasi}`
├• **BIT** ➥ `{bit}`
├• **Python Version** ➥ `{python_v}`
└• **Uptime** ➥ `{uptime}` detik

❏ **DISK 💾**
├• **CPU** ➥ `{cpu}%`
├• **RAM** ➥ `{mem}%`
└• **Disk** ➥ `{disk}%`
"""
    await m.reply_video(vid,caption=msg)
  except Exception as e:
    await m.reply_text(f"Terjadi kesalahan dalam mengumpulkan data system\n**EROR**: `{e}`")

