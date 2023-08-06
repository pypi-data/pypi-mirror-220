import pyaudio
import telegram
import asyncio
import audioop


class BabyMayCry:
    def __init__(self, bot_token, chat_id, threadhold=1000, verbose=False):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.threshold = threadhold
        self.verbose = verbose
        
    def run(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024)

        print("Listening for baby cry...")

        while True:
            try:
                data = stream.read(1024)
                rms = audioop.rms(data, 2)
                
                if self.verbose:
                    print("RMS:", rms)

                if rms > self.threshold:
                    print("Baby cry detected!")
                    self.send_message("Baby is crying!")
            except Exception as e:
                stream.stop_stream()
                stream.close()
                audio.terminate()
                raise e
        
    def infinity_run(self):
        while True:
            try:
                self.run()
            except Exception as e:
                import time
                print(e)
                time.sleep(5)
                continue
  
    def send_message(self, text):
        bot = telegram.Bot(token=self.bot_token)
        asyncio.run(bot.sendMessage(chat_id=self.chat_id, text=text))

