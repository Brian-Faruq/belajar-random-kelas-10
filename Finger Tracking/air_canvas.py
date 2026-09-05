import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# Inisialisasi Kamera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Lebar resolusi
cap.set(4, 720)   # Tinggi resolusi

# Inisialisasi Hand Detector (Akurasi 85%)
detector = HandDetector(detectionCon=0.85, maxHands=1)

# Pilihan Warna (Format BGR)
# Merah, Hijau, Biru, dan Hitam (Penghapus)
colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 0, 0)]
drawColor = colors[0]
brushThickness = 15
eraserThickness = 50

# Kanvas kosong transparan tempat menyimpan garis gambar
imgCanvas = np.zeros((720, 1280, 3), np.uint8)

# Titik koordinat awal garis (xp = x previous, yp = y previous)
xp, yp = 0, 0

while cap.isOpened():
    success, frame = cap.read()
    if not success or frame is None:
        continue

    # Cermin gambarnya
    frame = cv2.flip(frame, 1)
    
    # Deteksi tangan
    hands, frame = detector.findHands(frame, draw=True)

    # 1. Gambar UI Palette Warna di bagian atas layar
    cv2.rectangle(frame, (100, 10), (300, 100), (0, 0, 255), cv2.FILLED)    # Kotak Merah
    cv2.rectangle(frame, (350, 10), (550, 100), (0, 255, 0), cv2.FILLED)    # Kotak Hijau
    cv2.rectangle(frame, (600, 10), (800, 100), (255, 0, 0), cv2.FILLED)    # Kotak Biru
    cv2.rectangle(frame, (850, 10), (1150, 100), (255, 255, 255), cv2.FILLED) # Kotak Penghapus
    cv2.putText(frame, "PENGHAPUS", (910, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]
        fingers = detector.fingersUp(hand)

        # Ambil titik koordinat Ujung Telunjuk (Index 8) & Ujung Jari Tengah (Index 12)
        x1, y1 = lmList[8][0], lmList[8][1]
        x2, y2 = lmList[12][0], lmList[12][1]

        # Mode 1: SELECTION MODE (2 Jari Naik: Telunjuk & Jari Tengah)
        # Digunakan untuk memilih warna di menu atas tanpa menggoreskan garis
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0  # Reset koordinat garis
            
            # Jika posisi jari berada di area menu atas (Y < 100)
            if y1 < 100:
                if 100 < x1 < 300:
                    drawColor = colors[0] # Merah
                elif 350 < x1 < 550:
                    drawColor = colors[1] # Hijau
                elif 600 < x1 < 800:
                    drawColor = colors[2] # Biru
                elif 850 < x1 < 1150:
                    drawColor = colors[3] # Penghapus

            # Tampilkan indikator kotak pemilihan
            cv2.rectangle(frame, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # Mode 2: DRAWING MODE (Hanya 1 Jari Naik: Telunjuk)
        # Digunakan untuk melukis di udara
        elif fingers[1] and not fingers[2]:
            cv2.circle(frame, (x1, y1), 15, drawColor, cv2.FILLED)
            
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            # Tentukan ketebalan garis (Kuas biasa vs Penghapus)
            thickness = eraserThickness if drawColor == (0, 0, 0) else brushThickness

            # Gambar garis dari titik sebelumnya ke titik sekarang
            cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, thickness)
            xp, yp = x1, y1

        else:
            xp, yp = 0, 0

    # 2. Penggabungan Kanvas Lukisan dengan Umpan Kamera
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, imgInv)
    frame = cv2.bitwise_or(frame, imgCanvas)

    cv2.imshow("Virtual Air Canvas", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# Pilih Warna (2 Jari):

# Angkat 2 jari (Telunjuk + Jari Tengah).

# Arahkan ke menu warna kotak di bagian atas layar (Merah, Hijau, Biru, atau PENGHAPUS).

# Menggambar / Melukis (1 Jari):

# Turunkan jari tengah, sehingga hanya jari telunjuk yang terangkat.

# Gerakkan telunjukmu di udara untuk menggambar secara bebas.

# Menghapus Tulisan:

# Angkat 2 jari, pilih kotak PENGHAPUS di kanan atas.

# Turunkan jari tengah (sisa telunjuk), lalu usap bagian gambar yang ingin dihapus.