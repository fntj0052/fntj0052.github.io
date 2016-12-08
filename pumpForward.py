import sys
import time
import RPi.GPIO as GPIO


mode=GPIO.getmode()
print " mode ="+str(mode)


StepPinForward=32
StepPinBackward=36

GPIO.setmode(GPIO.BOARD)
GPIO.setup(StepPinForward, GPIO.OUT)
GPIO.setup(StepPinBackward, GPIO.OUT)

def forward(x):
    GPIO.output(StepPinForward, GPIO.HIGH)
    print "forwarding running pump"
    time.sleep(10)
    GPIO.output(StepPinForward, GPIO.LOW)


print "forward pump"
forward(5)

print "Stopping motor"
GPIO.cleanup()
