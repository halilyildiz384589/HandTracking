import cv2
import mediapipe as mp #özellikle el yüz tanımada önemli bir python kütüphanesidir.
import time

class HandDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=False, trackCon=0.5):
        self.mode = mode #parametre değerlerini yukarıda belirttiğim üzere varsayılan olarak aldım
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        #Mediapipe el tespiti kodları
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)

        self.mpDraw = mp.solutions.drawing_utils #el tespitini görselleştirdik

    def findHands(self, img, draw=True): #eli görselleştireceğimizi seçtik
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results =  self.hands.process(imgRGB) #elin anahtar noktalarını result a attık

        if self.results.multi_hand_landmarks: #el varsa fonksiyona girer
            for handLms in self.results.multi_hand_landmarks: #anahtar noktalarını alır
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)

        return img

    def findPosition(self, img, handNo=0, draw=True):

        lmList = [] #anahtar nokta koordinatlarnı bir listede tutuyoruz
        if self.results.multi_hand_landmarks: #el gördüyse içine girer
            myHand = self.results.multi_hand_landmarks[handNo] #0.elin anahtar noktalarını aldık
            for id, lm in enumerate(myHand.landmark): #elin anahtar noktalarının koordinatlarını belirliyoruz
                h,w,c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx,cy), 15, (0,0,255), cv2.FILLED)

        return lmList


def main():
    pTime=0
    cTime=0
    cap=cv2.VideoCapture(0)
    detector = handDetector()

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)

        if len(lmList) != 0:
            print(lmList[4]) #4.parmağın kodunu ekrana yazdıracağız.

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

if __name__ == "__main__":
    main()


