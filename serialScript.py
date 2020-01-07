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
            
    #CRC
    def getCRC(data):
        print("take crc here") 
        crc = 0xff;
        for d in data:
            crc = crc ^ data
            
        return crc

    #Send 0x7f on serial so that the host selects the connected UART port
    #and adjusts the baud rate.
    #All the command routines should start after this.
    def checkReady(self):
        self.serialInstance.write(to_bytes([0x7F]))
        response = self.serialInstance.read()
        response = hex(int.from_bytes(response,byteorder='little'))
        
        if len(response) == 0:
            return False
        
        if response == hex(ACK):
            return True
            
    def getCmd(self):
        self.serialInstance.write(to_bytes([0x00, 0xFF]))
        
        #Wait for ACK/NACK
        response = self.serialInstance.read()
        response = hex(int.from_bytes(response,byteorder='little'))

        if response == hex(ACK):
            #Get the number of bytes
            resp = self.serialInstance.read()
            resp = int.from_bytes(resp,byteorder='little')
            resp = self.serialInstance.read(int(resp)) #Read resp number of bytes
            #resp = int.from_bytes(resp,byteorder='little')

            resp = list(resp)
            for r in range(len(resp)):
                if r == 0:
                    versionString = str(hex(resp[r]))
                    versionString = versionString.strip('0x')
                    versionString = versionString[:1] + '.' + versionString[1:]
                    print("Bootloader Version: ", versionString)
                    print("Supported Commands: ")
                else:
                    print(hex(resp[r]), end=" ")

            print()
                
        else:
            print("Communication Error!")
            exit(1)
            
    def getVersionAndReadProtectionCmd(self):
        print("Get Version and Read Protection Status")
        self.serialInstance.write(to_bytes([0x01, 0xFE]))
        
        #wait for ACK/NACK
        response = self.serialInstance.read(1)
        
        if response == hex(ACK):
            print("Got ACK")
            resp = self.serialInstance.read(3)
            print(resp) #Should print Bootloader Version and 2 option bytes
        else:
            print("Communication Error!")
            exit(1)
            
            
    def getIDCmd(self):
        print("Sending Get ID Command...")
        self.serialInstance.write(to_bytes([0x02, 0xFD]))
        
        #Wait for ACK/NACK
        response = self.serialInstance.read(1)
        
        if response == hex(ACK):
            print("Got ACK")
            resp = self.serialInstance.read(1)
            #The device sends number of bytes-1 which is excluding ACK
            resp = self.serialInstance.read(int(resp)) #Include ACK
            print(resp)
            
        else:
            print("Communication Erro!")
            exit(1)
            
    def readMemoryCmd(self):
        print("Sending Read Memory Command...")
        resp = self.serialInstance.write(to_bytes([0x11, 0xEE]))
        
        #Wait for ACK/NACK
        response = self.serialInstance.read(1)
        if response == hex(ACK):
            print("Got ACK")
            #Sending a dummy hardcoded haddress here, add arg later
            addr = [0x08, 0x00, 0x00, 0x00]
            addr.append((getCRC(addr) * 0xff))
            resp = self.serialInstance.write(addr)
            
            response = self.serialInstance.read(1)
            if response == hex(ACK):
                #Reading hardcoded 8 bytes
                noOfBytes = 0x07 #8 Bytes
                resp = self.serialInstance.write([noOfBytes, ~noOfBytes])
                
                response = self.serialInstance.read(1)
                if response == hex(ACK):
                    response = self.serialInstance.read(noOfBytes)
            
        
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', help='Set serial baud rate')
    parser.add_argument('-d', help='Serial Device Path')
    
    return parser
    
def main(FlasherObj):
    if FlasherObj.checkReady():
        FlasherObj.getCmd()
    else:
        print("Cannot init device.")

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
