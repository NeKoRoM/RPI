import sys
import os
# import lib directory
# Додаємо шлях до батьківської директорії поточного файлу
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
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



print(bot.get_pose())
# One axis at a time
bot.set_point_to_point_command(3, 100, 10, 10, 10)
sleep(1)

# One axis at a time
#bot.set_point_to_point_command(3, 30, 30, 30, 30)
#sleep(1)

def reset_error():
    device_alarm = bot.get_alarms_state()
    print(device_alarm)
    bot.clear_alarms_state()
    device_alarm = bot.get_alarms_state()
    print(device_alarm)
#reset_error()
