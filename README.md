# Smart_LX
## Умный переезд
### Python + OpenCV + Yolo

Программа в реальном времени анализирует видеопоток с камер у железнодорожного переезда с помощью OpenCV и YOLO.
Она определяет, свободна ли зона переезда от препятствий автомобилей. 
Одновременно программа контролирует состояние огней переездных автогужевых светофоров — проверяет их горение.
При обнаружении препятствия или неисправности огнй светофоров формирует оповещения и может автоматически управлять заградительными светофорами.

Переезд открыт
![lx_open](https://github.com/ZagBaZ/Smart_LX/images/lx_open.png)

Переезд закрыт, препятствие на пути
![lx_close](https://github.com/ZagBaZ/Smart_LX/images/lx_close.png)

Переезд закрыт, светофор исправен
![signal_lx_close](https://github.com/ZagBaZ/Smart_LX/images/signal_lx_close.png)

Переезд открыт, неисправность белого огня светофора
![signal_lx_open](https://github.com/ZagBaZ/Smart_LX/images/signal_lx_open.png)
