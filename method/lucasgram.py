import pytz
from datetime import datetime
from pyrogram import Client
import calendar

class MyClient(Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timezone = pytz.timezone('Asia/Jakarta')

    def to_local_time(self, date):
        return self.timezone.localize(date).strftime('%Y-%m-%d %H:%M:%S')

    async def send_kalender(self, chat_id: int, year: int, month: int, timezone: str = 'Asia/Jakarta'):
        # konversi waktu ke zona waktu yang diberikan
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)

        # membuat objek calendar untuk bulan dan tahun yang diberikan
        cal = calendar.monthcalendar(year, month)

        # membuat teks kalender dalam format yang diinginkan
        calendar_text = f"Kalender untuk bulan {calendar.month_name[month]} {year}:\n\n"
        for week in cal:
            for day in week:
                if day == 0:
                    calendar_text += "   "
                else:
                    # menandai hari ini dengan tanda asterisk (*) jika day sama dengan tanggal sekarang
                    if day == now.day and month == now.month and year == now.year:
                        calendar_text += f"*{day:2d}* "
                    else:
                        calendar_text += f"{day:2d} "
            calendar_text += "\n"

        # kirim pesan dengan teks kalender menggunakan fungsi send_message
        await self.send_message(chat_id, calendar_text)
        
    async def reply_kalender(self, message, year: int, month: int, timezone: str = 'Asia/Jakarta'):
        chat_id = message.chat.id
        # konversi waktu ke zona waktu yang diberikan
        tz = pytz.timezone(timezone)
        now = datetime.now(tz)

        # membuat objek calendar untuk bulan dan tahun yang diberikan
        cal = calendar.monthcalendar(year, month)

        # membuat teks kalender dalam format yang diinginkan
        calendar_text = f"Kalender untuk bulan {calendar.month_name[month]} {year}:\n\n"
        for week in cal:
            for day in week:
                if day == 0:
                    calendar_text += "   "
                else:
                    # menandai hari ini dengan tanda asterisk (*) jika day sama dengan tanggal sekarang
                    if day == now.day and month == now.month and year == now.year:
                        calendar_text += f"*{day:2d}* "
                    else:
                        calendar_text += f"{day:2d} "
            calendar_text += "\n"
        
        # kirim pesan dengan teks kalender menggunakan fungsi reply_to_message
        await self.send_message(chat_id, calendar_text, reply_to_message_id=message.message_id)
