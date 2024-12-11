import os
import asyncio
from pyrogram import Client, errors

os.makedirs("channel", exist_ok=True)
os.makedirs("media", exist_ok=True)
os.makedirs("sessions", exist_ok=True)
os.makedirs("text", exist_ok=True)

def baca_akun():
    
    akun = {}
    with open("akun.txt", "r", encoding="utf-8") as file:
        for index, line in enumerate(file, start=1):
            line = line.strip()
            if not line or line.startswith("#") or line.count(",") < 2:
                continue
            data = line.split(",")
            
            # Pastikan setidaknya ada 2 elemen (NamaAkun, NamaFileSession)
            if len(data) < 4:
                print(f"Baris {index} tidak valid: {line}")
                continue
            
            # Parsing data dengan panjang variabel
            akun[data[0]] = {
                "NamaFileSession": data[1],
                "FileChannel": data[2] if len(data) > 2 else "",
                "FileText": data[3] if len(data) > 3 else "",
                "FileGambar": data[4] if len(data) > 4 else "",
                "FileVideo": data[5] if len(data) > 5 else "",
                "JumlahPost": int(data[6]) if len(data) > 6 and data[6] else None,
                "api_id": int(data[7]) if len(data) > 7 and data[7] else None,
                "api_hash": data[8] if len(data) > 8 else "",
            }
    return akun

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
    
    config = baca("config.json")
    
    akun = baca_akun()
    
    if not akun[NamaAkun]['FileChannel']:
        print(f"[Akun {index}: {NamaAkun}] - belum menentukan file channel di akun.txt")
        return
    if not akun[NamaAkun]['FileText'] and not akun[NamaAkun]['FileGambar'] and not akun[NamaAkun]['FileVideo']:
        print(f"[Akun {index}: {NamaAkun}] - miniml harus menentukan file text, gambar, atau video di akun.txt")
        return
    if akun[NamaAkun]['api_id'] and akun[NamaAkun]['api_hash']:
        api_id = akun[NamaAkun]['api_id']
        api_hash = akun[NamaAkun]['api_hash']
    elif config['pengaturan'][0]['api_id'] and config['pengaturan'][0]['api_hash']:
        api_id = config['pengaturan'][0]['api_id']
        api_hash = config['pengaturan'][0]['api_hash']
    else:
        print(f"[Akun {index}: {NamaAkun}] - isi api_id dan api_hash di config.json")
        return
    if akun[NamaAkun]['JumlahPost']:
        JumlahPost = akun[NamaAkun]['JumlahPost']
    elif config['pengaturan'][0]['JumlahPost']:
        JumlahPost = config['pengaturan'][0]['JumlahPost']
    else:
        JumlahPost = 2

    FileSession = akun[NamaAkun]['NamaFileSession']
    FileChannel = akun[NamaAkun]['FileChannel']
    FileText = akun[NamaAkun]['FileText']
    FileGambar = akun[NamaAkun]['FileGambar']
    FileVideo = akun[NamaAkun]['FileVideo']
    
    FolderChannel = os.path.join(os.path.dirname(__file__), 'channel')
    FolderMedia = os.path.join(os.path.dirname(__file__), 'media')
    FolderSessions = os.path.join(os.path.dirname(__file__), 'sessions')
    Foldertext = os.path.join(os.path.dirname(__file__), 'text')

    JalurFileSession = os.path.join(FolderSessions, FileSession)
    JalurFileChannels = os.path.join(FolderChannel, FileChannel)
    JalurFileText = os.path.join(Foldertext, FileText)
    JalurFileGambar = os.path.join(FolderMedia, FileGambar)
    JalurFileVideo = os.path.join(FolderMedia, FileVideo)
    
    if FileChannel != "":
        JalurFileChannels = JalurFileChannels.split('.')[0]
        file_paths = glob.glob(f"{JalurFileChannels}.*")
        JalurFileChannels = file_paths[0]
        if not os.path.exists(JalurFileChannels):
            print(f"[Akun {index}: {NamaAkun}] - File {FileChannel} tidak ditemukan")
            return
    if FileText != "":
        JalurFileText = JalurFileText.split('.')[0]
        file_paths = glob.glob(f"{JalurFileText}.*")
        JalurFileText = file_paths[0]
        if not os.path.exists(JalurFileText):
            print(f"[Akun {index}: {NamaAkun}] - File {FileText} tidak ditemukan")
            return
    if FileGambar != "":
        JalurFileGambar = JalurFileGambar.split('.')[0]
        file_paths = glob.glob(f"{JalurFileGambar}.*")
        JalurFileGambar = file_paths[0]
        if not os.path.exists(JalurFileGambar):
            print(f"[Akun {index}: {NamaAkun}] - File {FileGambar} tidak ditemukan")
            return
    if FileVideo != "":
        JalurFileVideo = JalurFileVideo.split('.')[0]
        file_paths = glob.glob(f"{JalurFileVideo}.*")
        JalurFileVideo = file_paths[0]
        if not os.path.exists(JalurFileVideo):
            print(f"[Akun {index}: {NamaAkun}] - File {FileVideo} tidak ditemukan")
            return
    
    with open(JalurFileChannels, 'r') as file:
        target_channels = [line.strip().replace('https://t.me/', '') for line in file if line.strip()]
    
    if not os.path.exists(JalurFileSession):
        if isinstance(details.get('NamaFileSession'), int) or (isinstance(details.get('NamaFileSession'), str) and details.get('NamaFileSession').isdigit()):
            pass
        else:
            print(f"[Akun {index}: {NamaAkun}] - File {FileSession}.session tidak ditemukan. jika belum memiliki file session, gunakan nomor yang ingin digunakan sebagai session baru")
            return
    else:
        try:
            async with Client(name=details.get('NamaFileSession'), api_id=api_id, api_hash=api_hash, workdir=FolderSessions) as app:
                me = await app.get_me()
        except Exception:
            os.remove(os.path.join(FolderSessions, f"{details.get('NamaFileSession')}.session"))
            print(f"[Akun {index}: {NamaAkun}] - File {FileSession}.session dihapus karena tidak dapat digunakan")
            return
    
    try:
        async with Client(name=details.get('NamaFileSession'), api_id=api_id, api_hash=api_hash, workdir=FolderSessions) as app:
            me = await app.get_me()
            FullName = f"{me.first_name} {me.last_name}" if me.last_name else me.first_name
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
                            if akun[NamaAkun]['FileText'] and akun[NamaAkun]['FileVideo']:
                                await discussion_message.reply_video(video=JalurFileVideo, caption=message_text)
                                NamaFileText = FileText.split('.')[0]
                                NamaFileVideo = FileVideo.split('.')[0]
                                print(f"[Akun {index}: {FullName}] - [{NoSaluran}] ✅ {NamaSaluran} | {NamaFileText} | {NamaFileVideo}")
                                x += 1
                                message_id -= 1
                            elif akun[NamaAkun]['FileText'] and akun[NamaAkun]['FileGambar']:
                                await discussion_message.reply_photo(photo=JalurFileGambar, caption=message_text)
                                NamaFileText = FileText.split('.')[0]
                                NamaFileGambar = FileGambar.split('.')[0]
                                print(f"[Akun {index}: {FullName}] - [{NoSaluran}] ✅ {NamaSaluran} | {NamaFileText} | {NamaFileGambar}")
                                x += 1
                                message_id -= 1
                            elif akun[NamaAkun]['FileText']:
                                await discussion_message.reply(message_text)
                                NamaFileText = FileText.split('.')[0]
                                print(f"[Akun {index}: {FullName}] - [{NoSaluran}] ✅ {NamaSaluran} | {NamaFileText}")
                                x += 1
                                message_id -= 1
                            elif akun[NamaAkun]['FileVideo']:
                                await discussion_message.reply_video(video=JalurFileVideo)
                                NamaFileVideo = FileVideo.split('.')[0]
                                print(f"[Akun {index}: {FullName}] - [{NoSaluran}] ✅ {NamaSaluran} | {NamaFileVideo}")
                                x += 1
                                message_id -= 1
                            elif akun[NamaAkun]['FileGambar']:
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

    FolderSessions = os.path.join(os.path.dirname(__file__), 'sessions')
    
    config = baca("config.json")
    
    akun = baca_akun()
    
    if not akun:
        print("Tidak ada akun yang terdaftar di akun.txt")
        print("Baris yang diawali dengan tanda '#' akan diabaikan.")
        exit()
    
    for index, (NamaAkun, details) in enumerate(akun.items()):
                
        if akun[NamaAkun]['api_id'] and akun[NamaAkun]['api_hash']:
            api_id = akun[NamaAkun]['api_id']
            api_hash = akun[NamaAkun]['api_hash']
        elif config['pengaturan'][0]['api_id'] and config['pengaturan'][0]['api_hash']:
            api_id = config['pengaturan'][0]['api_id']
            api_hash = config['pengaturan'][0]['api_hash']
        else:
            print(f"[Akun {index}: {NamaAkun}] - isi api_id dan api_hash di: \nakun.txt untuk akun {NamaAkun} \nconfig.json untuk semua akun")
            return
                
        FileSession = akun[NamaAkun]['NamaFileSession']
        JalurFileSession = os.path.join(FolderSessions, FileSession)
    
        if not os.path.exists(JalurFileSession):
            if isinstance(details.get('NamaFileSession'), int) or (isinstance(details.get('NamaFileSession'), str) and details.get('NamaFileSession').isdigit()):
                async with Client(name=details.get('NamaFileSession'), phone_number=details.get('NamaFileSession'), api_id=api_id, api_hash=api_hash, workdir=FolderSessions) as app:
                    print(f"Login untuk [{NamaAkun} - {FileSession}]")
                    me = await app.get_me()
            else:
                continue
        
    
    tasks = [
        send_message(NamaAkun, details, index + 1)
        for index, (NamaAkun, details) in enumerate(akun.items())
    ]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
