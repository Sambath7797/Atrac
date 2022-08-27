import csv
import json
import os.path

class CSVManager:
    def __init__(self) -> None:
        self.Config = json.load( open("Modules//config.json",'r') )

        if( not os.path.isfile(self.Config["paths"]["attendancePath"]) ):
            self.AttendanceSheet = open(self.Config["paths"]["attendancePath"],"w")
        self.__readFile()

    def addColumn(self):
        self.__readFile()
        lines = self.AttendanceSheet
        for line in lines:
            if(line == []):continue
            line.append("absent")
        lines[0][-1] = str(len(lines[0])-1)
        self.__writeFile(lines)
    
    def __isDataExists(self,rollNumber):
        lines = self.AttendanceSheet
        for line in lines:
            if(line != [] and line[0] == rollNumber):return True
        return False
    
    def __readFile(self):
        self.AttendanceSheet = list( csv.reader(open(self.Config["paths"]["attendancePath"],'r')) )
        
    def __writeFile(self,LINES):
        LINES = [x for x in LINES if x != []]
        writer = csv.writer(open(self.Config["paths"]["attendancePath"], 'w'))
        writer.writerows(LINES)

    def addValue(self,rollNumber):

        self.__readFile()
        if(self.__isDataExists(rollNumber)):
            lines = self.AttendanceSheet
            for line in lines:
                if(line != [] and line[0] == rollNumber):
                    line[len(line)-1] = 'present'
        else:
            ls = [rollNumber]
            lines = self.AttendanceSheet
            for i in range( 1,len(lines[0]) ):
                ls.append("absent")
            lines.append(ls)

        self.__writeFile(lines)