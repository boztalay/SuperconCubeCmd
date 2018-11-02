import cmd
import serial
import sys

class Cube(object):
    def __init__(self, serialPort):
        self.port = serial.Serial(serialPort, 115200)

    def sendCommand(self, command):
        self.port.write(command + "\r")
        return self.readResponse()

    def readResponse(self):
        response = ""

        while not response.endswith("\n+"):
            character = self.port.read(1)
            if len(character) == 0:
                print "Whoops, couldn't read a response"
                sys.exit(1)

            response += character

            if response.endswith("error"):
                print "Got an error!"
                self.port.flush()
                return response

        self.port.flush()
        return response[:-2].strip()

def main(serialPort):
    cube = Cube(serialPort)
    print cube.sendCommand("m b u")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Gimme a serial port!"
        sys.exit(1)

    serialPort = sys.argv[1]

    main(serialPort)
