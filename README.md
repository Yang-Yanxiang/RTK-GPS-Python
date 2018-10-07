# RTK-GPS-Python
### Hardware components:
* Ublox RTK Package C94-M8P [buy!](https://www.u-blox.com/en/product/c94-m8p#tab-kit-includes)
* Intel UP Squared Board [buy!](http://www.up-board.org/upsquared/specifications-up2/)

### Testing the hardware

To identify the tty device node number in Linux corresponding to a particular hardware uart open a terminal and execute the following command
```
ls /sys/bus/pci/devices/0000\:00\:18.?/dw-apb-uart.*/tty/ | grep tty

/sys/bus/pci/devices/0000:00:18.0/dw-apb-uart.8/tty/:
ttyS4
/sys/bus/pci/devices/0000:00:18.1/dw-apb-uart.9/tty/:
ttyS5
```
The first UART (associated to dw-apb-uart.8) is the uart on the M10 connector, and the one associated with dw-apb-uart.9 is the one on the HAT. So to access the uart on the HAT on ubilinux I have to open the device file /devttyS1
```
sudo screen /dev/ttyS1 115200
```

### Connection:
Up_Squared pin8 <---------> ublox pin9
Up_Squared pin10 <---------> ublox pin10
![ublox_pinout](https://github.com/Yang-Yanxiang/RTK-GPS-Python/blob/master/doc/ublox_pinout.png)
![Up_squared pinout](https://github.com/Yang-Yanxiang/RTK-GPS-Python/blob/master/doc/up%20squared%20pinout.png)
### Example code:
```
import mraa
import time
import sys

# serial port
port = "/dev/ttyS5"
u = mraa.Uart(port)

u.setBaudRate(19200)
u.setMode(8, mraa.UART_PARITY_NONE, 1)
u.setFlowcontrol(False, False)

# Start a neverending loop waiting for data to arrive.
# Press Ctrl+C to get out of it.
while True:
    if u.dataAvailable():
        # We are doing 1-byte reads here
        data = u.readStr(1)
        print(data)
```
