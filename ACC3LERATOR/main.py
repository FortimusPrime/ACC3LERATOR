#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Objects
ev3 = EV3Brick()
engine = Motor(Port.A)
push_start = TouchSensor(Port.S4)
accelerator = Motor(Port.D)
# horn = TouchSensor(Port.S1)



# Adjustable Variables for easy engine tuning, without affecting unnecessary parts of the program.
engine_on = False
engine_off = True
current_rpms = 0
startup_rpms = 800
warmup_time = 300
idle_rpms = 250
acceleration_angle = 1

# Check
ev3.speaker.beep()  

# press_and_depress changes the boolean only after the button is pressed and then depressed. 
def press_and_depress(button, toggle):
    value = toggle
    if button.pressed():
        print("PRESSED")
        wait(10)
        while button.pressed(): # This loop gives the time space for releasing the button. 
            wait(10)
        print("LET GO")
        value = not value
    return value

def start_sequence(motor):
    global current_rpms
    count = 0
    while count < startup_rpms - 200:
        if press_and_depress(push_start, False):
            return False
        motor.run(count)
        wait(10)
        count += 5
    current_rpms = startup_rpms
    motor.run(current_rpms)
    
    # Holding the warmup rpms
    warmup = 0
    while warmup < warmup_time:
        if press_and_depress(push_start, False):
            return False
        print("LOOP 1, CURRENT RPMS:", current_rpms)
        wait(10)
        warmup += 1
        
    # Smoothly lowering the rpms
    while current_rpms > idle_rpms:
        if press_and_depress(push_start, False):
            return False
        print("LOOP 2, CURRENT RPMS:", current_rpms)
        current_rpms -= 1
        motor.run(current_rpms)
        wait(30)
    ev3.speaker.beep()  
    return True

ev3.speaker.set_volume(50)
ev3.speaker.set_speech_options(voice='m1')

# ev3.speaker.say("Welcome to")
# ev3.speaker.set_speech_options(language='de')
# ev3.speaker.say("Volkswagen!")
# ev3.speaker.set_speech_options(language='en')
# ev3.speaker.say("This is a model imitation of the 2.0 TSI engine. It's a 4-cylinder turbocharged engine. This model simply has the 4-cylinder orientation found in the real-life engine. You can push the pedal to accelerate after the engine warms up. Press the button to start!")


accelerator.reset_angle(1)
while True:
    # if horn.pressed():
    #     ev3.speaker.say("OK")
    #     ev3.speaker.play_file("bin/Semi Truck Horn.mp3")
        
    acceleration_angle = (int(accelerator.angle())*-1) * 5
    if acceleration_angle < 1:
        accelerator.reset_angle(1)
        
    ev3.screen.clear()
    ev3.screen.print("CURRENT RPMS: \n" +  str(current_rpms) + "\nANGLE: " + str(acceleration_angle))
    
    print("CURRENT RPMS:", current_rpms)
    print("ANGLE:", acceleration_angle)
    
    if (current_rpms > 600):
        ev3.light.on(Color.RED)
    else:
        ev3.light.on(Color.GREEN)
    
    current_rpms = idle_rpms + acceleration_angle
    engine.run(current_rpms) # This will make the engine run at the current_rpms in the program in every loop. 
    engine_on = press_and_depress(push_start, engine_on) # Checks for the button being clicked and released in every loop. 
   
    if engine_on and engine_off: # This condi
        ev3.light.on(Color.BLUE)
        engine_on = start_sequence(engine)
        engine_off = not engine_on
    elif engine_on:
        rmps = current_rpms
    else:
        engine.stop()
        current_rpms = 0
        engine_off = True
        
    wait(10)