import machine
import utime

def task1(last_run):
    diff_time = utime.ticks_diff(utime.ticks_us(), last_run)
    if diff_time > 10000: # 10msごとに実行
        v0 = ph0.read_u16()
        v1 = ph1.read_u16()
        v2 = ph2.read_u16()
        v3 = ph3.read_u16()
        print("Time", diff_time, "V0 ", v0, "V1 ", v1, "V2", v2, "V3", v3)
        return utime.ticks_us()
    return last_run


ph0 = machine.ADC(0)
ph1 = machine.ADC(1)
ph2 = machine.ADC(2)
ph3 = machine.ADC(3)

last_run1 = utime.ticks_us()

while True:
    last_run1 = task1(last_run1)