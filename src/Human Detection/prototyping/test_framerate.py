import cv2
import numpy as np
import time

# YOLOv3-Modelldateien
yolo_net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
yolo_layer_names = yolo_net.getUnconnectedOutLayersNames()

# Funktion zum Erkennen und Zeichnen des Rahmens um Personen


def detect_people(frame):

    pass


# Hauptprogramm
# cap = cv2.VideoCapture(0) für webcam
cap = cv2.VideoCapture('')
total_time = 0
num_frames = 50

# Öffne die Textdatei zum Schreiben
with open('tracking_zeiten.txt', 'w') as f:
    for _ in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            break

        start_time = time.time()
        detect_people(frame)
        end_time = time.time()
        elapsed_time = end_time - start_time
        total_time += elapsed_time

        # Schreibe die Erkennungszeit in die Textdatei
        f.write(f"Erkennungszeit: {elapsed_time:.2f} Sekunden\n")

    avg_time = total_time / num_frames
    f.write(f"\nDurchschnittliche Erkennungszeit: {avg_time:.2f} Sekunden")

cap.release()
cv2.destroyAllWindows()
