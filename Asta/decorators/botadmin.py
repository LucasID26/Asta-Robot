from functools import wraps


def bot_admin(func):
  @wraps(func)
  async def admins(client,m,*args,**kwargs):
    imbot = await bot.get_me()
    idbot = imbot.id
    if m.from_user.id in own:
      return await func(client,m,*args,**kwargs)
    if m.chat.type.value == 'private':
      return await func(client,m,*args,**kwargs) 
    else:
      infobot = await bot.get_chat_member(m.chat.id,idbot)
      if infobot.status.value in ['owner','administrator']:
        return await func(client,m,*args,**kwargs)
      else:
        return await m.reply_text("Saya harus menjadi admin untuk menjalankan perintah ini.")
  return admins
