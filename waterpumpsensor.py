########################################
#  Login credentials to send email#
########################################

username = 'jv2ee@yahoo.com'
password = 'EmailPassword'

############################
# General Email Parameters #
############################ 

From = "jv2ee@yahoo.com"
To =  "jv2ee@yahoo.com"

#######################################
# Email Parameters when sensor is Wet #
#######################################

Subject_wet = "RPi Water Sensor is WET"
Body_wet = "Your water sensor is wet."

#######################################
# Email Parameters when semsor is Dry #
#######################################

Subject_dry = "RPi Water Sensor is DRY"
Body_dry = " Your water sensor is dry again!"

import smtplib
from email.mime.text import MIMEText
import RPi.GPIO as GPIO
import string
import time

#Function Definitions

#takes either "wet" or "dry" as the condition.
def email(condition):
    print "Attempting to send email"
    if condition == 'wet':
        Body = string.join((
        "From: %s" % From,
        "To: %s" % To,
        "Subject: %s" % Subject_wet,
        "",
        Body_wet,
        ), "\r\n")
    if condition == 'dry':        
        Body = string.join((
            "From: %s" % From,
            "To: %s" % To,
            "Subject: %s" % Subject_dry,
            "",
            Body_dry,
            ), "\r\n")
    
    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    print "Logging in..."
    server.login(username,password)
    print "Logged in as "+username+"."
    server.sendmail(From, [To], Body)
    server.quit()
    print "Email sent."

#Tests whether wter is present.
# returns 0 for dry
# returns 1 for wet
# tested to work on pin 18 
def RCtime (RCpin):
    reading = 0
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RCpin, GPIO.OUT)
    GPIO.output(RCpin, GPIO.LOW)
    time.sleep(0.1) 
    GPIO.setup(RCpin, GPIO.IN)
    # This takes about 1 millisecond per loop cycle
    while True:
        if (GPIO.input(RCpin) == GPIO.LOW):
            reading += 1
        if reading >= 1000:
            return 0
        if (GPIO.input(RCpin) != GPIO.LOW):
            return 1


def buzz_on (pin):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def buzz_off(pin):

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# Main Loop

print 'Waiting for wetness...'
while True:
    time.sleep(1)
    if RCtime(18) == 1:
        print "Sensor is wet"
        email('wet')
        while True:
            time.sleep(1)
            if RCtime(18) == 1:
                print "Sensor is still wet..."
                buzz_on(17)
                continue
            if RCtime(18) == 0:
                buzz_off(17)
                print "Sensor is dry again"
                email('dry')
                print "Waiting for wetness..."
                break
