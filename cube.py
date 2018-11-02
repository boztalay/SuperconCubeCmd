import cmd
import serial
import sys

MAX_PAGE_INDEX = 32767

CIPHER_FLASH_PAGE = 0

def main(serialPort):
    cube = Cube(serialPort)
    cubeCommand = CubeCommand(cube)

    try:
        cubeCommand.cmdloop()
    except KeyboardInterrupt:
        print

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

class CubeCommand(cmd.Cmd):

    def __init__(self, cube):
        cmd.Cmd.__init__(self)

        self.cube = cube

        self.desiredColor = None
        self.colorCorrectionEnabled = True
        self.gammaCorrectionEnabled = True

        self.intro =  "Hackaday Supercon 2018 Cube Command\n"
        self.intro += "===================================\n"

        self.prompt = ":) "

        self.doc_header = "Commands:"
        self.ruler = "-"

    def splitArgs(self, args, expectedArgumentCount):
        if args is None:
            args = ""

        args = args.split()
        if len(args) != expectedArgumentCount:
            print "Expected %d arguments, %d given!" % (expectedArgumentCount, len(args))
            return None

        return args

    def do_generateCipher(self, args):
        """
        Generate a new 512-byte cipher, place it in buffer C, save it to flash,
        and print it out
        """

        # Generate a true random block and put it in buffer C
        self.cube.sendCommand("m t c")

        # Write it to flash to save it
        self.cube.sendCommand("w %d" % CIPHER_FLASH_PAGE)
        self.cube.sendCommand("m c f")

        # Print out the cipher
        cipher = self.cube.sendCommand("m c u")
        print cipher

    # def do_loadCipher(self, args):
        # """
        # Read in the given cipher, place it in buffer C, save it to flash, and
        # then print it out
        # """

        # self.cube.send

    def do_readFlash(self, args):
        """
        Read a 512-byte page of flash, takes in a page index and an output
        format (one of ['decimal', 'hex'])
        """

        args = self.splitArgs(args, 2)
        if args is None:
            return

        try:
            pageIndex = int(args[0])
            if pageIndex > MAX_PAGE_INDEX:
                raise ValueError
        except ValueError:
            print "Page index must be an integer in the range [0, 2^16)"
            return

        printFormat = args[1]
        if printFormat not in ["decimal", "hex"]:
            print "The print format must be one of ['decimal', 'hex']"
            return

        contents = self.readFlashPage(pageIndex)

        if printFormat == "decimal":
            print " ".join(map(lambda x: "%03d" % x, contents))
        elif printFormat == "hex":
            self.printPage(contents)

    def do_quit(self, args):
        """ quit """

        sys.exit(0)

    def do_exit(self, args):
        """ exit """

        sys.exit(0)

    def emptyline(self):
        return

    def default(self, line):
        if len(line.strip()) == 0:
            return

        if line == "EOF":
            print
            sys.exit(1)

        print "Unknown command, use \"help\" to see all available commands"

    def readFlashPage(self, pageIndex):
        self.cube.sendCommand("r %d" % (pageIndex * 2))
        rawContents = self.cube.sendCommand("m f u")
        return map(int, rawContents.split())

    def writeFlashPage(self, pageIndex, contents):
        if len(contents) > PAGE_SIZE:
            print "Page too large to write to flash!"

        while len(contents) < PAGE_SIZE:
            contents.append(0)

        self.cube.sendCommand("w %d" % pageIndex)
        self.cube.sendCommand("m u f")
        self.cube.write(" ".join(map(lambda x: "%03d" % x, contents)))
        self.cube.sendCommand("q")

    def printPage(self, contents):
        rowFormat = "% 4X |" + (" %02X" * 16)
        for rowStartIndex in range(0, 512, 16):
            print rowFormat % tuple([rowStartIndex] + contents[rowStartIndex:rowStartIndex + 16])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Gimme a serial port!"
        sys.exit(1)

    serialPort = sys.argv[1]

    main(serialPort)
