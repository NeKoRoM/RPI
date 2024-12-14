import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../lib')))
import os
from lib.interface import Interface
from time import sleep
from serial.tools import list_ports

# Підключення до Dobot
port = list_ports.comports()[0].device
bot = Interface(port)

print('Bot status:', 'connected' if bot.connected() else 'not connected')

device_name = bot.get_device_name()
print('Name:', device_name)

bot.set_device_name('dobot-python')
device_name = bot.get_device_name()
print('New name:', device_name)

device_id = bot.get_device_id()
print('ID:', device_id)

device_serial_number = bot.get_device_serial_number()
print('Serial number:', device_serial_number)

[device_version_major, device_version_minor, device_version_revision] = bot.get_device_version()
print('Version: {}.{}.{}'.format(device_version_major, device_version_minor, device_version_revision))

device_time = bot.get_device_time()
print('Time: {}ms'.format(device_time))

# Reset name
bot.set_device_name(device_name)
