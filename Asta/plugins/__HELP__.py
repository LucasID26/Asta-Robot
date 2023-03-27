from config import bot ,own, prefix
from pyrogram import filters 
from pykeyboard import InlineButton, InlineKeyboard 


from Asta.decorators.info_cmd import info_cmd

@bot.on_message(filters.command(["help","start"],prefix))
@info_cmd
async def helpp(client, m):
  if m.chat.type.value != 'private':
    button = InlineKeyboard(row_width=2)
    button.add(
      InlineButton(
      'HELP❓',url=f'https://t.me/{bot.me.username}?start=help'),
      InlineButton(
        'OWNER👤',url='https://t.me/LucasBukanKalengSarden'),
      InlineButton(
      'CHANNEL',url='https://t.me/YoiID_robot'))
    await m.reply_text(f'**Yo hallo saya adalah {bot.me.first_name}\nJika ingin mengetahui fitur saya silahkan tekan tombol help dibawah!**', reply_markup=button)
  elif m.chat.type.value == 'private':
    button = InlineKeyboard(row_width=3)
    button.add(
      InlineButton(
        'PERINTAH📚',callback_data='help'),
      InlineButton(
        'OWNER👤',url='https://t.me/LucasBukanKalengSarden'),
      InlineButton(
      'CHANNEL',url='https://t.me/YoiID_robot'),
      InlineButton(
        'Add to your group',url=f'http://t.me/{bot.me.username}?startgroup=true'
      ))
    await m.reply_text(f'**Yo hallo saya adalah {bot.me.first_name}\nJika ingin mengetahui fitur saya silahkan tekan tombol help dibawah!**', reply_markup=button)

    
    
#filters.regex(pattern=(r"help | admin")
@bot.on_callback_query(group=1)
async def def_callback(_, call):
  if call.data == 'help1':
    button = InlineKeyboard(row_width=3)
    button.add(
      InlineButton('PERINTAH📚',callback_data='help'),
      InlineButton('OWNER👤',url='https://t.me/LucasBukanKalengSarden'),
      InlineButton(
      'CHANNEL',url='https://t.me/YoiID_robot'),
      InlineButton('Add to your group',url=f'http://t.me/{bot.me.username}?startgroup=true'
      ))
    await bot.edit_message_text(call.message.chat.id,text=f'**Yo hallo saya adalah {bot.me.first_name}\nJika ingin mengetahui fitur saya silahkan tekan tombol help dibawah!**',message_id=call.message.id,reply_markup=button)
    
  elif call.data == 'help':
    button = InlineKeyboard(row_width=3)
    button.add(
    InlineButton(
      'ADMINS', callback_data='admins'),
    InlineButton(
      'FILTERS', callback_data='filters'),
    InlineButton(
      'SEARCHING',callback_data='search'),
    InlineButton(
      'GENERATOR',callback_data='generator'),
    InlineButton(
      'STICKERS',callback_data='stickers'),
    InlineButton(
      'LAINNYA',callback_data='lain'))
    button.row(InlineButton('Back', callback_data='help1')) 
    await bot.edit_message_text(call.message.chat.id, text=f"__**HELP {bot.me.first_name}**__\n\nTambahkan saya ke group mu dan jadikan saya admin supaya saya berfungsi dengan baik!.",message_id=call.message.id,reply_markup=button)


  #MANGGIL HELP
  button = InlineKeyboard()
  button.add(
    InlineButton('Back',callback_data='help'))
  if call.data == 'lain':   
    await bot.edit_message_text(call.message.chat.id, text=lain_help,message_id=call.message.id,reply_markup=button)
  elif call.data == 'filters':
    await bot.edit_message_text(call.message.chat.id, text=filter_help,message_id=call.message.id,reply_markup=button)
  elif call.data == 'search':
    await bot.edit_message_text(call.message.chat.id, text=search_help,message_id=call.message.id,reply_markup=button) 
  elif call.data == 'admins':
    await bot.edit_message_text(call.message.chat.id, text=admins_help,message_id=call.message.id,reply_markup=button)
  elif call.data == 'generator':
    await bot.edit_message_text(call.message.chat.id, text=generator_help,message_id=call.message.id,reply_markup=button)
  elif call.data == 'stickers':
    await bot.edit_message_text(call.message.chat.id, text=sticker_help,message_id=call.message.id,reply_markup=button) 
  #await bot.send_message(call.message.chat.id,f"`Tommbol Satu`",reply_to_message_id=call.message.id)



