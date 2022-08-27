from datetime import datetime
import cv2
import json
import openpyxl
from Modules.FaceRec import FaceRec
from Modules.csvManager import CSVManager

class AttendanceManager:
    def __init__(self) -> None:
        self.Config = json.load( open("Modules//config.json",'r') )
        self.CSV = CSVManager()
        self.sfr = FaceRec()
        self.sfr.load_encoding_images("Modules//images//")
        self.cap = cv2.VideoCapture(0)

    def checkForStudent(self):
        if not self.cap.isOpened():
            print("Unable To Open Camera!")
            return

        ret, frame = self.cap.read()
        # Detect Faces
        face_locations, face_names = self.sfr.detect_known_faces(frame)
        for face_loc, name in zip(face_locations, face_names):
            y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

            cv2.putText(frame, name.split(".")[0],(x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 200), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 4)

            self.Present(name)

        cv2.imshow("Frame", frame)
        

    def Present(self,rollNumber:str):
        self.CSV.addValue(rollNumber)