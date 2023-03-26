import os
import asyncio
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

@bot.on_message(filters.command(["tikel", "kang"],prefix))
@info_cmd
@bot_admin
@error
async def kang(client,m):
  user = m.from_user
  replied = m.reply_to_message
  rep = m if replied.from_user.is_bot == True else replied
  Asta = await rep.reply_text("`Boleh juga ni stickernya colong ahh...`")
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
    args = get_arg(message)
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

    u_name = user.username
    u_name = "@" + u_name if u_name else user.first_name or user.id
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
        exist = await bot.invoke(
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
