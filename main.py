from machine import Pin, I2C
from lcd128_64 import lcd128_64

# i2c config
clock_pin = 27
data_pin = 26
bus = 1
i2c_addr = 0x3f
use_i2c = True


def scan_for_devices():
    i2c = I2C(bus, sda=Pin(
        data_pin), scl=Pin(clock_pin))
    devices = i2c.scan()
    if devices:
        for d in devices:
            print(hex(d))
    else:
        print('no i2c devices')


if use_i2c:
    scan_for_devices()
    lcd = lcd128_64(data_pin, clock_pin, bus, i2c_addr)


lcd.cursor(0, 2)
lcd.display("ST7567S 128x64")
lcd.cursor(1, 0)
lcd.display("ABCDEFGHIJKLMNOPQR")
lcd.cursor(2, 0)
lcd.display("123456789+-*/<>=$@")
lcd.cursor(3, 0)
lcd.display("%^&(){}:;'|?,.~\\[]")
lcd.cursor(4, 2)
lcd.display("ST7567S 128x64")
lcd.cursor(5, 0)
lcd.display("ABCDEFGHIJKLMNOPQR")
lcd.cursor(6, 0)
lcd.display("123456789+-*/<>=$@")
lcd.cursor(7, 0)
lcd.display("%^&(){}:;'|?,.~\\[]")
