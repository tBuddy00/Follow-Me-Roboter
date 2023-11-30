import cv2


class HumanDetector():
    def __init__(self):
        # Initialize the HumanDetector class with necessary attributes
        self.name = "HumanDetector"
        self.full_body_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_fullbody.xml')
        self.tracker = cv2.TrackerMIL_create()
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
            center_of_person = (bbox[0] + bbox[2] // 2, bbox[1] + bbox[3] // 2)
            frame_height = frame.shape[0]
            percentage_of_frame_height = self.get_percentage_of_height(
                bbox, frame_height)

            values.append(bbox)
            values.append(center_of_person)
            values.append(percentage_of_frame_height)

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
        # Placeholder method for calculating the percentage of height
        return 'percentage of height - placeholder'
