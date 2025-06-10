from telethon import TelegramClient, events
from datetime import datetime
import os

API_ID = int(os.environ['API_ID'])
API_HASH = os.environ['API_HASH']
BOT_TOKEN = os.environ['BOT_TOKEN']

client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
pesan_terpantau = {}

@client.on(events.NewMessage)
async def simpan_pesan(event):
    if event.is_group or event.is_channel:
        pesan_terpantau[event.id] = {
            'user_id': event.sender_id,
            'message': event.raw_text or "",
            'waktu_kirim': datetime.now()
        }

@client.on(events.MessageDeleted())
async def pantau_hapus(event):
    for msg_id in event.deleted_ids:
        if msg_id in pesan_terpantau:
            data = pesan_terpantau[msg_id]
            await client.send_message(
                event.chat_id,
                f"⚠️ *Peringatan!* Pesan dihapus:\n\n"
                f"🗣️ *Isi*: `{data['message']}`\n"
                f"👤 *ID Pengirim*: `{data['user_id']}`\n"
                f"📤 *Dikirim*: `{data['waktu_kirim'].strftime('%Y-%m-%d %H:%M:%S')}`\n"
                f"🗑️ *Dihapus*: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`",
                parse_mode='markdown'
            )
        else:
            await client.send_message(event.chat_id, "⚠️ Pesan dihapus (tidak ditemukan di cache).")

print("Bot siap berjalan.")
client.run_until_disconnected()
