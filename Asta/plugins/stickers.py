import os
import asyncio
import requests
from bs4 import BeautifulSoup as BS
from config import bot,asisstant,prefix
from pyrogram import filters,emoji
from pyrogram.errors import StickersetInvalid, YouBlockedUser
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName
from pyrogram.enums import ParseMode


from Asta.func.tools import get_arg,get_text,resize_media
from Asta.decorators.info_cmd import info_cmd
from Asta.decorators.cek_admin import bot_admin
from Asta.decorators.error import error

@bot.on_message(filters.command(["addsticker", "tikel", "kang"],prefix))
@info_cmd
@bot_admin
@error
async def kang(client,m):
  user = m.from_user
  replied = m.reply_to_message
  Asta = await m.reply_text("`Menambahkan sticker ke sticker pack mu...`")
  media_ = None
  emoji_ = None
  is_anim = False
  is_video = False
  resize = False
  ff_vid = False
  if replied and replied.media:
    if replied.photo:
      resize = True
    elif replied.document and "image" in replied.document.mime_type:
      resize = True
      replied.document.file_name
    elif replied.document and "tgsticker" in replied.document.mime_type:
      is_anim = True
      replied.document.file_name
    elif replied.document and "video" in replied.document.mime_type:
      resize = True
      is_video = True
      ff_vid = True
    elif replied.animation:
      resize = True
      is_video = True
      ff_vid = True
    elif replied.video:
      resize = True
      is_video = True
      ff_vid = True
    elif replied.sticker:
      if not replied.sticker.file_name:
        return await Asta.edit("**Stiker tidak memiliki Nama!**")
      emoji_ = replied.sticker.emoji
      is_anim = replied.sticker.is_animated
      is_video = replied.sticker.is_video
      if not (
                replied.sticker.file_name.endswith(".tgs")
                or replied.sticker.file_name.endswith(".webm")
            ):
        resize = True
        ff_vid = True
    else:
      return await Asta.edit("**File Tidak Didukung**")
    media_ = await bot.download_media(replied, file_name="Asta/downloads/")
  else:
    return await Asta.edit("**Silahkan Reply ke Media Foto/GIF/Sticker!**")
  if media_:
    args = get_arg(m)
    pack = 1
    if len(args) == 2:
      emoji_, pack = args
    elif len(args) == 1:
      if args[0].isnumeric():
        pack = int(args[0])
      else:
        emoji_ = args[0]

    if emoji_ and emoji_ not in (
            getattr(emoji, _) for _ in dir(emoji) if not _.startswith("_")
        ):
      emoji_ = None
    if not emoji_:
      emoji_ = "✨"

    #u_name = user.username
    u_name = user.first_name
    packname = f"Sticker_u{user.id}_v{pack}"
    custom_packnick = f"{u_name} Sticker Pack"
    packnick = f"{custom_packnick} Vol.{pack}"
    cmd = "/newpack"
    if resize:
      media_ = await resize_media(media_, is_video, ff_vid)
    if is_anim:
      packname += "_animated"
      packnick += " (Animated)"
      cmd = "/newanimated"
    if is_video:
      packname += "_video"
      packnick += " (Video)"
      cmd = "/newvideo"
    exist = False
    while True:
      try:
        exist = await asisstant.invoke(
                    GetStickerSet(
                        stickerset=InputStickerSetShortName(short_name=packname), hash=0
                    )
                )
      except StickersetInvalid:
        exist = False
        break
      limit = 50 if (is_video or is_anim) else 120
      if exist.set.count >= limit:
        pack += 1
        packname = f"a{user.id}_by_userge_{pack}"
        packnick = f"{custom_packnick} Vol.{pack}"
        if is_anim:
          packname += f"_anim{pack}"
          packnick += f" (Animated){pack}"
        if is_video:
          packname += f"_video{pack}"
          packnick += f" (Video){pack}"
        await Asta.edit(
                    f"`Membuat Sticker Pack Baru {pack} Karena Sticker Pack Sudah Penuh`"
                )
        continue
      break
    if exist is not False:
      try:
        await asisstant.send_message("stickers", "/addsticker")
      except YouBlockedUser:
        await asisstant.unblock_user("stickers")
        await asisstant.send_message("stickers", "/addsticker")
      except Exception as e:
        return await Asta.edit(f"**ERROR:** `{e}`")
      await asyncio.sleep(2)
      await asisstant.send_message("stickers", packname)
      await asyncio.sleep(2)
      limit = "50" if is_anim else "120"
      while limit in await get_response(m, asisstant):
        pack += 1
        packname = f"a{user.id}_by_{user.username}_{pack}"
        packnick = f"{custom_packnick} vol.{pack}"
        if is_anim:
          packname += "_anim"
          packnick += " (Animated)"
        if is_video:
          packname += "_video"
          packnick += " (Video)"
        await Asta.edit(
                    "`Membuat Sticker Pack Baru "
                    + str(pack)
                    + " Karena Sticker Pack Sudah Penuh`"
                )
        await asisstant.send_message("stickers", packname)
        await asyncio.sleep(2)
        if await get_response(m, asisstant) == "Invalid pack selected.":
          await asisstant.send_message("stickers", cmd)
          await asyncio.sleep(2)
          await asisstant.send_message("stickers", packnick)
          await asyncio.sleep(2)
          await asisstant.send_document("stickers", media_)
          await asyncio.sleep(2)
          await asisstant.send_message("Stickers", emoji_)
          await asyncio.sleep(2)
          await asisstant.send_message("Stickers", "/publish")
          await asyncio.sleep(2)
          if is_anim:
              await asisstant.send_message(
                            "Stickers", f"<{packnick}>", parse_mode=ParseMode.MARKDOWN
                        )
              await asyncio.sleep(2)
          await asisstant.send_message("Stickers", "/skip")
          await asyncio.sleep(2)
          await asisstant.send_message("Stickers", packname)
          await asyncio.sleep(2)
          return await Asta.edit(
                        f"**Sticker Berhasil Ditambahkan!**\n         🔥 **[KLIK DISINI](https://t.me/addstickers/{packname})** 🔥\n**Untuk Menggunakan Stickers**"
                    )
      await asisstant.send_document("stickers", media_)
      await asyncio.sleep(2)
      if (
                await get_response(m, asisstant)
                == "Sorry, the file type is invalid."
            ):
        return await Asta.edit(
                    "**Gagal Menambahkan Sticker, Gunakan @Stickers Bot Untuk Menambahkan Sticker Anda.**"
                )
      await asisstant.send_message("Stickers", emoji_)
      await asyncio.sleep(2)
      await asisstant.send_message("Stickers", "/done")
    else:
      await Asta.edit("`Membuat Sticker Pack Baru`")
      try:
        await asisstant.send_message("Stickers", cmd)
      except YouBlockedUser:
        await asisstant.unblock_user("stickers")
        await asisstant.send_message("stickers", "/addsticker")
      await asyncio.sleep(2)
      await asisstant.send_message("Stickers", packnick)
      await asyncio.sleep(2)
      await asisstant.send_document("stickers", media_)
      await asyncio.sleep(2)
      if (
                await get_response(m, asisstant)
                == "Sorry, the file type is invalid."
            ):
        return await Asta.edit(
                    "**Gagal Menambahkan Sticker, Gunakan @Stickers Bot Untuk Menambahkan Sticker Anda.**"
                )
      await asisstant.send_message("Stickers", emoji_)
      await asyncio.sleep(2)
      await asisstant.send_message("Stickers", "/publish")
      await asyncio.sleep(2)
      if is_anim:
          await asisstant.send_message("Stickers", f"<{packnick}>")
          await asyncio.sleep(2)
      await asisstant.send_message("Stickers", "/skip")
      await asyncio.sleep(2)
      await asisstant.send_message("Stickers", packname)
      await asyncio.sleep(2)
    await Asta.edit(
            f"**Sticker Berhasil Ditambahkan!**\n         🔥 **[KLIK DISINI](https://t.me/addstickers/{packname})** 🔥\n**Untuk Menggunakan Stickers**"
        )
    if os.path.exists(str(media_)):
      os.remove(media_)

