from pyrogram import Client
from telegraph import Telegraph
  
class MyClient(Client):
  #FUN
  async def CreateTextGraph(self, title: str, content: list):
    telegraph = Telegraph()
    telegraph.create_account(short_name='my_account')
    page = telegraph.create_page(title=title, html_content=''.join(content))
    return page['url']
