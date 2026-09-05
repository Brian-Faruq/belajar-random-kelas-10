import cv2
from cvzone.HandTrackingModule import HandDetector

# Inisialisasi kamera
cap = cv2.VideoCapture(0)

# Inisialisasi pengenal tangan (detectionCon: tingkat akurasi minimal 80%, maxHands: maksimal 2 tangan)
detector = HandDetector(detectionCon=0.8, maxHands=2)

while cap.isOpened():
    success, frame = cap.read()
    if not success or frame is None:
        continue

    # Cermin gambarnya
    frame = cv2.flip(frame, 1)

    # Deteksi tangan dan ambil titik koordinatnya
    hands, frame = detector.findHands(frame)

    if hands:
        # Mengambil data tangan pertama yang terdeteksi
        hand1 = hands[0]
        lmList = hand1["lmList"]  # Daftar 21 titik koordinat jari
        handType = hand1["type"]  # Tangan Kiri atau Kanan

        # Hitung berapa jari yang sedang berdiri
        fingers = detector.fingersUp(hand1)
        totalFingers = fingers.count(1)

        # Tampilkan teks jumlah jari di layar
        cv2.putText(frame, f'{handType}: {totalFingers} Jari', (50, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Hand & Finger Tracking', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()