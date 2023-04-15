from pyrogram import Client
import os
import importlib
from functools import partial



class MyClient(Client):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    methods_dir = "lucasgram/methods"

    for filename in os.listdir(methods_dir):
      if filename.endswith(".py"):
        module_name = filename[:-3]
        module = importlib.import_module(f"{methods_dir}.{module_name}")

        for name in dir(module):
          if not name.startswith("__"):
            method = getattr(module, name)
            setattr(self, name, partial(method, self))

