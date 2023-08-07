from pyrogram import filters 
from pyrogram.errors import ChatForwardsRestricted, UserNotParticipant
from config import asisstant,botasupan,own,CH_DB,SUBS_ID,CH_SHARE
from urllib.parse import urlparse
import os
import asyncio
import base64
import re 
import random
from pyrogram.enums import ChatMemberStatus 
from pykeyboard import InlineButton, InlineKeyboard 


data_antrian = asyncio.Queue()
status_antrian = False
list_text = {}

@asisstant.on_message(filters.chat([-1001549051935,-1001892232448,-1001366229535,1928677026]))
async def sharing(client,m):
  global status_antrian
  
  text = m.text or m.caption
  url_pattern = re.compile(r'https?://\S+')
  urls = url_pattern.findall(text)
  teks = re.sub(url_pattern, '', text)
  kalimat = "\n".join([line for line in teks.splitlines() if line.strip() != ""])
  
  for url in urls:
    if urlparse(url).path in ['/ADITXROBOT','/SATUNUSAOFFICIAL_BOT','/aditygy_bot','/B4CKUP_BOT','/B0KEPHIJABINDO_BOT']:
      split_url = urlparse(url).query.split("=")[1]
      query = f"/start {split_url}"
      bott = str(urlparse(url).path.replace('/',''))
      await data_antrian.put((bott, query, kalimat))
  if status_antrian == False:
    status_antrian = True
    await is_antri()
  else:
    pass 


async def is_antri():
  jumlah = 0
  while not data_antrian.empty():
    bott,query,pesan = await data_antrian.get() 
    list_text = {'pesan': pesan}
    await asisstant.send_message(bott,query)
    await asyncio.sleep(5)
    async for message in asisstant.get_chat_history(bott,limit=1):
      if message.video:
        try:
          id = message.video.file_id
          await asisstant.send_video(CH_DB,video=id)
        except ChatForwardsRestricted:
          thumb = await asisstant.download_media(message.video.thumbs[0].file_id)
          vd = await asisstant.download_media(message.video.file_id)
          await asisstant.send_video(CH_DB,video=vd,thumb=thumb)  
        await asisstant.delete_messages(chat_id=bott,message_ids=message.id)
        del list_text["pesan"]        
        jumlah += 1
        try:
          os.remove(vd)
          os.remove(thumb)
        except:
          pass 
  
  if data_antrian.empty():
    status_antrian = False
    await asisstant.send_message(1928677026,f'**Berhasil mengirim {jumlah} video ke Channel DATABASE**')
  list_text.clear()
    

@botasupan.on_message(filters.chat(CH_DB))
async def get_asupan(client,m):
  global list_text
  msg_id = m.id
  string = f"{msg_id}|{m.chat.id}"
  string_bytes = string.encode("ascii")
  base64_bytes = base64.urlsafe_b64encode(string_bytes)
  base64_string = (base64_bytes.decode("ascii")).strip("=")
  link = f"https://t.me/{(await botasupan.get_me()).username}?start={base64_string}"
  caption = "❤️ JANGAN LUPA TAP LOVE NYA\n✅ DAN BERGABUNG DISINI" if not list_text else list_text['pesan']
  msg = f"{link}\n\n{caption}"
  await botasupan.send_photo(CH_SHARE,photo=open("Asta/source/photo_asupan.jpg","rb"),caption=msg)
  

@botasupan.on_message(filters.command('start') & filters.private)
async def start_asupan(client,m):
  if len(m.command) == 1:
    button = InlineKeyboard(row_width=2)
    button.add(
      InlineButton(
      'CHANNEL',url="https://t.me/YoiID_267"),
      InlineButton(
      'CHANNEL',url="https://t.me/YoiAsupan"),
      InlineButton(
      'GROUP',url="https://t.me/+GOZFVyKIOXQxN2Jl"))
    return await m.reply(f"""
Hallo {m.from_user.mention}
Anda harus bergabung di Channel/Grup saya Terlebih dahulu untuk Melihat File yang saya Bagikan

Silakan Join Ke Channel & Group Terlebih Dahulu   
""",reply_markup=button)
  user_id = m.from_user.id 
  subs = 0
  for id in SUBS_ID.split(" "):
    try:
      member = await botasupan.get_chat_member(int(id),user_id) 
      if not member.status in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
       subs += 1
    except UserNotParticipant:
      subs += 1
  text = m.text
  if subs == 0:
    msg = await m.reply("<code>Tunggu Sebentar. . .</code>")
    try:
      base64_string = text.split(" ",1)[1]
      string = await encode(base64_string)
      get_id = string.split("|",1)
      await msg.delete() 
      await botasupan.copy_message(m.chat.id,int(get_id[1]),int(get_id[0]))
    except:
      await msg.edit("TIDAK ADA VIDEO DENGAN ID TERSEBUT!")
  else:
    base64_string = text.split(" ",1)
    try:
      button = InlineKeyboard(row_width=2)
      button.add(
      InlineButton(
      'CHANNEL',url="https://t.me/YoiID_267"),
      InlineButton(
      'CHANNEL',url="https://t.me/YoiAsupan"),
      InlineButton(
      'GROUP',url="https://t.me/+GOZFVyKIOXQxN2Jl"))
      button.row(
      InlineButton("COBA LAGI",url=f"https://t.me/YoiAsupanbot?start={base64_string[1]}"))
      
      await m.reply(f"""
Hallo {m.from_user.mention}
Anda harus bergabung di Channel/Grup saya Terlebih dahulu untuk Melihat File yang saya Bagikan

Silakan Join Ke Channel & Group Terlebih Dahulu   
""",reply_markup=button)
      
    except Exception as e:
      print(e)
      await m.reply("TIDAK ADA VIDEO DENGAN ID TERSEBUT!")
    
      
  
async def encode(base64_string):
  base64_string = base64_string.strip("=")
  base64_bytes = (base64_string + "=" * (-len(base64_string) % 4)).encode("ascii")
  string_bytes = base64.urlsafe_b64decode(base64_bytes) 
  string = string_bytes.decode("ascii")
  return string 


@asisstant.on_message(filters.private & ~filters.bot & ~filters.user(own)) 
async def asisstant_cek_join(client,m):
  user_id = m.from_user.id
  try:
    return await client.get_chat_member(-1001756630661,user_id)
  except UserNotParticipant:
    msg = "ih kamu belum join yaa join dulu disini {}","Mending join disini {}"," join dlu atuh {}","{} Join dulu awas aja ga join"
    msg1 = random.choice(msg)
    await m.reply(msg1.format("@YoiAsupan"))




