import numpy as np
from datetime import datetime
import numpy as np
import os.path
import sqlite3
import xlsxwriter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
from datetime import datetime
import matplotlib.pyplot
from matplotlib import dates, pyplot
import numpy as np
import databaseEngine
import excellEngine

class MainDatabase:
    def __init__(self):
        self._dataBase = databaseEngine.DatabaseEngine()
        self._excelGenerator = excellEngine.ExcellEngine()
    def PushExcellSheet(self, Path):
        if self._dataBase.ReadBase(Path) is False:
            return False
        self._excelGenerator.PushExcellSheet(Path, self._dataBase.MonthList,
                                             self._dataBase.DayList, self._dataBase.RawData)
        return True