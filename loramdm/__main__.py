#!/usr/bin/env python3
"""Send a sequence of commands to a LoRa modem (e.g. DX-LR02) over serial.
"""
import argparse
import time
import serial

__version__ = '0.0.3 2026-07-09'#v0.0.3 released using uv
usage = ('    Usage:\n'
   "python -m loramdm -d/dev/ttyUSB0 -b9600 '+++;AT+HELP;+++'\n"
   "python -m loramdm -d/dev/ttyUSB0 -b9600 '+++;AT+LEVEL7;AT+MAC10,00;AT+BAUD8;+++'\n"
   "python -m loramdm -d/dev/ttyUSB0 -b115200 'hello from loramdm @ttyUSB0!' -l\n"
   )

# Globals
pargs = None
serDev = None

def printTime(): return time.strftime("%m%d:%H%M%S")
def _printv(msg, level=0):
    if pargs.verbose > level:
        print(f'dbg{level}@{printTime()}: '+msg)
def printv(msg):   _printv(msg, 0)
def printvv(msg):  _printv(msg, 1)

def send_and_print(data, sleep):
    """Send *data* over *serDev* and print the response.

    Reads until no new bytes arrive for *sleep* seconds so that slow modems
    or multi-line replies are captured in full.
    """
    printv(f'sending {data.encode()}')
    serDev.write(data.encode())
    time.sleep(sleep)
    chunks = []
    while True:
        chunk = serDev.read(serDev.in_waiting or 1)
        if chunk:
            chunks.append(chunk)
        else:
            break
    print(b''.join(chunks).decode(errors='replace'), end='', flush=True)

def main():
    global pargs, serDev
    parser = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        #argparse.RawTextHelpFormatter,
        #argparse.RawDescriptionHelpFormatter,
        epilog=f'loramdm {__version__}. {usage}')
    parser.add_argument('-b','--baudrate', type=int, default=9600, help=
        'Serial baud rate')
    parser.add_argument('-d','--device', default='/dev/ttyUSB0', help=
        'Serial device')
    parser.add_argument('-l','--listen', action='store_true', help=
        'Keep listening till keyboard interrupt')
    parser.add_argument('-s','--sleep', type=float, default=0.1, help=
        'Sleep duration after sending each command')
    parser.add_argument('-t','--timeout', type=float, default=0.1, help=
        'Serial read timeout in seconds')
    parser.add_argument('-v','--verbose', action='count', default=0, help=
      'Show more log messages (-vv: show even more).')
    parser.add_argument('commands', metavar='COMMAND', help=
      'List of commands (separated by ;) to send to the modem')
    pargs = parser.parse_args()

    serDev = serial.Serial(port=pargs.device,
        baudrate=pargs.baudrate, timeout=pargs.timeout)

    for cmd in pargs.commands.split(';'):
        send_and_print((cmd + '\r\n'), pargs.sleep)

    if pargs.listen:
        printv('listening...')
        while True:
            chunk = serDev.read(serDev.in_waiting or 1)
            if chunk:
                print(chunk.decode(errors='replace'), end='', flush=True)

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt):#, SystemExit):
        print('\nProgram Stopped Manually!')


