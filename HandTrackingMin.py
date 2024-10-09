import cv2
import mediapipe as mp #özellikle el yüz tanımada önemli bir python kütüphanesidir.
import time

cap = cv2.VideoCapture(0)

mphands = mp.solutions.hands #el i tanıması için içeri aktardık
hands = mpHands.Hands() #el tespiti için el modelini yükledik
mpDraw = mp.solutions.drawing_utils #el nesnesini çizmek için kullanıyoruz.

#zamanı tutuyoruz
pTime = 0 #(past time = geçmiş zaman)
cTime = 0 #(current time - anlık zaman)

while True:
    success, img = cap.read() #kamera görüntüsünü al img değişkenine at
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #aslında gereksiz gibi görünüyor. ama biraz liteartür taraması yapılınca özellikle el için bu dönüşümün yapılması çok gerekli
    results = hands.process(imgRGB) #hands.process ile elin anahtar noktalarını belirleriz.
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks: #kaç el tespit edildi, bir el tespit edildiyse bu bloğa girer.
        for handLms in results.multi_hand_landmarks: #anahtar noktalarını aldık.
            for id, lm in enumerate(handLms.landmark): #anahtar noktalarına isim, sayı vb. atayacağız.
                #print(id,lm)
                h, w, c = img.shape #görüntünün yükseklik, genişlik ve kanal sayısını belirledik.
                cx, cy = float(lm.x * w), float(lm.y * h) #(lm = landmark (x,y noktaları), int ile tam sayı istediğimiz belirttik)
                print(id, cx, cy)
                #if id == 4:
                cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED) #anahtar noktalarına circle komutu ile anahtar daire çizdik
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS) #draw_landmarks ile anahtar noktaları birleştiiryoruz. parmak, bile vb. önemli yerleri CONNECTIONS komutu ile çiziyoruz.

    cTime = time.time() #anlık zamanı aldık

    fps = 1/(cTime - pTime) #fps i hesapladık
    pTime = cTime #şuan ki zamanı geçmiş zamana attık

    cv2.putText(img, str(float(fps)), (10,70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3) #basic ayarlar yaptık
    cv2.imshow("Image", img)
    cv2.waitKey(1)




