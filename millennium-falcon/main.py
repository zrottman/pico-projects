from machine import Pin
import time
import random

class LED:
    def __init__(self, pin_num):
        self.led = Pin(pin_num, Pin.OUT)
        self.last_toggle = time.ticks_ms()
        self.state = False  # LED is initially off
        self.generate_random_interval()

    def update(self):
        now = time.ticks_ms()
        if time.ticks_diff(now, self.last_toggle) >= self.interval:
            self.state = not self.state
            self.led.value(self.state)
            self.last_toggle = now
            self.generate_random_interval()

    def generate_random_interval(self):
        if self.state:
            # LED is on: shorter intervals
            self.interval = random.randint(100, 1000)
        else:
            # LED is off: longer intervals
            self.interval = random.randint(1000, 3500)


leds = [
    LED(2),
    LED(3),
    LED(4),
    LED(5),
    LED(6),
    LED(7),
    LED(8),
    LED(9)
]

while True:
    for led in leds:
        led.update()
    time.sleep(0.01)