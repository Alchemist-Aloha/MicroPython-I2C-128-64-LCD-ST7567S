from ST7567 import ST7567
import machine
import time

C_SDA = 26
C_SCL = 27
sda_pin = machine.Pin(C_SDA)
scl_pin = machine.Pin(C_SCL)
i2c = machine.I2C(1, sda=sda_pin, scl=scl_pin, freq=100000)

oled = ST7567( 128, 64, i2c )
oled.set_contrast(25)
oled.text("1234567890123456", 0, 00)
oled.text("abcdefghijklmnop", 0, 10)
oled.text("qrstuvwxyz", 0, 20)
oled.text("ABCDEFGHIJKLMNOP", 0, 30)
oled.text("QRSTUVWXYZ", 0, 40)
oled.text("5678901234567890", 0, 50)
oled.text("6789012345678901", 0, 60)
oled.show()