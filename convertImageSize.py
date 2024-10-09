import cv2
import os

image = cv2.imread("C:\\Users\\halil\\Desktop\\OpenCV_python\\Computer Vision Projects\\HandTrackingProject\\FingerImages\\6.jpg")

new_image = cv2.resize(image, (200, 200))

print("Yeni görüntü shape'i:", new_image.shape)

save_dir = "C:\\Users\\halil\\Desktop\\OpenCV_python\\Computer Vision Projects\\HandTrackingProject\\FingerImages"

dosya_adi = "yeni_goruntu.jpg"  # Yeni dosya adı

dosya_yolu = os.path.join(save_dir, dosya_adi)

cv2.imwrite(dosya_yolu, new_image)
