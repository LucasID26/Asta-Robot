from pyrogram import filters
from config import bot,prefix,own,dbname
import requests

db = dbname.Monitor


@bot.on_message(filters.command("addmonitor",prefix) & filters.user(own[0]))
async def save_monitor(client,m):
  if len(m.command) == 1:
    return await m.reply_text("Cantumkan URL yang mau ditambahkan dalam daftar monitor")
  url = m.text.split(" ",1)[1]
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
