import cmd
import serial
import sys

class Cube:

def main(serialPort):
    port = serial.Serial(serialPort, 115200)

    for page in range(0, 65536):
        sendCommand(port, "w " + str(page))
        sendCommand(port, "m b f")
        print page

def sendCommand(port, command):
    port.write(command + "\r")
    return readToPlus(port)

def readToPlus(port):
    response = ""

    while not response.endswith("\n+"):
        character = port.read(1)
        if len(character) == 0:
            print "Whoops, couldn't read a response"
            sys.exit(1)

        response += character

        if response.endswith("error"):
            print "Got an error!"

    return response[:-2].strip()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Gimme a serial port!"
        sys.exit(1)

    serialPort = sys.argv[1]

    main(serialPort)
