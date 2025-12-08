import cv2
import numpy as np

image_path = "/home/sunny/Learning_CV/Image_processing/img/PROFILE.jpg" # Image path 
img = cv2.imread(image_path)
original_img = img.copy() 
display_img = img.copy()

cv2.namedWindow("Image",cv2.WINDOW_NORMAL)
cv2.resizeWindow("Image",900,900)

drawing = False
start_point = (-1, -1)
cropped_roi = None
crop_x, crop_y, crop_w, crop_h = -1, -1, -1, -1


def crop_image(event, x, y, flags, param):
    global display_img, drawing, start_point, cropped_roi, crop_x, crop_y, crop_w, crop_h

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)
        display_img = original_img.copy() 

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            temp_img = display_img.copy()
            cv2.rectangle(temp_img, start_point, (x, y), (0, 255, 0), 6)
            cv2.imshow("Image", temp_img)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(display_img, start_point, (x, y), (0, 255, 0), 4)
        x1, y1 = start_point
        x2, y2 = x, y
        crop_x = min(x1, x2)
        crop_y = min(y1, y2)
        crop_w = abs(x2 - x1)
        crop_h = abs(y2 - y1)
        cropped_roi = original_img[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
        cv2.imshow("Image", display_img) 

cv2.setMouseCallback("Image", crop_image)

while True:
    cv2.imshow("Image", display_img)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        if cropped_roi is not None:
            cv2.imwrite("cropped_image.jpg", cropped_roi)
            cv2.imshow("Cropped_Image", cropped_roi)
            print(f"Cropped image shape: {cropped_roi.shape}")
            print("Cropped image saved!")
    if key == ord('b'):
        if cropped_roi is not None:
            blur = cv2.blur(cropped_roi,(50,50))
            display_img[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w] = blur
            original_img = display_img.copy()
            print("Blur applied. Press 'r' to reset.")
    if key == ord('g'):
        if cropped_roi is not None and cropped_roi.size > 0:
            blurred_roi = cv2.GaussianBlur(cropped_roi, (15, 15), 0)
            display_img[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w] = blurred_roi
            original_img = display_img.copy()
            print("Gaussian blur applied. Press 'r' to reset.")

    if key == ord('r'):
        display_img = img.copy()
        original_img = img.copy()
        print("Image has been reset.")
    if key == ord('q'):
        break
cv2.destroyAllWindows()