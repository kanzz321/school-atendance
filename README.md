## Apa saja yang perlu diinstall & Bagaimana cara istalnya
1. face_recognition
pip install face_recognition
2. pyttsx3 (membuat teks bersuara)
pip install pyttsx3
3. datetime

## Cara menjalankan aplikasinya
1. Pastikan semua pustaka sudah terinstal.
2. Sesuaikan jalur ke file database (DATABASE_PATH) dan file CSV (CSV_FILE_PATH) sesuai
3. Jalankan script
4. Aplikasi akan membuka video stream dari kamera dan mulai mendeteksi wajah
5. Ketika wajah dikenali, aplikasi akan menampilkan nama dan peran orang tersebut
6. Menyimpan waktu kehadiran dalam file CSV, dan memberikan ucapan selamat datang(ketika pukul 08:00-12:00)
 dan selamat jalan (ketika mulai pukul 14:00)
7. Jika wajah tidak dikenali, maka menekan tombol S untuk mendaftarkan wajah
8. Tekan Q untuk keluar dari aplikasi

## Output filenya apa saja? (excel, csv,ss, dll)
1. csv (Comma-Separated Values) untuk menyimpan data
Nama: Nama siswa yang dikenali.
Role: Peran atau jabatan siswa (misalnya, "Student").
Time: Waktu kedatangan atau kepergian siswa.
File CSV akan disimpan di lokasi yang ditentukan oleh CSV_FILE_PATH.
