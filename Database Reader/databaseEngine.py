import numpy as np
from datetime import datetime
import numpy as np
import os.path
import sqlite3
import xlsxwriter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

class DatabaseEngine:
    def __init__(self):
        self.Name = []
        self.RawData = []
        self.MonthList = []
        self.DayList = []

    def _yearStringSplit(self, Date):
        year = str(Date)
        year = year.split(".")
        return str(year[2])

    def _monthStringSplit(self, Date):
        month = str(Date)
        month = month.split(".")
        return str(month[0])
    def _dayStringSplit(self, Date):
        day = str(Date)
        day = day.split(".")
        return str(day[1])
    def _timeInHour(self, Time):
        time = str(Time)
        time = time.split(":")
        timeSec = 0
        for i in range(len(time)):
            index = len(time) - 1 - i
            timeSec += int(time[i]) * np.power(60, index)
        return timeSec/np.power(60, 2)

    def _dayAdder(self):
        lastDay = self._dayStringSplit(self.RawData[0][1])
        date = self.RawData[0][1]
        toolTime = 0
        distance = 0
        distancePrhour = 0
        dayList = []
        for i in range(len(self.RawData)):
            currentDay = self._dayStringSplit(self.RawData[i][1])
            if lastDay != currentDay:
                lastDay = currentDay
                dayList.append((date, toolTime, distance, distancePrhour))
                date = self.RawData[i][1]
                toolTime = 0
                distance = 0
                distancePrhour = 0

            toolTime += self._timeInHour(self.RawData[i][4])
            distance += float(self.RawData[i][5])
            distancePrhour += float(self.RawData[i][6])
        dayList.append((date, toolTime, distance, distancePrhour))
        return dayList
    def _monthAdder(self):
        lastMonth = self._monthStringSplit(self.RawData[0][1])
        date = self._monthStringSplit(self.RawData[0][1]) + "." + self._yearStringSplit(self.RawData[0][1])
        toolTime = 0
        distance = 0
        distancePrhour = 0
        monthList = []
        for i in range(len(self.RawData)):
            currentMonth = self._monthStringSplit(self.RawData[i][1])
            if lastMonth != currentMonth:
                lastMonth = currentMonth
                monthList.append((date, toolTime, distance, distancePrhour))
                date = self._monthStringSplit(self.RawData[i][1]) + "." + self._yearStringSplit(self.RawData[i][1])
                toolTime = 0
                distance = 0
                distancePrhour = 0

            toolTime += self._timeInHour(self.RawData[i][4])
            distance += float(self.RawData[i][5])
            distancePrhour += float(self.RawData[i][6])
        monthList.append((date, toolTime, distance, distancePrhour))
        return monthList

    def _dataCollector(self, Path):
        connectToFile = sqlite3.connect(str(Path))
        file = connectToFile.cursor()
        file.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabel = str(file.fetchall())
        tabel = tabel.replace("[('","")
        tabel = tabel.replace("',)]", "")
        file.execute('PRAGMA TABLE_INFO({})'.format(tabel))
        columnNames = [tup[1] for tup in file.fetchall()]
        file.execute("SELECT * FROM {tn} WHERE {idf}={my_id}".format(tn=tabel, cn=columnNames, idf=2, my_id=2))
        self.Name = str(tabel)
        self.RawData = list(file.fetchall())
        file.close()
    def ReadBase(self, Path):
        self._path = Path
        if os.path.exists(self._path):
            try:
                self._dataCollector(self._path)
                self.MonthList = self._monthAdder()
                self.DayList = self._dayAdder()
                return True
            except:
                return False




