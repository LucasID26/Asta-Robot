import os 
from pyrogram import Client 

ID = os.environ['API_ID']
HASH = os.environ['API_HASH']
TOKEN = os.environ['BOT_TOKEN']

bot = Client('Asta-Robot',
             api_id=ID,
             api_hash=HASH,
             bot_token=TOKEN,
             in_memory=True
            )
