from pyrogram import Client
from telegraph import Telegraph,upload_file
from typing import List

  
class MyClient(Client):
  async def create_graph(self, title: str, content):
    telegraph = Telegraph()
    telegraph.create_account(short_name='my_account')

    if isinstance(content, str):  # jika content berupa path file
      with open(content, "rb") as f:
        file_bytes = f.read()
      image_url = upload_file(file_bytes)
      html_content = f'<img src="{image_url.link}"/>'
    else:
      html_content = content

    page = telegraph.create_page(title=title, html_content=html_content)
    return page['url']

