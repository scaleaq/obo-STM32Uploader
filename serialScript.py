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

    def flushSerial(self):
        self.serialInstance.flushInput()
        self.serialInstance.flushOutput()
            
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
                    cmd = resp[r]
                    print(hex(cmd), end=" ")
                    if cmd == 0:
                        print("Get")
                    if cmd == 1:
                        print("Get Version & Read Protection Status")
                    if cmd == 2:
                        print("Get ID")
                    if cmd == 17:
                        print("Read Memory")
                    if cmd == 33:
                        print("Go")
                    if cmd == 49:
                        print("Write Memory")
                    if cmd == 67:
                        print("Erase")
                    if cmd == 68:
                        print("Extended Erase")
                    if cmd == 99:
                        print("Write Protect")
                    if cmd == 115:
                        print("Write Unprotect")
                    if cmd == 130:
                        print("Readout Protect")
                    if cmd == 146:
                        print("Readout Unprotect")
                    

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
            print("Communication Error!")
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
                resp = self.serialInstance.write(to_bytes(packet))
                response = self.serialInstance.read(1)
                response = hex(int.from_bytes(response,byteorder='little'))
                if response == hex(ACK):
                    print("Write Complete")
                if response == hex(NACK):
                    print("Got NACK!")

    def eraseMemoryCmd(self, noOfPages, pageNo):
        resp = self.serialInstance.write(to_bytes([0x43, 0xBC]))
        #Wait for ACK/NACK
        response = self.serialInstance.read(1)
        response = hex(int.from_bytes(response,byteorder='little'))
        if response == hex(ACK):
            if noOfPages == 0xff:
                #Global Erase
                resp = self.serialInstance.write(to_bytes([0xFF, 0x00]))
                response = self.serialInstance.read(1)
                response = hex(int.from_bytes(response,byteorder='little'))
                if response == hex(ACK):
                    print("Global Erase Complete")
                else:
                    print(response)
                    print("Could not complte global erase")

            if noOfPages != 0xff and noOfPages != 0x00: 
                noOfPages = noOfPages-1
                packet = list()
                packet.append(noOfPages)
                packet = packet + pageNo
                packet.append(self.getCRC(packet))
                print(packet)
                resp = self.serialInstance.write(to_bytes(packet))
                response = self.serialInstance.read(1)
                response = hex(int.from_bytes(response,byteorder='little'))
                if response == hex(ACK):
                    print("Erase complete.")
                else:
                    print("Could not complete erase.")

        if response == hex(NACK):
            print("Got Nack")
    '''
    Right now the function just supports Special Erase cases...
    Mass Erase, Bank1
    TODO: Support Extended Erase with number of pages
    '''
    def extendEraseMemoryCmd(self, noOfPages):
        resp = self.serialInstance.write(to_bytes([0x44, 0xBB]))
        #Wait for ACK/NACK
        response = self.serialInstance.read(1)
        response = hex(int.from_bytes(response,byteorder='little'))
        if response == hex(ACK):
            print("Got ACK")
            if noOfPages == 0xFFFF:
                packet = list()
                packet.append(0xFF)
                packet.append(0xFF)
                packet.append(self.getCRC(packet))
                print(packet)
                resp = self.serialInstance.write(to_bytes(packet))
                response = self.serialInstance.read(1)
                response = hex(int.from_bytes(response,byteorder='little'))
                if response == hex(ACK):
                    print("Extended erase complete.")
                else:
                    print("Could not complete extended erase.")

            if noOfPages == 0xFFFE:
                packet = list()
                packet.append(0xFF)
                packet.append(0xFE)
                packet.append(self.getCRC(packet))
                print(packet)
                resp = self.serialInstance.write(to_bytes(packet))
                response = self.serialInstance.read(1)
                response = hex(int.from_bytes(response,byteorder='little'))
                if response == hex(ACK):
                    print("Extended erase complete.")
                else:
                    print("Could not complete extended erase.")

            if noOfPages == 0xFFFD:
                packet = list()
                packet.append(0xFF)
                packet.append(0xFD)
                packet.append(self.getCRC(packet))
                print(packet)
                resp = self.serialInstance.write(to_bytes(packet))
                response = self.serialInstance.read(1)
                response = hex(int.from_bytes(response,byteorder='little'))
                if response == hex(ACK):
                    print("Extended erase complete.")
                else:
                    print("Could not complete extended erase.")
        else:
            print("Got NACK")
        
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
    parser.add_argument('-b', help='Set serial baud rate.')
    parser.add_argument('-d', help='Serial Device Path.')
    parser.add_argument('-c', action='store_true',help='Get hex codes of all supported commands.')
    parser.add_argument('-v', action='store_true',help='Get bootloader version and option bytes.')
    parser.add_argument('-i', action='store_true',help='Get part ID')
    parser.add_argument('-r', help='Read Memory Pages.', nargs=2)
    parser.add_argument('-g', help='Start Execution from the given address.')
    parser.add_argument('-e', help='Erase pages', nargs=2)
    parser.add_argument('-x', help='Erase pages')
    
    return parser
    
def main(FlasherObj, args):
    if FlasherObj.checkReady():

        if args.i:
            FlasherObj.getIDCmd()
            FlasherObj.flushSerial()
            
        if args.c:
            FlasherObj.getCmd()
            FlasherObj.flushSerial()

        if args.v:
            FlasherObj.getVersionAndReadProtectionCmd()
            FlasherObj.flushSerial()

        if args.r:
            if len(args.r[0]) < 8:
                pre = 8 - len(args.r[0])
                args.r[0] = "0"*pre + args.r[0]
            FlasherObj.readMemoryCmd(args.r[0], int(args.r[1]))
        
        if args.g:
            print(args.g)
            print(type(args.g))
            if len(args.g) < 8:
                pre = 8 - len(args.g)
                args.g = "0"*pre + args.g
            FlasherObj.goCmd(args.g)

        if args.e:
           FlasherObj.readoutUnprotect()
           pageNo = list()
           pageNo.append(1)
           FlasherObj.eraseMemoryCmd(0, 0)

        if args.x:
           #FlasherObj.readoutUnprotect()
           pageNo = list()
           pageNo.append(1)
           FlasherObj.extendEraseMemoryCmd(args.x)
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
    main(flashing, args)
