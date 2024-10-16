import cv2
import mediapipe as mp
import time

# MediaPipe Pose çözümünü başlattık
mpPose = mp.solutions.pose #insanın 33 farklı noktasını (landmark) alır
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils


cap = cv2.VideoCapture('C:\\Users\\halil\\Desktop\\OpenCV_python\\Computer Vision Projects\\HandTrackingProject\\PoseVideos\\1.mp4')
pTime=0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB) #landmarkları tespit ettik
    #print(results.pose_landmarks)

    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS) #tespit edilenleri çiz
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h,w,c = img.shape
            print(id, lm)
            cx, cy = int(lm.x*w), int(lm.y*h)
            cv2.circle(img, (cx,cy), 5, (255,0,0), cv2.FILLED)



    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70,50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
