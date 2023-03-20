from pyrogram import filters 
from pykeyboard import InlineKeyboard,InlineButton 
from config import bot,prefix
from pyrogram.types import InputMediaPhoto, InputMediaVideo, InputMediaAudio
import os

from Asta.func.cek_admin import bot_admin
from Asta.func.info_cmd import info_cmd
from Asta.func.error import error
from Asta.func.donghua import get_donghua,eps


hasil = {}

@bot.on_message(filters.command('donghua',prefix))
@info_cmd 
@bot_admin
@error
async def donghua(client,m):
  userid = str(m.from_user.id)
  if len(m.command) == 1:
    return await m.reply_text("Pencarian Donghua, /donghua [query]")
  text = m.text.split(" ",1)
  msg = await m.reply_text(f"__Searching Donghua__ {text[1]}...")
  dh = get_donghua(m,text[1]) 
  if len(dh) == 0:
    return await msg.edit(f"Tidak ada hasil untuk {text[1]}")
  hasil[str(m.id)] = dh[str(m.id)]
  try:
      jumlah = 1
      markup = InlineKeyboard()
      result = dh[str(m.id)]
      markup.paginate(
        len(result),jumlah,'page_donghua#{number}' + f"#{m.id}#{userid}")
      markup.row(
        InlineButton("EPISODE",callback_data=f'episode_donghua#{jumlah}' + f"#{m.id}#{userid}#0"))
      markup.row(
        InlineButton("Close",callback_data='close_donghua#{number}' + f"#{m.id}#{userid}"))
      text = f"""
**Judul:** {result[0]['judul']}

**Deskripsi:** {result[0]['desc']} 

**Detail:**
{result[0]['info']}
"""
      await m.reply_photo(photo=result[0]['img'],caption=text,reply_markup=markup) 
      await msg.delete()
  except:
    pass


@bot.on_callback_query(filters.create(lambda _, __, query: "page_donghua#" in query.data))
async def callkaze(_,call):
  if call.from_user.id != int(call.data.split("#")[3]):
    return await call.answer("Bukan buat lu..!",True)
  page = int(call.data.split("#")[1])
  msgid = str(call.data.split("#")[2])
  user = str(call.data.split("#")[3]) 
  try:
    kueri = hasil[msgid]
  except KeyError:
    await call.answer('Invalid callback data..!',True)
    return await call.message.delete()
  markup = InlineKeyboard()
  result = hasil[msgid] 
  markup.paginate(
    len(result),page,'page_donghua#{number}' + f"#{msgid}#{user}")
  markup.row(
    InlineButton("EPISODE",callback_data=f'episode_donghua#1' + f"#{msgid}#{user}#{page - 1}"))
  markup.row(InlineButton("Close",callback_data='close_donghua#{number}' + f"#{msgid}#{user}"))
  text = f"""
**Judul:** {result[page - 1]['judul']}

**Deskripsi:** {result[page - 1]['desc']}

**Detail:**
{result[page - 1]['info']}
"""
  await bot.edit_message_media(call.message.chat.id,message_id=call.message.id,reply_markup=markup,media=InputMediaPhoto(result[page - 1]['img']))
  await bot.edit_message_text(call.message.chat.id,text=text,message_id=call.message.id,reply_markup=markup)


@bot.on_callback_query(filters.create(lambda _, __, query: "episode_donghua#" in query.data))
async def callkaze(_,call):
  if call.from_user.id != int(call.data.split("#")[3]):
    return await call.answer("Bukan buat lu..!",True)
  page = int(call.data.split("#")[1])
  msgid = str(call.data.split("#")[2])
  user = str(call.data.split("#")[3]) 
  page_link = int(call.data.split("#")[4]) 
  try:
    result = hasil[msgid]
  except KeyError:
    await call.answer('Invalid callback data..!',True)
  markup = InlineKeyboard()
  episode = eps(result[page_link]['link']) 
  title = episode[-1 - (page - 1)].split("/")[3]
  link = episode[-1 - (page - 1)]
  markup.paginate(
    len(episode),page,'episode_donghua#{number}' + f"#{msgid}#{user}#{page_link}")
  markup.row(
    InlineButton(
      "URL",url=link)
  )
  markup.row(
    InlineButton(
      "back",callback_data=f'page_donghua#{page_link + 1}' + f"#{msgid}#{user}"))
  await call.message.edit(f"**EPISODE:**\n{title}",reply_markup=markup)
  

@bot.on_callback_query(filters.create(lambda _, __, query: "close_donghua#" in query.data))
async def callclose(_,call):
  if call.from_user.id != int(call.data.split("#")[3]):
    return await call.answer("Bukan buat lu..!",True)
  msgid = int(call.data.split("#")[2])
  #user = str(call.data.split("#")[2]) 
  return await call.message.delete()
