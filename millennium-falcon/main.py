from machine import Pin
import time
import random
from neopixel import NeoPixel

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

class PulsingStrip:
    def __init__(self, pin_num, num_leds, target_color, steps_increasing, steps_decreasing):
        self.np = NeoPixel(Pin(pin_num), num_leds)
        self.target_color = target_color
        self.step_up = tuple(c / steps_increasing for c in target_color)
        self.step_down = tuple(c / steps_decreasing for c in target_color)
        self.current_color = [0.0, 0.0, 0.0]
        self.is_increasing = True

    def update(self):
        if self.is_increasing:
            self.current_color = [
                min(curr + step, target)
                for curr, step, target in zip(self.current_color, self.step_up, self.target_color)
            ]

            if all(curr >= target for curr, target in zip(self.current_color, self.target_color)):
                self.is_increasing = False
        else:
            self.current_color = [
                max(curr - step, 0)
                for curr, step in zip(self.current_color, self.step_down)
            ]

            if all(curr <= 0 for curr in self.current_color):
                self.is_increasing = True

        self.np.fill((int(self.current_color[0]), int(self.current_color[1]), int(self.current_color[2])))
        self.np.write()

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

pulsing_strip = PulsingStrip(pin_num=15, num_leds=120, target_color=(10, 10, 20), steps_increasing=150, steps_decreasing=20)

while True:
    for led in leds:
        led.update()
    pulsing_strip.update()
    time.sleep(0.01)