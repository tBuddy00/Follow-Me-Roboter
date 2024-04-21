import cv2
import humanDetection

#detector = human_detector.HumanDetector(show_frame= True)
detector = humanDetection.HumanDetector(show_frame= True)
#cap = cv2.VideoCapture('video.mp4')
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    print(detector.locate_person(frame))

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
