import cv2
import os
class HumanDetector():
    def __init__(self, show_frame = False, save_image = False, path_to_image = "/home/ubuntu/image", xml_file = "haarcascade_frontalface_default.xml"):
        # Initialize the HumanDetector class with necessary attributes
        self.name = "HumanDetector"        

        self.bbox_person = None
        self.frame_counter = 0
        self.show_frame = show_frame
        self.save_image = save_image
        self.path_to_image = path_to_image
        
        xml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/{}".format(xml_file))     # determins relative path to the xml file
        self.full_body_cascade = cv2.CascadeClassifier(xml_path)

    def locate_person(self, frame):
        values = []

        # Process the frame to detect and track humans
        image = self.process_frame(frame)

        # If a person is being tracked, gather information
        if self.bbox_person is not None:
            frame_height, frame_width, _ = frame.shape
            custom_x, custom_y = self.cv_to_custom_coordinates(
                x_cv=self.bbox_person[0], y_cv=self.bbox_person[1], frame_width=frame_width, frame_height=frame_height)
            custom_center_of_person = self.cv_to_custom_coordinates(
                x_cv=self.bbox_person[0] + self.bbox_person[2] // 2, y_cv=self.bbox_person[1] + self.bbox_person[3] // 2
                , frame_width=frame_width, frame_height=frame_height)

            values.append(int(custom_center_of_person[0]))  # custom_x center of person
            values.append(int(custom_center_of_person[1]))  # custom_y center of person
            values.append(int(self.bbox_person[2]))         # width of person
            values.append(int(self.bbox_person[3]))         # height of person
            values.append(int(frame_width))                 # width of image
            values.append(int(frame_height))                # height of image
            values.append(self.frame_counter)               # amount of images processed

        return values, image

    def process_frame(self, frame):
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        humans = self.full_body_cascade.detectMultiScale(
            gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Select a human to track every 5 frames
        self.select_human(humans)

        # Visualize the bounding boxes of detected faces (for testing purposes)
        for (x, y, w, h) in humans:
            color = (255, 0, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        self.frame_counter += 1
        frame = self.draw_coordinate_system(frame)

        if self.show_frame:            
            cv2.imshow("Video Stream", frame)

        path = "{}/image_{:03d}.jpg".format(self.path_to_image, self.frame_counter)
        if self.save_image:
            try:
                cv2.imwrite(path, frame)    #saves the image in the image folder
            except:
                pass

        return frame

    def select_human(self, humans):
        # Select the first detected human for tracking
        if len(humans) > 0:
            selected_human = humans[0]
            x, y, w, h = selected_human
            self.bbox_person = (x, y, w, h)
        else:
            # No human detected, reset bbox
            self.bbox_person = None

    def get_percentage_of_height(self, location, frame_height):
        if frame_height > 0:
            percentage_of_height = (location[3]/frame_height*100)
            return round(percentage_of_height)
        else:
            return None

    def draw_coordinate_system(self, frame):
        height, width, _ = frame.shape

        cv2.line(frame, (0, height // 2), (width, height // 2),
                 (0, 0, 255), 2)  # Horizontal line (x-axis)
        cv2.line(frame, (width // 2, 0), (width // 2, height),
                 (0, 0, 255), 2)  # Vertical line (y-axis)

        x = width // 2
        count = 0
        while x < width:
            x += 10
            count += 10
            cv2.line(frame, (x, height // 2 - 2),
                     (x, height // 2 + 2), (0, 0, 255), 2)
            if count % 100 == 0:
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
                cv2.line(frame, (x, 0), (x, height), (255, 100, 0), 1)
                cv2.putText(frame, str(count), (x, height // 2 + 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 0), 2)

        y = height // 2
        count = 0
        while y < height:
            y += 10
            count -= 10
            cv2.line(frame, (width // 2 - 2, y), (width // 2 + 2, y),
                     (0, 0, 255), 2)
            if count % 100 == 0:
                cv2.line(frame, (0, y), (width, y), (255, 100, 0), 1)
                cv2.putText(frame, str(count), (width // 2 + 5, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 0), 2)

        y = height // 2
        count = 0
        while y > 0:
            y -= 10
            count += 10
            cv2.line(frame, (width // 2 - 2, y), (width // 2 + 2, y),
                     (0, 0, 255), 2)
            if count % 100 == 0:
                cv2.line(frame, (0, y), (width, y), (255, 100, 0), 1)
                cv2.putText(frame, str(count), (width // 2 + 5, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 100, 0), 2)

        return frame

    def cv_to_custom_coordinates(self, x_cv, y_cv, frame_width, frame_height):
        x_custom = x_cv - frame_width // 2
        y_custom = frame_height // 2 - y_cv
        return x_custom, y_custom

# Beispiel für die Verwendung des HumanDetector
if __name__ == "__main__":
    video_capture = cv2.VideoCapture(0)

    detector = HumanDetector
