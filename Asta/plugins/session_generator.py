import traceback
import os
from logging import getLogger
from pyrogram import Client, filters
from pyrogram.errors import ApiIdInvalid, PasswordHashInvalid, PhoneCodeExpired, PhoneCodeInvalid, PhoneNumberInvalid, SessionPasswordNeeded
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from telethon import TelegramClient
from telethon.errors import ApiIdInvalidError, PasswordHashInvalidError, PhoneCodeExpiredError, PhoneCodeInvalidError, PhoneNumberInvalidError, SessionPasswordNeededError
from telethon.sessions import StringSession
from config import bot


from Asta.decorators.info_cmd import info_cmd
from Asta.decorators.pv_or_gc import no_group


LOGGER = getLogger(__name__)
API_ID = os.environ['API_ID']
API_HASH = os.environ['API_HASH']

ask_ques = "**» Silakan pilih pustaka yang ingin Anda hasilkan string :**\n\nCatnCatatanatan: Saya tidak mengumpulkan info pribadi apa pun dari fitur ini."
buttons_ques = [
    [
        InlineKeyboardButton("Pyrogram", callback_data="pyrogram"),
        InlineKeyboardButton("Telethon", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("Pyrogram Bot", callback_data="pyrogram_bot"),
        InlineKeyboardButton("Telethon Bot", callback_data="telethon_bot"),
    ],
]

gen_button = [[InlineKeyboardButton(text="🤖 Generate Session 🤖", callback_data="genstring")]]


async def is_batal(msg):
    if msg.text == "/cancel":
        await msg.reply("**» Membatalkan proses pembuatan sesi string yang sedang berlangsung!**", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
        return True
    elif msg.text == "/skip":
        return False
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("**» Membatalkan proses pembuatan sesi string yang sedang berlangsung!**", quote=True)
        return True
    else:
        return False


@bot.on_callback_query(filters.regex(pattern=r"^(genstring|pyrogram|pyrogram_bot|telethon_bot|telethon)$"))
async def callbackgenstring(bott, callback_query):
    query = callback_query.matches[0].group(1)
    if query == "genstring":
        await callback_query.answer()
        await callback_query.message.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))
    elif query.startswith("pyrogram") or query.startswith("telethon"):
        try:
            if query == "pyrogram":
                await callback_query.answer()
                await generate_session(bott, callback_query.message)
            elif query == "pyrogram_bot":
                await callback_query.answer("» Generator sesi akan dari Pyrogram v2.", show_alert=True)
                await generate_session(bott, callback_query.message, is_bot=True)
            elif query == "telethon_bot":
                await callback_query.answer()
                await generate_session(bott, callback_query.message, telethon=True, is_bot=True)
            elif query == "telethon":
                await callback_query.answer()
                await generate_session(bott, callback_query.message, telethon=True)
        except Exception as e:
            LOGGER.error(traceback.format_exc())
            ERROR_MESSAGE = "Ada sesuatu yang salah. \n\n**ERROR** : {} " "\n\n**Harap teruskan pesan ini ke Pemilik saya!**"
            await callback_query.message.reply(ERROR_MESSAGE.format(str(e)))


