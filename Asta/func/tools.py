import asyncio
import math
import os
import re
import shlex
import ffmpeg
from typing import Tuple
from PIL import Image
import httpx 
from inspect import getfullargspec
#from pymediainfo import MediaInfo


async def run_cmd(cmd: str) -> Tuple[str, str, int, int]:
    """Run Commands"""
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )

def text_posisi(text, posisi):
  max_chars = 40
  text = re.sub(r'<[^>]*>', ' ', text)
  text = re.sub(r'[\*_~]', ' ', text)
  total_spaces = max_chars - len(text)
  if posisi == 'kiri':
      spaces_kiri = 0
      spaces_kanan = total_spaces
  elif posisi == 'tengah':
      spaces_kiri = total_spaces // 2
      spaces_kanan = total_spaces - spaces_kiri
  elif posisi == 'kanan':
      spaces_kiri = total_spaces
      spaces_kanan = 0

  message = " " * spaces_kiri + text + " " * spaces_kanan
  return message



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




async def resize_media(media: str, video: bool, fast_forward: bool) -> str:
    if video:
        return await convert_video(media)
        info_ = Media_Info.data(media)
        width = info_["pixel_sizes"][0]
        height = info_["pixel_sizes"][1]
        sec = info_["duration_in_ms"]
        s = round(float(sec)) / 1000

        if height == width:
            height, width = 512, 512
        elif height > width:
            height, width = 512, -1
        elif width > height:
            height, width = -1, 512

        resized_video = f"{media}.webm"
        if fast_forward:
            if s > 3:
                fract_ = 3 / s
                ff_f = round(fract_, 2)
                set_pts_ = ff_f - 0.01 if ff_f > fract_ else ff_f
                cmd_f = f"-filter:v 'setpts={set_pts_}*PTS',scale={width}:{height}"
            else:
                cmd_f = f"-filter:v scale={width}:{height}"
        else:
            cmd_f = f"-filter:v scale={width}:{height}"
        fps_ = float(info_["frame_rate"])
        fps_cmd = "-r 30 " if fps_ > 30 else ""
        cmd = f"ffmpeg -i {media} {cmd_f} -ss 00:00:00 -to 00:00:03 -an -c:v libvpx-vp9 {fps_cmd}-fs 256K {resized_video}"
        _, error, __, ___ = await run_cmd(cmd)
        os.remove(media)
        return resized_video

    image = Image.open(media)
    maxsize = 512
    scale = maxsize / max(image.width, image.height)
    new_size = (int(image.width * scale), int(image.height * scale))

    image = image.resize(new_size, Image.LANCZOS)
    resized_photo = "sticker.png"
    image.save(resized_photo)
    os.remove(media)
    return resized_photo



async def convert_video(filename: str) -> str:
    downpath, f_name = os.path.split(filename)
    webm_video = os.path.join(downpath, f"{f_name.split('.', 1)[0]}.webm")
    cmd = [
        "ffmpeg",
        "-loglevel",
        "quiet",
        "-i",
        filename,
        "-t",
        "00:00:03",
        "-vf",
        "fps=30",
        "-c:v",
        "vp9",
        "-b:v:",
        "500k",
        "-preset",
        "ultrafast",
        "-s",
        "512x512",
        "-y",
        "-an",
        webm_video,
    ]

    proc = await asyncio.create_subprocess_exec(*cmd)
    # Wait for the subprocess to finish
    await proc.communicate()

    if webm_video != filename:
        os.remove(filename)
    return webm_video

async def convert_video2(filename: str) -> str:
    downpath, f_name = os.path.split(filename)
    webm_video = os.path.join(downpath, f"{f_name.split('.', 1)[0]}.webm")
    ffmpeg.input(filename).output(webm_video, t='00:00:03', vf='fps=30', vcodec='vp9', vb='500k', preset='ultrafast', s='512x512', y=None, an=None).run()
    if webm_video != filename:
        os.remove(filename)
    return webm_video
    
async def edit_or_reply(m,text):
  if m.from_user and m.from_user.is_self:
    await m.edit_text(text)
  else:
    await m.reply_text(text)

#REQUESTS
class HTTP:
    async def get(self, url, format='text'):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    if format == 'text':
                        return response.text
                    elif format == 'json':
                        return response.json()
                    elif format == 'content':
                        return response.content
                    else:
                        raise ValueError("Invalid format specified.")
                else:
                    return None
            except Exception as e:
                print(f"Error: {e}")
                return None

    async def post(self, url, data, headers=None, format='text'):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, data=data, headers=headers)
                if response.status_code == 200:
                    if format == 'text':
                        return response.text
                    elif format == 'json':
                        return response.json()
                    elif format == 'content':
                        return response.content
                    else:
                        raise ValueError("Invalid format specified.")
                else:
                    return None
            except Exception as e:
                print(f"Error: {e}")
                return None
