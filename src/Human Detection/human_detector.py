import cv2


class HumanDetector():
    def __init__(self):
        # Initialize the HumanDetector class with necessary attributes
        self.name = "HumanDetector"
        self.full_body_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_fullbody.xml')
        self.tracker = None
        self.tracker_bbox = None
        self.selected_human = None
        self.frame_counter = 0

    def locate_person(self, frame):
        # Locate a person in the frame and retrieve relevant information
        values = []

        # Process the frame to detect and track humans
        self.process_frame(frame)

        # If a person is being tracked, gather information
        if self.tracker_bbox is not None:
            bbox = self.tracker_bbox
            frame_height, frame_width, _ = frame.shape
            # cv_center_of_person = (bbox[0] + bbox[2] // 2, bbox[1] + bbox[3] // 2)
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
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        humans = self.full_body_cascade.detectMultiScale(
            gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Select a human to track every 5 frames
        if self.frame_counter % 5 == 0:
            # sets self.selected_human and self.tracker
            self.select_human(frame, humans)

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
        for (x, y, w, h) in humans:
            color = (255, 0, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        # Increment the frame counter
        self.frame_counter += 1

        # Display the processed frame (for testing purposes)
        frame = self.draw_coordinate_system(frame)
        cv2.imshow("Video Stream", frame)

        return frame

    def select_human(self, frame, humans):
        # Select the first detected human for tracking
        if len(humans) > 0:
            selected_human = humans[0]
            x, y, w, h = selected_human

            # Initialize a MIL tracker for the selected human
            self.tracker = cv2.TrackerMIL_create()
            self.tracker.init(frame, (x, y, w, h))

        else:
            # No human detected, reset the tracker attributes
            # self.tracker = None
            # self.tracker_bbox = None
            self.selected_human = None

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
