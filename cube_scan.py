import random
import sys

import cubey

def main(serialPort):
    cube = cubey.Cube(serialPort)

    minNumberLength = 0
    maxNumberLength = 100

    try:
        while True:
            letters = pickRandomLetters()
            numbers = pickRandomNumbers()

            command = "r " + letters
            if len(numbers) != 0:
                command += " " + numbers

            result = cube.sendCommand(command)
            if result is None:
                print "Invalid command found: " + command
    except KeyboardInterrupt:
        print

    print "Done!"

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

def pickRandomNumbers():
    validNumbers = "0123456789"
    minNumbersLength = 0
    maxNumbersLength = 100

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
