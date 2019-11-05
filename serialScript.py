#!/usr/bin/python3
import argparse
from serial import *

class Flasher():

    def __init__(self, device, baud=115200):
        self.serialInstance = Serial()
        self.serialInstance.baudrate = baud
        self.serialInstance.port = device
        self.serialInstance.bytesize = EIGHTBITS
        self.serialInstance.parity = PARITY_EVEN
        self.serialInstance.stopbits = STOPBITS_ONE
        
        self.serialInstance.open()
        
        if self.serialInstance.isOpen() is False:
            print("Cannot open serial port!")
            exit(1)
        
        
        
    def checkReady(self):
        self.serialInstance.write(to_bytes([0x7F]))
    

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', help='Set serial baud rate')
    parser.add_argument('-d', help='Serial Device Path')
    
    return parser
    
def main(FlasherObj):
    print("Here...")
    #FlasherObj.checkReady()

if __name__ == "__main__":
    arg_parser = parse_arguments()
    
    args = arg_parser.parse_args()
    if args.d is None:
        print("No device selected")
        exit(0)
        
    if args.b is None:
        print("Baud rate not selected, default=115200")
        args.b = 115200

    flashing = Flasher(args.d, args.b)
    main(flashing)
