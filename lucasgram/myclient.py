from pyrogram import Client, Message
from typing import List


class MyClient(Client):
    async def build_table(self, judul: List[str], query: List[str]) -> str:
        # menghitung panjang maksimal untuk setiap kolom berdasarkan isi data
        max_lengths = [len(max(judul, key=len))] + [len(max(query[i], key=len)) for i in range(len(judul))]

        # membangun header
        header = '|'.join([f'{judul[i]:^{max_lengths[i]}}' for i in range(len(judul))])
        header += '\n' + '|'.join(['-' * length for length in max_lengths])

        # membangun baris data
        rows = ''
        for i in range(len(query[0])):
            row = '|'.join([f'{query[j][i]:^{max_lengths[j]}}' for j in range(len(judul))])
            rows += '\n' + row

        # mengembalikan teks tabel
        return f'{header}\n{rows}'

    async def send_table(self, chat_id: int, judul: List[str], query: List[str]):
        # membangun teks tabel menggunakan method build_table
        table_text = await self.build_table(judul, query)

        # kirim pesan dengan teks tabel menggunakan fungsi send_message
        await self.send_message(chat_id, table_text, parse_mode='Markdown')

    async def reply_table(self, message: Message, judul: List[str], query: List[str]):
        # membangun teks tabel menggunakan method build_table
        table_text = await self.build_table(judul, query)

        # kirim pesan dengan teks tabel menggunakan fungsi reply
        await message.reply(table_text, parse_mode='Markdown')
