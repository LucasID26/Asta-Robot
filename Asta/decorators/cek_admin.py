from functools import wraps
from config import bot,own 


def admins_only(func):
  @wraps(func)
  async def admins(client,m,*args,**kwargs): 
    if m.from_user.id in own:
      return await func(client, m, *args, **kwargs)
    if m.chat.type.value == 'private':
      return await func(client,m,*args,**kwargs) 
    else:
      admin = await bot.get_chat_member(m.chat.id,m.from_user.id)
      if admin.status.value in ['owner','administrator']:
        return await func(client, m, *args, **kwargs)
      else:
        return await m.reply_text("Anda harus menjadi admin untuk melakukan ini.")
  return admins
