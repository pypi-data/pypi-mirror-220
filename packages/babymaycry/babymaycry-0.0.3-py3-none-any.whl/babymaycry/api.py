import pyaudio
import telegram


class BabyMayCry:
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.threshold = 1000
        
    def run(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

        print("Listening for baby cry...")

        while True:
            try:
                data = stream.read(1024)
                max_amplitude = max(abs(int.from_bytes(data, byteorder='little', signed=True)) for _ in range(1024))

                if max_amplitude > self.threshold:
                    print("Baby cry detected!")
                    self.send_message("Baby is crying!")

            except KeyboardInterrupt:
                break

        stream.stop_stream()
        stream.close()
        audio.terminate()
    
    def send_message(self, text):
        bot = telegram.Bot(token=self.bot_token)
        bot.sendMessage(chat_id=self.chat_id, text=text)

