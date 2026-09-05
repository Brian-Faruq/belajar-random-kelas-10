import cv2
import pyautogui
import time
from cvzone.FaceMeshModule import FaceMeshDetector

# Ukuran Frame Kamera
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Detector khusus Wajah & Mata
detector = FaceMeshDetector(maxFaces=1)

# Variabel pembantu untuk debouncing (mencegah kombo berulang secara tidak sengaja)
last_action_time = 0
cooldown_time = 1.5  # Jeda 1.5 detik antar aksi

while cap.isOpened():
    success, frame = cap.read()
    if not success or frame is None:
        continue

    frame = cv2.flip(frame, 1)
    frame, faces = detector.findFaceMesh(frame, draw=False)

    if faces:
        face = faces[0]

        # Points Kelopak Mata Kanan (Atas: 159, Bawah: 145)
        top_r, bottom_r = face[159], face[145]
        dist_r, _ = detector.findDistance(top_r, bottom_r)

        # Points Kelopak Mata Kiri (Atas: 386, Bawah: 374)
        top_l, bottom_l = face[386], face[374]
        dist_l, _ = detector.findDistance(top_l, bottom_l)

        # Visualisasi titik mata di layar
        cv2.circle(frame, top_r, 3, (0, 255, 255), cv2.FILLED)
        cv2.circle(frame, bottom_r, 3, (0, 255, 255), cv2.FILLED)
        cv2.circle(frame, top_l, 3, (0, 255, 0), cv2.FILLED)
        cv2.circle(frame, bottom_l, 3, (0, 255, 0), cv2.FILLED)

        current_time = time.time()

        # -------------------------------------------------------------
        # 1. KEDIP MATA KIRI & KANAN BERSAMAAN -> SCREENSHOT
        # -------------------------------------------------------------
        if dist_r < 12 and dist_l < 12:
            if current_time - last_action_time > cooldown_time:
                # Ambil Screenshot
                screenshot = pyautogui.screenshot()
                screenshot.save(f"screenshot_{int(current_time)}.png")
                
                cv2.putText(frame, "SCREENSHOT CAPTURED!", (50, 80),
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
                last_action_time = current_time

        # -------------------------------------------------------------
        # 2. KEDIP MATA KANAN SAJA -> ZOOM IN (Ctrl + Plus)
        # -------------------------------------------------------------
        elif dist_r < 12 and dist_l >= 12:
            if current_time - last_action_time > cooldown_time:
                pyautogui.hotkey('ctrl', '+')
                cv2.putText(frame, "ZOOM IN (+)", (50, 80),
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 255), 2)
                last_action_time = current_time

        # -------------------------------------------------------------
        # 3. KEDIP MATA KIRI SAJA -> ZOOM OUT (Ctrl + Minus)
        # -------------------------------------------------------------
        elif dist_l < 12 and dist_r >= 12:
            if current_time - last_action_time > cooldown_time:
                pyautogui.hotkey('ctrl', '-')
                cv2.putText(frame, "ZOOM OUT (-)", (50, 80),
                            cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 2)
                last_action_time = current_time

    cv2.imshow("Eye Gesture Controller", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Cara Kerjanya:
# Screenshot: Kedipkan kedua mata secara bersamaan. Gambar layar monitor otomatis tersimpan ke folder proyekmu.

# Zoom In (+): Kedipkan mata kanan saja (mengedip/wink kanan) untuk memperbesar tampilan aplikasi atau browser.

# Zoom Out (-): Kedipkan mata kiri saja (wink kiri) untuk memperkecil tampilan.

# Cooldown (1.5 detik): Ditambahkan variabel cooldown_time agar sistem tidak terus-menerus mengambil puluhan screenshot saat kamu memejamkan mata agak lama.