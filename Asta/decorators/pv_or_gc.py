from functools import wraps


def no_private(func):
  @wraps(func)
  async def pv(client,m,*args,**kwargs):
    if m.chat.type.value == 'private':
      return await m.reply_text("Perintah ini dibuat untuk digunakan di obrolan grup, bukan di pm!",quote=True)
    else:
      return await func(client, m, *args, **kwargs)
  return pv

def no_group(func):
  @wraps(func)
  async def pv(client,m,*args,**kwargs):
    if m.chat.type.value != 'private':
      return await m.reply_text("Perintah ini dibuat untuk digunakan di pm, bukan di obrolan group!",quote=True)
    else:
      return await func(client, m, *args, **kwargs)
  return pv
