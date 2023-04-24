from pyrogram import Client
import os
import importlib
from . import methods


class MyClient(Client):
  async def create_text_graph(self, title: str, content: list):
    return await CreateTextGraph(title, content)
  async def get_top_sender(self, chat_id):
    return await GetTopSender(self, chat_id)
  async def send_table(self, chat_id: int, data, caption: str = None, message_thread_id: int = None):
    return await SendTable(self, chat_id, data, caption, message_thread_id)
  async def get_top_admins(self, chat_id):
    return await GetTopAdmins(self, chat_id)
