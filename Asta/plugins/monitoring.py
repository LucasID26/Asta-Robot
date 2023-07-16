from pyrogram import filters
from config import bot,prefix,own
import requests
import os
import json
from urllib.parse import urlparse


api_key = os.environ['UPTIME_API']


@bot.on_message(filters.command("addmonitor",prefix) & filters.user(own))
async def save_monitor(client,m):
  if len(m.command) == 1:
    return await m.reply_text("Cantumkan URL yang mau ditambahkan dalam daftar monitor")
  url = m.text.split(" ",1)[1]
  if not urlparse(url).scheme:
    return await m.reply_text("Cantumkan URL yang valid")
  
  url_uptime  = "https://api.uptimerobot.com/v2/newMonitor"
  monitor_url = []

  for monitor in get_monitor():
    monitor_url.append(monitor["url"])
  if url in monitor_url:
    return await m.reply_text('URL sudah terdaftar dalam monitor')
  payload = {
        "api_key": api_key,
        "url": url,
        "type": 1,
        "friendly_name": urlparse(url).netloc
  }
  res = requests.post(url_uptime, data=payload).json()
  stat = "Berhasil✅" if res['stat'] == "ok" else "Kegagalan❎"
  if stat == 'Berhasil✅':
    pesan = f"**Nama :** `{urlparse(url).netloc}`\n**Stat :** `{stat}`\n**Status :** `{res['monitor']['status']}`\n**ID :** `{res['monitor']['id']}`"
    await m.reply_text(pesan)
  elif stat == 'Kegagalan❎':
    pesan = f"**Stat :** `{stat}`\n**Error :** `{res['error']['message']}`" 
    await m.reply_text(pesan)




@bot.on_message(filters.command("monitor",prefix) & filters.user(own))
async def get_monitor(client,m):
  msg = await m.reply_text("`Mengumpulkan data monitor . . .`")  
  pesan = "**STATISTIK MONITOR**\n\n"
  for monitor in get_monitor():
    nama = monitor['friendly_name']
    status = monitor['status']
    id = monitor['id']
    interval = monitor['interval']
    timeout = monitor['timeout']
    pesan += f"**Nama :** `{nama}`\n**Status :** `{status}`\n**ID :** `{id}`\n**Interval :** `{interval}`\n**Timeout :** `{timeout}`\n\n"
  await msg.edit(pesan)

@bot.on_message(filters.command("delmonitor",prefix) & filters.user(own))
async def del_monitor(client,m):
  if len(m.command) == 1:
    return await m.reply_text("Cantumkan ID monitor yang mau dihapus dari daftar monitor")
  id = m.text.split(" ",1)[1]
  if not id.isdigit():
    return await m.reply_text("Cantumkan ID berupa integer bukan string")
  url_uptime = "https://api.uptimerobot.com/v2/deleteMonitor"
  payload = {
    "api_key": api_key,
    "format": "json",
    "type": 1,
    "id": id
  }

  res = requests.post(url_uptime, data=payload).json()
  stat = "Berhasil✅" if res['stat'] == "ok" else "Kegagalan❎"
  if stat == 'Berhasil✅':
    pesan = f"**Stat :** `{stat}`\n**ID :** `{res['monitor']['id']}`"
    await m.reply_text(pesan)
  elif stat == 'Kegagalan❎':
    pesan = f"**Stat :** `{stat}`\n**Error :** `{res['error']['message']}`" 
    await m.reply_text(pesan)



def get_monitor():
  url = "https://api.uptimerobot.com/v2/getMonitors"
  payload = {
    "api_key": api_key,
    "format": "json"
  }
  res = requests.post(url, data=payload).json()
  return res['monitors']



