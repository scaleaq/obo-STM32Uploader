#!/usr/bin/python3
import argparse
from serial import *

ACK = 0x79
NACK = 0x1F

class Flasher():

    def __init__(self, device, baud=115200):
        self.serialInstance = Serial()
        self.serialInstance.baudrate = baud
        self.serialInstance.port = device
        self.serialInstance.bytesize = EIGHTBITS
        self.serialInstance.parity = PARITY_EVEN
        self.serialInstance.stopbits = STOPBITS_ONE
        self.serialInstance.timeout = 1

        self.serialInstance.open()

        if self.serialInstance.isOpen() is False:
            print("Cannot open serial port!")
            exit(1)

    #Send 0x7f on serial so that the host selects the connected UART port
    #and adjusts the baud rate.
    #All the command routines should start after this.
    def checkReady(self):
        self.serialInstance.write(to_bytes([0x7F]))
        response = self.serialInstance.read()
        response = hex(int.from_bytes(response,byteorder='little')) 
        #print(response)
        
        if len(response) == 0:
            print("Read timeout!")
            exit(1)
        
        if response == hex(ACK):
            print("Device ready!")
            
    def getCmd(self):
        print("Start Get...") #ToDo: Remove
        self.serialInstance.write(to_bytes([0x00, 0xFF]))
        
        #Wait for ACK/NACK
        response = self.serialInstance.read()
        
        if response == hex(ACK):
            print("Got ACK")
            #Get the number of bytes
            resp = self.serialInstance.read()
            resp = self.serialInstance.read(int(resp))
            #print the output of get here or store somewhere
            
        else:
            print("Communication Error!")
            exit(1)
    

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', help='Set serial baud rate')
    parser.add_argument('-d', help='Serial Device Path')
    
    return parser
    
def main(FlasherObj):
    print("Here...")
    FlasherObj.checkReady()

if __name__ == "__main__":
    arg_parser = parse_arguments()
    
    args = arg_parser.parse_args()
    if args.d is None:
        print("No device selected")
        exit(0)
        
    if args.b is None:
        print("Baud rate not selected, default=115200")
        args.b = 115200
    elif (int(args.b) < 1200 or int(args.b) > 115200) is True:
        print("Baud Rate should be between 1200 and 115200")
        exit(0)

    flashing = Flasher(args.d, args.b)
    main(flashing)
