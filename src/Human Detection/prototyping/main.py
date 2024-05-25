import time
import cv2
import numpy as np

class TestHumanDetector:
    #def test_locate_person(self):


        #frame = np.zeros((640, 480, 3), dtype=np.uint8)


        #detector = HumanDetector(show_frame=False)


        #start_time = time.time()


        #values = detector.locate_person(frame)


        #end_time = time.time()

        # Calculate the elapsed time
        #elapsed_time = end_time - start_time

        # Print the elapsed time
        #print(f"Elapsed time: {elapsed_time:.2f} seconds")

        # Assert that the method returns a list of values
        #assert isinstance(values, list)

    def test_multiple_frames(self):

        frame = np.zeros((640, 480, 3), dtype=np.uint8)


        detector = HumanDetector(show_frame=False)

        start_time = time.time()

        for _ in range(50):
            values = detector.locate_person(frame)

        end_time = time.time()

        elapsed_time = end_time - start_time

        print(f"Zeit die vergangen ist wurde um Person zu erkennen: {elapsed_time:.2f} seconds")


        assert isinstance(values, list)

if __name__ == "__main__":
    test = TestHumanDetector()
    test.test_locate_person()
    test.test_multiple_frames()