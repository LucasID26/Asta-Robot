from pyrogram import Client
from telegraph import Telegraph,upload_file
from typing import List

  
class MyClient(Client):
  async def create_graph(self, title: str, content):
    telegraph = Telegraph()
    telegraph.create_account(short_name='my_account')

    if isinstance(content, str):
      with open(content, 'rb') as f:
        img = f.read()
      image_url = upload_image(img)
      html_content = f'<img src="{image_url}"/>'
    elif isinstance(content, str):  # jika content berupa teks
      html_content = content
    else:
      raise ValueError('Content harus berupa teks atau path file')

    page = telegraph.create_page(title=title, html_content=html_content)
    return page['url']
