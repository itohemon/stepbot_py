import machine
import time

ph0 = machine.ADC(0)
ph1 = machine.ADC(1)
ph2 = machine.ADC(2)
ph3 = machine.ADC(3)

while True:
    v0 = ph0.read_u16()
    v1 = ph1.read_u16()
    v2 = ph2.read_u16()
    v3 = ph3.read_u16()
    print("V0 ", v0, "V1 ", v1, "V2", v2, "V3", v3)
    
    time.sleep(0.1)
    