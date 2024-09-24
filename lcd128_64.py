"""
Micropython (Raspberry Pi Pico)
2022/1/12     DENGFEI
2024/9/23     Alchemist Aloha
lcd.Display() Only 94 limited characters in fonts can be displayed
"""
import time
from machine import I2C, Pin
import lcd128_64_fonts
cursor = [0, 0]
class lcd128_64:
    '''LCD12864 display ST7567S controller'''
    
    def __init__(self,dt,clk,bus,addr):
        self.addr = addr
        self.i2c = I2C(bus,sda=Pin(dt),scl=Pin(clk))
        self.init()
        
    def writebyte_command(self, cmd):
        '''Write a command to the display.'''
        self.reg_write(0x00, cmd)
    
    def writebyte_dat(self, dat):
        '''Write data to the display.'''
        self.reg_write(0x40, dat)
    
    def reg_write(self, reg, data):
        '''Write data to the register.'''
        msg = bytearray()
        msg.append(data)
        self.i2c.writeto_mem(self.addr, reg, msg)
    
    def init(self):
        '''Initialize the display.'''
        time.sleep(0.01)
        self.writebyte_command(0xe2)    # system reset
        time.sleep(0.01)
        self.writebyte_command(0xa2)    # 1/9 bias
        self.writebyte_command(0xa0)    # Set SEG direction, normal
        self.writebyte_command(0xc8)    # Set COM direction, normal
        self.writebyte_command(0x25)    # Select internal VDD regulator
        self.writebyte_command(0x81)    # Set electronic volume (EV) level
        self.writebyte_command(0x20)    # Set electronic volume (EV) level
        self.writebyte_command(0x2c)    # Booster on
        self.writebyte_command(0x2e)    # regulator on
        self.writebyte_command(0x2f)    # Follower on
        self.clear()
        # self.writebyte_command(0xff)    # 11111111
        # self.writebyte_command(0x72)    # 01110010
        # self.writebyte_command(0xfe)    # 11111110
        # self.writebyte_command(0xd6)    # 11010110 orig=d6
        # self.writebyte_command(0x90)    # 10010000
        # self.writebyte_command(0x9d)    # 10011101
        self.writebyte_command(0xaf)    # Display on
        self.writebyte_command(0x40)    # Set start line
        
    def clear(self):
        '''Clear the screen'''
        for i in range(8):
            self.writebyte_command(0xb0 + i)    # set page address
            self.writebyte_command(0x10)    # set column address MSB
            self.writebyte_command(0x00)    # set column address LSB
            for j in range(128):
                self.writebyte_dat(0x00)    # clear all columns
    
    def cursor(self, y, x):
        '''Set the cursor position. y: 0-7, x: 0-17'''
        if x > 17:
            x = 17
        if y > 7:
            y = 7
        cursor[0] = y
        cursor[1] = x
        
    def write_font(self, num):
        '''Write the corresponding font for each character in the text to the display.'''
        for item in lcd128_64_fonts.textFont[num]:
            self.writebyte_dat(item)
    
    def find_and_write_font(self, text):
        """
        Write the corresponding font for each character in the text to the display.
        
        Args:
            text (str): The string to be displayed.
        """
        font_map = {
            '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
            'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15, 'g': 16, 'h': 17, 'i': 18, 'j': 19,
            'k': 20, 'l': 21, 'm': 22, 'n': 23, 'o': 24, 'p': 25, 'q': 26, 'r': 27, 's': 28, 't': 29,
            'u': 30, 'v': 31, 'w': 32, 'x': 33, 'y': 34, 'z': 35, 'A': 36, 'B': 37, 'C': 38, 'D': 39,
            'E': 40, 'F': 41, 'G': 42, 'H': 43, 'I': 44, 'J': 45, 'K': 46, 'L': 47, 'M': 48, 'N': 49,
            'O': 50, 'P': 51, 'Q': 52, 'R': 53, 'S': 54, 'T': 55, 'U': 56, 'V': 57, 'W': 58, 'X': 59,
            'Y': 60, 'Z': 61, '!': 62, '"': 63, '#': 64, '$': 65, '%': 66, '&': 67, '\'': 68, '(': 69,
            ')': 70, '*': 71, '+': 72, ',': 73, '-': 74, '/': 75, ':': 76, ';': 77, '<': 78, '=': 79,
            '>': 80, '?': 81, '@': 82, '{': 83, '|': 84, '}': 85, '~': 86, ' ': 87, '.': 88, '^': 89,
            '_': 90, '`': 91, '[': 92, '\\': 93, ']': 94
        }
        for char in text:
            if char in font_map:
                self.write_font(font_map[char])
                
    def display(self, text):
        '''Display the text on the screen.'''
        self.writebyte_command(0xb0 + cursor[0])    # set page address
        self.writebyte_command(0x10 + cursor[1] * 7 // 16)  # set column address MSB. 7 pixels per character
        self.writebyte_command(0x00 + cursor[1] * 7 % 16)   # set column address LSB. 7 pixels per character
        try:
            self.find_and_write_font(text)
        except:
            print(f"Error: {e}")