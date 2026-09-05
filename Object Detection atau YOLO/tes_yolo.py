import cv2
from ultralytics import YOLO

# Load model YOLO paling ringan (nano)
model = YOLO("yolov8n.pt")

# Buka webcam dan deteksi objek secara real-time
results = model.predict(source="0", show=True)


# nama teknologi: Object Detection

# penjelasan:
# Computer Vision (Bidang Utama)
# Cabang dari Artificial Intelligence (AI) yang melatih komputer agar bisa "melihat" dan memahami isi gambar atau video seperti mata manusia.
# YOLOv8 / Ultralytics (Model AI)
# Algoritma Deep Learning cerdas yang bertugas menganalisis gambar dari kamera dan menebak objek secara instan. yolov8n.pt adalah model khusus berukuran kecil (nano) yang dirancang agar cepat dijalankan di laptop tanpa beban berat.
# OpenCV (Library Pemrosesan Gambar)
# Perpustakaan kode yang menangani urusan teknis hardware: mengambil feed video dari webcam kamu frame-demi-frame, lalu menampilkan jendela pop-up di layar.
# PyTorch (Framework Deep Learning)
# Mesin di balik layar yang memproses hitungan matematika rumit dari model YOLO agar deteksi objeknya bisa berjalan lancar.
# Python (Bahasa Pemrograman)
# Bahasa yang kamu gunakan untuk menghubungkan semua teknologi di atas hanya dalam 2–3 baris perintah.