from machine import Pin, PWM

class TB67S249():

    def __init__(self,
                 pin_num_enablen, pin_num_dmode0, pin_num_dmode1, pin_num_dmode2, 
                 pin_num_resetn, pin_num_agc, pin_num_step, pin_num_dir):
        self._enablen = Pin(pin_num_enablen, Pin.OUT)
        self._dmode0 = Pin(pin_num_dmode0, Pin.OUT)
        self._dmode1 = Pin(pin_num_dmode1, Pin.OUT)
        self._dmode2 = Pin(pin_num_dmode2, Pin.OUT)
        self._resetn = Pin(pin_num_resetn, Pin.OUT)
        self._agc    = Pin(pin_num_agc, Pin.OUT)
        self._step   = PWM(Pin(pin_num_step))
        self._dir    = Pin(pin_num_dir, Pin.OUT)
        
        self._enablen.off()
        self._dmode0.off()
        self._dmode1.off()
        self._dmode2.off()
        self._resetn.off()
        self._agc.off()
        self._dir.off()
        self._step.duty_u16(0)

    def setEnable(self, flg):
        if flg:
            self._enablen.off()
        else:
            self._enablen.on()

    def setStepSize(self, mode):
        if mode == 0:           # StandByMode(output disable)
            self._dmode0.off()
            self._dmode1.off()
            self._dmode2.off()
        elif mode == 1:         # Full step
            self._dmode0.off()
            self._dmode1.off()
            self._dmode2.on()
        elif mode == 2:         # Non-circular half step("a")
            self._dmode0.off()
            self._dmode1.on()
            self._dmode2.off()
        elif mode == 3:         # 1/4 step
            self._dmode0.off()
            self._dmode1.on()
            self._dmode2.on()
        elif mode == 4:         # Circular half step("b")
            self._dmode0.on()
            self._dmode1.off()
            self._dmode2.off()
        elif mode == 5:         # 1/8 step
            self._dmode0.on()
            self._dmode1.off()
            self._dmode2.on()
        elif mode == 6:         # 1/16 step
            self._dmode0.on()
            self._dmode1.on()
            self._dmode2.off()
        else:                    # 1/32 step
            self._dmode0.on()
            self._dmode1.on()
            self._dmode2.on()

    def setReset(self, flg):
        if flg:
            self._resetn.off()
        else:
            self._resetn.on()

    def setAgc(self, flg):
        if flg:
            self._agc.on()
        else:
            self._agc.off()

    def setDir(self, flg):
        if flg:
            self._dir.on()
        else:
            self._dir.off()

    def setStep(self, step):
        if step < 8:
            self._step.freq(8)
        elif step < 800:
            self._step.freq(step)
        else:
            self._step.freq(800)
            
    def start(self):
        self._step.duty_u16(32768)

    def stop(self):
        self._step.duty_u16(0)
