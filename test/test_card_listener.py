import unittest
import datetime
import json
from unittest.mock import patch, MagicMock
from cardreader.cardreader import CardListener, CardSheet

class MockKey(object):
  def __init__(self, char):
    self.char = char

class CardListenerTester(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    with open('settings-test.json', 'r') as config_file:
      cls.settings = json.load(config_file)
    # cls.expected_facility = None
    # cls.expected_card = None
    cls.expected_card_characters = None

  def test_01_convert_hex(self):
    self.settings['hexformat'] = '2:2'
    (facility, card) = CardListener(self.settings).convert_card_number('1a2b3c4d')
    self.assertEqual(facility, '6699')
    self.assertEqual(card, '15437')
    self.settings['hexformat'] = '2:3'
    (facility, card) = CardListener(self.settings).convert_card_number('1a2b3c4d5e')
    self.assertEqual(facility, '6699')
    self.assertEqual(card, '3951966')

  def catch_registration(self, card_characters):
    # TODO: this approach does not seem to work, never gets called
    self.assertEqual(self.expected_card_characters, card_characters)

  def test_02_collect_checkin(self):
    l = CardListener(self.settings)
    # self.expected_facility = 202
    # self.expected_card = 65518
    self.expected_card_characters = 'CAFFEE'
    l.registration_handler = self.catch_registration
    l.on_press(MockKey(self.settings['startchar']))
    for char in 'CAFFEE':
      l.on_press(MockKey(char))
    l.on_press(MockKey(self.settings['stopchar_in']))



class CardSheetTester(unittest.TestCase):

  @classmethod
  def setUpClass(cls):
    with open('settings-test.json', 'r') as config_file:
      cls.settings = json.load(config_file)


  def test_02_find_a_card_number_in_key_sheet(self):
    found = CardSheet(self.settings).find_name_by_numbers('77','556677')
    self.assertEqual(found, 'Kate Ross')

  def test_03_entry_unknown_card(self):
    message = CardSheet(self.settings).entry('999', '999999999', 'in')
    self.assertEqual(message, 'error finding name')

  def test_01_entry_known_card(self):
    message = CardSheet(self.settings).entry('98', '6789', 'in')
    self.assertEqual(message, 'Jack Reacher checked in')
