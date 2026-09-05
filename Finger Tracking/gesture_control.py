import cv2
import numpy as np
import screen_brightness_control as sbc
from cvzone.HandTrackingModule import HandDetector
from pycaw.pycaw import AudioUtilities

# Inisialisasi Kamera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Inisialisasi Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Inisialisasi Audio Control Windows (Pycaw Versi Baru)
devices = AudioUtilities.GetSpeakers()
volume = devices.EndpointVolume
volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]

volBar = 400
volPer = 0
brightBar = 400
brightPer = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success or frame is None:
        continue

    frame = cv2.flip(frame, 1)
    hands, frame = detector.findHands(frame, draw=True)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        fingers = detector.fingersUp(hand)

        # Koordinat Ujung Ibu Jari (4) & Telunjuk (8)
        x_thumb, y_thumb = lmList[4][0], lmList[4][1]
        x_index, y_index = lmList[8][0], lmList[8][1]

        # 1. MODE VOLUME (Telunjuk & Ibu Jari)
        if fingers[1] == 1 and fingers[2] == 0 and fingers[4] == 0:
            length, info, frame = detector.findDistance((x_thumb, y_thumb), (x_index, y_index), frame)

            volBar = np.interp(length, [20, 180], [400, 150])
            volPer = np.interp(length, [20, 180], [0, 100])

            volume.SetMasterVolumeLevelScalar(volPer / 100, None)

            cv2.putText(frame, 'Mode: Volume Control', (20, 40), 
                        cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 0, 0), 2)

        # 2. MODE BRIGHTNESS (Telunjuk + Kelingking)
        elif fingers[1] == 1 and fingers[4] == 1:
            length, info, frame = detector.findDistance((x_thumb, y_thumb), (x_index, y_index), frame)

            brightPer = np.interp(length, [20, 180], [0, 100])
            brightBar = np.interp(length, [20, 180], [400, 150])

            sbc.set_brightness(int(brightPer))

            cv2.putText(frame, 'Mode: Brightness Control', (20, 40), 
                        cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 255), 2)

    # UI Visual HUD Bar
    cv2.rectangle(frame, (50, 150), (85, 400), (255, 0, 0), 2)
    cv2.rectangle(frame, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(frame, f'Vol: {int(volPer)} %', (40, 430), 
                cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 0, 0), 2)

    cv2.rectangle(frame, (560, 150), (595, 400), (0, 255, 255), 2)
    cv2.rectangle(frame, (560, int(brightBar)), (595, 400), (0, 255, 255), cv2.FILLED)
    cv2.putText(frame, f'Bri: {int(brightPer)} %', (540, 430), 
                cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 255, 255), 2)

    cv2.imshow("Gesture Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Atur Volume:

# Buka Ibu Jari & Telunjuk saja.

# Makin lebar jarak jepitan jari = Volume naik.

# Makin makin rapat (mencubit) = Volume turun / Mute.

# Atur Kecerahan Layar:

# Buka Ibu Jari + Telunjuk + Kelingking (gestur Rock/Metal / I Love You).

# Atur jarak antara Ibu Jari & Telunjuk untuk menaikkan/menurunkan kecerahan layar monitor laptopmu.