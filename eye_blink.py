import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
from cvzone.PlotModule import LivePlot

cap=cv2.VideoCapture(r'C:\Users\DELL\Downloads\vedio.mp4')
detector=FaceMeschDetector(maxFaces=1)
plotY=LivePlot(640,360,[20,50],invert=True)
idList=[22,23,24,26,110,157,158,159,160,161]
ratioList=[]
blinkCounter=0
counter =0
color=(255,0,255)
while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES)==cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES,0)
    success,img=cap.read()
    img,faces=detector.findFaceMesh(img,draw=False)
    if faces:
        face=faces[0]
        for id in idList:
            cv2.circle(img,face[id],5,color,cv2.FILLED)
        leftup=face[159]
        leftDown=face[23]
        leftLeft=face[130]
        leftRight=face[243]
        lenghtVer,_=detector.findDistance(leftUp,leftDown)
        lenghtHor=detector.findDistance(leftUp,leftDown)
        cv2.line(img,leftUp,leftDown,(0,200,0), 3)
        cv2.line(img,leftLeft,leftRight,(0,200,0), 3)
        ratio=((lenghtVer/lenghtHor)*100)
        ratioList.append(ratio)
        if len(ratioList)>5:
            ratioList.pop(0)
        ratioAvg =sum(ratioList/len(ratioList))
        if ratioAvg<35 and counter==0:
            blinkCounter +=1
            color=(0,200,0)
            counter=1
        if counter !=0:
            counter+=1
            if counter>10:
                counter=0
                color=(250,0,255)           
        cvzone.putTextRect(img,f'Blink Count: {blinkCounter}',(50,100),
                           colorR=color)
        imgPlot=plotY.update(ratioAvg,color)
        cv2.imshow("ImagePlot",imgPlot)
        img=cv2.resize(img,(640,360))
        imgStack= cvzone.stackImages([img,imgPlot],2,1)
    else:
        img=cv2.resize(img,(640,360))
        imgStack= cvzone.stackImages([img,imgPlot],2,1)
    cv2.imshow("Image",imgstack)   
    cv2.waitKey(25)
    print(lenghtHor)
    #img=cv2.resize(img,(640,360))
    cv2.imshow("image",img)
    
    
