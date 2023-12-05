import cv2
import human_detector

detector = human_detector.HumanDetector()
cap = cv2.VideoCapture('video2.mp4')
#cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    print(detector.locate_person(frame))

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
