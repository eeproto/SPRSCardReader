import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice
from piper.download import ensure_voice_exists, get_voices
import os

class VoiceOutput(object):

  def __init__(self, settings):
    self.settings = settings
    self.model = "en_US-lessac-medium"
    self.voice_path = os.getcwd()
    voices_available = get_voices(self.voice_path, update_voices=False)
    ensure_voice_exists(
      name=self.model,
      data_dirs=[self.voice_path],
      download_dir=self.voice_path,
      voices_info=voices_available)
    self.voice = PiperVoice.load(f'{self.model}.onnx')

  def say(self, text):
    stream = sd.OutputStream(samplerate=self.voice.config.sample_rate, channels=1, dtype='int16')
    stream.start()
    for audio_bytes in self.voice.synthesize_stream_raw(text):
      int_data = np.frombuffer(audio_bytes, dtype=np.int16)
      stream.write(int_data)
    stream.stop()
    stream.close()
