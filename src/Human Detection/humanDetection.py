import math

import cv2
import numpy as np


class HumanDetector():
    def __init__(self, show_frame=False):
        # Initialize the HumanDetector class with necessary attributes
        self.name = "HumanDetector"
        self.net = cv2.dnn.readNetFromDarknet('yolov3.cfg', 'yolov3.weights')
        self.layer_names = self.net.getLayerNames()
        self.layer_names = [self.layer_names[i - 1]
                            for i in self.net.getUnconnectedOutLayers()]
        self.selected_human = None
        self.frame_counter = 0
        self.show_frame = show_frame
        self.yolo_boxes = []
        self.detected_humans = []  # Personen die 'im ganzen' zu sehen sind

    def locate_person(self, frame):
        frame_height, width, _ = frame.shape
        values = []

        # YOLO vorwärts durch das Netzwerk laufen lassen
        yolo_blob = cv2.dnn.blobFromImage(
            frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(yolo_blob)
        yolo_outs = self.net.forward(self.layer_names)

        # Listen für Boxen, Konfidenzen und Klassen initialisieren
        self.yolo_boxes = []
        yolo_confidences = []

        # Durch die Ausgaben von YOLO laufen und relevante Informationen speichern
        for yolo_out in yolo_outs:
            for detection in yolo_out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > 0.7 and class_id == 0:  # Klasse 0 entspricht einer Person
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * frame_height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * frame_height)

                    # Rechteckkoordinaten berechnen
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    self.yolo_boxes.append([x, y, w, h])
                    yolo_confidences.append(float(confidence))

        # print(yolo_confidences)
        # Sortiere die YOLO-Ergebnisse nach Sicherheit
        indices = cv2.dnn.NMSBoxes(
            self.yolo_boxes, yolo_confidences, 0.8, 0.6)

        # Rahmen um die erkannten Personen zeichnen und das Seitenverhältnis überprüfen
        for i in indices:
            yolo_box = self.yolo_boxes[i]
            x, y, w, h = yolo_box

            # Überprüfen, ob die Person im Ganzen zu sehen ist
            aspect_ratio = w / h
            # print(f'ratio: {aspect_ratio}')
            if aspect_ratio < 0.5:  # Beispiel: Seitenverhältnis überprüfen
                self.detected_humans.append(yolo_box)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        self.selected_human = self.get_most_centered_person(
            frame_height=frame_height, frame_width=width)
        if self.selected_human != None:
            x, y, w, h = self.selected_human
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            custom_center_of_person = self.cv_to_custom_coordinates(
                x_cv=x + w // 2, y_cv=y + h // 2, frame_width=frame_height, frame_height=frame_height)
            percentage_of_frame_height = self.get_percentage_of_height(
                self.selected_human, frame_height)

            # custom_x center of person
            values.append(custom_center_of_person[0])
            # custom_y center of person
            values.append(custom_center_of_person[1])
            values.append(w)  # width of person
            values.append(h)  # height of person
            # values.append(percentage_of_frame_height)
            values.append(width)
            values.append(frame_height)
        # Increment the frame counter
        self.frame_counter += 1
        if self.show_frame == True:
            # Display the processed frame (for testing purposes)
            frame = self.draw_coordinate_system(frame)
            cv2.imshow("Video Stream", frame)
        # self.selected_human = None
        self.detected_humans = []
        return values

    def get_percentage_of_height(self, location, frame_height):
        # Function to get the Percentage of the Person in the Picture
        if frame_height > 0:
            percentage_of_height = (location[3]/frame_height*100)
            # Number is real Percent (*100)
            return round(percentage_of_height)
        else:
            return None

    def draw_coordinate_system(self, frame):

        height, width, _ = frame.shape

        # Koordinatensystem zeichnen
        cv2.line(frame, (0, height // 2), (width, height // 2),
                 (0, 0, 255), 2)  # Horizontale Linie (x-Achse)
        cv2.line(frame, (width // 2, 0), (width // 2, height),
                 (0, 0, 255), 2)  # Vertikale Linie (y-Achse)

        x = width // 2
        count = 0
        while x < width:
            x += 10
            count += 10
            cv2.line(frame, (x, height // 2 - 2),
                     (x, height // 2 + 2), (0, 0, 255), 2)
            if count % 100 == 0:
                # Alle 100 Pixel (dickere Linie)
                cv2.line(frame, (x, 0), (x, height), (255, 100, 0), 1)
                cv2.putText(frame, str(count), (x, height // 2 + 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 0), 2)

        x = width // 2
        count = 0
        while x > 0:
            x -= 10
            count -= 10
            cv2.line(frame, (x, height // 2 - 2),
                     (x, height // 2 + 2), (0, 0, 255), 2)
            if count % 100 == 0:
                # Alle 100 Pixel (dickere Linie)
                cv2.line(frame, (x, 0), (x, height), (255, 100, 0), 1)
                cv2.putText(frame, str(count), (x, height // 2 + 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 0), 2)

        y = height // 2
        count = 0
        while y < height:
            y += 10
            count -= 10
            cv2.line(frame, (width // 2 - 2, y), (width // 2 + 2, y),
                     (0, 0, 255), 2)  # Alle 10 Pixel
            if count % 100 == 0:
                # Alle 100 Pixel (dickere Linie)
                cv2.line(frame, (0, y), (width, y), (255, 100, 0), 1)
                cv2.putText(frame, str(count), (width // 2 + 5, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 0), 2)

        y = height // 2
        count = 0
        while y > 0:
            y -= 10
            count += 10
            cv2.line(frame, (width // 2 - 2, y), (width // 2 + 2, y),
                     (0, 0, 255), 2)  # Alle 10 Pixel
            if count % 100 == 0:
                # Alle 100 Pixel (dickere Linie)
                cv2.line(frame, (0, y), (width, y), (255, 100, 0), 1)
                cv2.putText(frame, str(count), (width // 2 + 5, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 0), 2)

        return frame

    def cv_to_custom_coordinates(self, x_cv, y_cv, frame_width, frame_height):
        x_custom = x_cv - frame_width // 2
        y_custom = frame_height // 2 - y_cv
        return x_custom, y_custom

    def get_most_centered_person(self, frame_height, frame_width):
        def get_squared_distance_to_center(x, y):
            distance = x*x+y*y
            return int(distance)

        min_distance = 10000000
        person_min_distance = None
        if self.detected_humans != None:
            for person in self.detected_humans:
                custom_x, custom_y = self.cv_to_custom_coordinates(
                    person[0], person[1], frame_width, frame_height)
                distance = get_squared_distance_to_center(custom_x, custom_y)

                if distance < min_distance:
                    min_distance = distance
                    person_min_distance = person

            return person_min_distance
        else:
            return None
