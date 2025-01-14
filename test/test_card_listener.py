import unittest
import datetime
import json
from unittest.mock import patch, MagicMock
from cardreader.cardreader import CardListener, CardSheet


class CardListenerTester(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    with open('../cardreader/settings-test.json', 'r') as config_file:
      cls.settings = json.load(config_file)

  def test_01_convert_hex(self):
    self.settings['hexformat'] = '2:2'
    combined = CardListener(self.settings).convert_card_number('1a2b3c4d')
    self.assertEqual(combined, '669915437')
    self.settings['hexformat'] = '2:3'
    combined = CardListener(self.settings).convert_card_number('1a2b3c4d5e')
    self.assertEqual(combined, '66993951966')

class CardSheetTester(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    with open('../cardreader/settings-test.json', 'r') as config_file:
      cls.settings = json.load(config_file)


  def test_02_find_a_card_number_in_key_sheet(self):
    found = CardSheet(self.settings).find_cardnumber_by_key('73','18310')
    self.assertEqual(found, 'Dylan Condell')
