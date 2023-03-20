import traceback
from functools import wraps
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden



def error(func):
  @wraps(func)
  async def capture(client, message, *args, **kwargs):
    try:
      return await func(client, message, *args, **kwargs)
    except ChatWriteForbidden:
      return await app.leave_chat(message.chat.id)
    except Exception as err:
      exc = traceback.format_exc()
      error_feedback = split_limits(
          "**ERROR** | `{}` | `{}({})`\n\n```{}```\n\n```{}```\n".format(
          message.from_user.mention if message.from_user else 0,
          message.chat.id if message.chat else 0,
          message.chat.title if message.chat else 0,
          message.text or message.caption,
          exc,
        )
      )
      error = f"__**Respon Error!**__\n**Error:** {err}"
      for x in error_feedback:        
        try:
          await bot.send_message(-1001519186585, x)
          try:
            await client.message.edit(error)
          except Exception as e:
            await message.reply(error)
        except FloodWait as e:
          await asyncio.sleep(e.value)
        raise err

  return capture
