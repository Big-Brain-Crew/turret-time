import RPi.GPIO as GPIO
import math
import time
import socket
import asyncio
from threading import Thread

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
message = b'Connected'
addr = ("add your ip address here!", 12000)
client_socket.sendto(message, addr)

servoPIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
p = GPIO.PWM(servoPIN, 50) # for PWM with 50Hz
p.start(0) # Initialization

start_time = time.time()
servo_target = 0;

# servo updater callback
def updateServoCommand_cb(servo_command_pin, cycle_freq):
    while True:
        time.sleep(1/cycle_freq);
        servo_command_pin.ChangeDutyCycle(servo_target)

# sine wave callback - keeps the servo target tracking a configurable sinewave
def sine_cb(hz, amp, center):
    while True:
        global servo_target
        time.sleep(1/hz)
        time_dif = time.time() - start_time
        val = time_dif % (1/hz)
        adjusted_val = val*hz*hz*2*math.pi
        cent_adj = center - (amp/2)
        servo_target = ((math.sin(adjusted_val) * amp + amp)/2) + cent_adj

# maps the values. Considering the servos are usually in the range of  2-12ish
#    then this will come in handy for converting all sorts of things
def mapValue( value, fromLow, fromHigh, toLow, toHigh):
    return ((toHigh-toLow)*(value-fromLow) / (fromHigh - fromLow) + toLow)

# sine tracking thread:  10hz frequency, 6 amplitude, 7 as the sine center.
sine_thread = Thread(target = sine_cb,args = (10,6,7))
#sine_thread.start()

# update servo's command: gpio 23, running at 10 hz
servo_thread = Thread(target = updateServoCommand_cb, args = (p,100))
servo_thread.start()

async def newUpdateMessage (update_fq):
    print ("we be updating things")
    

# asyncio functions for udp comms
async def updateMessage (update_fq):
    while True:
        message, address = client_socket.recvfrom(50)
        joystick_data = message.decode('utf-8').split(", ")
        # print("updated message:", message, "joystick_data:", joystick_data)
        joystick_data_y = float(joystick_data[1])
        normalized_joystick = mapValue(joystick_data_y, -1.0, 1.0, 2, 12)
        global servo_target
        servo_target = normalized_joystick
        await asyncio.sleep(1/update_fq)

async def main():
    global message
    await asyncio.gather(updateMessage(30))

    
if __name__ == "__main__":
    try:
        asyncio.run(main())
      
    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()
