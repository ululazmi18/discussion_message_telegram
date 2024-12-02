import json
import gc
from pyrogram import Client

def baca_konfigurasi(nama_file):
    """
    Membaca konfigurasi dari file JSON.
    """
    with open(nama_file, "r", encoding="utf-8") as file:
        return json.load(file)

async def buat_sesi(phone_number, api_id, api_hash):
    """
    Membuat sesi Pyrogram dengan nomor telepon yang diberikan.
    """
    async with Client(
        name=phone_number,
        phone_number=phone_number,
        api_id=api_id,
        api_hash=api_hash,
        workdir='sessions'  # Direktori untuk menyimpan sesi
    ) as app:
        if app.is_connected:
            print("Sesi berhasil dibuat!")
    
    # Bebaskan sumber daya (gc.collect is optional here due to `async with`)
    gc.collect()

if __name__ == "__main__":
    import asyncio

    # Membaca konfigurasi dari file config.json
    config = baca_konfigurasi("config.json")
    api_id = config['pengaturan'][0]['api_id']
    api_hash = config['pengaturan'][0]['api_hash']

    # Meminta input nomor telepon dari pengguna
    phone_number = input("Masukkan nomor Anda: ")

    # Membuat sesi
    asyncio.run(buat_sesi(phone_number, api_id, api_hash))
