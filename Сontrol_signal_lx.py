import cv2
import numpy as np
import time


# Константы
RED = (0, 0, 255)
WHITE = (255, 255, 255)
FONT = cv2.FONT_HERSHEY_DUPLEX

# Переменные
alert = 1
delay_red1 = 0
delay_red2 = 0
delay_white = 0
work_red1 = 0
work_red2 = 0
work_white = 0
standby_red1 = 0

# Инициализация камеры, в данном случае видео переезда
cap = cv2.VideoCapture('./videos/signal_lx.MOV')
fourcc = cv2.VideoWriter_fourcc(*'FMP4')
out = cv2.VideoWriter('./results/ControlSignalLX.avi',fourcc, 20.0, (400, 711))

while True:
    ret, frame = cap.read()
    res_img = cv2.resize(frame, (400, 711), cv2.INTER_NEAREST)
    
    # Выделение огней светофора
    crop_img = frame[650:900, 360:850]
    img_red = np.zeros(crop_img.shape[:2], dtype='uint8')    
    img_white = np.zeros(crop_img.shape[:2], dtype='uint8')
    circle_red1 = cv2.circle(img_red.copy(), (105, 160), 50, 255, -1)
    circle_red2 = cv2.circle(img_red.copy(), (400, 150), 50, 255, -1)
    circle_white = cv2.circle(img_white.copy(), (260, 130), 50, 255, -1)  
    img_red1 = cv2.bitwise_and(crop_img, crop_img, mask=circle_red1)
    img_red2 = cv2.bitwise_and(crop_img, crop_img, mask=circle_red2)
    img_white = cv2.bitwise_and(crop_img, crop_img, mask=circle_white)
    cv2.imshow("red signal1", img_red1)
    cv2.imshow("red signal2", img_red2)
    cv2.imshow("white signal", img_white)
    
    # Выделение контуров огней
    img_red1= cv2.medianBlur(img_red1,7)
    img_red2= cv2.medianBlur(img_red2,7)
    hsv_red1 = cv2.cvtColor(img_red1, cv2.COLOR_BGR2HSV)
    hsv_red2 = cv2.cvtColor(img_red2, cv2.COLOR_BGR2HSV)
    hsv_white = cv2.cvtColor(img_white, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 85, 50], dtype = "uint8")
    upper_red = np.array([60, 255, 255], dtype = "uint8")
    lower_violet = np.array([165, 85, 110], dtype = "uint8")
    upper_violet = np.array([180, 255, 255], dtype = "uint8")
    
    # Маска для первого красного огня
    red1_mask_orange = cv2.inRange(hsv_red1, lower_red, upper_red)        #применяем маску по цвету
    red1_mask_violet = cv2.inRange(hsv_red1, lower_violet, upper_violet)  #для красного таких 2
    red1_mask_full = red1_mask_orange + red1_mask_violet #полная масква предствавляет из себя сумму
    
    # Маска для второго красного огня
    red2_mask_orange = cv2.inRange(hsv_red2, lower_red, upper_red)        #применяем маску по цвету
    red2_mask_violet = cv2.inRange(hsv_red2, lower_violet, upper_violet)  #для красного таких 2
    red2_mask_full = red2_mask_orange + red2_mask_violet #полная масква предствавляет из себя сумму
    
    # Маска для белого огня
    lower_white = np.array([0, 0, 190], dtype = "uint8")
    upper_white = np.array([255, 27, 255], dtype = "uint8")
    white_mask = cv2.inRange(hsv_white, lower_white, upper_white)
     
    # Определение горения первого красного огня
    moments = cv2.moments(red1_mask_full, 1)
    dM01 = moments['m01']
    dM10 = moments['m10']
    dArea = moments['m00']  
    if dArea > 1000 and alert == 1:
        x = int(dM10 / dArea)
        y = int(dM01 / dArea)
        delay_red1 = time.time()
    work_red1 = time.time() - delay_red1
    if  0 <= work_red1 < 0.4 and alert == 1:
        cv2.putText(crop_img, 'RED1 OK', (50, 100), FONT, 1, (100, 100, 255), 2)
        cv2.putText(res_img, 'RED1 OK', (150, 285), FONT, 0.4 , (WHITE), 2)
    cv2.imshow('result_red1', red1_mask_full)
    if work_red1 > 4 and alert == 1:
        cv2.putText(res_img, 'RED1 BROKEN', (100, 285), FONT, 0.4 , (WHITE), 2)
        cv2.putText(res_img, 'WARNING!', (100, 200), FONT, 1.5 , (RED), 2)
    
    # Определение горения второго красного огня
    moments = cv2.moments(red2_mask_full, 1)
    dM01 = moments['m01']
    dM10 = moments['m10']
    dArea = moments['m00']  
    if dArea > 1000 and alert == 1:
        x = int(dM10 / dArea)
        y = int(dM01 / dArea)
        delay_red2 = time.time()
    work_red2 = time.time() - delay_red2
    if  0 <= work_red2 < 0.4 and alert == 1:
        cv2.putText(crop_img, 'RED2 OK', (150, 100), FONT, 1, (100, 100, 255), 2)
        cv2.putText(res_img, 'RED2 OK', (260, 270), FONT, 0.4 , (WHITE), 2)
    cv2.imshow('result_red2', red2_mask_full) 
    if work_red2 > 4 and alert == 1:
        cv2.putText(res_img, 'RED2 BROKEN', (260, 270), FONT, 0.4 , (WHITE), 2)
        cv2.putText(res_img, 'WARNING!', (100, 200), FONT, 1.5 , (RED), 2)
          
    # Определение горения белого огня
    moments_white = cv2.moments(white_mask, 1)
    dM01 = moments_white['m01']
    dM10 = moments_white['m10']
    dArea = moments_white['m00']
    if dArea > 800 and alert == 0:
        x = int(dM10 / dArea)
        y = int(dM01 / dArea)
        delay_white = time.time()
    work_white = time.time() - delay_white
    if  0 <= work_white < 1 and alert == 0:
        cv2.putText(crop_img, 'WHITE OK', (x+50, y+50), FONT, 0.4, (WHITE), 2)
        cv2.putText(res_img, 'WHITE OK', (150, 300), FONT, 0.4, (WHITE), 2)
    cv2.imshow('result_white', white_mask)
    if work_white > 5 and alert == 0:
        cv2.putText(res_img, 'WHITE BROKEN', (150, 300), FONT, 0.4 , (WHITE), 2)
        cv2.putText(res_img, 'WARNING!', (100, 200), FONT, 1.5 , (RED), 2)
  
    # Управление режимом извещения (клавиша 'z'), возможно получение извещения от контакта реле
    if cv2.waitKey(1) & 0xFF == ord('z'):
        if alert == 0:
            alert = 1
            COLOR_PEREEZD = RED
            print('Alert: ', alert)
            start_izv = time.time()
        else:
            alert = 0
            work_white = 0
            COLOR_PEREEZD = (102, 217, 255)
            print('Alert: ', alert)
    
    if alert == 0:
        cv2.putText(res_img, 'lx OFF', (30, 50), FONT, 1, (0, 255, 0), 2)
        cv2.putText(res_img, 'status: open', (30, 80), FONT, 1, (0, 255, 0), 1)
    else:
        cv2.putText(res_img, 'lx ON', (30, 50), FONT, 1, (0, 0, 255), 2)
        cv2.putText(res_img, 'status: close', (30, 80), FONT, 1, (0, 0, 255), 2)
  
    # Выход по клавише 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    out.write(res_img)
    cv2.imshow('video feed', res_img)

cap.release()
out.release()
cv2.destroyAllWindows()
