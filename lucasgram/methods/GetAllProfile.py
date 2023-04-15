from pyrogram.types import InputMediaPhoto, InputMediaVideo 

@staticmethod
async def get_all_profile(chat_id: int, user_id: int, inputphoto: bool = True, inputvideo: bool = True):
  media = []
  if inputphoto:
    photos = await MyClient.get_profile_photos(user_id)
    media.extend(photos)
  if inputvideo:
    videos = await MyClient.get_profile_videos(user_id)
    media.extend(videos)

  for item in media:
    if isinstance(item, dict) and item.get("file_id") is not None:
      await MyClient.send_photo(chat_id, photo=item["file_id"])
    elif isinstance(item, dict) and item.get("video_file_id") is not None:
      await MyClient.send_video(chat_id, video=item["video_file_id"])
    else:
      print("Tipe media tidak didukung")
