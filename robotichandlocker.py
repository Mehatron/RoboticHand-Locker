#!/usr/bin/env python

import RPi.GPIO as GPIO
import MFRC522
import signal

database = (
     [ 0, 4, 0, 5, 9, 9, 8, 0, 0, 0, 1, 13, 0, 0, 0, 0 ],
     [ 0, 4, 0, 5, 9, 9, 8, 0, 0, 0, 1, 13, 255, 255, 255, 255 ]
)

reading = True

def signal_handler(signum, frame):
    global reading
    reading = False
    GPIO.cleanup()

def toggle_lock():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p.communicate()

    for line in out.splitlines():
        if 'RoboticHand' in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGUSR1)

signal.signal(signal.SIGINT, signal_handler)

reader = MFRC522.MFRC522()

while reading:
    (status, tagType) = reader.MFRC522_Request(reader.PICC_REQIDL)

    if status == reader.MI_OK:

        (status, uid) = reader.MFRC522_Anticoll()

        if status == reader.MI_OK:

            key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]

            reader.MFRC522_SelectTag(uid)

            status = reader.MFRC522_Auth(reader.PICC_AUTHENT1A, 8, key, uid)

            if status == reader.MI_OK:
                status, user = reader.MFRC522_Read(8)
                if status == False:
                    continue;
                for data in database:
                    wrong = False
                    print user
                    for i in range(0, 16):
                        if user[i] != data[i]:
                            wrong = True
                            break
                    if wrong == False:
                        toggle_lock()
                reader.MFRC522_StopCrypto1()
