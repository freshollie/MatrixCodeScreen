from DisplayDriver import DisplayDriver
from DisplayDriver.GuiObjects import *
import random
import string


TEXTSIZE = 12

RES = [640, 480]

DisplayDriver.engine.graphics.setRes(RES)

DisplayDriver.engine.setFrameRate(50)
DisplayDriver.engine.graphics.setBackground([0, 0, 0])


class Line:
    TRAILLENGHT = 8

    def __init__(self, xPos):
        self.letters = []
        self.xPos = xPos
        self.bottomPos = 0
        self.renderer = None
        self.spacing = 8
        self.length = random.randint(int(RES[1]/self.spacing*0.1),int(RES[1]/self.spacing)*1)
        self.newLetterTick()

    def generateRandomLetter():
        return random.choice(string.printable)

    def newLetterTick(self):
        self.letters.append(OnscreenText(Line.generateRandomLetter(), [self.xPos, self.bottomPos], size = TEXTSIZE, colour = [200, 255, 200]))

        if self.renderer:
            self.letters[-1].render(self.renderer)

        self.bottomPos += self.spacing

        if len(self.letters) >= self.length:
            if len(self.letters) > self.TRAILLENGHT:
                toValue = self.TRAILLENGHT
            else:
                toValue = len(self.letters) - 1

            for i in range(0, toValue):

                if self.letters[i].colour[1] == 255:
                    self.letters[i].setColour([0, 255 * (self.TRAILLENGHT - 1) /self.TRAILLENGHT, 0])
                    break
                else:
                    self.letters[i].setColour([0, 255 * (((self.letters[i].colour[1]/255) * self.TRAILLENGHT) - 1)/self.TRAILLENGHT, 0])

            if self.letters[0].colour[1] == 0:
                self.letters[0].removeNode()
                del self.letters[0]

        if len(self.letters) > 2:
            self.letters[-3].setColour([0, 255, 0])

    def tick(self):
        if not self.letters:
            return

        for i in range(random.randint(0, 3)):
            random.choice(self.letters).setText(Line.generateRandomLetter())

    def render(self, renderer):
        self.renderer = renderer

    def destroy(self):
        for letter in self.letters:
            letter.removeNode()
        self.renderer = None

class MatrixScreen():
    SIDESPACING = 7

    def __init__(self):
        self.lineFrequency = 1 # The lower the more likley chance
        self.lines = []
        self.sequenceDict = {}

    def newLine(self):
        self.lines.append(Line(random.randint(0, int(RES[0]/self.SIDESPACING))*self.SIDESPACING))
        self.lines[-1].render(DisplayDriver.engine)

        self.sequenceDict[self.lines[-1]] = [

            Sequence(DisplayDriver.engine,
                 Func(self.lines[-1].newLetterTick),
                 Wait(random.random() * 0.1)),

            Sequence(DisplayDriver.engine,
                     Func(self.lines[-1].tick),
                     Wait(0.1))
        ]

        self.sequenceDict[self.lines[-1]][0].loop()
        self.sequenceDict[self.lines[-1]][1].loop()

    def tick(self):

        if random.randint(0, self.lineFrequency) == 0 and len(self.lines) < int(RES[0]/self.SIDESPACING)*5:
            self.newLine()

        for line in self.lines:

            if not line.letters or line.letters[0].getY() > RES[1]:
                self.sequenceDict[line][0].finish()
                self.sequenceDict[line][1].finish()
                line.destroy()
                del self.sequenceDict[line]
                self.lines.remove(line)


DisplayDriver.engine.addTask(MatrixScreen().tick)

DisplayDriver.init()