#!/usr/bin/env python3

import time
from ev3dev2.motor import MoveTank, OUTPUT_A, OUTPUT_B
from ev3dev2.sensor import INPUT_1, INPUT_2
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor

tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
color_sensor = ColorSensor(INPUT_1)
ultrasonic = UltrasonicSensor(INPUT_2)

# Початковий стан
stan = "poshuk"

while True:

    # 1. Пошук об'єкта
    if stan == "poshuk":
        tank_drive.on(20, 20)

        if ultrasonic.distance_centimeters < 25:
            tank_drive.off(brake=True)
            stan = "perevirka"

    # 2. Перевірка кольору
    elif stan == "perevirka":
        print("Перевірка кольору")

        if ultrasonic.distance_centimeters > 8:
            tank_drive.on(10, 10)
        else:
            tank_drive.off(brake=True)

            kolir = color_sensor.color
            print("Колір:", kolir)

            if kolir == 5:
                stan = "zupynka"
            else:
                stan = "obizd"

    # 3. Об'їзд перешкоди
    elif stan == "obizd":
        print("Об'їзд")

        tank_drive.on(-20, -20)
        time.sleep(0.7)

        tank_drive.on(20, -20)
        time.sleep(1)

        tank_drive.off(brake=True)
        stan = "poshuk"

    # 4. Зупинка біля червоного куба
    elif stan == "zupynka":
        tank_drive.off(brake=True)
        print("Червоний куб знайдено!")
        break

    time.sleep(0.1)

tank_drive.off(brake=True)
