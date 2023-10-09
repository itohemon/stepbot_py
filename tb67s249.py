from machine import Pin, PWM
import utime

class TB67S249():

    def __init__(self,
                 pin_num_enablen, pin_num_dmode0, pin_num_dmode1, pin_num_dmode2, 
                 pin_num_resetn, pin_num_agc, pin_num_step, pin_num_dir):
        self._pin_num_enablen = pin_num_enablen
        self._pin_num_dmode0  = pin_num_dmode0
        self._pin_num_dmode1  = pin_num_dmode1
        self._pin_num_dmode2  = pin_num_dmode2
        self._pin_num_resetn  = pin_num_resetn
        self._pin_num_agc     = pin_num_agc
        self._pin_num_step    = pin_num_step
        self._pin_num_dir     = pin_num_dir
        self._run_mode = "v"
    
    def setRunMode(self, mode):
        self._enablen = Pin(self._pin_num_enablen, Pin.OUT)
        self._dmode0  = Pin(self._pin_num_dmode0,  Pin.OUT)
        self._dmode1  = Pin(self._pin_num_dmode1,  Pin.OUT)
        self._dmode2  = Pin(self._pin_num_dmode2,  Pin.OUT)
        self._resetn  = Pin(self._pin_num_resetn,  Pin.OUT)
        self._agc     = Pin(self._pin_num_agc,     Pin.OUT)
        self._dir     = Pin(self._pin_num_dir,     Pin.OUT)
        
        if (mode == "v"):
            self._step = PWM(Pin(self._pin_num_step))
            self._step.duty_u16(0)
        elif (mode == "p"):
            self._step = Pin(self._pin_num_step, Pin.OUT)
            self._step.off()
        else:
            print(f'Unsupport mode {mode}')
            return
        
        self._run_mode = mode
    
        self._ccw = True
        self._rpsteps = 0
            
        self._enablen.off()
        self._dmode0.off()
        self._dmode1.off()
        self._dmode2.off()
        self._resetn.off()
        self._agc.off()
        self._dir.off()
        
    def setForwardStep(self):
        interval_time = 1000
        if self._run_mode != "p":
            print("This func support only p mode")
            return
        
        if self._ccw:
            self.setDir(True)
        else:
            self.setDir(False)
        
        self._step.on()
        utime.sleep_us(interval_time)
        self._step.off()
        utime.sleep_us(interval_time)
        
    def setReverseStep(self):
        interval_time = 1000
        if self._run_mode != "p":
            print("This func support only p mode")
            return
        
        if self._ccw:
            self.setDir(False)
        else:
            self.setDir(True)
        
        self._step.on()
        utime.sleep_us(interval_time)
        self._step.off()
        utime.sleep_us(interval_time)
        
    def setRPS(self, rps):
        if rps > 0:
            if self._ccw:
                self.setDir(True)
            else:
                self.setDir(False)
        else:
            if self._ccw:
                self.setDir(False)
            else:
                self.setDir(True)
        
        rps = abs(rps)
        if rps < 0.05:
            rps = 0.0
        if rps > 3.0:
            rps = 3.0
        step = rps * self._rpsteps
        self.setStep(rps * self._rpsteps)
            
    def setCCWRot(self, flg):
        '''
        False ... CW
        True  ... CCW
        '''
        self._ccw = flg

    def setTorque(self, flg):
        if flg:
            self._enablen.off()
        else:
            self._enablen.on()

    def setStepSize(self, mode):
        if mode == 0:           # StandByMode(output disable)
            self._dmode0.off()
            self._dmode1.off()
            self._dmode2.off()
            self._rpsteps = 0
        elif mode == 1:         # Full step
            self._dmode0.off()
            self._dmode1.off()
            self._dmode2.on()
            self._rpsteps = 200
        elif mode == 2:         # Non-circular half step("a")
            self._dmode0.off()
            self._dmode1.on()
            self._dmode2.off()
            self._rpsteps = 400
        elif mode == 3:         # 1/4 step
            self._dmode0.off()
            self._dmode1.on()
            self._dmode2.on()
            self._rpsteps = 800
        elif mode == 4:         # Circular half step("b")
            self._dmode0.on()
            self._dmode1.off()
            self._dmode2.off()
            self._rpsteps = 400
        elif mode == 5:         # 1/8 step
            self._dmode0.on()
            self._dmode1.off()
            self._dmode2.on()
            self._rpsteps = 1600
        elif mode == 6:         # 1/16 step
            self._dmode0.on()
            self._dmode1.on()
            self._dmode2.off()
            self._rpsteps = 3200
        else:                    # 1/32 step
            self._dmode0.on()
            self._dmode1.on()
            self._dmode2.on()
            self._rpsteps = 6400

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
        if step == 0:
            self.stop()
        else:
            self._step.freq(int(step))
            
    def start(self):
        self._step.duty_u16(32768)

    def stop(self):
        self._step.duty_u16(0)
