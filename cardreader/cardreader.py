from pynput import keyboard
import pygsheets
from datetime import datetime, timezone
import json


class CardSheet(object):

  def __init__(self, settings):
    gclient = pygsheets.authorize('client_secret_rfidsheets.json', local=True)
    # TODO: json import sheets id
    document = gclient.open_by_key(settings['sheets_id'])
    self.worksheet = document.worksheet_by_title('Active')
    self.keysheet = document.worksheet_by_title('Key')
    self.keysheet_first_column = 4
    self.keysheet_last_column = 5
    self.keysheet_card_number_column = 2
    self.keysheet_site_number_column = 1

  def find_row_by_number(self, number):
    cells = self.keysheet.find(number)
    print('found row', cells[0].row)

  def entry(self, facility, card, state):
    # us_timestamp = datetime.now().strftime('%m/%d/%Y-%H:%M:%S')
    iso_timestamp = datetime.now().isoformat()
    try:
      self.worksheet.append_table([iso_timestamp, f'{facility}{card}', state], start='A1', end=None, dimension='ROWS',
                           overwrite=False)
    except Exception as ex:
      return f'error writing to sheet {ex}'
    try:
      name = self.find_name_by_numbers(facility, card)
      return f'{name} checked {state}'
    except Exception as ex:
      return f'error finding name'

  def find_name_by_numbers(self, site_number, card_number):
    cells = self.keysheet.find(card_number, matchEntireCell=True)
    if len(cells) == 0:
      raise Exception('can not find site number')
    match_row = None
    for cell in cells:
      if self.keysheet.cell((cell.row, self.keysheet_site_number_column)).value == site_number:
        match_row = cell.row
    return f'{self.keysheet.cell((match_row, self.keysheet_first_column)).value} {self.keysheet.cell((match_row, self.keysheet_last_column)).value}'


class CardListener(object):

  def __init__(self, settings):
    self.cardid = ''
    self.settings = settings
    self.startchar = self.settings['startchar']
    self.stopchar_in = self.settings['stopchar_in']
    self.stopchar_out = self.settings['stopchar_out']
    self.collecting = False
    self.maxlength = 16
    self.registration_handler = self.register

  def convert_card_number(self, card_characters):
    hexcard = int(card_characters, 16)
    if self.settings['hexformat'] == '2:2':
      facility = (hexcard >> 16) & 0xffff
      card = hexcard & 0xffff
    elif self.settings['hexformat'] == '2:3':
      facility = (hexcard >> 24) & 0xffff
      card = hexcard & 0xffffff
    else:
      raise Exception('hex format setting unknown')
    print('facility:', facility, 'card:', card)
    return (str(facility), str(card))

  def register(self, card_characters, state):
    facility, card = self.convert_card_number(card_characters)
    result_message = CardSheet(self.settings).entry(facility, card, state)

  def on_press(self, key):
    try:
      # print('alphanumeric key {0} pressed'.format(key.char))
      if key.char == self.stopchar_in:
        self.collecting = False
        try:
          self.registration_handler(self.cardid, 'in')
        except Exception as ex:
          print('Error decoding card', self.cardid, ex)
        self.cardid = ''
      if key.char == self.stopchar_out:
        self.collecting = False
        try:
          self.registration_handler(self.cardid, 'out')
        except Exception as ex:
          print('Error decoding card', self.cardid, ex)
        self.cardid = ''
      if self.collecting:
        self.cardid += key.char
      if key.char == self.startchar:
        self.collecting = True
      if len(self.cardid) > self.maxlength:
        self.cardid = ''
        self.collecting = False
    except AttributeError:
      pass
      # print('special key {0} pressed'.format(key))

  def on_release(self, key):
    pass
    # print('{0} released'.format(key))
    # if key == keyboard.Key.esc:
    #    # Stop listener
    #    return False


if __name__ == '__main__':
  with open('settings.json', 'r') as config_file:
    settings = json.load(config_file)
  cards = CardListener(settings)

  # Collect events until released
  with keyboard.Listener(
      on_press=cards.on_press,
      on_release=cards.on_release) as listener:
    listener.join()

#  # ...or, in a non-blocking fashion:
#  listener = keyboard.Listener(
#      on_press=on_press,
#      on_release=on_release)
#  listener.start()
