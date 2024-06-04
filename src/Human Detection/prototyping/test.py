import time
import cv2
from humanDetection import HumanDetector
import os

file_path = "C:/Users/jonat/PycharmProjects/pythonProject/erkennungszeiten.txt"


# Öffne die Textdatei zum Schreiben
with open(file_path, 'w') as f:
    detector = HumanDetector(show_frame=False)
    cap = cv2.VideoCapture('one-by-one-person-detection.mp4')  # Passe den Pfad zu deinem Video an
    total_time = 0
    num_frames = 50

    for _ in range(num_frames):
        ret, frame = cap.read()
        if not ret:
            break

        start_time = time.time()
        values = detector.locate_person(frame)
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Schreibe die Erkennungszeit in die Textdatei
        f.write(f"Erkennungszeit: {elapsed_time:.2f} Sekunden\n")

        total_time += elapsed_time

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    avg_time = total_time / num_frames
    f.write(f"\nDurchschnittliche Erkennungszeit: {avg_time:.2f} Sekunden")

cap.release()
cv2.destroyAllWindows()
