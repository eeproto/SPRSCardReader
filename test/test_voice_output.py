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

  def test_01say_hi(self):
    VoiceOutput(self.settings).say('this is a test, 1, 2, 3.')

