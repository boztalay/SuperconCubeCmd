import random
import sys

import cubey

def main(serialPort):
    cube = cubey.Cube(serialPort)

    commandNumber = 0

    try:
        while True:
            # letters = pickRandomLetters()
            # numbers = pickRandomNumbers()
            letters = pickSetOfBadLetters()
            numbers = pickSetOfBadNumbers()

            command = "w " + letters
            if len(numbers) != 0:
                command += " " + numbers

            result = cube.sendCommand(command)
            commandNumber += 1

            if commandNumber % 100 == 0:
                print "Command %d is: %s" % (commandNumber, command)

            # if result is None:
                # print "Invalid command found: " + command

            if result is not None:
                print "Valid command found: " + command
    except KeyboardInterrupt:
        print

    print "Done!"

def pickSetOfBadLetters():
    badLetterSets = [
        "qP",
        "mf",
        "b",
        "au",
        "Hc",
        "WN",
        "JR",
        "Gz",
        "tz"
    ]

    letterSetIndex = random.randint(0, len(badLetterSets) - 1)
    return badLetterSets[letterSetIndex]

def pickRandomLetters():
    validLetters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    minLettersLength = 1
    maxLettersLength = 2

    lettersLength = random.randint(minLettersLength, maxLettersLength)

    letters = ""
    for _ in range(lettersLength):
        letterIndex = random.randint(0, len(validLetters) - 1)
        letters += validLetters[letterIndex]

    return letters

def pickSetOfBadNumbers():
    badNumberSets = [
        "511246339",
        "65537442",
        "720899288",
        "7864395327",
        "0786439478",
        "3014659",
        "395968513",
        "1441796181",
        "83230771"
    ]

    numberSetIndex = random.randint(0, len(badNumberSets) - 1)
    return badNumberSets[numberSetIndex]

def pickRandomNumbers():
    validNumbers = "0123456789"
    minNumbersLength = 0
    maxNumbersLength = 10

    numbersLength = random.randint(minNumbersLength, maxNumbersLength)

    numbers = ""
    for _ in range(numbersLength):
        numberIndex = random.randint(0, len(validNumbers) - 1)
        numbers += validNumbers[numberIndex]

    return numbers

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Gimme a serial port!"
        sys.exit(1)

    serialPort = sys.argv[1]

    main(serialPort)
