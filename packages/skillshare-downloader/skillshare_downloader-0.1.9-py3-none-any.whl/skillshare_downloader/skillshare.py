import unicodedata
import requests
import json
import shutil
import subprocess
import sys
import os
from slugify import slugify
from tqdm import tqdm
from telethon.sync import TelegramClient
from skillshare_downloader.progress import ffmpegDown
import telethon
import telethon.tl.functions


class Downloader(object):
    def __init__(
        self,
        cookie,
        download_path=os.environ.get('FILE_PATH', './downloads'),
        api_id=None,
        api_hash=None,
        phone=None
    ):
        self.cookie = cookie.strip().strip('"')
        self.download_path = download_path
        self.pythonversion = 3 if sys.version_info >= (3, 0) else 2
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.error_color_code = '\033[91m'
        self.reset_color_code = '\033[0m'

    def create_registry_file(self, base_path, registry):
        registry_file = os.path.join(base_path, 'reg.json')
        with open(registry_file, 'w') as f:
            json.dump(registry, f, indent=4)

    def load_registry_file(self, base_path):
        registry_file = os.path.join(base_path, 'reg.json')
        if os.path.exists(registry_file):
            with open(registry_file, 'r') as f:
                try:
                    registry = json.load(f)
                    return registry
                except json.JSONDecodeError:
                    pass
        return {"topic_id": None, "upfiles": []}

    def is_unicode_string(self, string):
        if (self.pythonversion == 3 and isinstance(string, str)) or (self.pythonversion == 2 and isinstance(string, unicodedata)):
            return True
        else:
            return False

    def create_topic(self, chat_id, topic_name):
        with TelegramClient(self.phone, self.api_id, self.api_hash) as client:
            print(f'Creating Topic: {topic_name.title()}')
            chat = client.get_entity(chat_id)
            new_id = str(-100) + str(chat.id)
            try:
                result = client(telethon.tl.functions.channels.CreateForumTopicRequest(
                    channel=chat_id,
                    title=topic_name.title()
                ))
                print('Topic Created')
                return result.updates[1].message.id
            except Exception as e:
                # Print the error
                print(e)

    def upload_to_telegram_group(self, file_path, telegram, file_name, topic_id):
        with TelegramClient(self.phone, self.api_id, self.api_hash) as client:
            client.start()
            entity = client.get_entity(telegram)
            caption = f'{file_name}'
            
            file_size = os.path.getsize(file_path)
            progress_bar = tqdm(total=file_size, unit='B', unit_scale=True, desc=f'Sending to Telegram')

            def callback(current, total):
                progress_bar.update(current - progress_bar.n)

            message = client.send_file(entity, file_path, caption=caption, reply_to=topic_id, progress_callback=callback)

    def download(self, class_id, language, resolution, telegram, erase):
        data = self.fetch_course(class_id=class_id)
        teacher_name = None

        if '_embedded' not in data or 'sessions' not in data['_embedded'] or not isinstance(data['_embedded']['sessions'], dict):
            
            print(self.error_color_code + 'Course data is incomplete or missing.' + self.reset_color_code)
            print(self.error_color_code + 'This Course can\'t be downloaded' + self.reset_color_code)
            return

        sessions = data['_embedded']['sessions'].get('_embedded', {}).get('sessions', [])

        if not sessions:
            print("No sessions found in the course.")
            return

        if 'vanity_username' in data['_embedded']['teacher']:
            teacher_name = data['_embedded']['teacher']['vanity_username']

        if not teacher_name:
            teacher_name = data['_embedded']['teacher']['full_name']

        if not teacher_name:
            raise Exception('Failed to read teacher name from data')

        if self.is_unicode_string(teacher_name):
            teacher_name = teacher_name.encode('ascii', 'replace')

        title = data['title']

        if self.is_unicode_string(title):
            title = title.encode('ascii', 'replace')  # ignore any weird char

        base_path = os.path.abspath(
            os.path.join(
                self.download_path,
                slugify(teacher_name),
                slugify(title),
            )
        ).rstrip('/')

        teacher_path = os.path.abspath(
            os.path.join(
                self.download_path,
                slugify(teacher_name)
            )
        ).rstrip('/')

        if telegram is not None:
            if not os.path.exists(os.path.join(base_path, 'reg.json')):
                topic_id = self.create_topic(telegram, title)
            else:
                reg = self.load_registry_file(base_path)
                topic_id = reg['topic_id']
        else:
            topic_id=None

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://www.skillshare.com/en/home',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'es-MX,es;q=0.9,en-US;q=0.8,en;q=0.7,es-419;q=0.6',
            'Cookie': self.cookie,
        }
        
        num_files = 0
        total_files = len(data['_embedded']['sessions']['_embedded']['sessions'])

        for s in data['_embedded']['sessions']['_embedded']['sessions']:

            download_url = s['_links']['stream']['href']
            file = self.fetch_stream(download_url)

            s_title = s['title']

            if self.is_unicode_string(s_title):
                s_title = s_title.encode('ascii', 'replace')  # ignore any weird char

            file_name = '{} - {}'.format(
                str(s['index'] + 1).zfill(2),
                slugify(s_title),
            )
            stream = file['streams'][1]['url']

            self.get_content(stream, resolution, language, base_path, file_name, telegram, topic_id, erase)

            num_files += 1
            
        if num_files == total_files:
            # ANSI escape sequence for green color
            success_color_code = '\033[92m'
            reset_color_code = '\033[0m'
            
            success_message = 'All files downloaded successfully.'
            print(success_color_code + success_message + reset_color_code)

            if erase:
                shutil.rmtree(base_path)
                shutil.rmtree(teacher_path)

    def fetch_course(self, class_id):
        res = requests.get(
            url='https://api.skillshare.com/classes/{}'.format(class_id),
            headers={
                'Accept': 'application/vnd.skillshare.class+json;,version=0.8',
                'User-Agent': 'Skillshare/5.3.0; Android 9.0.1',
                'Host': 'api.skillshare.com',
                'Referer': 'https://www.skillshare.com/',
                'cookie': self.cookie,
            }
        )

        if not res.status_code == 200:
            raise Exception('Fetch error, code == {}'.format(res.status_code))

        return res.json()
    
    def fetch_stream(self, dwn_url):
        res = requests.get(
            url='https://api.skillshare.com{}'.format(dwn_url),
            headers={
                'User-Agent': 'Skillshare/5.3.0; Android 9.0.1',
                'Host': 'api.skillshare.com',
                'Referer': 'https://www.skillshare.com/',
                'cookie': self.cookie,
            }
        )

        if not res.status_code == 200:
            raise Exception('Fetch error, code == {}'.format(res.status_code))

        return res.json()

    def get_content(self, url, resolution, lang, base_path, file_name, telegram, topic_id, erase):
        
        format = 'mp4' if telegram is not None else 'mkv'
        response = requests.get(url)
        m3u8_content = response.text
        # print(m3u8_content)
        lines = m3u8_content.split("\n")
        output_file = os.path.join(base_path, file_name + '.' + format)
        base_url = os.path.dirname(url)

        if os.path.exists(output_file):
            print('File already exists. Skipping download:', file_name + '.' + format)
            if telegram is None:
                return
            else:
                try:
                    self.upload_to_telegram_group(output_file, telegram,file_name,topic_id)
                    registry = self.load_registry_file(base_path)
                    registry["upfiles"].append(file_name)
                    registry["topic_id"] = topic_id
                    self.create_registry_file(base_path, registry)
                except Exception as e:
                    print(f'Error uploading file: {file_name}.mp4')
                    print(f'Error message: {str(e)}')
                
                if erase:
                    if os.path.exists(output_file):
                        os.remove(output_file)
                return
            
        if telegram is not None:
            registry = self.load_registry_file(base_path)
            upfiles = set(registry["upfiles"])
            if file_name in upfiles:
                print(f"Skipping {file_name}. Already uploaded.")
                return

        pbar = tqdm(total=2 if telegram is not None else 3, desc='Downloading: ' + file_name + '.' + format, unit="file")

        # Download audio, subtitles, and video files
        audio_file = "audio.aac"
        subtitles_file = "subtitles.srt"
        video_file = "video.ts"
        FNULL = open(os.devnull, "w")
        
        # Extract audio URL
        audio_url = None
        lines = m3u8_content.split("\n")
        for line in lines:
            if line.startswith("#EXT-X-MEDIA:TYPE=AUDIO") and "group_audio" in line:
                audio_path = line.split('URI="')[-1].split('"')[0]
                audio_url = f"{base_url}/{audio_path}"
                break

        # Extract matching video URL
        video_url = None
        for line in lines:
            if line.startswith("#EXT-X-STREAM-INF:RESOLUTION="):
                if resolution in line:
                    video_path = lines[lines.index(line) + 1]
                    video_url = f"{base_url}/{video_path}"
                    break

        # Download audio
        ffmpegDown(
            ["ffmpeg", "-i", audio_url, "-c:a", "aac", "-b:a", "128k", "-y", audio_file], 'audio'
        ).run()
        pbar.update(1)

        # Download video
        lookres = ['1920x1080', '1728x1080', '1280x720', '1152x720', '854x480', '768x480', '640x360', '576x360', '426x240', '384x240']
        if video_url is not None:
            ffmpegDown(
                ["ffmpeg", "-i", video_url, "-c", "copy", "-bsf:v", "h264_mp4toannexb", "-y", video_file], 'video'
            ).run()
            pbar.update(1)
        else:
            skip = False  # Flag to indicate if previous resolutions should be skipped
            for resolution_choice in lookres:
                if skip and resolution_choice != resolution:
                    continue
                for line in lines:
                    if line.startswith("#EXT-X-STREAM-INF:RESOLUTION="):
                        if resolution_choice in line:
                            video_path = lines[lines.index(line) + 1]
                            video_url = f"{base_url}/{video_path}"
                            break

                if video_url is not None:
                    print(f'\033[91mResolution {resolution} not found looking for lower resolution\033[0m')
                    print(f'\033[92mDownloading at {resolution_choice}\033[0m')
                    ffmpegDown(
                        ["ffmpeg", "-i", video_url, "-c", "copy", "-bsf:v", "h264_mp4toannexb", "-y", video_file], 'video'
                    ).run()
                    pbar.update(1)
                    if resolution_choice == resolution:
                        skip = True  # Set the flag to True to skip previous resolutions
                    break


        if telegram is not None:
            # Combine audio and video into a single .mp4 file
            print(f'\033[33mCombining resources into .mp4 \033[0m')
            subprocess.run(
                [
                    "ffmpeg", "-i", video_file, "-i", audio_file,
                    "-map", "0:v", "-map", "1:a", "-c", "copy", "-y", output_file
                ],
                stdout=FNULL,
                stderr=subprocess.PIPE
            )
            try:
                self.upload_to_telegram_group(output_file, telegram,file_name,topic_id)
                registry["upfiles"].append(file_name)
                registry["topic_id"] = topic_id
                self.create_registry_file(base_path, registry)
            except Exception as e:
                print(f'Error uploading file: {file_name}.mp4')
                print(f'Error message: {str(e)}')
            
            if erase:
                if os.path.exists(output_file):
                    os.remove(output_file)
            
        else:
            # Extract matching subtitles URL
            subtitles_url = None
            for line in lines:
                if line.startswith("#EXT-X-MEDIA:TYPE=SUBTITLES"):
                    subtitle_info = line.split(",")
                    subtitle_lang = subtitle_info[2].split("=")[-1].strip('"')
                    subtitle_path = line.split('URI="')[-1].split('"')[0]
                    subtitle_url = f"{base_url}/{subtitle_path}"
                    if subtitle_lang == lang:
                        subtitles_url = subtitle_url
                        break

            if subtitles_url is None:
                for line in lines:
                    if line.startswith("#EXT-X-MEDIA:TYPE=SUBTITLES"):
                        subtitle_info = line.split(",")
                        subtitle_lang = subtitle_info[2].split("=")[-1].strip('"')
                        subtitle_path = line.split('URI="')[-1].split('"')[0]
                        subtitle_url = f"{base_url}/{subtitle_path}"
                        if subtitle_lang == "en-US":
                            subtitles_url = subtitle_url
                            break

            if subtitles_url:
                # Download subtitles
                subprocess.run(
                    ["ffmpeg", "-i", subtitles_url, "-y", subtitles_file],
                    stdout=FNULL,
                    stderr=subprocess.PIPE
                )
                pbar.update(1)
            
            # Combine audio, subtitles, and video into a single .mkv file
            print(f'\033[33mCombining resources into .mkv \033[0m')
            subprocess.run(
                [
                    "ffmpeg", "-i", video_file, "-i", audio_file, "-i", subtitles_file,
                    "-map", "0:v", "-map", "1:a", "-map", "2:s", "-c", "copy", "-y", output_file
                ],
                stdout=FNULL,
                stderr=subprocess.PIPE
            )
            os.remove(subtitles_file)

        # Clean up temporary files
        os.remove(audio_file)
        os.remove(video_file)

        pbar.close()
        pbar.clear()
        success_color_code = '\033[92m'
        reset_color_code = '\033[0m'
        success_message = f'{file_name}.{format} was proccesed correctly'
        print(success_color_code + success_message + reset_color_code)