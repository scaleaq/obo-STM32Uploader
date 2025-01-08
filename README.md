# STM32Uploader
The bootloader on most STM32 microcontrollers supports UART protocol to download code into the internal flash memory through the interface. STM32Uploader is a simple python program to communicate with STM32 bootloader via the UART peripheral.


# Usage
Get usage information
```
python3 serialScript.py -h
```

## Example
Get part ID

```
python3 serialScript.py -d /dev/ttyUSB0 -i
```

Get a list of supported commands

```
python3 serialScript.py -d /dev/ttyUSB0 -c
```

Extended Erase (Mass Erase)
```
python3 serialScript.py -d /dev/ttyUSB0 -x 0xFFFF
```

Erase Pages (Mass Erase)
```
python3 serialScript.py -d /dev/ttyUSB0 -e 255 0
```

Write binary file
```
python3 serialScript.py -d /dev/ttyUSB0 -f ./bins/stm32f072b/blinky.bin 8000000
```

Start Execution
```
python3 serialScript.py -d /dev/ttyUSB0 -g 8000000
```

# Flash procedure

## Bring chip into bootloader

by BOOT1=0, BOOT0=1 while power up/reset

## Erase flash

```
python3 serialScript.py -d /dev/ttyUSB0 -x 0xFFFF
```

## Bring chip into bootloader again

by BOOT1=0, BOOT0=1 while power up/reset

## Program flash by binary file

```
python3 serialScript.py -d /dev/ttyUSB0 -f ./bins/stm32f072b/blinky.bin 8000000
```

## reboot the board to run
