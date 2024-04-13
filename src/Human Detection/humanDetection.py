import cv2
import numpy as np

class HumanDetector():
    def __init__(self, show_frame = False):
        # Initialize the HumanDetector class with necessary attributes
        self.name = "HumanDetector"
        self.net = cv2.dnn.readNetFromDarknet('/path/to/yolov3.cfg', '/path/to/yolov3.weights')
        self.layer_names = self.net.getLayerNames()
        self.layer_names = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.tracker = None
        self.tracker_bbox = None
        self.selected_human = None
        self.frame_counter = 0
        self.show_frame = show_frame

    def locate_person(self, frame):
        # Locate a person in the frame and retrieve relevant information
        values = []

        # Process the frame to detect and track humans
        self.process_frame(frame)

        # If a person is being tracked, gather information
        if self.tracker_bbox is not None:
            bbox = self.tracker_bbox
            frame_height, frame_width, _ = frame.shape
            custom_x, custom_y = self.cv_to_custom_coordinates(
                x_cv=bbox[0], y_cv=bbox[1], frame_width=frame_width, frame_height=frame_height)
            custom_center_of_person = self.cv_to_custom_coordinates(
                x_cv=bbox[0] + bbox[2] // 2, y_cv=bbox[1] + bbox[3] // 2, frame_width=frame_width, frame_height=frame_height)
            percentage_of_frame_height = self.get_percentage_of_height(
                bbox, frame_height)

            # custom_x center of person
            values.append(custom_center_of_person[0])
            # custom_y center of person
            values.append(custom_center_of_person[1])
            values.append(bbox[2])  # width of person
            values.append(bbox[3])  # height of person
            # values.append(percentage_of_frame_height)
            values.append(frame_width)
            values.append(frame_height)

        return values

    def process_frame(self, frame):
        # Process each frame to detect and track humans
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.layer_names)

        # Select a human to track every 5 frames
        if self.frame_counter % 5 == 0:
            # sets self.selected_human and self.tracker
            self.select_human(frame, outs)

        # Update the tracker and visualize the bounding box
        if self.tracker is not None:
            success, bbox = self.tracker.update(frame)
            self.tracker_bbox = bbox

            if success:
                x, y, w, h = map(int, bbox)
                color = (0, 0, 255)
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, f'({x}, {y})', (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Visualize the bounding boxes of detected humans
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * frame.shape[1])
                    center_y = int(detection[1] * frame.shape[0])
                    w = int(detection[2] * frame.shape[1])
                    h = int(detection[3] * frame.shape[0])

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    color = [0, 255, 0]

                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        # Increment the frame counter
        self.frame_counter += 1
        if self.show_frame == True:
            # Display the processed frame (for testing purposes)
            frame = self.draw_coordinate_system(frame)
            cv2.imshow("Video Stream", frame)

        return frame

    def select_human(self, frame, outs):
        # Select the first detected human for tracking
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]