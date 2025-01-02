from pynput import keyboard
import pygsheets
from datetime import datetime, timezone

class CardSheet(object):

  def __init__(self):
    gclient = pygsheets.authorize('client_secret_rfidsheets.json', local=True)
    # TODO: json import sheets id
    document = gclient.open_by_key(sheets_id)
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

  def __init__(self):
    self.cardid = ''
    self.startchar = '~'
    self.stopchar_in = '#'
    self.stopchar_out = '$'
    self.collecting = False
    self.maxlength = 16

  def register(self, state):
    hexcard = int(self.cardid, 16)
    facility = (hexcard>>16) & 0xff
    card = hexcard & 0xffff
    combined = f'{facility}{card}'
    print('facility:', facility, 'card:', card)
    CardSheet().entry(combined, state)
  
  def on_press(self, key):
      try:
        #print('alphanumeric key {0} pressed'.format(key.char))
        if key.char == self.stopchar_in:
          self.collecting = False
          try:
            self.register('in')
          except Exception as ex:
            print('Error decoding card', self.cardid, ex)
          self.cardid = ''
        if key.char == self.stopchar_out:
          self.collecting = False
          try:
            self.register('out')
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
  cards = CardListener()

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

