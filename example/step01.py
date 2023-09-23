import machine
import utime

spd = machine.PWM( machine.Pin(14, machine.Pin.OUT))
dir = machine.Pin(15, machine.Pin.OUT)

spd.duty_u16(32768)
dir.value(0)

min_hz = 9
max_hz = 3200

while True:
    dir.value(1)
    
    for i in range(min_hz, max_hz):
        spd.freq(i)
        print(i)
        utime.sleep_ms(10)
    
    for i in range(max_hz, min_hz, -1):
        spd.freq(i)
        print(i)
        utime.sleep_ms(10)
    

    dir.value(0)
    
    for i in range(min_hz, max_hz):
        spd.freq(i)
        print(i)
        utime.sleep_ms(10)
    
    for i in range(max_hz, min_hz, -1):
        spd.freq(i)
        print(i)
        utime.sleep_ms(10)
    

