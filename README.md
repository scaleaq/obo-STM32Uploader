# STM32Uploader
The bootloader on most STM32 microcontrollers supports UART protocol to download code into the internal flash memory through the interface. STM32Uploader is a simple python program to communicate with STM32 bootloader via the UART peripheral. 


| Device        | Result        | Setting                            |
| ------------- | ------------- | ---------------------------------  |
| STM32F072RBT6 | Works         | Boot0(pin) = 1 and nBoot1(bit) = 1 |
| STM32F103     | Not tested    | Boot0(pin) = 1 and Boot1(pin) = 0  |
| STM32F401     | Not tested    | Boot0(pin) = 1 and Boot1(pin) = 0  |
| STM32F303     | Not tested    | Boot0(pin) = 1 and nBoot1(bit) = 1 |
| STM32L4R5     | Not tested    |                                    |
