import os 
from pyrogram import Client 

ID = os.env['API_ID']
HASH = os.env['API_HASH']
TOKEN = os.env['BOT_TOKEN']

bot = Client('Asta-Robot',
             api_id=ID,
             api_hash=HASH,
             bot_token=TOKEN,
             in_memory=True
            )
