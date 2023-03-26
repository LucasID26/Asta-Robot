import os

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

def resize_image(image):
  im = Image.open(image)
  maxsize = (512, 512)
  if (im.width and im.height) < 512:
    size1 = im.width
    size2 = im.height
    if im.width > im.height:
      scale = 512 / size1
      size1new = 512
      size2new = size2 * scale
    else:
      scale = 512 / size2
      size1new = size1 * scale
      size2new = 512
    size1new = math.floor(size1new)
    size2new = math.floor(size2new)
    sizenew = (size1new, size2new)
    im = im.resize(sizenew)
  else:
    im.thumbnail(maxsize)
  file_name = "Sticker.png"
  im.save(file_name, "PNG")
  if os.path.exists(image):
    os.remove(image)
  return file_name
