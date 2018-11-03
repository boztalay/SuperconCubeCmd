import serial

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
                self.port.flush()
                return None

        self.port.flush()
        return response[:-2].strip()

    def writeBlock(self, destination, block):
        self.port.write("m u " + destination + "\r")
        for i, element in enumerate(block):
            self.port.write(chr(element))
            if i == 2:
                self.port.write(chr(element))

        return self.readResponse()

    def breakOut(self):
        self.port.write("q\r")
