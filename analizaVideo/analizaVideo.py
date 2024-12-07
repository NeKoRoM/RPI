import cv2
import numpy as np

from picamera2 import Picamera2
from libcamera import controls
import time
import numpy

def findPt(contour_main, perent_contour_second,output_image, color =(0, 255, 255) ):
       
        x, y = contour_main[0][0]
        x_parent, y_parent = parent_contour[0][0]
    
        xL, yL = contour[0][0]
        x_parentL, y_parentL = perent_contour_second[0][0]
        
        for pt in contour_main:
            if pt[0][0]>x:
                x=pt[0][0] 
                y= pt[0][1]
            if pt[0][0]<xL:
                xL=pt[0][0] 
                yL= pt[0][1]
            
        for pt in perent_contour_second:
            if pt[0][0]>x_parent:
                x_parent =pt[0][0]
                y_parent = pt[0][1]
            if pt[0][0]<x_parentL:
                x_parentL =pt[0][0]
                y_parentL = pt[0][1]
                
        cv2.line(output_image, (x, y), (x_parent , y_parent), color, 1)
        cv2.putText(output_image, f"Left width: {x_parentL-xL}px", (xL, yL - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        cv2.line(output_image, (xL, yL), (x_parentL , y_parentL), color, 1)
        cv2.putText(output_image, f"right width: {x_parent-x}px", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
   

cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640,480)}))
picam2.start()
time.sleep(2)
picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": 1000000000.0})
cv2.namedWindow("Camera")
cv2.namedWindow("Camera1")


all_controls = picam2.camera_controls
print("Available controls:")
for control_name, control_info in all_controls.items():
    print(f"{control_name}: {control_info}")


trackbars = {}
for control_name, control_info in all_controls.items():
    min_value, max_value = control_info[0], control_info[1]
    default_value = control_info[2] if len(control_info) > 2 else min_value
    if min_value < max_value:  # Створюємо трекбари лише для діапазонів значень
        try:
                cv2.createTrackbar(
                    control_name, "Camera",
                    int(default_value), int(max_value),
                    lambda val, c=control_name: update_control(c, val)
                )
                trackbars[control_name] = default_value
        except Exception as e:
                print(f"Error creating trackbar for {control_name}: {e}")




def on_trackbar(val):
        pass
        
def on_trackbar_exp(val):
        pass
        
def on_trackbar_lovH(val):
        pass
def on_trackbar_lovS(val):
        pass
def on_trackbar_lovV(val):
        pass
        
def on_trackbar_highH(val):
        pass
def on_trackbar_highS(val):
        pass
def on_trackbar_highV(val):
        pass
        
cv2.createTrackbar("focus", "Camera", 5,25, on_trackbar)
cv2.createTrackbar("exposure", "Camera", 100,100000, on_trackbar_exp)



cv2.createTrackbar("lov_h", "Camera1", 0,180, on_trackbar_lovH)
cv2.createTrackbar("lov_s", "Camera1", 0,255, on_trackbar_lovS)
cv2.createTrackbar("lov_v", "Camera1", 0,255, on_trackbar_lovV)

cv2.createTrackbar("high_h", "Camera1", 180,180, on_trackbar_highH)
cv2.createTrackbar("high_s", "Camera1", 255,255, on_trackbar_highS)
cv2.createTrackbar("high_v", "Camera1", 55,255, on_trackbar_highV)

on_trackbar_prev = cv2.getTrackbarPos("focus", "Camera")
on_trackbar_exp_prev = cv2.getTrackbarPos("exposure", "Camera")


prev_time = time.time()

while True:
        
         # Оновлення значень параметрів
    for control_name in trackbars.keys():
        trackbar_value = cv2.getTrackbarPos(control_name, "Camera")
        if trackbar_value != trackbars[control_name]:  # Перевірка на зміни
            trackbars[control_name] = trackbar_value
            picam2.set_controls({control_name: trackbar_value})
            print(f"Updated {control_name} to {trackbar_value}")

        
        
        focus_track = cv2.getTrackbarPos("focus", "Camera")
        if focus_track != on_trackbar_prev:
                on_trackbar_prev = focus_track
                picam2.set_controls({"AfMode": controls.AfModeEnum.Manual, "LensPosition": focus_track})
                print(focus_track)
                
        exp_track = cv2.getTrackbarPos("exposure", "Camera")
        if exp_track != on_trackbar_exp_prev:
                on_trackbar_exp_prev = exp_track
                print(f"exp: {exp_track}" )        
                picam2.set_controls({"ExposureTime": exp_track*10})


        
        im = picam2.capture_array()
        low_black = numpy.array([
         cv2.getTrackbarPos("lov_h", "Camera1"),
         cv2.getTrackbarPos("lov_s", "Camera1"),
         cv2.getTrackbarPos("lov_v", "Camera1")], numpy.uint8)
        high_black = numpy.array([
        cv2.getTrackbarPos("high_h", "Camera1"), 
        cv2.getTrackbarPos("high_s", "Camera1"),
        cv2.getTrackbarPos("high_v", "Camera1") ], numpy.uint8)
        
        img_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        # Завантаження зображення
        image = cv2.inRange(img_hsv, low_black, high_black)

        # Застосування порогової обробки для виділення рамок
        _, binary = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)

        # Інверсія зображення, щоб рамки стали білими на чорному фоні
        binary = cv2.bitwise_not(binary)

        # Пошук контурів із використанням ієрархії
        contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Створити копію зображення для відображення результатів
        output_image = im

        min_area = 1000  # Мінімальна площа контуру для обробки

        # Перебір контурів
        for i, contour in enumerate(contours):
            # Ігнорувати зовнішній контур, якщо він не має вкладених контурів
            area = cv2.contourArea(contour)
            if area < min_area:
                continue  # Ігнорувати контур, якщо його площа менша за поріг
                
            if hierarchy[0][i][2] != -1 and hierarchy[0][i][3] != -1 :  # Перевірка наявності дочірнього контуру
                # Отримати батьківський контур (зовнішня рамка
                print(hierarchy[0][i])
                x1, y1, w1, h1 = cv2.boundingRect(contour)

                # Шукати дочірній контур (внутрішня рамка)
                parent_idx = hierarchy[0][i][3]
                parent_contour = contours[parent_idx]
                
                child_idx = hierarchy[0][i][2]
                child_contour = contours[child_idx]
                # Виміряти ширину рамки як різницю між батьківським і дочірнім прямокутниками
                findPt(contour, parent_contour, output_image, (255,255,0))
                findPt(child_contour,contour, output_image, (255,0,255))
                
                
                epsilon = 0.006*cv2.arcLength(parent_contour,True)
                approx = cv2.approxPolyDP(parent_contour,epsilon,True)
                

                # Відобразити контури і виміри на зображенні
                cv2.drawContours(output_image, [contour], -1, (0, 255, 0), 1)  # Зовнішній  gbr GREEN
                cv2.drawContours(output_image, [child_contour], -1, (255, 255, 0), 1)  # Внутрішній контур BLUE
                cv2.drawContours(output_image, [parent_contour], -1, (0, 0, 255), 1)  # Внутрішній контур RED
               
                        
        current_time = time.time()
        fps = 1/(current_time - prev_time)
        prev_time = current_time
        cv2.putText(output_image, f"{fps:.2f}" ,(10,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2,cv2.LINE_AA)
        # Відображення зображення з результатами
        cv2.imshow("Camera1", image)
        cv2.imshow("Camera", output_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
picam2.close()
cv2.destroyAllWindows()
