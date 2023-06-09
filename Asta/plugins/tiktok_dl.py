from config import bot,prefix 
from pyrogram import filters 
import requests,json,os
from pykeyboard import InlineKeyboard,InlineButton
from urllib.parse import urlparse 
import asyncio

from Asta.decorators.cek_admin import bot_admin
from Asta.decorators.info_cmd import info_cmd
from Asta.decorators.error import error


async def progress(current, total):
    return f"{current * 100 / total:.1f}%"

link_data = {}
@bot.on_message(filters.command("ttdl",prefix))
@info_cmd
@bot_admin 
@error
async def tiktok_dl(client,m):
  link = m.text.split(" ",1)
  id = m.from_user.id
  if len(m.command) == 1:
    return await m.reply_text("Silahkan cantumkan link dari TikTok!")
  url_info = urlparse(link[1])
 # if url_info.scheme:
  if not url_info.netloc in ['vt.tiktok.com']:
    return await m.reply_text("Url tidak valid!")
  msg = await m.reply_text("`prosesss`")
  button = InlineKeyboard(row_width=2)
  button.add(
    InlineButton('Video',callback_data=f'tiktok|video_tt|{id}'),
    InlineButton('Audio',callback_data=f'tiktok|audio_tt|{id}')
  )
  try:
    req = requests.get(f"https://apimu.my.id/downloader/tiktok3?link={link[1]}").json()
    v_title = req['hasil']['video_title']
    thumb = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTwmXHPxszprboid-r4LESK4WPtDdSRNMnliQ&amp;usqp=CAU"
    video = req['hasil']['download_mp4_hd']
    audio = req['hasil']['download_mp3']
    name = req['hasil']['name']
    username = req['hasil']['username']
    like = req['hasil']['like']
    comment = req['hasil']['comment']
    share = req['hasil']['share']
    views = req['hasil']['views']
    a_title = req['hasil']['music_title']
    a_author = req['hasil']['music_author']
    link_data[str(m.from_user.id)] = {'video':video,
                                      'audio':audio, 
                                      'v_title':v_title,
                                      'thumb':thumb,
                                      'name':name,
                                      'username':username,
                                      'like':like,
                                      'comment':comment,
                                      'share':share,
                                      'views':views,
                                      'a_title':a_title,
                                      'a_author':a_author}
    


    await m.reply_photo(photo=thumb,caption=f"""
**Name:** {name}
**Username:** {username}

`👍: {like}  🔁: {share}  
💬: {comment}   👀: {views}` 
""",reply_markup=button)
    await msg.delete() 
  except Exception as e: 
    await msg.edit(f"ERORR : {e}")

@bot.on_callback_query(filters.create(lambda _, __, query: "tiktok|" in query.data))
async def callback_dl_tt(client,call):
  data = call.data.split("|",2)
  id = str(call.from_user.id)
  if id != data[2]:
    return await call.answer("Bukan buat lu!",True)
  try:
    data_tt = link_data[id]
  except KeyError:
    return await call.answer("Timeout Callback data!",True)
  msg = await bot.edit_message_caption(chat_id=call.message.chat.id,message_id=call.message.id,caption=f"📥 **Mengunduh**")    
  if data[1] == 'video_tt': 
    title = link_data[id]['v_title']
    like = link_data[id]['like']
    comment = link_data[id]['comment']
    share = link_data[id]['share']
    views = link_data[id]['views']
    video = link_data[id]['video']
    await msg.edit_caption(f"📤 **Mengunggah Hasil**\n{title}")
    await asyncio.sleep(2)
    await call.message.reply_video(video,caption=f"""
{title}

`👍: {like}  🔁: {share}  
💬: {comment}   👀: {views}` 
""")
    return await call.message.delete()
  elif data[1] == 'audio_tt':
    title = link_data[id]['a_title']
    author = link_data[id]['a_author']
    like = link_data[id]['like']
    comment = link_data[id]['comment']
    share = link_data[id]['share']
    views = link_data[id]['views']
    audio = link_data[id]['audio']
    await msg.edit_caption(f"📤 **Mengunggah Hasil**\n{title}")
    await asyncio.sleep(2)
    await call.message.reply_audio(audio,thumb=link_data[id]['thumb'],caption=f"""
**Author:** {author}
{title}

`👍: {like}  🔁: {share}  
💬: {comment}   👀: {views}` 
""")
    return await call.message.delete()
