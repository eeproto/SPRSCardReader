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
    self.keysheet  = document.worksheet_by_title('Key')

  def find_row_by_number(self, number):
    cells = self.keysheet.find(number)
    print('found row', cells[0].row)

  def entry(self, cardnumber, state):
    #self.find_row_by_number(cardnumber)
    us_timestamp = datetime.now().strftime('%m/%d/%Y-%H:%M:%S')
    iso_timestamp = datetime.now().isoformat()
    self.worksheet.append_table([iso_timestamp, cardnumber, state], start='A1', end=None, dimension='ROWS', overwrite=False)

class CardListener(object):

  def __init__(self, settings):
    self.cardid = ''
    self.settings = settings
    self.startchar = self.settings['startchar'] 
    self.stopchar_in = self.settings['stopchar_in']
    self.stopchar_out = self.settings['stopchar_out']
    self.collecting = False
    self.maxlength = 16

  def convert_card_number(self, card_characters):
    hexcard = int(card_characters, 16)
    if self.settings['hexformat'] == '2:2':
      facility = (hexcard>>16) & 0xffff
      card = hexcard & 0xffff
    elif self.settings['hexformat'] == '2:3':
      facility = (hexcard>>24) & 0xffff
      card = hexcard & 0xffffff
    else:
      raise Exception('hex format setting unknown')
    print('facility:', facility, 'card:', card)
    combined = f'{facility}{card}'
    return combined

  def register(self, card_characters, state):
    combined = self.convert_card_number(card_characters)
    CardSheet(self.settings).entry(combined, state)
  
  def on_press(self, key):
      try:
        #print('alphanumeric key {0} pressed'.format(key.char))
        if key.char == self.stopchar_in:
          self.collecting = False
          try:
            self.register(self.cardid, 'in')
          except Exception as ex:
            print('Error decoding card', self.cardid, ex)
          self.cardid = ''
        if key.char == self.stopchar_out:
          self.collecting = False
          try:
            self.register(self.cardid, 'out')
          except Exception as ex:
            print('Error decoding card', self.cardid, ex)
          self.cardid = ''
        if self.collecting:
          self.cardid += key.char
        if key.char == self.startchar:
          self.collecting = True
        if len(self.cardid)>self.maxlength:
          self.cardid = ''
          self.collecting = False
      except AttributeError:
          pass
          #print('special key {0} pressed'.format(key))
  
  def on_release(self, key):
      pass
      #print('{0} released'.format(key))
      #if key == keyboard.Key.esc:
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

