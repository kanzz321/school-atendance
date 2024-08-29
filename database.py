import sqlite3
from datetime import datetime

### Bagian 1: School Attendance System ###

# Membuat koneksi ke database SQLite untuk sistem kehadiran
conn1 = sqlite3.connect('school_attendance.db')

# Membuat objek cursor untuk eksekusi perintah SQL
cursor1 = conn1.cursor()

# Membuat tabel 'students' jika belum ada
cursor1.execute('''
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    face_encoding BLOB NOT NULL
)
''')

# Membuat tabel 'attendance' jika belum ada
cursor1.execute('''
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    date TEXT,
    status TEXT,
    FOREIGN KEY(student_id) REFERENCES students(student_id)
)
''')

# Menyimpan perubahan
conn1.commit()

# Fungsi untuk menambahkan siswa
def add_student(name, role, face_encoding):
    cursor1.execute('INSERT INTO students (name, role, face_encoding) VALUES (?, ?, ?)',
                    (name, role, face_encoding))
    conn1.commit()
    print(f"Siswa '{name}' berhasil ditambahkan.")

# Fungsi untuk mencatat kehadiran siswa
def record_attendance(student_id, status):
    date = datetime.now().strftime("%Y-%m-%d")
    cursor1.execute('INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)', (student_id, date, status))
    conn1.commit()
    print(f"Kehadiran untuk siswa ID {student_id} berhasil dicatat.")

# Fungsi untuk mendapatkan data siswa
def get_students():
    cursor1.execute('SELECT name, role, face_encoding FROM students')
    students = cursor1.fetchall()
    return students

# Fungsi untuk menampilkan semua siswa
def view_students():
    cursor1.execute('SELECT * FROM students')
    students = cursor1.fetchall()
    print("\nData Siswa:")
    for student in students:
        print(student)

# Fungsi untuk menampilkan kehadiran
def view_attendance():
    cursor1.execute('''
    SELECT a.attendance_id, s.name, a.date, a.status
    FROM attendance a
    JOIN students s ON a.student_id = s.student_id
    ''')
    attendance_records = cursor1.fetchall()
    print("\nData Kehadiran:")
    for record in attendance_records:
        print(record)

# Fungsi untuk memperbarui status kehadiran
def update_attendance(attendance_id, status):
    cursor1.execute('UPDATE attendance SET status = ? WHERE attendance_id = ?', (status, attendance_id))
    conn1.commit()
    print(f"Status kehadiran ID {attendance_id} berhasil diperbarui.")

# Fungsi untuk menghapus data kehadiran
def delete_attendance(attendance_id):
    cursor1.execute('DELETE FROM attendance WHERE attendance_id = ?', (attendance_id,))
    conn1.commit()
    print(f"Data kehadiran ID {attendance_id} berhasil dihapus.")

# Menutup koneksi ke database school_attendance.db
def close():
    conn1.close()
