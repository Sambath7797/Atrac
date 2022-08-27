import cv2
from Modules.Attendance import AttendanceManager
from Modules.Timer import Timer
from Modules.FaceRec import FaceRec
import smtplib 
import openpyxl 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart 

def mailstu(li, msg):           
    msg = MIMEText(msg, 'plain')
    server = smtplib.SMTP('smtp.gmail.com')
    server.starttls()
    server.login('newproject7797@gmail.com','Newproject@7797')

    msg['Subject'] = "Attendance Report"
    msg['From'] = ('newproject7797@gmail.com')
    msg['To'] = (','.join(li))
    server.sendmail(msg.get('From'), msg["To"], msg.as_string())
    server.quit()
 

if(__name__ == "__main__"):
    
    timer = Timer()
    attendanceManager = AttendanceManager()
    isColumnAdded = False

    while(True):
        if(timer.CanTakeAttendance()):
            attendanceManager.checkForStudent()
            if(isColumnAdded): 
                attendanceManager.cap = cv2.VideoCapture(0)
                isColumnAdded = False
        else:
            if(not isColumnAdded):
                attendanceManager.cap.release()
                cv2.destroyAllWindows()
                isColumnAdded = True
                attendanceManager.CSV.addColumn()

                print("Attendance Session Ended")
                person_lst = []
                for line in attendanceManager.CSV.AttendanceSheet[1:]:
                    if(line == []):continue
                    
                    percent = 0
                    for word in line[1:]:percent = percent+1 if word == "present" else percent+0
                    
                    if(percent/len(line[1:]) <= 80):person_lst.append([ line[0], (percent/len(line[1:])) * 100])
                print(person_lst)
                mailstu([_[0]  for _ in person_lst ], "You Lack Attendance!")
                print("Mail Sent")
                
      
        key = cv2.waitKey(1)
        if key == 27:
            exit()
    
    attendanceManager.cap.release()
    cv2.destroyAllWindows()
    
