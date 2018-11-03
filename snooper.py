import sys
import cubey

def main(serialPort):
    cube = cubey.Cube(serialPort)

    print "Listening, Ctrl-C to stop..."

    try:
        while True:
            rawMessage = cube.sendCommand("m n u") 
            printMessage(rawMessage)
    except KeyboardInterrupt:
        print

    cube.breakOut() 
    print "Done!"

def printMessage(rawMessage):
    print
    print "Got a message!"
    print "=============="
    print

    contents = map(int, rawMessage.split())

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
