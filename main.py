import os
import asyncio

os.makedirs("channel", exist_ok=True)
os.makedirs("media", exist_ok=True)
os.makedirs("sessions", exist_ok=True)
os.makedirs("text", exist_ok=True)

files = [f for f in os.listdir("sessions") if f.endswith(".session")]
if not files:
    print("\nJalankan python add.py untuk membuat session baru.\n")
    exit()

def baca(nama_file):
    import json
    with open(nama_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

async def countdown(t):
    for i in range(t, 0, -1):
        print(f"Wait - {i}          ", flush=True, end="\r")
        await asyncio.sleep(1)

async def send_message(NamaAkun, details, index):
    from pyrogram import Client, errors
    
    config = baca("config.json")
        
    if not config['akun'][NamaAkun][0]['FileChannel']:
        return
    if not config['akun'][NamaAkun][0]['FileText'] and not config['akun'][NamaAkun][0]['FileGambar'] and not config['akun'][NamaAkun][0]['FileVideo']:
        return
    if config['akun'][NamaAkun][0]['api_id'] and config['akun'][NamaAkun][0]['api_hash']:
        api_id = config['akun'][NamaAkun][0]['api_id']
        api_hash = config['akun'][NamaAkun][0]['api_hash']
    elif config['pengaturan'][0]['api_id'] and config['pengaturan'][0]['api_hash']:
        api_id = config['pengaturan'][0]['api_id']
        api_hash = config['pengaturan'][0]['api_hash']
    else:
        print(f"[Akun {index}: {NamaAkun}] - isi api_id dan api_hash di config.json")
        return
    if config['akun'][NamaAkun][0]['JumlahPost']:
        JumlahPost = config['akun'][NamaAkun][0]['JumlahPost']
    else:
        JumlahPost = config['pengaturan'][0]['JumlahPost']

    FileChannel = config['akun'][NamaAkun][0]['FileChannel']
    FileText = config['akun'][NamaAkun][0]['FileText']
    FileGambar = config['akun'][NamaAkun][0]['FileGambar']
    FileVideo = config['akun'][NamaAkun][0]['FileVideo']
    
    FolderChannel = os.path.join(os.path.dirname(__file__), 'channel')
    FolderMedia = os.path.join(os.path.dirname(__file__), 'media')
    FolderSessions = os.path.join(os.path.dirname(__file__), 'sessions')
    Foldertext = os.path.join(os.path.dirname(__file__), 'text')

    JalurFileChannels = os.path.join(FolderChannel, FileChannel)
    JalurFileText = os.path.join(Foldertext, FileText)
    JalurFileGambar = os.path.join(FolderMedia, FileGambar)
    JalurFileVideo = os.path.join(FolderMedia, FileVideo)
    
    if FileText != "":
        if not os.path.exists(JalurFileText):
            print(f"[Akun {index}: {NamaAkun}] - File {FileText} tidak ditemukan")
            return
    if FileGambar != "":
        if not os.path.exists(JalurFileGambar):
            print(f"[Akun {index}: {NamaAkun}] - File {FileGambar} tidak ditemukan")
            return
    if FileVideo != "":
        if not os.path.exists(JalurFileVideo):
            print(f"[Akun {index}: {NamaAkun}] - File {FileVideo} tidak ditemukan")
            return
    
    
    with open(JalurFileChannels, 'r') as file:
        target_channels = [line.strip().replace('https://t.me/', '') for line in file if line.strip()]
            
    try:
        async with Client(name=details[0].get('Nomor'), api_id=api_id, api_hash=api_hash, workdir=FolderSessions) as app:
            me = await app.get_me()
            FullName = me.first_name if me.first_name else me.username
            print(f"[Akun {index}: {NamaAkun}] - [{FullName} | {me.phone_number}]")
            NoSaluran = 1
            for NamaSaluran in target_channels:
                
                x = 0
                message_id = None
                async for message in app.get_chat_history(NamaSaluran, limit=1):
                    message_id = message.id
                    break
                
                while True:
                    if x == JumlahPost:
                        break
                    
                    try:
                        discussion_message = await app.get_discussion_message(NamaSaluran, message_id)

                        with open(JalurFileText, 'r', encoding='utf-8') as text_file:
                            message_text = text_file.read().strip()

                        try:
                            if config['akun'][NamaAkun][0]['FileText'] and config['akun'][NamaAkun][0]['FileVideo']:
                                await discussion_message.reply_video(video=JalurFileVideo, caption=message_text)
                                NamaFileText = FileText.split('.')[0]
                                NamaFileVideo = FileVideo.split('.')[0]
                                print(f"[Akun {index}: {FullName}] - [{NoSaluran}] ✅ {NamaSaluran} | {NamaFileText} | {NamaFileVideo}")
                                x += 1
                                message_id -= 1
                            elif config['akun'][NamaAkun][0]['FileText'] and config['akun'][NamaAkun][0]['FileGambar']:
                                await discussion_message.reply_photo(photo=JalurFileGambar, caption=message_text)
                                NamaFileText = FileText.split('.')[0]
                                NamaFileGambar = FileGambar.split('.')[0]
                                print(f"[Akun {index}: {FullName}] - [{NoSaluran}] ✅ {NamaSaluran} | {NamaFileText} | {NamaFileGambar}")
                                x += 1
                                message_id -= 1
                            elif config['akun'][NamaAkun][0]['FileText']:
                                await discussion_message.reply(message_text)
                                NamaFileText = FileText.split('.')[0]
                                print(f"[Akun {index}: {FullName}] - [{NoSaluran}] ✅ {NamaSaluran} | {NamaFileText}")
                                x += 1
                                message_id -= 1
                            elif config['akun'][NamaAkun][0]['FileVideo']:
                                await discussion_message.reply_video(video=JalurFileVideo)
                                NamaFileVideo = FileVideo.split('.')[0]
                                print(f"[Akun {index}: {FullName}] - [{NoSaluran}] ✅ {NamaSaluran} | {NamaFileVideo}")
                                x += 1
                                message_id -= 1
                            elif config['akun'][NamaAkun][0]['FileGambar']:
                                await discussion_message.reply_photo(photo=JalurFileGambar)
                                NamaFileGambar = FileGambar.split('.')[0]
                                print(f"[Akun {index}: {FullName}] - [{NoSaluran}] ✅ {NamaSaluran} | {NamaFileGambar}")
                                x += 1
                                message_id -= 1
                        
                        except errors.FloodWait as e:
                            print(f"Flood wait: {e.x + 10} detik. Menghentikan sementara...")
                            await countdown(e.x + 10)
                    
                    except Exception as e:
                        print(f"[Akun {index}: {FullName}] - [{NoSaluran}] ❌ {NamaSaluran}")
                        message_id -= 1
                NoSaluran += 1
                            
    except Exception as e:
        print(f"Kesalahan pada akun {NamaAkun}: {e}")

async def main():
    
    config = baca("config.json")
    
    akun = config.get("akun", {})
    
    tasks = [
        send_message(NamaAkun, details, index + 1)
        for index, (NamaAkun, details) in enumerate(akun.items())
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
