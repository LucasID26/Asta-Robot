from pyrogram import Client
import os
import importlib
from . import methods


class MyClient(Client):
  async def create_text_graph(self, title: str, content: list):
    return await CreateTextGraph(title, content)
  async def get_top_sender(self, chat_id):
    return await GetTopSender(self, chat_id)
  async def send_table(self, chat_id: int, data, caption: str, message_thread_id: int):
    return await SendTable(self, chat_id, data, caption, message_thread_id)

