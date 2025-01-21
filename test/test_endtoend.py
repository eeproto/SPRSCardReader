import unittest
import datetime
import json
from unittest.mock import patch, MagicMock


class EndToEndTester(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    with open('settings-test.json', 'r') as config_file:
      cls.settings = json.load(config_file)

  def test_01_checkin(self):
    self.fail()

  def test_02_checkout(self):
    self.fail()

  def test_03_cardunknown(self):
    self.fail()

