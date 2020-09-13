import threading
import os
import urllib.request
import urllib
import cv2
import numpy as np
import time
import sys
from datetime import datetime


folder=os.getcwd()
print(folder)
saveTo="H:\\recording"
file='cameraaddress.txt'
IPADDR=[]
# print("Default",IPADDR)

with open(os.path.join(folder,file),'r') as f:
    for line in f.read().split("\n"):
        print(line, sep='\n')
  

print("these are addresses stored ","if wanna reset then press 1, else 0")
re=int(input())

if re==1:
    while(True):
       print("enter IP address:port")
       ip=input()
       temp='http://'+ip+'/video'
       IPADDR.append(temp)
       print ("Add more? 1 Yes 0 No")
       if(int(input())==0):
          break
       else:
           continue

if re==1:
    with open(os.path.join(folder,file),'w') as f:
        for addr in IPADDR:
            f.write(addr+"\n")
else:
    IPADDR=[]
    with open(os.path.join(folder,file),'r') as f:
        for line in f.read().split("\n"):
            IPADDR.append(line)

print(IPADDR)

class MultiThreading(threading.Thread):
    def __init__(self,threadID,cameraID,IPaddress,IsRun):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.cameraID=cameraID
        self.IPaddress=IPaddress
        self.IsRun=True
        # self.currDate=str(datetime.now().strftime("%d-%m-%Y-%H-%M-%S"))
        # self.rec=cv2.VideoWriter(os.path.join(saveTo,'output-'+self.cameraID+"-"+self.currDate+'.avi'),cv2.VideoWriter_fourcc('M','J','P','G'),30,(640,480))

    def run(self):
        print("starting camera ", self.cameraID)
        # start the camera and process
        if self.IsRun:
            # openCamera(self.cameraID,self.IPaddress,self.IsRun,self.rec)
            openCamera(self.cameraID,self.IPaddress,self.IsRun)
        else:
            return  0 #self.IsRun # thread stopped


# def record(cameraID,frame,IPaddress):

# #define recording save:

#     out.write(frame)
    


# define camera open
# def openCamera(cameraID,IPaddress,IsRun,rec):
def openCamera(cameraID,IPaddress,IsRun):
    print(cameraID)
    try:
        cam=cv2.VideoCapture(IPaddress)
        if cam is None or not cam.isOpened() :
            print("ERROR HANDLED BY IF IN TRY")
            print("camera ",cameraID," is unavailable", " at the IP:port ",IPaddress)
            print("retrying from due to TCP error ")
            for i in range(0,2):
                time.sleep(i) # seconds
                print("retrying in ",i ,"seconds for the camera ID ", cameraID, "IP:port " ,IPaddress )
            openCamera(cameraID,IPaddress,IsRun)
            # openCamera(cameraID,IPaddress,IsRun,rec)

        else:
            currDate=str(datetime.now().strftime("%d-%m-%Y-%H-%M-%S"))
            rec=cv2.VideoWriter(os.path.join(saveTo,'output-'+cameraID+"-"+currDate+'.avi'),cv2.VideoWriter_fourcc('M','J','P','G'),20,(640,480)) #20 is normal speed 30=1.5x 60=3x
            print("FEED STARTED ",cameraID,"IP:port ",IPaddress)
            while True and IsRun :
                _,frame=cam.read()
                rec.write(frame)
                cv2.imshow(cameraID,frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    IsRun=False
                    print("forced destruction of IP:port@ ",IPaddress," camera ID ", cameraID)
                    cam.release()
                    rec.release()
                    cv2.destroyAllWindows()
                    exit(1)
                    break
            
    except :
        if not IsRun:
            return 0
        else:
            try:
                rec.release()
                cam.release()
                cv2.destroyAllWindows()
            except :
                pass

            print("ERROR HANDLED BY EXCEPTION")
            print("failure in connection to the IP:port", cameraID, IPaddress)
            for i in range(0,2):
                time.sleep(i) # seconds
                print("retrying in ",i ,"seconds for the camera ID ", cameraID, "IP:port " ,IPaddress )
            print("trying to connect")
            # openCamera(cameraID,IPaddress,IsRun,rec)
            openCamera(cameraID,IPaddress,IsRun)

nIP=len(IPADDR)
threads=[]
for i in range(0,nIP):
    if IPADDR[i]!='':
        thread=MultiThreading(str(i),str(i),IPADDR[i],True)
        threads.append(thread)

    else:
        continue

for start_thread in threads:
    start_thread.start()
    

# thread1=MultiThreading('1','1','http://192.168.1.2:8080/video')
# thread1.start()
# thread2=MultiThreading('2','2','http://192.168.1.7:8081/video')
# thread2.start()
# while True:


#     _,frame=cam.read()
#     # Finally decode the array to OpenCV usable format ;) 
#     #img = cv2.imdecode(imgNp,-1)	
# 	# put the image on screen
#     cv2.imshow('IPWebcam',frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
# cam.release()
# cv2.destroyAllWindows()
