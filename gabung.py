import cv2
import face_recognition
import os
import numpy as np
from datetime import datetime
import pyttsx3
import csv  # Importing csv module for saving data to CSV
import database

engine = pyttsx3.init()

DATABASE_PATH = "C:\\Users\\MyBook Hype AMD\\Documents\\Praxisai\\siswahadir.db"
FACE_RECOGNITION_THRESHOLD = 0.4
CSV_FILE_PATH = "C:\\Users\\MyBook Hype AMD\\Documents\\Praxisai\\siswahadir.csv"

def play_greeting(message):
    engine.say(message)
    engine.runAndWait()

def check_known_face(face_encoding):
    students = database.get_students()
    results = []
    for name, role, known_face_encoding in students:
        known_face_encoding = np.frombuffer(known_face_encoding)
        distance = face_recognition.face_distance([known_face_encoding], face_encoding)[0]
        if distance < FACE_RECOGNITION_THRESHOLD:
            results.append((name, role))
    return results

def improve_lighting(image):
    yuv_img = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    yuv_img[:, :, 0] = cv2.equalizeHist(yuv_img[:, :, 0])
    img_output = cv2.cvtColor(yuv_img, cv2.COLOR_YUV2BGR)
    return img_output

def save_to_csv(name, role, time):
    with open(CSV_FILE_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, role, time])
    print(f"Data saved to CSV for {name} ({role}) at {time}.")

def register_face(face_image, face_encoding):
    # Show a registration screen
    registration_screen = np.zeros((400, 800, 3), dtype=np.uint8)
    cv2.putText(registration_screen, "REGISTRATION MODE", (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(registration_screen, "Enter name and role on console", (150, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow('Registration', registration_screen)
    cv2.waitKey(1)

    name = input("Enter name: ")
    role = input("Enter role: ")

    # Close the registration screen
    cv2.destroyWindow('Registration')

    face_encoding_str = face_encoding.tobytes()
    database.add_student(name, role, face_encoding_str)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_to_csv(name, role, current_time)
    print(f"Face registered for {name} ({role}).")

def start_video_stream():
    video_capture = cv2.VideoCapture(0)
    arrival_times = {}

    while True:
        ret, frame = video_capture.read()
        frame = improve_lighting(frame)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            names_roles = check_known_face(face_encoding)
            current_time = datetime.now().time()

            if names_roles:
                for name, role in names_roles:
                    if name not in arrival_times:
                        if datetime.strptime("07:00:00", "%H:%M:%S").time() <= current_time <= datetime.strptime("12:00:00", "%H:%M:%S").time():
                            arrival_times[name] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            play_greeting(f"Selamat datang di Praxis High School, {name}.")
                            print(f"{name} ({role}) datang pada {arrival_times[name]}")
                        elif datetime.strptime("14:00:00", "%H:%M:%S").time() <= current_time <= datetime.strptime("17:00:00", "%H:%M:%S").time():
                            play_greeting(f"Selamat jalan, {name}.")
                            print(f"{name} ({role}) sedang meninggalkan sekolah.")

                    label = f"{name} ({role})"
            else:
                label = "Press 'S' to register"

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(frame, label, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s') and len(face_encodings) > 0:
            register_face(frame, face_encodings[0])

        if key == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

start_video_stream()
database.close()
