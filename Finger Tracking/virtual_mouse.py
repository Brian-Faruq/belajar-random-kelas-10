import cv2
import numpy as np
import pyautogui
from cvzone.HandTrackingModule import HandDetector

# Matikan failsafe pyautogui agar gerak kursor lancar ke pojok layar
pyautogui.FAILSAFE = False

# Ukuran Layar Monitor
screen_w, screen_h = pyautogui.size()

# Ukuran Frame Kamera
cam_w, cam_h = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, cam_w)
cap.set(4, cam_h)

# Detector Tangan
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Area Aktif Kontrol (Padding agar kursor bisa mencapai pinggir monitor)
frame_margin = 100
smooth_factor = 5
prev_x, prev_y = 0, 0
curr_x, curr_y = 0, 0

while cap.isOpened():
    success, frame = cap.read()
    if not success or frame is None:
        continue

    frame = cv2.flip(frame, 1)
    hands, frame = detector.findHands(frame, draw=True)

    # Gambar area batas kendali (Bounding Box)
    cv2.rectangle(frame, (frame_margin, frame_margin), 
                  (cam_w - frame_margin, cam_h - frame_margin), (255, 0, 255), 2)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        fingers = detector.fingersUp(hand)

        # Koordinat Ujung Telunjuk (8) & Ujung Ibu Jari (4)
        x_index, y_index = lmList[8][0], lmList[8][1]
        x_thumb, y_thumb = lmList[4][0], lmList[4][1]

        # 1. MODE GERAK KURSOR (Hanya Telunjuk Naik)
        if fingers[1] == 1 and fingers[2] == 0:
            # Konversi koordinat kamera ke resolusi monitor
            x_target = np.interp(x_index, (frame_margin, cam_w - frame_margin), (0, screen_w))
            y_target = np.interp(y_index, (frame_margin, cam_h - frame_margin), (0, screen_h))

            # Penghalusan gerak kursor (Smoothing)
            curr_x = prev_x + (x_target - prev_x) / smooth_factor
            curr_y = prev_y + (y_target - prev_y) / smooth_factor

            pyautogui.moveTo(curr_x, curr_y)
            cv2.circle(frame, (x_index, y_index), 12, (255, 0, 0), cv2.FILLED)
            prev_x, prev_y = curr_x, curr_y

        # 2. MODE KLIK KIRI (Cubit / Pinch: Jarak Telunjuk & Ibu Jari Dekat)
        length, info, frame = detector.findDistance((x_index, y_index), (x_thumb, y_thumb), frame)
        if length < 30 and fingers[1] == 1:
            cv2.circle(frame, (info[4], info[5]), 12, (0, 255, 0), cv2.FILLED)
            pyautogui.click()
            pyautogui.sleep(0.15) # Delay singkat mencegah spam-click

        # 3. MODE SCROLL (Telunjuk & Jari Tengah Naik Bersamaan)
        if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0:
            y_middle = lmList[12][1]
            if y_index < 200:
                pyautogui.scroll(120)  # Scroll ke atas
            elif y_index > 300:
                pyautogui.scroll(-120) # Scroll ke bawah

    cv2.imshow("Virtual Mouse Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Menggerakkan Kursor: Angkat hanya jari telunjuk. Gerakkan jari di dalam area kotak ungu pada layar kamera.

# Klik Kiri: Dekatkan ujung jari telunjuk dan ibu jari sampai bersentuhan (gestur mencubit).

# Scroll Halaman: Angkat jari telunjuk + jari tengah bersamaan. Gerakkan tangan ke atas untuk scroll up, atau ke bawah untuk scroll down.