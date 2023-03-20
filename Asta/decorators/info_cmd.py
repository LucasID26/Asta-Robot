from functools import wraps
from config import bot,own
from datetime import datetime 
from pytz import timezone
from pyrogram import Client


t_zona= datetime.now(tz=timezone('Asia/Makassar')) 
hari = t_zona.strftime("%A")
tgl = t_zona.strftime("%d/%B/%Y")
jam = t_zona.strftime("%H:%M:%S")



def info_cmd(func):
  @wraps(func)
  async def cmd(client,m,*args,**kwargs):
    user = m.from_user.mention
    cmd1 = m.command
    text = f"**Informasi Bot CMD:**\n"
    if m.from_user.id in own:
      return await func(client,m,*args,**kwargs)
    if m.chat.type.value == 'private':
      text += f"""
**Chat type {m.chat.type.value}**
**From:** {user}
**Hari:** `{hari}`
**TGL:** `{tgl}`
**Jam:** `{jam}`
**Perintah:** `{cmd1}`
"""     
      await bot.send_message(-1001738215280,text)
      return await func(client,m,*args,**kwargs)
   
    else:
      chtid = str(m.chat.id)[4:]
      title = m.chat.title
      msg_id = m.id
      if m.chat.is_forum == True:
        thread_id = m.topics.id
        link_id = f"https://t.me/c/{chtid}/{thread_id}/{msg_id}"
      else:
        link_id = f"https://t.me/c/{chtid}/{msg_id}"

      text += f"""
**Chat type {m.chat.type.value}**
**Group:** {title}
**Pesan:** <a href={link_id}>click</a>
**From:** {user}
**Hari:** `{hari}`
**TGL:** `{tgl}`
**Jam:** `{jam}`
**Perintah:** `{cmd}`
"""
      await bot.send_message(-1001738215280,text)
