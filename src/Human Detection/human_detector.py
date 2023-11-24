import cv2 as cv
import imutils


class HumanDetector():
    def __init__(self):
        self.name = "HumanDetector"

    def locate_person(self):
        image = cv.imread('image.jpg')
        cv.imshow('test', image)
        cv.waitKey(0)


detector = HumanDetector()
detector.locate_person()
