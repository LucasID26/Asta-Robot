from pyrogram import filters
from config import bot,prefix,own,dbname
import requests
from urllib.parse import urlparse

db = dbname.Monitor


@bot.on_message(filters.command("addmonitor",prefix) & filters.user(own[0]))
async def save_monitor(client,m):
  if len(m.command) == 1:
    return await m.reply_text("Cantumkan URL yang mau ditambahkan dalam daftar monitor")
  url = m.text.split(" ",1)[1]
  if not urlparse(url).scheme:
    return await m.reply_text("Cantumkan URL yang valid")
  key = {"name": "MONITOR"}
  if db.find_one(key):
    if url in db.find_one(key)['monitor_url']:
      await m.reply_text("URL sudah ada dalam daftar monitor saya!")
    else:
      save = db.update_one(key, {"$push": {"monitor_url": url}})
      await m.reply_text("URL ditambahkan dalam daftar monitor")
  else:
    save = db.insert_one({"name": "MONITOR", "monitor_url": [url]})
    await m.reply_text("URL ditambahkan dalam daftar monitor")

@bot.on_message(filters.command("monitor",prefix) & filters.user(own[0]))
async def get_monitor(client,m):
  msg = await m.reply_text("`Mengumpulkan data monitor . . .`")
  hasil = ""
  valid = "**STATISTIK MONITOR**\n"
  invalid = "**URL TIDAK VALID**\n"
  j_valid = 0
  j_invalid = 0
  a = 1
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
      j_valid += 1
    except:
      invalid += f"{a}. {url}\n"
      j_invalid += 1
      a += 1
  if j_valid and j_invalid != 0:
    hasil += valid + invalid
  elif j_valid and j_invalid == 0:
    hasil += "Monitor Kosong"
  elif j_valid != 0 and j_invalid == 0:
    hasil += valid
  elif j_invalid != 0 and j_valid == 0:
    hasil += invalid
  await msg.edit(hasil)

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
