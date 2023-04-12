from config import bot,prefix
from pyrogram import filters
from pyrogram.errors import FloodWait
from pyrogram.enums import ChatMemberStatus
import asyncio


from Asta.decorators.cek_admin import admins_only,bot_admin
from Asta.decorators.pv_or_gc import no_private
from Asta.decorators.info_cmd import info_cmd
from Asta.decorators.error import error

chatQueue = []

stopProcess = False

#TAG ALL
@bot.on_message(filters.command("all",prefix)) 
@info_cmd
@no_private
@bot_admin
@admins_only
@error
async def everyone(client, m):
  global stopProcess  
  try:
    bott = await bot.get_chat_member(m.chat.id, "self")
    if bott.status == ChatMemberStatus.MEMBER:
      return await m.reply(text="🕹 | Jadiin gw admin dong biar bisa tag all",quote=True)
    if len(chatQueue) > 5:
      await m.reply(text="⛔️ | Saya sudah mengerjakan jumlah maksimal 5 obrolan saya saat ini. Coba lagi sebentar lagi.")
    else:  
      if m.chat.id in chatQueue:
        await m.reply(text="🚫 | Lagi tag all ini anj.",quote=True)
      else:  
        chatQueue.append(m.chat.id)
        if len(m.command) > 1:
          inputText = m.text.split(" ",1]
        elif len(m.command) == 1:
          inputText = "@all"    
        membersList = []
        async for member in bot.get_chat_members(m.chat.id):
          if member.user.is_bot == True:
            pass
          elif member.user.is_deleted == True:
            pass
          else:
            membersList.append(member.user)
        i = 0
        lenMembersList = len(membersList)
        if stopProcess: stopProcess = False
        while len(membersList) > 0 and not stopProcess :
          j = 0
          text1 = f"{inputText}\n\n"
          try:    
            while j < 10:
              user = membersList.pop(0)
              if user.username == None:
                text1 += f"{user.mention} "
                j+=1
              else:
                text1 += f"@{user.username} "
                j+=1
            try:
              if m.chat.is_forum == True:
                await bot.send_message(m.chat.id, text1, message_thread_id=m.topics.id)
              else:
                await bot.send_message(m.chat.id, text1)
            except Exception:
              pass  
            await asyncio.sleep(10) 
            i+=10
          except IndexError:
            try:
              if m.chat.is_forum == True:
                await bot.send_message(m.chat.id, text1, message_thread_id=m.topics.id)
              else:
                await bot.send_message(m.chat.id, text1)  
            except Exception:
              pass  
            i = i+j
        if i == lenMembersList:
          if m.chat.is_forum == True: 
            await bot.send_message(m.chat.id,f"✅ | Sukses mention **total keseluruhan {i} member**.\n❌ | Bot dan akun terhapus tidak diikut sertakan.",message_thread_id=m.topics.id) 
          else:
            await bot.send_message(m.chat.id,f"✅ | Sukses mention **total keseluruhan {i} member**.\n❌ | Bot dan akun terhapus tidak diikut sertakan.") 
        else:
          if m.chat.is_forum == True:
            await bot.send_message(m.chat.id,f"✅ | Sukses mention **{i} member.**\n❌ | Bot dan akun terhapus tidak diikut sertakan.",message_thread_id=m.topics.id) 
          else:
            await bot.send_message(m.chat.id,f"✅ | Sukses mention **{i} member.**\n❌ | Bot dan akun terhapus tidak diikut sertakan.") 
        chatQueue.remove(m.chat.id)
  except FloodWait as e:
    await asyncio.sleep(e.value) 

#STOP TAGG ALL
@bot.on_message(filters.command("stop",prefix))
@info_cmd
@no_private
@bot_admin
@admins_only
@error
async def stop(client, m):
  global stopProcess
  try:
    if not m.chat.id in chatQueue:
      await m.reply(text="🤷🏻‍♀️ | Tidak ada proses yang berkelanjutan untuk dihentikan.",quote=True)
    else:
      stopProcess = True
      await m.reply(text="🛑 | Stop proses.",quote=True)
  except FloodWait as e:
    await asyncio.sleep(e.value)





 
