def get_arg(m):
  msg = m.text
  msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
  split = msg[1:].replace("\n", " \n").split(" ")
  if " ".join(split[1:]).strip() == "":
    return ""
  return " ".join(split[1:])

def get_text(m):
  text_to_return = m.text
  if m.text is None:
    return None
  if " " in text_to_return:
    try:
      return m.text.split(None, 1)[1]
    except IndexError:
      return None
  else:
    return None
