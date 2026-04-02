# baudsniff

Probably already exists. Built mine anyway.

Automates UART baud rate detection by brute-forcing through common speeds
and measuring how much of the received data is actually readable ASCII.
Useful when you're staring at a router PCB at 2am and don't feel like
guessing.

## how it works

Opens each baud rate, flushes the OS buffer, tickles the device with a
`\r\n` and measures the ASCII printable ratio of whatever comes back.
Sorts by readability percentage, not raw character count — because 2 chars
at 100% beats 300 chars of garbage.

Also handles devices that switch baud rates mid-boot (bootloader vs kernel),
which is more common than it should be.

## usage
```bash
pip install pyserial
python baudsniff.py COM8        # windows
python baudsniff.py /dev/ttyUSB0  # linux
```

## output
```
[*] Waiting for signal on the device...
[*] Power on the device now.

[+] Signal detected!

[*] Baud rate bruteforce on COM8

      110 baud |  256 ASCII chars | 100.0% readable | <<< CANDIDATE
      300 baud |    0 ASCII chars |   0.0% readable |
      600 baud |    0 ASCII chars |   0.0% readable |
     1200 baud |    2 ASCII chars |  50.0% readable |
     2400 baud |    0 ASCII chars |   0.0% readable |
     4800 baud |    0 ASCII chars |   0.0% readable |
     9600 baud |    5 ASCII chars |  31.2% readable |
    14400 baud |   42 ASCII chars |  20.0% readable |
    19200 baud |   98 ASCII chars |  38.3% readable |
    38400 baud |   65 ASCII chars |  41.7% readable |
    57600 baud |    2 ASCII chars | 100.0% readable |
   115200 baud |  256 ASCII chars | 100.0% readable | <<< CANDIDATE
   128000 baud |    0 ASCII chars |   0.0% readable |
   256000 baud |   61 ASCII chars |  23.8% readable |

[+] Best match: 115200 baud  (256 chars, 100.0% readable)
[+] Use this baud rate in PuTTY or the dump script.
```

Multiple candidates means the device changes speed during boot.
Usually bootloader on the low one, Linux shell on the high one.

## tested on

- Cisco home routers
- Generic OpenWRT devices
- Whatever cursed thing I find next

## notes

- Windows buffers serial data between opens — flush is mandatory
- 3 second delay after signal detection lets the device settle
- If everything shows 100%, you probably have a different problem
