import unittest
import datetime
import json
from unittest.mock import patch, MagicMock
from cardreader.voiceoutput import VoiceOutput


class VoiceOuputTester(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    with open('settings-test.json', 'r') as config_file:
      cls.settings = json.load(config_file)

  def test_01_say_hi(self):
    vo = VoiceOutput(self.settings)
    vo.say('this is a test, 1, 2, 3.')

  def test_02_say_hi_with_workaround(self):
    vo = VoiceOutput(self.settings)
    vo.use_external_call_workaround = True
    vo.say('speaking through external call.')
