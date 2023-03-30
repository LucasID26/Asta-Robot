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
@bot.on_message(filters.command("ttdl",prefix))
@info_cmd
@bot_admin 
@error
async def yt_dlyt_dl(client,m):
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
    InlineButton('Video',callback_data=f'video_tt|{id}'),
    InlineButton('Audio',callback_data=f'audio_tt|{id}')
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

👍: {like}  🔁: {share}  💬: {comment}   👀: {views}  
""",reply_markup=button)
    await msg.delete() 
  except Exception as e: 
    await msg.edit(f"ERORR : {e}")

@bot.on_callback_query(group=3)
async def callback_dl(client,call):
  data = call.data.split("|",1)
  id = str(call.from_user.id)
  try:
    if data[1] == id:
      msg = await bot.edit_message_caption(chat_id=call.message.chat.id,message_id=call.message.id,caption=f"📥 **Mengunduh**")    
      if data[0] == 'video_tt': 
        title = link_data[id]['v_title']
        like = link_data[id]['like']
        comment = link_data[id]['comment']
        share = link_data[id]['share']
        views = link_data[id]['views']
        video = link_data[id]['video']
        #res = requests.get(link_data[id]['video']).content
        #with open(title, 'wb') as vd_file:
         # vd_file.write(res)
         # vd_file.close()
        await bot.edit_message_caption(chat_id=call.message.chat.id,message_id=call.message.id,caption=f"📤 **Mengunggah Hasil**\n{title}")
        await call.message.reply_video(video,thumb=link_data[id]['thumb'],caption=f"""
{title}

👍: {like}  🔁: {share}  💬: {comment}   👀: {views}  
""")
        await msg.delete()
        os.remove(title)
      elif data[0] == 'audio_tt':
        title = link_data[id]['a_title'] + '.mp3'
        like = link_data[id]['like']
        comment = link_data[id]['comment']
        share = link_data[id]['share']
        views = link_data[id]['views']
        res = requests.get(link_data[id]['audio']).content
        with open(title, 'wb') as vd_file:
          vd_file.write(res)
          vd_file.close()
        await bot.edit_message_caption(chat_id=call.message.chat.id,message_id=call.message.id,caption=f"📤 **Mengunggah Hasil**\n{title}")
        await call.message.reply_video(open(title,"rb"),thumb=link_data[id]['thumb'],caption=f"""
{title}

👍: {like}  🔁: {share}  💬: {comment}   👀: {views}  
""")
        await call.message.delete()
        os.remove(title) 
    else:
      await call.answer("Bukan buat lu!",True)
  except Exception as e:
    pass
    #await call.answer("Timeout Callback data!",True)
