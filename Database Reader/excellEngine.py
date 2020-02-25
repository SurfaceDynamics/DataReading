
import xlsxwriter


class ExcellEngine:
    def __init__(self):
        yo = 0
    def _addWorkSheet(self, WorkBook, SheetName, ColumnNames, Data):
        worksheet = WorkBook.add_worksheet(SheetName)
        for h in range(len(ColumnNames)):
            worksheet.write(0, h, ColumnNames[h])
        for i in range(len(Data)):
            for j in range(len(Data[0])):
                worksheet.write(i + 1, j, str(Data[i][j]))
    def PushExcellSheet(self, Path, MonthList, DayList, FullList):
        workbook = xlsxwriter.Workbook(Path + '.xlsx')
        self._addWorkSheet(workbook, "Monthly Data",
                           ("Month", "Tool time [h]", "Distance [m]", "Distance pr hour [m/h]"), MonthList)
        self._addWorkSheet(workbook, "Daily Data",
                           ("Date", "Tool time [h]", "Distance [m]", "Distance pr hour [m/h]"), DayList)
        self._addWorkSheet(workbook, "Raw Data",
                           ("Index", "Date", "Start Time", "End Time", "Tool time",
                            "Distance [m]", "Distance pr hour [m/h]"), FullList)


