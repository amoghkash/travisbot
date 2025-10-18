import sys
sys.path.append('/home/travisbot/RPLCD')

from RPLCD.i2c import CharLCD

lcd = CharLCD("PCF8574", 0x26, 1, 20, 4)
lcd.write_string("Hello")
