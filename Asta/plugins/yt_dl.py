from config import bot,prefix 
from pyrogram import filters 
import requests,json,os
from pykeyboard import InlineKeyboard,InlineButton
from urllib.parse import urlparse 

from Asta.decorators.cek_admin import bot_admin
from Asta.decorators.info_cmd import info_cmd
from Asta.decorators.error import error


async def progress(current, total):
    return f"{current * 100 / total:.1f}%"

link_data = {}
@bot.on_message(filters.command("ytdl",prefix))
@info_cmd
@bot_admin 
@error
async def yt_dlyt_dl(client,m):
  link = m.text.split(" ",1)
  id = m.from_user.id
  if len(m.command) == 1:
    return await m.reply_text("Silahkan cantumkan link dari YouTube!")
  url_info = urlparse(link[1])
 # if url_info.scheme:
  if not url_info.netloc in ['www.youtube.com', 'youtu.be', 'youtube.com', 'youtu.be']:
    return await m.reply_text("Url tidak valid!")
  msg = await m.reply_text("`prosesss`")
  button = InlineKeyboard(row_width=2)
  button.add(
    InlineButton('Video',callback_data=f'video|{id}'),
    InlineButton('Audio',callback_data=f'audio|{id}')
  )
  try:
    req = requests.get(f"https://apimu.my.id/downloader/youtube3?link={link[1]}&type=720").json()
    title = req['title']
    thumb = req['thumbnail']
    sizev = req['mp4']['size']
    sizea = req['audio']['size']
    video = req['mp4']['download']
    audio = req['audio']['audio']
    link_data[str(m.from_user.id)] = {'video':video,'audio':audio,'title':title,'thumb':thumb,'sizev':sizev,'sizea':sizea}
    await m.reply_photo(photo=thumb,caption=f"""
**{title}**
• **Size video:** {sizev}
• **Size audio:** {sizea}""",reply_markup=button)
    await msg.delete() 
  except Exception as e: 
    await msg.edit(f"ERORR : {e}")

@bot.on_callback_query(group=2)
async def callback_dl(client,call):
  data = call.data.split("|",1)
  id = str(call.from_user.id)
  try:
    if data[1] == id:
      msg = await bot.edit_message_caption(chat_id=call.message.chat.id,message_id=call.message.id,caption=f"📥 **Mengunduh**")    
      if data[0] == 'video': 
        title = link_data[id]['title'] + '.mp4'
        size = link_data[id]['sizev']
        thumb = link_data[id]['thumb']
        res = requests.get(link_data[id]['video']).content
        with open(title, 'wb') as vd_file:
          vd_file.write(res)
          vd_file.close()
        with open(f"{title}.jpg","wb") as ph_file:
          ph_file.write(requests.get(thumb).content)
          ph_file.close() 
        await bot.edit_message_caption(chat_id=call.message.chat.id,message_id=call.message.id,caption=f"📤 **Mengunggah Hasil**\n{title}")
        await call.message.reply_video(open(title,"rb"),thumb=f"{title}.jpg",caption=f"""
{title}
• Size: {size}""")
        await msg.delete()
        os.remove(title)
        os.remove(f"{title}.jpg") 
      elif data[0] == 'audio':
        title = link_data[id]['title'] + '.mp3'
        size = link_data[id]['sizea']
        thumb = link_data[id]['thumb']
        res = requests.get(link_data[id]['audio']).content
        with open(title, 'wb') as vd_file:
          vd_file.write(res)
          vd_file.close()
        with open(f"{title}.jpg","wb") as ph_file:
          ph_file.write(requests.get(thumb).content)
          ph_file.close()
        await bot.edit_message_caption(chat_id=call.message.chat.id,message_id=call.message.id,caption=f"📤 **Mengunggah Hasil**\n{title}")
        await call.message.reply_audio(open(title,"rb"),thumb=f"{title}.jpg",caption=f"""
{title}
• Size: {size}""")
        await call.message.delete()
        os.remove(title)
        os.remove(f"{title}.jpg") 
    else:
      await call.answer("Bukan buat lu!",True)
  except:
    pass
    #await call.answer("Timeout Callback data!",True)
