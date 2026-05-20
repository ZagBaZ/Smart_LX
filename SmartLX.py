from ultralytics import YOLO
import cv2
import numpy as np
import time


def main():
        # Инициализация модели и камеры, в данном случае видео переезда
        model = YOLO("./models/yolov8n.pt")
        cap = cv2.VideoCapture('./videos/lx.MOV')
        
        # Настройки вывода видео
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
        fourcc = cv2.VideoWriter_fourcc(*'FMP4')
        out = cv2.VideoWriter('./results/SmartLX.avi', fourcc, 20.0, (960, 540))

        # Переменные
        alert = 0
        list_lx = [0]
        busy_lx = 0
        
        # Цветовые схемы (BGR)
        RED = (0, 0, 255)
        GREEN = (0, 255, 0)
        YELLOW = (102, 217, 255)
        COLOR_PEREEZD = YELLOW

        while True:
            ret, frame = cap.read()
            if not ret:
                break
        
            # Изменение размера кадра
            frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Распознавание объектов
            results = model.predict(frame)
            result = results[0]

            for box in result.boxes:
                conf = round((box.conf[0].item()) * 100)
                class_id = result.names[int(box.cls.item())]
                
                if conf > 35 and class_id == 'car':
                    for (x, y, w, h) in box.xyxy.tolist():
                        x = int(x)
                        y = int(y)
                        w = int(w)
                        h = int(h)
                        
                        # Проверка положения объекта
                        if (x + h) > 550 and x < 670:
                            frame = cv2.rectangle(frame, (x, y), (w, h), COLOR_PEREEZD, thickness=3)
                            list_lx.append(1)
                        else:
                            frame = cv2.rectangle(frame, (x, y), (w, h), GREEN, thickness=3)
                            list_lx.append(0)

            # Проверка занятости переезда
            if sum(list_lx) > 0:
                busy_lx = 1
            else:
                busy_lx = 0
            list_lx = [0]

            # Управление режимом извещения (клавиша 'z'), возможно получение извещения от контакта реле
            if cv2.waitKey(1) & 0xFF == ord('z'):
                if alert == 0:
                    alert = 1
                    COLOR_PEREEZD = RED
                    start_izv = time.time()
                else:
                    alert = 0
                    COLOR_PEREEZD = YELLOW

            # Состояние перезда
            font = cv2.FONT_HERSHEY_DUPLEX
            if alert == 0:
                cv2.putText(frame, 'lx OFF', (30, 50), font, 1, (0, 255, 0), 2)
                cv2.putText(frame, 'status: open', (30, 80), font, 1, (0, 255, 0), 1)
            else:
                cv2.putText(frame, 'lx ON', (30, 50), font, 1, (0, 0, 255), 2)
                elapsed = time.time() - start_izv
                elapsed_sec = 20 - round(elapsed)
                
                if elapsed_sec < 1:
                    cv2.putText(frame, "status: close!", (30, 80), font, 1, RED, 1)
                else:
                    cv2.putText(frame, "status: closing", (30, 80), font, 1, RED, 1)
                    cv2.putText(frame, str(elapsed_sec), (275, 80), font, 1, RED, 1)
                if elapsed_sec < 1 and busy_lx == 1:
                    cv2.putText(frame, "WARNING!!!", (400, 100), font, 2, RED, 2)

            # Выход по клавише 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                out.release()
                break

            out.write(frame)
            cv2.imshow('video feed', frame)

        cap.release()
        out.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()