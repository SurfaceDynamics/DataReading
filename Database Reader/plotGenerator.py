from datetime import datetime
import matplotlib.pyplot
from matplotlib import dates, pyplot
import numpy as np
import time
class PlotGenerator:
    def __init__(self, GUIPointer):
        self._guiPointer = GUIPointer
        self._plotGenerated = False
        self._plt = None
    def Plot(self):
        fpsLimit = 10
        endTime = 0
        while self._guiPointer.QUIT is False:
            startTime = time.clock()
            deltaTime = startTime - endTime
            if deltaTime > 0:
                if int(1 / deltaTime) >= fpsLimit:
                    time.sleep(abs(deltaTime - 1 / fpsLimit))
            endTime = time.clock()
            if self._plt is None:
                if self._guiPointer._generatePlot is not None:
                    if self._guiPointer._generatePlot.ButtonState:
                        self._guiPointer._generatePlot.ButtonState = False
                        List = self._guiPointer._database._dataBase.DayList
                        self._plt = matplotlib.pyplot
                        dateList = []
                        toolList = []
                        distList = []
                        distHourList = []
                        for i in range(len(List[:])):
                            date = str(List[i][0])
                            dateList.append(date)
                            toolList.append(str(List[i][1]))
                            distList.append(str(List[i][2]))
                            distHourList.append(str(List[i][3]))
                        Tool = (range(len(toolList)), toolList)
                        Dist = (range(len(toolList)), distList)
                        DistHour = (range(len(toolList)), distHourList)

                        fig, (ax1, ax2, ax3) = self._plt.subplots(3, sharex=True)
                        fig.suptitle('Data')
                        self._plt.xticks(range(len(dateList)), dateList)
                        ax1.plot(Tool[0], Tool[1], "b")
                        ax2.plot(Dist[0], Dist[1], "g")
                        ax3.plot(DistHour[0], DistHour[1], "r")
                        ax1.title.set_text('Tool time [h]')
                        ax2.title.set_text('Distance [m]')
                        ax3.title.set_text('Distance pr hour [m/h]')
                        self._plt.show()
            self._plt = None
