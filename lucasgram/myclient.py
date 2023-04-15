from pyrogram import Client
import os
import importlib
from . import methods


class MyClient(Client):
  async def create_text_graph(self, title: str, content: list):
    return await CreateTextGraph(title, content)
  async def get_top_sender(self, chat_id):
    return await GetTopSender(self, chat_id)

