from pyrogram import Client

from .method import graph
  
class MyClient(Client):
  async def CreateTextGraph(self, title: str, content: list):
    await graph.CreateTextGraph(self, title: str, content: list)

