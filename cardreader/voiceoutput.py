import numpy as np
import sounddevice as sd
import os
import platform
from subprocess import Popen, PIPE
import json


class VoiceOutput(object):

  def __init__(self, settings, force_external_piper_call=False):
    self.settings = settings
    self.model = "en_US-lessac-medium"
    self.voice_path = os.getcwd()
    self.use_external_call_workaround = force_external_piper_call or (platform.system().lower() == 'windows')
    if self.use_external_call_workaround:
      # do this without using piper python libraries
      with open(f'{self.model}.onnx.json', 'r', encoding="utf8") as voice_config_file:
        self.sample_rate = json.load(voice_config_file)['audio']['sample_rate']
    else:
      from piper.voice import PiperVoice
      from piper.download import ensure_voice_exists, get_voices
      voices_available = get_voices(self.voice_path, update_voices=False)
      ensure_voice_exists(
        name=self.model,
        data_dirs=[self.voice_path],
        download_dir=self.voice_path,
        voices_info=voices_available)
      self.voice = PiperVoice.load(f'{self.model}.onnx')
      self.sample_rate = self.voice.config.sample_rate

  def say(self, text):
    if self.use_external_call_workaround:
      speech = self._stream_external(text)
    else:
      speech = self._stream_internal(text)
    with sd.OutputStream(samplerate=self.sample_rate, channels=1, dtype='int16') as speaker:
      speaker.start()
      for audio_bytes in speech:
        int_data = np.frombuffer(audio_bytes, dtype=np.int16)
        speaker.write(int_data)

  def _stream_internal(self, text):
    """
    use piper's internal synthesizer
    :param text: text to speak
    :return: synthesizer generator
    """
    return self.voice.synthesize_stream_raw(text)

  def _stream_external(self, text):
    """
    call the external piper command, which is necessary in windows due to a precompiled binary
    :param text: text to speak
    :return: array with one entry, which is a bytearray of the generateo voice output.
      this is an array to be compatible with the generator style access for the internal method
    """
    piper_call = [
      os.path.join('piper','piper'),
      '--model', os.path.join(self.voice_path, f'{self.model}.onnx'),
      '--output-raw'
    ]
    child = Popen(piper_call, shell=False, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    stdout, stderr = child.communicate(input=text.encode('utf-8'))
    # returncode = child.returncode
    return [stdout]