lain_help = """
**LAINNYA**

Perintah:
- /ping: Kecepatan respon bot.
- /info [reply/username]: Informasi profile user/group dan channel.
- /id: Id obrolan saat ini.
"""

filter_help = """
**FILTERS**

Jadikan obrolan Anda lebih hidup dengan filter; Bot akan membalas kata-kata tertentu!

Filter peka huruf besar/kecil; setiap kali seseorang mengatakan kata-kata pemicu Anda, Virtual Bot akan membalas! dapat digunakan untuk membuat perintah Anda sendiri, jika diinginkan.

Perintah Admin di group:
- /filter [pemicu/reply]: Setiap kali seseorang mengatakan "pemicu", bot akan membalas dengan "kalimat". Untuk beberapa filter kata, kutip pemicunya.
- /filters: Menampilkan semua filter obrolan.
- /delfilter [pemicu]: Menghentikan bot membalas "pemicu".
"""

search_help = """
**SEARCHING** 

Ingin melakukan pencarian?,module search adalah module untuk anda! 

Perintah:
- /g atau /google [query]: Pencarian google.
- /img [query]: Pencarian google image.
- /kaze [query]: Pencarian anime atau donghua dari web kazefuri.
- /donghua [query]: Pencarian donghua dari web donghua
- /lokasi [query]: Pencarian lokasi.
""" 

admins_help = """
**ADMINS**

Beberapa orang perlu dilarang secara publik; spammer, gangguan, atau hanya troll.

Modul ini memungkinkan Anda melakukannya dengan mudah, dengan memaparkan beberapa tindakan umum, sehingga semua orang akan melihatnya!

Perintah Admin:
- /ban [reply/username]: Ban pengguna.
- /dban: Melarang pengguna dengan membalas, dan menghapus pesan mereka.
- /unban [reply/username]: Unban pengguna

- /mute [reply/username]: Mute pengguna
- /dmute: Bisukan pengguna dengan membalas, dan menghapus pesan mereka.
- /unmute [reply/username]: Unmute pengguna

- /kick [reply/username]: Kick pengguna
- /dkick: Tendang pengguna dengan membalas, dan menghapus pesan mereka.

Adapun Perintah lain
- /bots: Berfungsi untuk cek ada berapa bot didalam group.
- /staff: Daftar admin dalam obrolan saat ini.
- /clean atau /ghost: Module ini berfungsi untuk mengeluarkan akun terhapus dalam group.Tidak dapat dibatalkan.
- /speedtest: Cek kecepatan jaringan bot.
- /status: Informasi detail Bot.
- /alive: Bot aktif.
""" 

#GENERATOR HELP
generator_help = """
**SESSION GENERATOR**

Ingin membuat String Sessions?,module ini adalah solusinya.
Module ini mendukung generator session Pyrogram dan Telethon.

Perintah:
- /generate: Hasilkan sesi string menggunakan bot ini atau memakai bot ini @GenerateStringYoiRobot . Hanya mendukung Pyrogram v2 dan Telethon.
- /cancel: Untuk mengehentikan.
"""

#STICKER HELP
sticker_help = """
**STICKERS**

Module ini adalah solusi bagi kalian yang ingin membuat sticker dan membuat sticker pack.
Kamu bisa membuat sticker dari TEXT,PHOTO,VIDEO,GIF

Perintah:
- /q atau /quotly [reply]: Membuat sticker dari TEXT.
- /kang [reply_media]: Membuat sticker dari PHOTO,VIDEO,GIF termasuk menyimpan sticker yang sudah dibuat ke dalam sticker pack.
- /unkang [reply_sticker]: Menghapus sticker dari sticker pack mu.
"""
