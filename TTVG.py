import tempfile, shutil, json, praw, os, ffmpeg, random, subprocess, math, requests, base64, textwrap, time
from datetime import datetime
from TitlePic import TitlePic
from ImageCompile import Imager
from pydub import AudioSegment
from print_utils import *
from abbreviations import abbreviations
from dotenv import load_dotenv

class TTVG:
    def __init__(self, 
                 subreddit: str = 'AITA', 
                 time_frame: str = 'month', 
                 num_ask: int = 10,
                 voice: str = 'en_us_010', 
                 title_voice: str = 'en_us_010', 
                 video_speed: float = 1.1,
                 align_speed: float = 0.8,
                 base_video: str = 'Base_Videos/minecraft.mp4',
                 chunk_size: int = 180,
                 fps: int = 60
                 ):
        self.subreddit = subreddit
        self.time_frame = time_frame
        self.num_ask = num_ask
        self.voice = voice
        self.title_voice = title_voice
        self.video_speed = video_speed
        self.align_speed = align_speed
        self.base_video = base_video
        self.chunk_size = chunk_size
        self.fps = fps

    def start(self):
        '''Main starting function for TTVG.'''
        print('TTVG v1', color='blue')
        self.askPost()
        self.generate()

    def askPost(self):
        '''Asks user to choose a Reddit post to generate a video by typing the index into terminal. Generates 
           `self.num_ask` options.'''
        n = None
        posts = self.get_posts()
        saveCursor()
        while n is None or n < 0 or n >= self.num_ask:
            print("Enter reddit post number (or 'q' to quit):", color='yellow')
            for i in range(self.num_ask):
                print(f'[{i}]: {posts[i].title}')
            x = input()
            if x == 'q': 
                print(f'Quitting TTVG', color='red')
                quit()
            try: n = int(x)
            except: n = None
            restoreCursor()
        
        self.title = posts[n].title
        self.author = posts[n].author
        self.body = posts[n].selftext
        print(f'Successfully chose [{n}]: {self.title}', color='green')

    def generate(self):
        '''Starts TTS, alignment, and video generation. Make sure to choose a post with `askPost()` before running.'''
        print(f'Creating directory...', color='yellow')
        t1 = time.time()
        self.make_dir()
        print(f'Successfully created directory', color='green', replace=True)

        print(f'Generating TTS...', color='yellow')
        self.tts(self.title, self.title_file, self.title_voice)
        print(f'Successfully generated TTS for title', color='green', replace=True)
        
        print(f'Generating TTS...', color='yellow')
        self.tts(self.body, self.body_file, self.voice)
        print(f'Successfully generated TTS for body', color='green', replace=True)

        saveCursor()
        print(f'Aligning body text with audio...', color='yellow')
        self.align()
        restoreCursor() # to remove alpha version warning
        print(f'Successfully aligned {self.num_words} words with audio', color='green')

        print(f'Generating video...', color='yellow')
        self.generate_video()
        t2 = time.time()
        print(f'Successfully generated video in {(t2 - t1):.2f} seconds', color='green', replace=True)

    def make_dir(self):
        '''Creates a new directory to store all generated files. Replaces the previous directory if it is made on the 
           same day. Default directory name is "`self.subreddit`-YYYY-MM-DD".'''
        self.date = datetime.today().strftime('%Y-%m-%d')
        self.dir_name = f'{self.subreddit}-{self.date}'

        try: 
            os.mkdir(self.dir_name)
        except OSError:
            shutil.rmtree(self.dir_name)
            os.mkdir(self.dir_name)

        self.title_file = f'{self.dir_name}/title.wav'
        self.body_file = f'{self.dir_name}/body.wav'
        self.text_file = f'{self.dir_name}/body.txt'
        self.json_file = f'{self.dir_name}/body.json'
        self.video_file = f'{self.dir_name}/video.mp4'

    def get_posts(self):
        '''Returns a list of `num_ask` reddit posts. Each post contains the body text, author, and title.'''
        load_dotenv()
        subreddit = {'AITA': 'amitheasshole', 'TIFU': 'TIFU', 'RA': 'relationship_advice'}[self.subreddit]
        client_id: str = os.getenv('CLIENT_ID')
        client_secret: str = os.getenv('CLIENT_SECRET')
        user_agent: str = "reddit slideshow test"
        username: str = os.getenv('REDDIT_USERNAME')
        password: str = os.getenv('REDDIT_PASSWORD')

        reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent, username=username, password=password)
        posts = list(reddit.subreddit(subreddit).top(time_filter=f'{self.time_frame}', limit=self.num_ask))
        return posts

    def clean_text(self, text: str):   
        '''Cleans and returns `text` for TTS and alignment. Add custom abbreviations to abbreviations.py.'''
        # Replacements
        text = f' {text} '
        text = text.replace("&#x200B;", "")
        text = text.replace("~", "")
        text = text.replace("*", " ")
        text = text.replace("&", " and ")
        text = text.replace("@",  " at ")
        text = text.replace("+", " plus ")
        text = text.replace("%", " percent ")
        text = text.replace("/", " slash ")
        text = text.replace("ä", "ae")
        text = text.replace("ö", "oe")
        text = text.replace("ü", "ue")
        text = text.replace("ß", "ss")
        text = text.replace("é", "e")
        text = text.replace("‘", "'")
        text = text.replace("’", "'")
        text = text.replace('“', '"')
        text = text.replace('”', '"')
        text = text.replace("(", " , ")
        text = text.replace(")", " , ")
        text = text.replace(",", " , ")
        text = text.replace(".", " . ")
        text = text.replace("!", " ! ")
        text = text.replace("?", " ? ")
        text = text.replace(";", " ; ")
        text = text.replace(":", " : ")

        text = ''.join(c for c in text if ord(c) < 127)

        for k, v in abbreviations.items():
            text = text.replace(f' {k} ', f' {v} ')

        text = ' '.join(text.split())
        
        # Space Corrections
        text = text.replace(" ,", ",")
        text = text.replace(" ;", ";")
        text = text.replace(" :", ":")
        text = text.replace(" .", ".")
        text = text.replace(" !", "!")
        text = text.replace(" ?", "?")

        text = text.replace('. " ', '." ')
        text = text.replace(', " ', '," ')
        text = text.replace('! " ', '!" ')
        text = text.replace('? " ', '?" ')
        text = text.replace(': " ', ':" ')
        text = text.replace('; " ', ';" ')
        text = text.replace(' " ', ' "')

        text = text.replace(',.', '.')
        text = text.replace(',!', '!')
        text = text.replace(',?', '?')
        text = text.replace(',:', ':')
        text = text.replace(',;', ';')
        text = text.replace(',,', ',')

        text = ' '.join(text.split())

        while text[0] in ' !:,.?' and len(text) > 1: text = text[1:]
        
        return text

    def short_tts(self, text: str, output_file: str, voice: str):
        '''Generates an audio file with speaker `self.voice` with TikTok TTS. Max 200 characters.'''
        session_id: str = '9e6640058e7d34318f5073a2bd5737b8'
        if (len(text) > 200): return
        
        r = requests.post(
            f"https://api16-normal-useast5.us.tiktokv.com/media/api/text/speech/invoke/?text_speaker={voice}&req_text={text}&speaker_map_type=0&aid=1233",
            headers={
                'User-Agent': f"com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)",
                'Cookie': f'sessionid={session_id}'
            }
        )

        if r.json()["message"] == "Couldn't load speech. Try again.": raise RuntimeError("TTS couldn't be generated")

        with open(output_file, "wb") as out:
            out.write(base64.b64decode([r.json()["data"]["v_str"]][0]))

    def tts(self, text: str, output_file: str, voice: str):
        '''Main TTS function, which splits `text` into chunks to run `short_tts()`.'''
        text = self.clean_text(text)
        text = text.replace('. ', '.\n')
        text = text.replace('? ', '?\n')
        text = text.replace('! ', '!\n')
        text = text.replace('; ', ';\n')
        text = text.replace(': ', ':\n')
        text = text.replace(', ', ',\n')
        text = text.replace('...\n ', '...')

        segments = [segment for sentence in text.split("\n") for segment in textwrap.wrap(sentence, 200)]
        speech = AudioSegment.empty()
        for i, segment in enumerate(segments):
            with tempfile.NamedTemporaryFile() as file:
                self.short_tts(segment, file.name, voice)
                speech += AudioSegment.from_mp3(file.name)
                print(f'Generating TTS... {i+1}/{len(segments)}', color='yellow', replace=True)
        speech.export(output_file, format='wav')

    def align(self):
        '''Runs forced alignment on the body text and a slowed-down version of the TTS audio to get start and end
           timestamps of each word. Generates a json file with timestamps.'''
        dictionary = 'english_us_arpa'
        acoustic_model = 'english_us_arpa'

        with open(self.text_file, 'w') as f:
            f.write(self.clean_text(self.body))

        with tempfile.TemporaryDirectory() as temp_dir:
            audio = AudioSegment.from_wav(self.body_file)
            audio = self.speed_change(audio, self.align_speed)
            audio.export(f'{temp_dir}/temp.wav', format='wav')
            mfa = subprocess.Popen(['mfa', 'align_one', f'{temp_dir}/temp.wav', self.text_file, dictionary, acoustic_model, f'{temp_dir}/temp.json', '--single_speaker', '--fine_tune', '--beam', '1000', '--output_format', 'json', '--clean', '-q', '-use_mp', '--num_jobs', '1'])
            out, err = mfa.communicate()
            
            with open(f'{temp_dir}/temp.json', mode='r') as temp_json:
                self.timestamps = [{'word':l[2], 'start':l[0] * self.align_speed, 'end':l[1] * self.align_speed} for l in json.load(temp_json)['tiers']['words']['entries']]
                self.num_words = len(self.timestamps)
                with open(self.json_file, mode='w') as out_json:
                    json.dump(self.timestamps, out_json)

    def speed_change(self, sound, speed=1.0):
        '''Custom pydub function to slow down audio for alignment.'''
        sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * speed)
        })
        return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)
            
    def generate_video(self):
        '''Generates subtitles and overlays with video in chunks of size `self.chunk_size`. Video is then combined with 
           the audio.'''
        with tempfile.TemporaryDirectory() as temp_dir:
            for i, subtitle in enumerate(self.timestamps):
                word = '' if subtitle['word'] == '<eps>' else subtitle['word']
                imager = Imager(word, self.author, self.title)
                imager.generate(f'{temp_dir}/{i}.png')
                print(f'Generating video... Generated subtitle frame {i}/{self.num_words}: {word}', color='yellow', replace=True)

            imager = TitlePic(self.title, self.author, self.subreddit)
            imager.generate(f'{self.dir_name}/title.png')
            print(f'Generating video... Generated title image', color='yellow', replace=True)

            title_length = float(ffmpeg.probe(self.title_file)['format']['duration'])
            body_length = float(ffmpeg.probe(self.body_file)['format']['duration'])
            base_length = float(ffmpeg.probe(self.base_video)['format']['duration'])
            total_length = title_length + body_length

            title_audio = ffmpeg.input(self.title_file)
            body_audio = ffmpeg.input(self.body_file)
            audio = ffmpeg.concat(title_audio, body_audio, v=0, a=1)

            offset = random.randint(0, int(base_length - total_length))

            video = ffmpeg.input(self.base_video)
            video = ffmpeg.trim(video, start=offset, end=offset+title_length)
            video = ffmpeg.setpts(video, 'PTS-STARTPTS')
            video = ffmpeg.filter(video, 'fps', f'{self.fps}')
            overlay = ffmpeg.input(f'{self.dir_name}/title.png')
            video = ffmpeg.overlay(video, overlay, enable=f'between(t,0,{title_length:.3f})')
            video = ffmpeg.output(video, f'{temp_dir}/title.mp4', vcodec = "h264_videotoolbox")
            # video = ffmpeg.output(video, f'{temp_dir}/title.mp4')
            print(f'Generating video... Starting video title', color='yellow', replace=True)
            ffmpeg.run(video, overwrite_output=True, quiet=True)
            print(f'Generating video... Generated video title', color='yellow', replace=True)

            num_chunks = math.ceil(self.num_words / self.chunk_size)
            count = 0
            for chunk in range(0, num_chunks):
                a = chunk * self.chunk_size
                b = min(self.num_words, (chunk + 1) * self.chunk_size)

                video = ffmpeg.input(self.base_video)
                start = offset + title_length + self.timestamps[a]['start']
                end = offset + title_length + (self.timestamps[b - 1]['end'] + 1 if chunk == num_chunks - 1 else self.timestamps[b]['start'])
                video = ffmpeg.trim(video, start=start, end=end)
                video = ffmpeg.setpts(video, 'PTS-STARTPTS')
                video = ffmpeg.filter(video, 'fps', f'{self.fps}')

                for subtitle in self.timestamps[a:b]:
                    start = subtitle['start'] - self.timestamps[a]['start']
                    end = subtitle['end'] - self.timestamps[a]['start']
                    overlay = ffmpeg.input(f'{temp_dir}/{count}.png')
                    video = ffmpeg.overlay(video, overlay, enable=f'between(t,{start:.3f},{end:.3f})')
                    count += 1

                video = ffmpeg.output(video, f'{temp_dir}/{chunk}.mp4', vcodec = "h264_videotoolbox")
                print(f'Generating video... Starting video chunk {chunk+1}/{num_chunks} (Size: {self.chunk_size})', color='yellow', replace=True)
                ffmpeg.run(video, overwrite_output=True, quiet=True)
                print(f'Generating video... Generated video chunk {chunk+1}/{num_chunks} (Size: {self.chunk_size})', color='yellow', replace=True)

            video = ffmpeg.input(f'{temp_dir}/title.mp4')
            for chunk in range(0, num_chunks):
                video = ffmpeg.concat(video, ffmpeg.input(f'{temp_dir}/{chunk}.mp4'), v=1, a=0)

            title_audio = ffmpeg.input(self.title_file)
            body_audio = ffmpeg.input(self.body_file)
            audio = ffmpeg.concat(title_audio, body_audio, v=0, a=1)
            audio = ffmpeg.filter(audio, 'atempo', f'{self.video_speed}')
            video = ffmpeg.setpts(video, f'{1 / self.video_speed}*PTS')

            video = ffmpeg.concat(video, audio, v=1, a=1)
            video = ffmpeg.output(video, self.video_file, vcodec = "h264_videotoolbox")
            # video = ffmpeg.output(video, self.video_file)
            print(f'Generating video... Combining videos', color='yellow', replace=True)
            ffmpeg.run(video, overwrite_output=True, quiet=True)
            print(f'Generating video... Combined videos', color='yellow', replace=True)

if __name__ == '__main__':
    import main