async def get_response(m, asisstant):
    return [x async for x in asisstant.get_chat_history("Stickers", limit=1)][0].text



@bot.on_message(filters.command(['unkang','delsticker'],prefix))
@info_cmd
@bot_admin
@error
async def unkang(client,m):
  if not m.reply_to_message:
    return await m.reply_text("Silahkan reply sticker yang mau dihapus,pastikan reply sticker dari pesan mu sendiri")
  replied = m.reply_to_message
  Asta = await m.reply_text("`Menghapus sticker dari sticker pack mu . . .`")
  if replied.sticker:
    try:
      await asisstant.send_message("stickers", "/delsticker")
    except YouBlockedUser:
      await asisstant.unblock_user("stickers")
      await asisstant.send_message("stickers", "/delsticker")
    except Exception as e:
      return await Asta.edit(f"**ERROR:** `{e}`")
    await asyncio.sleep(2)
    packname = replied.sticker.set_name
    if not packname:
      return await Asta.edit("Sticker tidak terdaftar dalam pack manapun")
    await asisstant.send_message("stickers",packname)
    await asyncio.sleep(2)
    if await get_response(m, asisstant) == "Invalid set selected.":
      return await Asta.edit("Wow kamu mau hapus sticker ini dari sticker pack orang lain?")
    elif int(packname.split("_u")[1].split("_v")[0]) != int(m.from_user.id):
      await asisstant.send_message("stickers",'/cancel')
      return await Asta.edit("Wow kamu mau hapus sticker ini dari sticker pack orang lain?")
    await asisstant.forward_messages("stickers",from_chat_id=m.chat.id,message_ids=m.reply_to_message.id)
    await asyncio.sleep(2)
    if await get_response(m, asisstant) == "This is the last sticker in this set. Deleting it will also delete the set and free its link. Are you sure you want to do this?":
      await asisstant.send_message("stickers",'Delete anyway')
      await asyncio.sleep(2)
      if await get_response(m, asisstant) == "Done! The sticker set is gone.":
        return await Asta.edit(f"**Sticker Berhasil Dihapus!**\n         🔥 **[KLIK DISINI](https://t.me/addstickers/{packname})** 🔥\n**Untuk Menggunakan Stickers**")
    elif await get_response(m, asisstant) == "I have deleted that sticker for you, it will stop being available to Telegram users within an hour.":
      return await Asta.edit(f"**Sticker Berhasil Dihapus!**\n         🔥 **[KLIK DISINI](https://t.me/addstickers/{packname})** 🔥\n**Untuk Menggunakan Stickers**")
    elif await get_response(m, asisstant) == "Sorry, I can't do this. Looks like you are not the owner of the relevant set.":
      return await Asta.edit("Saya mendeteksi bahwa id sticker itu tidak ada dalam sticker pack mu")
    elif await get_response(m, asisstant) == "Please send me the sticker.":
      await asisstant.send_message("stickers",'/cancel')
      return await Asta.edit("Hmm sticker itu tidak ada dalam sticker pack mu!!")
  else:
    return await Asta.edit("**Silahkan Reply ke Sticker!**")



