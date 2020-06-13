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

# Tests

| Device        | Result        | Setting                            |
| ------------- | ------------- | ---------------------------------  |
| STM32F072RBT6 | &#10004;      | Boot0(pin) = 1 and nBoot1(bit) = 1 |
| STM32F103     | &#8722;       | Boot0(pin) = 1 and Boot1(pin) = 0  |
| STM32F401     | &#8722;       | Boot0(pin) = 1 and Boot1(pin) = 0  |
| STM32F303     | &#8722;       | Boot0(pin) = 1 and nBoot1(bit) = 1 |
| STM32L4R5     | &#8722;       |                                    |
