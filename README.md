# loramdm

`loramdm` is a command-line utility for configuring and communicating with LoRa modems (for example, the DX-LR02) over a serial connection.

Unlike standard serial terminal programs such as **minicom** or **pySerial's miniterm**, which can be inconvenient for issuing AT commands on Linux, `loramdm` automates modem configuration and message exchange. It allows you to:

* Execute one or more AT commands.
* Send text messages.
* Listen for incoming messages.
* Combine configuration commands and data transmission in a single invocation.

## Usage

Commands are supplied as a semicolon-separated sequence. The special `+++` command switches the modem into AT command mode (or back to data mode, depending on the modem state).

### Example 1: Execute an AT command

Display the modem's list of supported AT commands:

```bash
python -m loramdm '+++;AT+HELP;+++'
```

### Example 2: Configure the modem, send a message, and listen

Reduce the transmission power to **0 dBm**, return to data mode, send a message, and continue listening for incoming messages:

```bash
python -m loramdm '+++;AT+POWE0;+++;Hello from loramdm1!' -l
```
### Example 3: Configure modem for minimal transmitting power (0dBm), 
max radio baud rate 13 kBaud (LEVEL7), ID 10.00, and serial communication speed 115200 baud:  
```bash
python -m loramdm -d/dev/ttyUSB0 -b9600 '+++;AT+POWE0;AT+LEVEL7;AT+MAC10,00;AT+BAUD8;+++'
```

