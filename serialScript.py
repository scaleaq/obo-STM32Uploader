#!/usr/bin/python3
import argparse
from serial import *

class Flasher():

    def __init__(self, baud=115200):
        self.serialInstance = Serial()
        self.serialInstance.baudrate = baud
        self.serialInstance.port = "/dev/ttyUSB0" #Remove Hardcode
        self.serialInstance.bytesize = EIGHTBITS
        self.serialInstance.parity = PARITY_EVEN
        self.serialInstance.stopbits = STOPBITS_ONE
        
    def checkReady(self):
        self.serialInstance.write(to_bytes([0x7F]))
    

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', help='Set serial baud rate')
    
def main(FlasherObj, arg_parser):
    print("Here...")
    #FlasherObj.checkReady()

if __name__ == "__main__":
    arg_parser = parse_arguments()
    flashing = Flasher()
    main(flashing, arg_parser)
