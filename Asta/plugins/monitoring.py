from pyrogram import filters
from config import bot,prefix,own
import requests
import os
from urllib.parse import urlparse


api_key = os.environ['UPTIME_API']


@bot.on_message(filters.command("addmonitor",prefix) & filters.user(own[0]))
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
  res = requests.post(url_uptime, data=data).json()
  status = "Berhasil✅" if res['stat'] == "ok" else "Kegagalan❎"
  if status == 'Berhasil✅':
    pesan = f"**Nama :** `{urlparse(url).netloc}`\n**Status :** `{status}`\n**ID :** `{res['monitor']['id']}`"
    await m.reply_text(pesan)
  elif status == 'Kegagalan❎':
    pesan = f"**Status :** `{status}`\n**Error :** `{res['error']['message']}`" 
    await m.reply_text(pesan)




@bot.on_message(filters.command("monitor",prefix) & filters.user(own[0]))
async def get_monitor(client,m):
  msg = await m.reply_text("`Mengumpulkan data monitor . . .`")
  if len(db.find_one({"name":"MONITOR"})['monitor_url']) == 0:
    return await msg.edit("**MONITOR KOSONG**")
  valid = "**STATISTIK MONITOR**\n\n"
  for url in db.find_one({"name":"MONITOR"})['monitor_url']:
    name = urlparse(url).netloc.split(".",1)[0]
    try:
      res = requests.get(url)
      if res.status_code == 200:
        status = "Aktif"
        status_c = res.status_code
        respon = res.text
      else:
        status = "Tidak Aktif"
        status_c = res.status_code
        respon = "Tidak ada respon"
      valid += f"**Name:** `{name}`\n**Status:** `{status}`\n**Status Code:** `{status_c}`\n**Response:** `{respon}`\n\n"
    except:
      valid += f"**URL INVALID:** {url}\n\n"
  await msg.edit(valid)

@bot.on_message(filters.command("delmonitor",prefix) & filters.user(own[0]))
async def del_monitor(client,m):
  if len(m.command) == 1:
    return await m.reply_text("Cantumkan URL yang mau dihapus dari daftar monitor")
  url = m.text.split(" ",1)[1]
  if not urlparse(url).scheme:
    return await m.reply_text("Cantumkan URL yang valid")
  key = {"name": "MONITOR"}
  if db.find_one(key):
    if url in db.find_one(key)['monitor_url']:
      db.update_one(key,{"$pull":{"monitor_url": url}})
      await m.reply_text("URL dihapus dari daftar monitor")
    else:
      await m.reply_text("URL tidak ada dalam daftar monitor saya!")
  else:
    await m.reply_text("Monitor kosong")



def get_monitor():
  url = "https://api.uptimerobot.com/v2/getMonitors"
  payload = {
    "api_key": api_key,
    "format": "json"
  }
  res = requests.post(url, data=payload).json()
  return res['monitors']