@bot.on_message(~filters.forwarded & filters.command("generate"))
@info_cmd
@no_group
async def genstringg(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bott, msg, telethon=False, is_bot: bool = False):
    ty = "Telethon" if telethon else "Pyrogram"
    if is_bot:
        ty += " Bot"
    await msg.reply(f"» Mencoba memulai **{ty}** session generator...")
    msg.chat.id
    api_id_msg = await msg.chat.ask("Mohon kirimkan **API_ID** untuk melanjutkan.\n\nklik /skip untuk lewati sesi.", filters=filters.text)
    if await is_batal(api_id_msg):
        return
    if api_id_msg.text == "/skip":
        api_id = API_ID
        api_hash = API_HASH
    else:
        try:
            api_id = int(api_id_msg.text)
            await api_id_msg.delete()
        except ValueError:
            await api_id_msg.reply("**API_ID** harus bilangan bulat, mulailah membuat sesi Anda lagi.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
            return
        api_hash_msg = await msg.chat.ask("» Sekarang kirimkan **API_HASH** Anda untuk melanjutkan.", filters=filters.text)
        if await is_batal(api_hash_msg):
            return
        api_hash = api_hash_msg.text
        await api_hash_msg.delete()
    t = "Kirimkan **BOT_TOKEN** Anda untuk melanjutkan.\nContoh : `5432198765:abcdanonymousterabaapol`'" if is_bot else "» Silakan kirim **PHONE_NUMBER** Anda dengan kode negara yang ingin Anda buat sesinya. \nContoh : `+6286356837789`'"
    phone_number_msg = await msg.chat.ask(t, filters=filters.text)
    if await is_batal(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    await phone_number_msg.delete()
    if not is_bot:
        await msg.reply("» Mencoba mengirim OTP ke nomor yang diberikan...")
    else:
        await msg.reply("» Mencoba masuk menggunakan Bot Token...")
    if telethon and is_bot or telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name="bot", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    else:
        client = Client(name="user", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply("» Kombinasi **API_ID** dan **API_HASH** Anda tidak cocok. \n\nSilakan mulai membuat sesi Anda lagi.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply("» **PHONE_NUMBER** yang Anda miliki bukan milik akun mana pun di Telegram.\n\nMulai buat sesi Anda lagi.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await msg.chat.ask("» Silakan kirim **OTP** yang Anda terima dari Telegram di akun Anda.\nJika OTP adalah `12345`, **silakan kirimkan sebagai** `1 2 3 4 5`.", filters=filters.text, timeout=600)
            if await is_batal(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply("» Batas waktu mencapai 10 menit.\n\nSilakan mulai membuat sesi Anda lagi.", reply_markup=InlineKeyboardMarkup(gen_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        await phone_code_msg.delete()
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError):
            await msg.reply("» kode OTP yang Anda kirim **salah.**\n\nSilakan mulai membuat sesi Anda lagi.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError):
            await msg.reply("» OTP yang Anda kirimkan telah **kedaluwarsa.**\n\nSilakan mulai membuat sesi Anda lagi.", reply_markup=InlineKeyboardMarkup(gen_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError):
            try:
                two_step_msg = await msg.chat.ask("» Masukkan kata sandi **Verifikasi Dua Langkah** Anda untuk melanjutkan.", filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply("» Batas waktu mencapai 5 menit.\n\nSilakan mulai membuat sesi Anda lagi.", reply_markup=InlineKeyboardMarkup(gen_button))
                return
            try:
                password = two_step_msg.text
                await two_step_msg.delete()
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await is_batal(api_id_msg):
                    return
            except (PasswordHashInvalid, PasswordHashInvalidError):
                await two_step_msg.reply("» Kata sandi yang Anda kirim salah.\n\nSilakan mulai membuat sesi lagi.", quote=True, reply_markup=InlineKeyboardMarkup(gen_button))
                return
    elif telethon:
        await client.start(bot_token=phone_number)
    else:
        await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"**Ini adalah {ty} String Session** \n\n`{string_session}` \n\n**Dihasilkan Oleh :** @{bott.me.username}\n🍒 **Catatan :** Jangan bagikan kepada siapa pun Dan jangan lupa untuk mendukung pemilik bot ini jika Anda suka"
    try:
        if not is_bot:
            await client.send_message("me", text)
        else:
            await bott.send_message(msg.chat.id, text)
    except KeyError:
        pass
    await client.disconnect()
    await bott.send_message(
        msg.chat.id,
        f'» Berhasil membuat Sesi String {"Telethon" if telethon else "Pyrogram"} Anda.\n\nSilakan periksa pesan tersimpan untuk mendapatkannya ! \n\n**Bot Generator String oleh ** @LucasBukanKalengSarden',
    )
