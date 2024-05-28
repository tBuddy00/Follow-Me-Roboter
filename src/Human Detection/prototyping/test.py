# In der Datei test.py
import time
import cv2
import humanDetection

detector = humanDetection.HumanDetector(show_frame=True)
cap = cv2.VideoCapture(0)  # Für Webcam, oder 'video.mp4' für Video-Datei

# Öffne die Textdatei zum Schreiben
with open('erkennungszeiten.txt', 'w') as f:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        start_time = time.time()

        values = detector.locate_person(frame)

        end_time = time.time()
        elapsed_time = end_time - start_time

        # Schreibe die Erkennungszeit in die Textdatei
        f.write(f"Erkennungszeit: {elapsed_time:.2f} Sekunden\n")

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break


def locate_person(self, frame):
    frame_height, width, _ = frame.shape
    values = []


    if self.show_frame:
        frame = self.draw_coordinate_system(frame)
        cv2.imshow("Video Stream", frame)

    return values