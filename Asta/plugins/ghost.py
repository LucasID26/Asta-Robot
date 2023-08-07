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

#DEL ACCOUNT TERHAPUS 
@bot.on_message(filters.command(["clean","ghost"],prefix) & ~filters.private)
@info_cmd
@no_private
@bot_admin
@admins_only
@error
async def remove(client, message):
   global stopProcess
   try: 
     bott = await bot.get_chat_member(message.chat.id, "self")
     if bott.status == ChatMemberStatus.MEMBER:
       await message.reply(text="🕹 | Jadiin gw admin dong biar bisa hapus akun terhapus",quote=True)
     else:  
       if len(chatQueue) > 5 :
         await message.reply(text="⛔️ | Saya sudah mengerjakan jumlah maksimal 5 obrolan saya saat ini. Coba lagi sebentar lagi.",quote=True)
       else:  
         if message.chat.id in chatQueue:
           await message.reply(text="🚫 | Sudah ada proses yang sedang berlangsung dalam obrolan ini.",quote=True)
         else:  
           chatQueue.append(message.chat.id)  
           deletedList = []
           async for member in bot.get_chat_members(message.chat.id):
             if member.user.is_deleted == True:
               deletedList.append(member.user)
             else:
               pass
           lenDeletedList = len(deletedList)  
           if lenDeletedList == 0:
             await message.reply(text="👻 | Tidak ada akun terhapus dalam obrolan ini.",quote=True)
             chatQueue.remove(message.chat.id)
           else:
             msg = await message.reply("__Prosess ban akun terhapus! __")
             k = 0
             processTime = lenDeletedList*2
             temp = await msg.edit(text=f"🚨 | Jumlah dari {lenDeletedList} akun terhapus telah terdeteksi.\n⏳ | Perkiraan waktu: {processTime} detik dari sekarang.")
             if stopProcess: stopProcess = False
             while len(deletedList) > 0 and not stopProcess:   
               deletedAccount = deletedList.pop(0)
               try:
                 await bot.ban_chat_member(message.chat.id, deletedAccount.id)
               except Exception:
                 pass  
               k+=1
               await asyncio.sleep(2)
             if k == lenDeletedList:  
               await msg.edit(text=f"✅ | Berhasil menghapus semua akun terhapus dari obrolan ini.")  
             else:
               await message.reply(f"✅ | Berhasil menghapus {k} akun terhapus dari obrolan ini.",quote=True)  
             chatQueue.remove(message.chat.id)
   except FloodWait as e:
     await asyncio.sleep(e.value) 



