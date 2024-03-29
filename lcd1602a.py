import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

rs = 14
rw = 15
e = 18
d0 = 2
d1 = 3
d2 = 4
d3 = 17
d4 = 27
d5 = 22
d6 = 10
d7 = 9
d = [d7, d6, d5, d4, d3, d2, d1, d0]

GPIO.setup((rs, rw, e, d0, d1, d2, d3, d4, d5, d6, d7), GPIO.OUT, initial=GPIO.LOW)

def writeCommand(commandCode):
    sleep(0.001)
    l = [int(bit) for bit in bin(commandCode)[2:]]
    while len(l) < 8:
        l.insert(0, 0)
    GPIO.output(rs, GPIO.LOW)
    GPIO.output(rw, GPIO.LOW)
    GPIO.output(d, l)
    GPIO.output(e, GPIO.HIGH)
    sleep(0.001)
    GPIO.output(e, GPIO.LOW)

def initial1602():
    writeCommand(0x38)
    writeCommand(0x0c)
    writeCommand(0x06)
    writeCommand(0x01)

def writeCharacter(c):
    sleep(0.001)
    l = [int(bit) for bit in bin(ord(c))[2:]]
    while len(l) < 8:
        l.insert(0, 0)
    GPIO.output(rs, GPIO.HIGH)
    GPIO.output(rw, GPIO.LOW)
    GPIO.output(d, l)
    GPIO.output(e, GPIO.HIGH)
    sleep(0.001)
    GPIO.output(e, GPIO.LOW)

def writeString(s):
    writeCommand(0x80)
    for c in s[:16]:
        writeCharacter(c)
    writeCommand(0x80 + 0x40)
    for c in s[16:]:
        writeCharacter(c)

if __name__ == '__main__':
    initial1602()
    try:
        while True:
            writeString("Hello, World!")
    except KeyboardInterrupt:
        GPIO.cleanup()
