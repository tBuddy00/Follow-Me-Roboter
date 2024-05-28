import cv2
import numpy as np

# YOLOv3-Modelldateien
yolo_net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
yolo_layer_names = yolo_net.getUnconnectedOutLayersNames()

# Funktion zum Erkennen und Zeichnen des Rahmens um Personen


def detect_people(frame):
    height, width, _ = frame.shape

    # YOLO vorwärts durch das Netzwerk laufen lassen
    yolo_blob = cv2.dnn.blobFromImage(
        frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    yolo_net.setInput(yolo_blob)
    yolo_outs = yolo_net.forward(yolo_layer_names)

    # Listen für Boxen, Konfidenzen und Klassen initialisieren
    yolo_boxes = []
    yolo_confidences = []

    # Durch die Ausgaben von YOLO laufen und relevante Informationen speichern
    for yolo_out in yolo_outs:
        for detection in yolo_out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.7 and class_id == 0:  # Klasse 0 entspricht einer Person
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rechteckkoordinaten berechnen
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                yolo_boxes.append([x, y, w, h])
                yolo_confidences.append(float(confidence))

    print(yolo_confidences)
    # Sortiere die YOLO-Ergebnisse nach Vertrauenswürdigkeit
    indices = cv2.dnn.NMSBoxes(
        yolo_boxes, yolo_confidences, 0.8, 0.6)

    # Rahmen um die erkannten Personen zeichnen und das Seitenverhältnis überprüfen
    for i in indices:
        yolo_box = yolo_boxes[i]
        x, y, w, h = yolo_box

        # Überprüfen, ob die Person im Ganzen zu sehen ist
        aspect_ratio = w/h
        print(f'ratio: {aspect_ratio}')
        if aspect_ratio < 0.5:  # Beispiel: Seitenverhältnis überprüfen
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        else:
            print("Entfernung vergrößern")


# Hauptprogramm
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    detect_people(frame)

    cv2.imshow("Person Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
