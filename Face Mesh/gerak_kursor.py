import cv2
import pyautogui
from ultralytics import YOLO

# Supaya kursor tidak error/crash di pojok layar
pyautogui.FAILSAFE = False

# Ambil ukuran layar laptop
screen_w, screen_h = pyautogui.size()

# Gunakan model YOLO yang sudah terbukti bisa jalan di laptop kamu
model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success or frame is None:
        continue

    # Cermin gambarnya
    frame = cv2.flip(frame, 1)

    # Deteksi dengan YOLO (conf=0.5 artinya hanya deteksi yang yakin)
    results = model.predict(source=frame, stream=True, verbose=False, conf=0.5)

    for r in results:
        for box in r.boxes:
            # Jika objek yang terdeteksi adalah manusia (cls == 0 adalah 'person')
            if int(box.cls[0]) == 0:
                # Ambil koordinat kotak wajah/badan
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                
                # Hitung titik tengah kepala/badan
                center_x = int((x1 + x2) / 2)
                center_y = int((y1 + y2) / 2)

                # Konversi ke koordinat layar komputer
                cursor_x = int((center_x / frame.shape[1]) * screen_w)
                cursor_y = int((center_y / frame.shape[0]) * screen_h)

                # Gerakkan kursor
                pyautogui.moveTo(cursor_x, cursor_y, duration=0.01)

                # Gambar titik penanda di kamera
                cv2.circle(frame, (center_x, center_y), 8, (0, 255, 0), -1)
                break  # Hanya ikuti 1 orang utama

    cv2.imshow('YOLO Face/Body Tracking Cursor', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# nama fitur: AI-Powered Vision Motion Control

# penejelasan:
# YOLOv8 (You Only Look Once v8)
# Digunakan sebagai "mata" AI untuk mendeteksi keberadaan posisi kamu secara real-time. YOLO mengambil frame dari kamera, mencari koordinat kamu, lalu menentukan titik tengah posisi kamu.
# PyAutoGUI
# Bertindak sebagai jembatan antara Python dan sistem operasi Windows. Library ini menerima koordinat dari YOLO lalu menerjemahkannya menjadi perintah fisik untuk menggerakkan kursor mouse secara otomatis di layar.
# OpenCV
# Mengurus akses ke hardware webcam, mengambil umpan video (video feed), membalik gambar agar seperti cermin (flip), dan menampilkan jendela pratinjau kamera.
# Coordinate Mapping (Matematika Geometri)
# Algoritma sederhana yang mengonversi posisi piksel dari resolusi webcam (misal: 640x480) ke resolusi penuh layar monitor kamu (misal: 1920x1080), sehingga pergerakan kamu di kamera sejajar dengan posisi kursor di layar.