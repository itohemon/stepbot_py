import machine
import time
from machine import Pin, I2C  # 入出力モジュール
import ssd1306                # 液晶表示器用ライブラリ
import math                   # 数学関数
import utime
from tb67s249 import TB67S249

ph = [0, 0, 0, 0]

# I2C設定 (I2C識別ID 0or1, SDA, SCL)
i2c = I2C(0, sda=Pin(20), scl=Pin(21) )
# 使用するSSD1306のアドレス取得表示（通常は0x3C）
addr = i2c.scan()
print( "OLED I2C Address :" + hex(addr[0]) )
# ディスプレイ設定（幅, 高さ, 通信仕様）
display = ssd1306.SSD1306_I2C(128, 64, i2c)
# Screen Variables
width = 128
height = 64
line = 1
highlight = 1
shift = 0
list_length = 0
total_lines = 6

# フォトインタラプタ
phPin0 = machine.ADC(0)
phPin1 = machine.ADC(1)
phPin2 = machine.ADC(2)
phPin3 = machine.ADC(3)

tact1 = Pin(24, Pin.IN, Pin.PULL_UP)
tact2 = Pin(23, Pin.IN, Pin.PULL_UP)
tact3 = Pin(22, Pin.IN, Pin.PULL_UP)

pressTact = 0

rightMotor = TB67S249( 7,  6,  5,  4,  3,  2, 1, 0)
leftMotor  = TB67S249(15, 14, 13, 12, 11, 10, 9, 8)

leftMotor.setRunMode("v")
leftMotor.setReset(False)
leftMotor.setTorque(True)
leftMotor.setStepSize(4)
leftMotor.setAgc(True)
leftMotor.setCCWRot(True)

rightMotor.setRunMode("v")
rightMotor.setReset(False)
rightMotor.setTorque(True)
rightMotor.setStepSize(4)
rightMotor.setAgc(True)
rightMotor.setCCWRot(False)

def readPhotoInterrupter(timer):
    global ph
    ph[0] = 65535 - phPin0.read_u16()
    ph[1] = 65535 - phPin1.read_u16()
    ph[2] = 65535 - phPin2.read_u16()
    ph[3] = 65535 - phPin3.read_u16()

timerPI = machine.Timer()
timerPI.init(freq=100, mode=machine.Timer.PERIODIC, callback=readPhotoInterrupter)

timerTact = machine.Timer()

def tact1cb(timer):
    global pressTact
    print(pressTact)
    if tact1.value():
        pressTact = 1

def tact2cb(timer):
    global pressTact
    print(pressTact)
    if tact2.value():
        pressTact = 2

def tact3cb(timer):
    global pressTact
    print(pressTact)
    if tact3.value():
        pressTact = 3

def tact1cbDebounce(pin):
    timerTact.init(mode=machine.Timer.ONE_SHOT, period=200, callback=tact1cb)

def tact2cbDebounce(pin):
    timerTact.init(mode=machine.Timer.ONE_SHOT, period=200, callback=tact2cb)

def tact3cbDebounce(pin):
    timerTact.init(mode=machine.Timer.ONE_SHOT, period=200, callback=tact3cb)

tact1.irq(trigger=Pin.IRQ_RISING, handler=tact1cbDebounce)
tact2.irq(trigger=Pin.IRQ_RISING, handler=tact2cbDebounce)
tact3.irq(trigger=Pin.IRQ_RISING, handler=tact3cbDebounce)

def drawSensorDisplay():
    display.fill(0) # 表示内容消去
    display.text('PhotoInterrupter', 2, 2, True)  # ('内容', x, y, 色) テキスト表示
    display.hline(0, 12, 128, True)            # (x, y, 長さ, 色) 指定座標から横線
    display.hline(0, 32, 128, True)            # (x, y, 長さ, 色) 指定座標から横線
    display.hline(0, 52, 128, True)            # (x, y, 長さ, 色) 指定座標から横線
    display.vline(64, 12, 40, True)            # (x, y, 長さ, 色) 指定座標から 縦線
    
    display.text(str(ph[0]),  2, 20, True)
    display.text(str(ph[1]), 66, 20, True)
    display.text(str(ph[2]),  2, 40, True)
    display.text(str(ph[3]), 66, 40, True)
    
    # 設定した内容を表示
    display.show()

def get_menu():
    menu = ["menu1", "menu2", "menu3", "menu4", "menu5", "menu6", "menu7"]
    return(menu)

def drawMainDisplay(menu):
    global line, highlight, shift, list_length
    
    # menu variables
    item = 1
    line = 1
    line_height = 10
    
    # clear the display
    display.fill(0) # 表示内容消去
    #display.fill_rect(0, 0, width, height, 0)
    
    list_length = len(menu)
    short_list = menu[shift:shift+total_lines]
    
    for item in short_list:
        if highlight == line:
            display.fill_rect(0, (line-1) * line_height, width, line_height, 1)
            display.text(">", 0, (line-1) * line_height, 0)
            display.text(item, 10, (line-1) * line_height, 0)
            #display.show()
        else:
            display.text(item, 10, (line-1) * line_height, 1)
            #display.show()
        line += 1
    display.show()

e_pre = 0
ie = 0

def goToWallCallback(timer):
    global e_pre
    global ie
    
    KP = 0.00003
    KD = 0
    KI = 0
    T = 0.01
    
    time.sleep(T)
    
    y = (ph[1] + ph[2]) / 2
    r = 60000
    
    e = r - y
    de = (e - e_pre) / T
    ie = ie + (e + e_pre) * T / 2
    u = KP * e + KI * ie + KD * de
    
    print("PID: " + str(u))
    
    leftMotor.setRPS(u)
    rightMotor.setRPS(u)
    e_pre = e

def GoToWall():
    timerGoToWall = machine.Timer()
    leftMotor.start()
    rightMotor.start()
    timerGoToWall.init(freq=50, mode=machine.Timer.PERIODIC, callback=goToWallCallback)


menuNum = 0
menu = get_menu()
drawMainDisplay(menu)

countDown = False
countStartTime = utime.ticks_ms()

while True:
    if menuNum == 1:
        if pressTact == 3:
            menuNum = 0
            pressTact = 0
            drawMainDisplay(menu)
        else:
            drawSensorDisplay()
    elif menuNum == 0:
        if pressTact == 3:
            menuNum = 1
            pressTact = 0
            drawSensorDisplay()
        else:
            drawMainDisplay(menu)

    if pressTact == 2:
        countDown = True
        pressTact = 0
        countStartTime = utime.ticks_ms()

    if countDown:
        elapsed = 3 - int((utime.ticks_ms() - countStartTime) / 1000)
        print(elapsed)
        if elapsed <= 0:
            countDown = False
            GoToWall()