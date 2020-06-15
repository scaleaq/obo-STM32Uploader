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

# Tests

| Device                 | Result         | Setting                            | UART Pins           |
| ---------------------- | -------------- | ---------------------------------  | ------------------- |
| STM32F072 Discovery    | &#10004;       | Boot0(pin) = 1 and nBoot1(bit) = 1 | PA14(Tx), PA15(Rx)  |
| STM32F103 Blue Pill    | &#10004;       | Boot0(pin) = 1 and Boot1(pin) = 0  | PA9(Tx), PA10(Rx)   |
| STM32F401-C Discovery  | &#10004;       | Boot0(pin) = 1 and Boot1(pin) = 0  | PD5(Tx), PD6(Rx     |
| STM32F3 Discovery      | &#10004;       | Boot0(pin) = 1 and nBoot1(bit) = 1 | PA9(Tx), PA10(Rx)   |
| STM32L4R5              | &#8722;        |                                    |                     |
