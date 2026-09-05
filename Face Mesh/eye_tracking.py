import cv2
from cvzone.FaceMeshModule import FaceMeshDetector

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Detector khusus Wajah & Mata (Maksimal 1 wajah)
detector = FaceMeshDetector(maxFaces=1)

# Indeks titik landmark mata di MediaPipe Face Mesh
# Mata Kiri
LEFT_EYE = [362, 385, 387, 263, 373, 380]
# Mata Kanan
RIGHT_EYE = [33, 160, 158, 133, 153, 144]

while cap.isOpened():
    success, frame = cap.read()
    if not success or frame is None:
        continue

    frame = cv2.flip(frame, 1)
    frame, faces = detector.findFaceMesh(frame, draw=False)

    if faces:
        face = faces[0]

        # 1. Gambar titik-titik di sekitar Mata Kiri (Hijau)
        for id in LEFT_EYE:
            cv2.circle(frame, face[id], 3, (0, 255, 0), cv2.FILLED)

        # 2. Gambar titik-titik di sekitar Mata Kanan (Kuning)
        for id in RIGHT_EYE:
            cv2.circle(frame, face[id], 3, (0, 255, 255), cv2.FILLED)

        # 3. Hitung jarak kelopak atas dan bawah untuk deteksi kedipan (Mata Kanan)
        top_lid = face[159]
        bottom_lid = face[145]
        eye_distance, _ = detector.findDistance(top_lid, bottom_lid)

        # Jika jarak kelopak sangat rapat (kedip)
        if eye_distance < 12:
            cv2.putText(frame, "Mata Terpejam / Kedip!", (50, 50),
                        cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 0, 255), 2)
        else:
            cv2.putText(frame, "Mata Terbuka", (50, 50),
                        cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 2)

    cv2.imshow("Eye Tracking Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()