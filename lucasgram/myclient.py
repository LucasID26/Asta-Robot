from pyrogram import Client
from telegraph import Telegraph,upload_file
from typing import List

  
class MyClient(Client):
  async def create_graph(self, title: str, content):
    telegraph = Telegraph()
    telegraph.create_account(short_name='my_account')

    if isinstance(content, str):  # jika content berupa path file
      with open(content, 'rb') as f:
        #img = f.read()
        image_url = upload_file(f)
      html_content = f'<img src="{image_url}"/>'
    elif isinstance(content, bytes):  # jika content berupa bytes/file
      html_content = f'<img src="{upload_file(content)}"/>'
    else:
      html_content = content

    page = telegraph.create_page(title=title, html_content=html_content)
    return page['url']

