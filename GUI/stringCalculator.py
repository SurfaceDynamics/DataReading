import numpy as np

class StringCalculator:
    def __init__(self, DataType="float"):
        self._dataType = DataType
        self._allowedSignes = "()+-*/"
    def Calculator(self, String):
        try:
            float(String)
            return String
        except:
            pass
        sortList = self.stringToSortedList(String)
        bracketList = self._bracketSeperator(sortList)
        valueList = []
        for i in range(len(bracketList)):
            if bracketList[i] != "*" and bracketList[i] != "/" and bracketList[i] != "+" and bracketList[i] != "-":
                muldivList = self._multiplyDevidePass(bracketList[i])
                finalValue = self._addSubPass(muldivList)
                #print(muldivList, finalValue)
                valueList.append(finalValue)
            else:
                valueList.append(bracketList[i])
        muldivList = self._multiplyDevidePass(valueList)
        finalValue = self._addSubPass(muldivList)
        #print("Sorted List", sortList)
        #print("Bracket List", bracketList)
        #print("Final ValueList", valueList)
        #print("Final Value", finalValue)
        if self._dataType == "float":
            finalValue = np.round(finalValue, 3)
        elif self._dataType == "int":
            finalValue = int(finalValue)
        return str(finalValue)
    def stringToSortedList(self, String):
        stringLen = len(String)
        sortList = []
        innerVal = ""
        for i in range(stringLen):
            appender = False
            for j in range(len(self._allowedSignes)):
                if String[i] == self._allowedSignes[j]:
                    if innerVal != "":
                        sortList.append(innerVal)
                    innerVal = ""
                    sortList.append(String[i])
                    appender = True
                    break
            if appender:
                continue
            if String[i] != " ":
                innerVal += String[i]
        if innerVal != "":
            sortList.append(innerVal)
        return sortList
    def _multiplyDevidePass(self, List):
        firstNumb = True
        valueList = []
        mul = False
        div = False
        mulDivStart = False
        mulDivBreak = False
        value = 0
        for i in range(len(List)):
            addSign = False
            try:
                float(List[i])
                if firstNumb:
                    lastValue = float(List[i])
                    if i == 0 and List[i + 1] != "*" and List[i + 1] != "/":
                        valueList.append(List[i])
                        try:
                            float(List)
                            return List
                        except:
                            pass
                    #print(List[i], List, len(List))
                    firstNumb = False
                else:
                    if mul:
                        mul = False
                        value = lastValue * float(List[i])
                        lastValue = value
                    elif div:
                        div = False
                        value = lastValue / float(List[i])
                        lastValue = value
                    else:
                        lastValue = float(List[i])
                        addSingleNumb = True
                        if i <= len(List):
                            if List[i + 1] == "*" or List[i + 1] == "/":
                                addSingleNumb = False
                        if addSingleNumb:
                            valueList.append(List[i])
            except:
                if List[i] == "*":
                    mul = True
                    mulDivStart = True
                elif List[i] == "/":
                    div = True
                    mulDivStart = True
                else:
                    addSign = True
                    if mulDivStart:
                        mulDivBreak = True
            if mulDivStart and i == len(List) - 1:
                mulDivBreak = True
            if mulDivBreak:
                mulDivStart = False
                mulDivBreak = False

                valueList.append(str(value))
            if addSign:
                valueList.append(List[i])
        return valueList
    def _addSubPass(self, List):
        firstValue = True
        currentValue = 0
        finalValue = 0
        add = False
        sub = False
        for i in range(len(List)):
            try:
                float(List[i])

                if firstValue:
                    firstValue = False
                    currentValue = float(List[i])
                    finalValue = currentValue
                    try:
                        float(List)
                        return List
                    except:
                        pass
                else:
                    if add:
                        add = False
                        finalValue = currentValue + float(List[i])
                        currentValue =finalValue
                    elif sub:
                        sub = False
                        finalValue = currentValue - float(List[i])
                        currentValue = finalValue

            except:
                if List[i] == "+":
                    add = True
                elif List[i] == "-":
                    sub = True
        return finalValue
    def _bracketSeperator(self, List):
        if List[0] == "-":
            List.insert(0, "0")
        bracketStarted = False
        bracketEnded = False

        bracketList = []
        bracketStringList = []
        for i in range(len(List)):
            if List[i] == "(":
                bracketStarted = True
                continue
            elif List[i] == ")":
                bracketList.append(bracketStringList)
                bracketStringList = []
                bracketStarted = False
                bracketEnded = True
                continue
            if bracketEnded:
                bracketEnded = False
                bracketList.append(List[i])
                continue
            if bracketEnded is False and bracketStarted is False:
                try:
                    float(List[i])

                    bracketList.append(List[i])
                    continue
                except:
                    bracketList.append(List[i])
                    continue

            if bracketStarted:
                bracketStringList.append(List[i])
        return bracketList


#calc = StringCalculator()
#calc.Calculator("20.27/4.36")