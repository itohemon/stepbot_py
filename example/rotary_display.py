from machine import Pin, I2C, Timer
from ssd1306 import SSD1306_I2C
from time import sleep

upBtn = Pin(24, Pin.IN, Pin.PULL_UP)
downBtn = Pin(23, Pin.IN, Pin.PULL_UP)
state = None

timer = Timer()

# I2C variables
id = 0
sda = Pin(20)
scl = Pin(21)
i2c = I2C(id=id, scl=scl, sda=sda)

# Screen Variables
width = 128
height = 64
line = 1
highlight = 1
shift = 0
list_length = 0
total_lines = 6

# create the display
oled = SSD1306_I2C(width=width, height=height, i2c=i2c)
oled.init_display()


def get_menu():
    menu = ["menu1", "menu2", "menu3", "menu4", "menu5", "menu6", "menu7"]
    return(menu)

def show_menu(menu):
    global line, highlight, shift, list_length
    
    # menu variables
    item = 1
    line = 1
    line_height = 10
    
    # clear the display
    oled.fill_rect(0, 0, width, height, 0)
    
    list_length = len(menu)
    short_list = menu[shift:shift+total_lines]
    
    for item in short_list:
        if highlight == line:
            oled.fill_rect(0, (line-1) * line_height, width, line_height, 1)
            oled.text(">", 0, (line-1) * line_height, 0)
            oled.text(item, 10, (line-1) * line_height, 0)
            oled.show()
        else:
            oled.text(item, 10, (line-1) * line_height, 1)
            oled.show()
        line += 1
    oled.show()
    
def launch(filename):
    global file_list
    
    oled.fill_rect(0, 0, width, height, 0)
    oled.text("Launching", 1, 10)
    oled.text(filename, 1, 20)
    oled.show()
    sleep(3)
    # exec(open(filename).read())
    show_menu(file_list)
    
def downCB(timer):
    global highlight, shift, list_length
    
    if highlight < total_lines:
        highlight += 1
    else:
        if shift+total_lines < list_length:
            shift += 1
    show_menu(file_list)

def upCB(timer):
    global highlight, shift, list_length
    if highlight > 1:
        highlight -= 1
    else:
        if shift > 0:
            shift -= 1
    show_menu(file_list)

def upBtnDebounce(pin):
    timer.init(mode=Timer.ONE_SHOT, period=200, callback=upCB)

def downBtnDebounce(pin):
    timer.init(mode=Timer.ONE_SHOT, period=200, callback=downCB)

file_list = get_menu()
show_menu(file_list)

upBtn.irq(trigger=Pin.IRQ_FALLING, handler=upBtnDebounce)
downBtn.irq(trigger=Pin.IRQ_FALLING, handler=downBtnDebounce)


# Repeat forever
while True:
    print(highlight)
    sleep(0.1)