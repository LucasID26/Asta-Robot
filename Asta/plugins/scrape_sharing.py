from pyrogram import filters
from config import asisstant
from urllib.parse import urlparse

import asyncio

@asisstant.on_message(filters.chat(-1001519186585))
async def sharing(client,m):
  text = m.text
  urls = []
  words = text.split()
  for word in words:
    url_components = urlparse(word)
    if url_components.scheme and url_components.netloc:
      urls.append(word)
  for url in urls:
    if urlparse(url).path in ['/ADITXROBOT']:
      split_url = urlparse(url).query.split("=")[1]
      query = f"/start {split_url}"
      bot = str(urlparse(url).path.replace('/',''))
      await asisstant.send_message(bot,query)
      await asyncio.sleep(5)
      async for message in asisstant.get_chat_history(bot,limit=1):
        if message.video:
          id = message.video.file_id
          await asisstant.send_video("@aslibukansuci",video=id)
