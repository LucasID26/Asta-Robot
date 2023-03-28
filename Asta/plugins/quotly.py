import asyncio
import base64
import os
import requests
from config import bot,prefix
from pyrogram import filters

from Asta.decorators.info_cmd import info_cmd
from Asta.decorators.cek_admin import bot_admin
from Asta.decorators.error import error

@bot.on_message(filters.command(["q", "quotly"],prefix))
@info_cmd
@bot_admin
@error
async def quotly(client,m):
  if not m.reply_to_message:
    return await m.reply_text("**Mohon Balas ke Pesan**")
  if m.reply_to_message:
    if not m.reply_to_message.text:
      return await m.reply_text("**Mohon balas ke pesan text bukan media**")
    msg = await m.reply_text("`Membuat sticker . . .`")
    try:
      json_data = {
                'type': 'quote',
                'format': 'webp',
                'backgroundColor': '#1b1429',
                'width': 512,
                'height': 768,
                'scale': 2,
                'messages': [
                    {
                        'entities': [],
                        'chatId': m.chat.id,
                        'avatar': True,
                        'from': {
                            'id': m.reply_to_message.from_user.id,
                            'first_name': m.reply_to_message.from_user.first_name,
                            'last_name': m.reply_to_message.from_user.last_name,
                            'username': m.reply_to_message.from_user.username,
                            'language_code': 'id',
                            'title': m.chat.title,
                            'photo': {
                                'small_file_id': 'AQADBAADQrgxG-xw8FEAEAIAAwLRM3kABOEuO0ITTBqMAAQeBA',
                                'small_file_unique_id': 'AgADQrgxG-xw8FE',
                                'big_file_id': 'AQADBAADQrgxG-xw8FEAEAMAAwLRM3kABOEuO0ITTBqMAAQeBA',
                                'big_file_unique_id': 'AgADQrgxG-xw8FE',
                            },
                            'type': 'supergroup',
                            'name': m.reply_to_message.from_user.first_name,
                        },
                        'text': m.reply_to_message.text,
                        'replyMessage': {},
                    },
                ],
            }
      response = (requests.post('https://api.safone.me/quotly', json=json_data)).json()
      decode =base64.b64decode((response.get("image")))
      img_file ='sticker.webp', 'wb')
      img_file.write(decode)
      img_file.close()
      await m.reply_sticker(open("sticker.webp",'rb'))
      await msg.delete()
      os.remove("sticker.webp")
    except:
      return await msg.edit("**Gagal Membuat Sticker Quotly**")

