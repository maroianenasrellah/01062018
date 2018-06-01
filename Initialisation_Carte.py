#!/usr/bin/env python
# -*- coding: utf8 -*-

from datetime import datetime
import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True
#secteur 0
B0S2=2
##secteur1
B1S4=4
B1S5=5
B1S6=6
##secteur2
B2S8=8
B2S9=9
B2S10=10

##secteur3
B3S12=12
B3S13=13
B3S14=14
# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print ("Welcome to the MFRC522 data read example")
print ("Press Ctrl-C to stop.")

print ("Passer le tag RFID a lire\n")
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print ("Card detected")
        print ("\n")
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:

        # Print UID
        print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))
    
        # This is the default key for authentication
        key= [0x59,0x61,0x50,0x6F,0x54,0x74]
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        
       
        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, B1S4, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            # Variable for the data to write
            data = []
            # Fill the data with 0x00
            for x in range(0,16):
                 data.append(0x00)
                #Fill the data with 0xFF
                #data.append(0xFF)
            print ("Sector  looked like this:")
            print ("\n")
            MIFAREReader.MFRC522_Read(B1S4)
           # print ("\n")
            MIFAREReader.MFRC522_Read(B1S5)
            #print ("\n")
            MIFAREReader.MFRC522_Read(B1S6)
            print ("Now we fill it with 0x00:")
            # Write the data
            MIFAREReader.MFRC522_Write(B1S4, data)
            #print ("\n")
            MIFAREReader.MFRC522_Write(B1S5, data)
           # print ("\n")
            MIFAREReader.MFRC522_Write(B1S6, data)
            #print ("It now looks like this:")
            print ("It is now empty:")
            print ("\n")
            # Check to see if it was written
            MIFAREReader.MFRC522_Read(B1S4)
            #print ("\n")
            MIFAREReader.MFRC522_Read(B1S5)
           # print ("\n")
            MIFAREReader.MFRC522_Read(B1S6)
        else:
             print ("Authentication error. Sector Trailer " + str(B1S4))
########################################################################################################################################
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, B2S8, key, uid)
        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            # Variable for the data to write
            data = []
            # Fill the data with 0x00
            for x in range(0,16):
                 data.append(0x00)
                #Fill the data with 0xFF
                #data.append(0xFF)
            print ("Sector  looked like this:")
            print ("\n")
            MIFAREReader.MFRC522_Read(B2S8)
           # print ("\n")
            MIFAREReader.MFRC522_Read(B2S9)
            #print ("\n")
            MIFAREReader.MFRC522_Read(B2S10)
            print ("Now we fill it with 0x00:")
            # Write the data
            MIFAREReader.MFRC522_Write(B2S8, data)
            #print ("\n")
            MIFAREReader.MFRC522_Write(B2S9, data)
           # print ("\n")
            MIFAREReader.MFRC522_Write(B2S10, data)
            #print ("It now looks like this:")
            print ("It is now empty:")
            print ("\n")
            # Check to see if it was written
            MIFAREReader.MFRC522_Read(B2S8)
            #print ("\n")
            MIFAREReader.MFRC522_Read(B2S9)
           # print ("\n")
            MIFAREReader.MFRC522_Read(B2S10)
        else:
             print ("Authentication error. Sector Trailer " + str(B2S8))
########################################################################################################################################
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, B3S12, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            # Variable for the data to write
            data = []
            # Fill the data with 0x00
            for x in range(0,16):
                 data.append(0x00)
                #Fill the data with 0xFF
                #data.append(0xFF)
            print ("Sector  looked like this:")
            print ("\n")
            MIFAREReader.MFRC522_Read(B3S12)
           # print ("\n")
            MIFAREReader.MFRC522_Read(B3S13)
            #print ("\n")
            MIFAREReader.MFRC522_Read(B3S14)
            print ("Now we fill it with 0x00:")
            # Write the data
            MIFAREReader.MFRC522_Write(B3S12, data)
            #print ("\n")
            MIFAREReader.MFRC522_Write(B3S13, data)
           # print ("\n")
            MIFAREReader.MFRC522_Write(B3S14, data)
            #print ("It now looks like this:")
            print ("It is now empty:")
            print ("\n")
            # Check to see if it was written
            MIFAREReader.MFRC522_Read(B3S12)
            #print ("\n")
            MIFAREReader.MFRC522_Read(B3S13)
           # print ("\n")
            MIFAREReader.MFRC522_Read(B3S14)
            
            # Stop
            MIFAREReader.MFRC522_StopCrypto1()

            # Make sure to stop reading for cards
            continue_reading = False
        else:
             print ("Authentication error. Sector Trailer " + str(B3S12))
########################################################################################################################################
      

        
             
       


