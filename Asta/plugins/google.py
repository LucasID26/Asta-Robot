from pyrogram import filters 
from config import bot,prefix
from html import escape
from pyrogram.types import InputMediaPhoto, InputMediaVideo 
from pyrogram.errors import FloodWait 
import asyncio
from geopy.geocoders import Nominatim

from Asta.decorators.error import error
from Asta.decorators.info_cmd import info_cmd 
from Asta.decorators.cek_admin import bot_admin

from Asta.func.google import google,Gimages


@bot.on_message(filters.command(["google","g"],prefix)) 
@info_cmd
@bot_admin 
@error
async def s_google(client, m):
  text = m.text.split(" ",1)
  if len(m.command) == 1:
    return await m.reply_text("Pencarian google\n/g [query]")
  msg = await m.reply_text(f"__Searching google__ {text[1]}...")
  ggl = google(text[1], limit=20)
  hasil = f"📌 Hasil pencarian GOOGLE **{text[1]}** berjumlah {len(ggl)}:\n\n"
  for i in ggl:
    title = i['judul']
    link = i['link']
    deskripsi = i['deskripsi'] 
    hasil1 = f'<a href="{link}">{title}</a>'
    hasil += f"{hasil1}\n{escape(deskripsi)}\n\n"
  await msg.edit(hasil,disable_web_page_preview=True)


@bot.on_message(filters.command('img',prefix)) 
@info_cmd
@bot_admin 
@error
async def img(client, m):
  try:
    text = m.text.split(" ",1)
    if len(m.command) == 1:
      return await m.reply_text("Pencarian google image!\n/img [query]")
    msg = await m.reply_text(f"__Searching image__ {text[1]}...")
   # img = Gimages(text)
    photos = []
    media_full = []
    for photo in Gimages(text[1]):
      photos.append(
        InputMediaPhoto(str(photo['original'])))
    if len(photos) >= 10:
      media_full.append(photos[:10])
      media_full.append(photos[10:])
    if media_full:
      for media in media_full:
       # await asyncio.sleep(2)
        if m.chat.is_forum == True:
          await bot.send_media_group(m.chat.id,media,message_thread_id=m.topics.id)
        else:
          await bot.send_media_group(m.chat.id,media) 
        await bot.delete_messages(m.chat.id, msg.id)
  except FloodWait as e:
    await asyncio.sleep(e.value)
  #except Exception as e:
    #await msg.edit(f"Error : `{e}`")  


#SEARCH LOKASI 
@bot.on_message(filters.command('lokasi',prefix)) 
@info_cmd
@bot_admin 
@error
async def lokasi(client, m):
  text = m.text.split(" ",1)
  if len(m.command) == 1:
    return await m.reply_text("Pencarian lokasi, /lokasi [query]")
  text = m.text.split(" ",1)
  msg = await m.reply_text(f"__Searching lokasi__ {text[1]}...")
  try:
    geolocator = Nominatim(user_agent="MyApp")
    location = geolocator.geocode(text[1])

    lat = location.latitude
    long = location.longitude
    kordinat = str(lat) + ',' + str(long)
    loc = geolocator.reverse(kordinat)
    msgg = await m.reply_venue(lat,long,str(loc),kordinat)
    await bot.edit_message_caption(m.chat.id,message_id=msgg.id,caption=loc)
    await msg.delete() 
  except :
    await msg.edit("Hasil tidak ditemukan!")
