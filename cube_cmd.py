import cmd
import sys

import cubey

MAX_PAGE_INDEX = 32767

CIPHER_FLASH_PAGE = 0

def main(serialPort):
    cube = cubey.Cube(serialPort)
    cubeCommand = CubeCommand(cube)

    try:
        cubeCommand.cmdloop()
    except KeyboardInterrupt:
        print

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

        # Generate a true random block and put it in flash
        self.cube.sendCommand("w %d" % CIPHER_FLASH_PAGE)
        self.cube.sendCommand("m t f")

        # Print out the cipher
        self.cube.sendCommand("r %d" % CIPHER_FLASH_PAGE)
        cipher = self.cube.sendCommand("m f u")
        print cipher

    def do_loadCipher(self, args):
        """
        Read in the given cipher, place it in buffer C, save it to flash, and
        then print it out

        The cipher should be given as 512 whitespace-delimited decimal numbers
        """

        rawCipher = self.splitArgs(args, 512)
        if args is None:
            return

        try:
            cipher = map(int, rawCipher)
        except ValueError as e:
            print "Cipher must be decimal numbers: " + str(e)
            return

        # Write the cipher to flash to save it
        self.cube.sendCommand("w %d" % CIPHER_FLASH_PAGE)
        self.cube.writeBlock("f", cipher)

        # Print out the cipher
        self.cube.sendCommand("r %d" % CIPHER_FLASH_PAGE)
        cipher = self.cube.sendCommand("m f u")
        print cipher

    def do_broadcastMessage(self, args):
        """
        Broadcasts a message encrypted with the cipher in flash page 0
        """

        block = []
        for character in args:
            block.append(ord(character))

        while len(block) < 512:
            block.append(0)

        # Load the message into buffer B
        self.cube.writeBlock("b", block)

        # Encrypt the message with the cipher in flash and broadcast it
        self.cube.sendCommand("r %d" % CIPHER_FLASH_PAGE)
        self.cube.sendCommand("x b n")

    def do_receiveMessage(self, args):
        """
        Receives a message and decrypts it with the cipher in flash page 0
        """

        # Receive the message, put it in buffer B
        self.cube.sendCommand("x n b")

        # Decrypt the message with the cipher in flash
        self.cube.sendCommand("r %d" % CIPHER_FLASH_PAGE)
        rawMessage = self.cube.sendCommand("x b u")

        # Print the message
        messageBytes = map(int, rawMessage.split())
        message = ""

        for element in messageBytes:
            if element == 0:
                break
            message += chr(element)

        print message

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

    def printPage(self, contents):
        rowFormat = "% 4X |" + (" %02X" * 16)
        print "        0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F"
        print "      ------------------------------------------------"
        for rowStartIndex in range(0, 512, 16):
            print rowFormat % tuple([rowStartIndex] + contents[rowStartIndex:rowStartIndex + 16])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Gimme a serial port!"
        sys.exit(1)

    serialPort = sys.argv[1]

    main(serialPort)
