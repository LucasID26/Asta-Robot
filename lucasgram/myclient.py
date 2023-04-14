from pyrogram import Client

from .method.graph import CreateTextGraph
  
class MyClient(Client):
  async def CreateTextGraph(self, title: str, content: list):
    await CreateTextGraph(self, title: str, content: list)

