import numpy as np
import cv2
#import glob


class DistortionCorrection:
    def __init__(self, image_path):
        self.src = cv2.imread(image_path)
        h,  w = self.src.shape[:2]
        self.height = h
        self.width = w

    def undistort(self, focal_length=1000, k1=0, k2=0, p1=0, p2=0):
        mtx = np.array([[focal_length, 0, self.width // 2],
                        [0, focal_length, self.height // 2],
                        [0, 0, 1]])
        dist = np.array([k1, k2, p1, p2])
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(
            mtx, dist, (self.width, self.height), 1, (self.width, self.height))
        dst = cv2.undistort(self.src, mtx, dist, None, newcameramtx)
        height, width, bytesPerComponent = dst.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(dst, cv2.COLOR_BGR2RGB, dst)
        return dst
