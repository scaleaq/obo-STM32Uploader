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
    def getCRC(self, data):
        crc = 0x00;
        for d in data:
            crc = crc ^ d
            
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
        response = hex(int.from_bytes(response,byteorder='little'))
        if response == hex(ACK):
            print("Got ACK")
            resp = self.serialInstance.read(3)
            resp = list(resp)
            for r in range(len(resp)):
                if r == 0:
                    versionString = str(hex(resp[r]))
                    versionString = versionString.strip('0x')
                    versionString = versionString[:1] + '.' + versionString[1:]
                    print("Bootloader Version: ", versionString)
                    print("Option Bytes: ")
                else:
                    print(hex(resp[r]), end=" ")
            print()
        else:
            print("Communication Error!")
            exit(1)
            
            
    def getIDCmd(self):
        self.serialInstance.write(to_bytes([0x02, 0xFD]))
        
        #Wait for ACK/NACK
        response = self.serialInstance.read(1)
        response = hex(int.from_bytes(response,byteorder='little'))
        if response == hex(ACK):
            resp = self.serialInstance.read(1)
            #The device sends number of bytes-1 which is excluding ACK
            resp = int.from_bytes(resp,byteorder='little')
            resp = self.serialInstance.read(int(resp)+1) #Include ACK
            resp = int.from_bytes(resp,byteorder='little')
            print("Product Id: ", hex(resp))
            
        else:
            print("Communication Erro!")
            exit(1)
            
    def readMemoryCmd(self, addr, noOfBytes):
        resp = self.serialInstance.write(to_bytes([0x11, 0xEE]))
        
        #Wait for ACK/NACK
        response = self.serialInstance.read(1)
        response = hex(int.from_bytes(response,byteorder='little'))
        if response == hex(ACK):
            #Sending a dummy hardcoded haddress here, add arg later
            #addr = [0x08, 0x00, 0x00, 0x00]
            addrList = list(bytes.fromhex(addr))
            addrList.append((self.getCRC(addrList)))
            resp = self.serialInstance.write(to_bytes(addrList))
            
            response = self.serialInstance.read(1)
            response = hex(int.from_bytes(response,byteorder='little'))
            if response == hex(ACK):
                #Reading hardcoded 8 bytes
                #noOfBytes = 0xFF
                resp = self.serialInstance.write([noOfBytes, ~noOfBytes & 0xff])
                response = self.serialInstance.read(1)
                response = hex(int.from_bytes(response,byteorder='little'))
                if response == hex(ACK):
                    print("Reading bytes from device:")
                    response = self.serialInstance.read(noOfBytes)
                    response = list(response)
                    for i in range(len(response)):
                        if ((i % 8 == 0) and (i != 0)):
                            print("")
                        print('{:02x}'.format(response[i]), end=" ")

                    print("")
            if response == hex(NACK):
                print("Got NACK!")
                            
                            
    def goCmd(self, addr):
        resp = self.serialInstance.write(to_bytes([0x21, 0xDE]))
        
        #Wait for ACK/NACK
        response = self.serialInstance.read(1)
        response = hex(int.from_bytes(response,byteorder='little'))
        if response == hex(ACK):
            #Sending a dummy hardcoded haddress here, add arg later
            #addr = [0x08, 0x00, 0x00, 0x00]
            addrList = list(bytes.fromhex(addr))
            addrList.append((self.getCRC(addrList)))
            resp = self.serialInstance.write(to_bytes(addrList))
            
            response = self.serialInstance.read(1)
            response = hex(int.from_bytes(response,byteorder='little'))
            if response == hex(ACK):
                print("Starting execution...")
            if response == hex(NACK):
                print("Got NACK!")


    def writeMemoryCmd(self, addr, data, noOfBytes):
        resp = self.serialInstance.write(to_bytes([0x31, 0xCE]))
        
        #Wait for ACK/NACK
        response = self.serialInstance.read(1)
        response = hex(int.from_bytes(response,byteorder='little'))
        if response == hex(ACK):
            addrList = list(bytes.fromhex(addr))
            addrList.append((self.getCRC(addrList)))
            print(addrList)
            resp = self.serialInstance.write(to_bytes(addrList))
            
            response = self.serialInstance.read(1)
            response = hex(int.from_bytes(response,byteorder='little'))
            if response == hex(ACK):
                packet = list()
                packet.append(noOfBytes)
                packet = packet + data
                packet.append(self.getCRC(packet))
                print("Sending Packet")
                print(packet)
                resp = self.serialInstance.write(to_bytes(packet))
                response = self.serialInstance.read(1)
                response = hex(int.from_bytes(response,byteorder='little'))
                print(response)
                if response == hex(ACK):
                    print("Write Complete")
                if response == hex(NACK):
                    print("Got NACK!")

    def eraseMemoryCmd(self):
        print("Place holder for erase memory command")
        
    def extendEraseMemoryCmd(self):
        print("Place holder foe extended erase memory command")
        
    def writeProtectCmd(self):
        resp = self.serialInstance.write(to_bytes([0x63, 0x9C]))
        
        #Wait for ACK/NACK
        response = self.serialInstance.read(1)
        response = hex(int.from_bytes(response,byteorder='little'))
        if response == hex(ACK):
            print("Write Protect Done.")
        
    def writeUnprotectCmd(self):
        resp = self.serialInstance.write(to_bytes([0x73, 0x8C]))
        
        #Wait for ACK/NACK
        response = self.serialInstance.read(1)
        response = hex(int.from_bytes(response,byteorder='little'))
        if response == hex(ACK):
            print("Write Unprotect Done.")
        
    def readoutProtectCmd(self):
        resp = self.serialInstance.write(to_bytes([0x82, 0x7D]))
        
        #Wait for ACK/NACK
        response = self.serialInstance.read(1)
        response = hex(int.from_bytes(response,byteorder='little'))
        if response == hex(ACK):
            print("Readout Protect Done.")
        
    def readoutUnprotect(self):
        resp = self.serialInstance.write(to_bytes([0x92, 0x6D]))
        
        #Wait for ACK/NACK
        response = self.serialInstance.read(1)
        response = hex(int.from_bytes(response,byteorder='little'))
        if response == hex(ACK):
            print("Readout Unprotect Done.")
        
            
        
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', help='Set serial baud rate')
    parser.add_argument('-d', help='Serial Device Path')
    
    return parser
    
def main(FlasherObj):
    if FlasherObj.checkReady():
        #FlasherObj.getCmd()
        #FlasherObj.getIDCmd()
        #Send 1 byte less in count
        FlasherObj.writeMemoryCmd("0800FF00", [0x12, 0x12, 0x12, 0x12], 3)
        FlasherObj.readMemoryCmd("0800FF00", 4)
        #FlasherObj.goCmd("08000000")
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
