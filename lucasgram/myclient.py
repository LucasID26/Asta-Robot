from pyrogram import Client
from telegraph import Telegraph,upload_file
from typing import List

class MyClient(Client):
  async def create_graph(self, title: str, content: str, photo_path: str = None):
    telegraph = Telegraph()
    telegraph.create_account(short_name='my_account')

    if photo_path:
      with open(photo_path, 'rb') as file:
        photo_url = upload_file(file)['src']
      content.insert(0, f'<img src="{photo_url}"/>')

    html_content = ''.join(content)

    page = telegraph.create_page(title=title, html_content=html_content)
    return page['url']
