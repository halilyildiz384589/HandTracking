"""
Created on Sat Dec  13 07:26:05 2023

@author: halilyildiz
"""

import cv2
import time
import mediapipe
import numpy as np
import HandTrackingModule as htm #bizim kütüphane
import math
import os

#MIT kütüphaneleri
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

#parmak fotoğraflarını alalım
folderPath = "C:\\Users\\halil\\Desktop\\OpenCV_python\\Computer Vision Projects\\HandTrackingProject\\FingerImages"
mylist = os.listdir(folderPath)
print(mylist)

overlayList = [] #boş bir liste atadım.

for imgPath in mylist: #listemden elelmanları tek tek imgPath e ekledim(1-2-3-4--5-6.jpg gibi)
    image = cv2.imread(f'{folderPath}/{imgPath}') #f-string özelliği ile bir dosya yolu atadım. imgpath ile folder path köprüsü kurdum
    #print(f'{folderPath}/{imgPath}')

    overlayList.append(image) #(1.jpg, 2.jpg, ...) overlay listeme ekledim

print(len(overlayList)) #kaç elemanlı baktık


pTime = 0


detector = htm.HandDetector() #değişken atadım
tipIds = [4, 8, 12, 16, 20] #parmak uçlarını listeledim


totalFingers = 0 #toplam parmak diye bir değişken atadım

while True:

    success, img = cap.read()

    img = detector.findHands(img) #parmakları bul
    lmList = detector.findPosition(img, draw=False) #parmakları koordinalarını al lmList listesine at
    #print(lmList)

    if len(lmList) != 0: #parmak algılarsa gir

        fingers = [] #parmaklar için boş bir liste oluşturduk

        # baş parmak açık mı değil mi kontrol edelim ##-1 ile ilk duruma döndük
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]: #lmList de bulunan koordinat değerlerine göre ekleme yapacak. son durum y ekseni koordinatı > ilk y ekseni koordinatı ise parmak listesine ekleme yap (y eksenine göre ve sadece baş parmak)
            fingers.append(1)
        else: #yoksa değer ekleme
            fingers.append(0)


        # başparmak dışında kalan diğer 4 parmak için
        for id in range(1,5): #parmak indisleri - her parmağın ucuna bakar
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]: #koordinatlarını karşılaştırıyoruz. (z eksenine göre )
                fingers.append(1)
                #print("Index finger open")
            else:
                fingers.append(0)


        #print(fingers)
        totalFingers = fingers.count(1) #açık parmakalrın sayısını tut
        print(totalFingers)



    h,w,c = overlayList[totalFingers-1].shape #açık parmak sayısı - 1 = listeye ata ve shapeini al. h,w,c ye ata
    img[0:h, 0:w] = overlayList[totalFingers-1] #0.indeksi heigth ve weigth lerini 200*200 (h*w) e koydum, fakat burada kritik nokta 0.indeksteki fotoğrafın shape ini bilmek. yoksa hata alırız. hata alırsak convertImageSize dosyama bakabilirsiniz. 200:200 e çevirirsiniz. veya herhangi bir boyuta

    cv2.rectangle(img, (20, 225), (170,425), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, str(totalFingers), (45,375),cv2.FONT_HERSHEY_PLAIN, 10, (255,0,0), 25)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400,70), cv2.FONT_HERSHEY_PLAIN,
                3, (255,0,0), 3)

    #Fotoyu göster komutu:))
    cv2.imshow("Image", img)

    #q ya basınca kamera kapanır
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



"""
#foto shape öğrenme kodu 

img = cv2.imread("C:\\Users\\halil\\Desktop\\OpenCV_python\\Computer Vision Projects\\HandTrackingProject\\FingerImages\\1.jpg")
a = img.shape
print(a)

"""