import numpy as np
import Shader
import time
import stringCalculator

class KeyboardCommands:
    def __init__(self, WINDOW, FONTRENDERER, PRIMETIVES, DataType=False, Length=0.02, Color=(1, 1, 1)):
        self._Window = WINDOW
        self._FontRenderer = FONTRENDERER
        self._Primetive = PRIMETIVES
        self._startNumbNormal = 48
        self._startNumbKeypad = 320
        self._startLetter = 65
        self._alphabetStringLC = "abcdefghijklmnopqrstuvwxyz"
        self._alphabetStringUC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self._capsLockKey = False
        self._enterKey = False
        self._ctrlKey = False
        self._tabKey = False
        self._backSpaceKey = False
        self._dataType = DataType
        self._Calculator = stringCalculator.StringCalculator(DataType)


        self._keySilenceTime = 0
        self._keySilenceTimeHold = 0
        self._keySilenceTimeLimit = 0.2
        self._currentIndex = 0
        self._time = 0
        self._mouseClickHold = False
        self._firstClick = True
        self._mouseClickTime = 0
        self._mouseClickTimeHold = 0
        self._mouseClickTimeLimit = 0.3
        self._copy = False
        self._paste = False
        self._markString = True
        self._lineSeperatorTime = 0
        self._lineSeperatorTimeHold = 0
        self._lineSeperatorRefreshTime = 0.5
        self._lineSeperatorState = True
        self._lineSeperatorUpdate = False
        self._shaderLINE = Shader.shader("../shaders/Line.vs", "../shaders/Line.fs")
        self._shaderLINE.use()
        self._shaderLINE.float("length", Length)
        self._shaderLINE.vec3("color", Color)

        # Public
        self.KeyEvent = False
        self.MainString = ""
        self.MousePickStartPos = 1
        self.MousePickEndPos = 1
        self.MousePickHeightCenter = 1

        if DataType is not False:
            self.MainString = "0.0"
    def ForceFontPointerUpdate(self, FontPointer):
        self._FontRenderer = FontPointer
    def CopyPasteString(self, String):
        if self._markString is False:
            if self._copy:
                self._copy = False
                self.KeyEvent = True
                return self.MainString
            elif self._paste:
                self._paste = False
                self.KeyEvent = True
                self.MainString = String
        return String
    def RemoveMark(self):
        self._FontRenderer.MarkString(False)
        self._markString = True
    def UpdateStringPosition(self):
        self._lineSeperatorUpdate = True

    def KeyInput(self):
        self._time = time.clock()
        self._indexManipulator()
        if self._markString:
            self._letterSeperator()
        if self.KeyEvent:
            self.KeyEvent = False
        if self._Window.KeyPressed:
            self._keySilenceTime = self._time - self._keySilenceTimeHold
            self._lineSeperatorUpdate = True
            self._Window.KeyPressed = False
            if self._commandKeys():
                return

            if self._dataType is not False:
                if self._specialKeys():
                    return
                if self._numberKeys():
                    return
            else:
                if self._specialKeys():
                    return
                if self._numberKeys():
                    return
                if self._letterKeys():
                    return
    def _indexManipulator(self):
        self._mouseClickTime = self._time - self._mouseClickTimeHold
        if self._Window.MouseButtons[0] == 1 and self._mouseClickHold is False:
            self._mouseClickHold = True
            self._mouseClickTimeHold = self._time
            if self._mouseClickTime <= self._mouseClickTimeLimit and self._firstClick is False:
                self._markString = False
                self._FontRenderer.MarkString(True)
            else:
                self._FontRenderer.MarkString(False)
                self._markString = True
            self._firstClick = False

            self._letterSeperatorPlacer()
        elif self._Window.MouseButtons[0] == 0 and self._mouseClickHold:
            self._mouseClickHold = False


        if self._Window.LeftArrow:
            self._currentIndex -= 1
            self._Window.LeftArrow = False
        elif self._Window.RightArrow:
            self._currentIndex += 1
            self._Window.RightArrow = False

        if self._currentIndex >= len(self.MainString):
            self._currentIndex = len(self.MainString)
        elif self._currentIndex < 0:
            self._currentIndex = 0
    def _commandKeys(self):
        self._ctrlKey = self._Window.Keys[341]
        self._tabKey = self._Window.Keys[341]
        self._backSpaceKey = self._Window.Keys[259]
        self._enterKey = self._Window.Keys[257]
        if self._Window.Keys[280]:
            if self._capsLockKey:
                self._capsLockKey = False
            else:
                self._capsLockKey = True
            return True
        elif self._backSpaceKey:
            if self._markString is False:
                self.MainString = ""
            else:
                self.MainString = self._letterRemover(self.MainString)
                self.KeyEvent = True
            return True
        elif self._enterKey:
            if self._dataType is not False:
                self._enterKey = True
                self.MainString = self._Calculator.Calculator(self.MainString)
            return True
        elif self._ctrlKey:
            if self._Window.Keys[67]:
                if self._markString is False:
                    self._copy = True
                return True
            elif self._Window.Keys[86]:
                if self._markString is False:
                    self._paste = True
                return True
            return True
    def _specialKeys(self):
        self._clearString()
        if self._Window.Keys[340]:
            if self._Window.Keys[47]:
                self.MainString = self._letterAdder("_", self.MainString)
                return True
            elif self._Window.Keys[55]:
                self.MainString = self._letterAdder("/", self.MainString)
                return True
            elif self._Window.Keys[56]:
                self.MainString = self._letterAdder("(", self.MainString)
                return True
            elif self._Window.Keys[57]:
                self.MainString = self._letterAdder(")", self.MainString)
                return True
            elif self._Window.Keys[92]:
                self.MainString = self._letterAdder("*", self.MainString)
                return True
        else:
            if self._Window.Keys[32]:
                self.MainString = self._letterAdder(" ", self.MainString)
                return True
            elif self._Window.Keys[44]:
                self.MainString = self._letterAdder(",", self.MainString)
                return True
            elif self._Window.Keys[47] or self._Window.Keys[333]:
                self.MainString = self._letterAdder("-", self.MainString)
                self.KeyEvent = True
                return True
            elif self._Window.Keys[46]:
                self.MainString = self._letterAdder(".", self.MainString)
                self.KeyEvent = True
                return True
            elif self._Window.Keys[45] or self._Window.Keys[334]:
                self.MainString = self._letterAdder("+", self.MainString)
                self.KeyEvent = True
                return True
            elif self._Window.Keys[261]:
                if self._markString is False:
                    self.MainString = ""
                return True
    def _numberKeys(self):
        self._clearString()
        for numb in range(10):
            if self._Window.Keys[numb + self._startNumbNormal]:
                self.MainString = self._letterAdder(str(numb), self.MainString)
                self._Window.Keys[numb + self._startNumbNormal] = False
                self.KeyEvent = True
                return True
            elif self._Window.Keys[numb + self._startNumbKeypad]:
                self.MainString = self._letterAdder(str(numb), self.MainString)
                self._Window.Keys[numb + self._startNumbKeypad] = False
                self.KeyEvent = True
                return True
    def _letterKeys(self):
        self._clearString()
        for let in range(26):
            if self._Window.Keys[let + self._startLetter]:
                if self._Window.Keys[340] or self._capsLockKey:
                    self.MainString = self._letterAdder(self._alphabetStringUC[let], self.MainString)
                else:
                    self.MainString = self._letterAdder(self._alphabetStringLC[let], self.MainString)
                self._Window.Keys[let + self._startLetter] = False
                self.KeyEvent = True
                return True
    def _letterAdder(self, NewLetter, String):
        listString = list(String)
        listString.insert(self._currentIndex, NewLetter)
        newString = ""
        for i in range(len(listString)):
            newString += str(listString[i])
        self._currentIndex += 1
        return newString
    def _letterRemover(self, String):
        listString = list(String)
        if self._currentIndex > 0:
            self._currentIndex -= 1
            newString = ""
            for i in range(len(listString)):
                if i != self._currentIndex:
                    newString += str(listString[i])
            return newString
        else:
            return String
    def _letterSeperator(self):
        self._lineSeperatorTime = self._time - self._lineSeperatorTimeHold
        if self._lineSeperatorTime > self._lineSeperatorRefreshTime:
            self._lineSeperatorTimeHold = self._time
            if self._lineSeperatorState:
                self._lineSeperatorState = False
            else:
                self._lineSeperatorState = True
        if self._lineSeperatorState:
            self._shaderLINE.use()
            if self._lineSeperatorUpdate:
                self._lineSeperatorUpdate = False
                position = np.array([(self.MousePickStartPos + self.MousePickEndPos/2.0),
                                     self.MousePickHeightCenter/self._Window.height])
                stringLen = len(self._FontRenderer.StringLenght)
                for k in range(stringLen):
                    position[0] -= self._FontRenderer.StringLenght[k]/2.0
                    if k < self._currentIndex:
                        position[0] += self._FontRenderer.StringLenght[k]

                position[0] /= self._Window.width
                self._shaderLINE.vec2("position", position)
            self._Primetive.DrawLine()
    def _letterSeperatorPlacer(self):
        try:
            totalLenght = 0
            stringLen = len(self._FontRenderer.StringLenght)
            for k in range(stringLen):
                totalLenght += self._FontRenderer.StringLenght[k]
            startPos = self.MousePickStartPos + self.MousePickEndPos / 2 - totalLenght / 2
            endPos = totalLenght
            diff = (self._Window.MousePos[0] - startPos) / endPos
            if diff > 1.0:
                diff = 1.0
            elif diff < 0.0:
                diff = 0.0
            self._currentIndex = int(diff * stringLen)
        except:
            self._currentIndex = int(0)
        self._lineSeperatorUpdate = True
    def _clearString(self):
        if self._markString is False and self._ctrlKey is False:
            self.MainString = ""
            self._markString = True
            self._FontRenderer.MarkString(False)