@bot.on_message(filters.command(["packinfo", "stickerinfo"],prefix))
@info_cmd
@bot_admin
@error
async def packinfo(client,m):
  rep = await m.reply("`Processing...`")
  if not m.reply_to_message:
    await rep.edit("Silahkan Reply ke Sticker...")
    return
  if not m.reply_to_message.sticker:
    await rep.edit("Silahkan Reply ke Sticker...")
    return
  if not m.reply_to_message.sticker.set_name:
    await rep.edit("`Sepertinya Sticker Liar!`")
    return
  stickerset = await asisstant.invoke(
        GetStickerSet(
            stickerset=InputStickerSetShortName(
                short_name=m.reply_to_message.sticker.set_name
            ),
            hash=0,
        )
    )
  emojis = []
  for stucker in stickerset.packs:
    if stucker.emoticon not in emojis:
      emojis.append(stucker.emoticon)
  output = f"""**Sticker Pack Title **: `{stickerset.set.title}`
**Sticker Pack Short Name **: `{stickerset.set.short_name}`
**Stickers Count **: `{stickerset.set.count}`
**Archived **: `{stickerset.set.archived}`
**Official **: `{stickerset.set.official}`
**Masks **: `{stickerset.set.masks}`
**Animated **: `{stickerset.set.animated}`
**Emojis In Pack **: `{' '.join(emojis)}`
"""
  await rep.edit(output)



@bot.on_message(filters.command("stickers", prefix))
async def cb_sticker(client,m):
  query = get_text(m)
  if not query:
    return await m.reply("**Masukan Nama Sticker Pack!**")
  xx = await m.reply("`Searching sticker packs...`")
  text = requests.get(f"https://combot.org/telegram/stickers?q={query}").text
  soup = BS(text, "lxml")
  results = soup.find_all("div", {"class": "sticker-pack__header"})
  if not results:
    return await xx.edit("**Tidak Dapat Menemukan Sticker Pack 🥺**")
  reply = f"**Keyword Sticker Pack:**\n {query}\n\n**Hasil:**\n"
  for pack in results:
    if pack.button:
      packtitle = (pack.find("div", "sticker-pack__title")).get_text()
      packlink = (pack.a).get("href")
      reply += f" •  [{packtitle}]({packlink})\n"
  await xx.edit(reply)
