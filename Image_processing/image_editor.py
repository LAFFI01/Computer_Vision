import cv2
import numpy as np

img = cv2.imread("/home/sunny/Learning_CV/Image_processing/img/PROFILE.jpg")

cv2.namedWindow("Image",cv2.WINDOW_NORMAL)
cv2.resizeWindow("Image",900,900)

def crop_image(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.rectangle(img, (x, y), (x + 100, y + 100), (0, 255, 0), 2)
        cv2.imshow("Image", img)
        cv2.imwrite("cropped_image.jpg", img[y:y + 100, x:x + 100])
cv2.setMouseCallback("Image", crop_image)

while True:
    cv2.imshow("Image", img)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
cv2.destroyAllWindows()