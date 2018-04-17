import numpy as np
import cv2
#import glob


class DistortionCorrection:
    def __init__(self, image_path):
        self.src = cv2.imread(image_path)
        self.height,  self.width = self.src.shape[:2]
        self.dst = self.src.copy()

    def undistort(self, optical_center_x, optical_center_y, focal_length, *, k1=0, k2=0, p1=0, p2=0,  k3=0, k4=0, k5=0, k6=0):
        mtx = np.array([[focal_length, 0, optical_center_x],
                        [0, focal_length, optical_center_y],
                        [0, 0, 1]])
        dist = np.array([k1, k2, p1, p2, k3, k4, k5, k6])
        newcameramtx, self.roi = cv2.getOptimalNewCameraMatrix(
            mtx, dist, (self.width, self.height), 1, (self.width, self.height))
        self.dst = cv2.undistort(self.src, mtx, dist, None, newcameramtx)
        #self.dst = self.dst[y:y + h, x:x + w]
        dst = self.dst.copy()
        cv2.cvtColor(dst, cv2.COLOR_BGR2RGB, dst)
        return dst

    def getImage(self):
        dst = self.dst.copy()
        cv2.cvtColor(dst, cv2.COLOR_BGR2RGB, dst)
        return dst

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def setImage(self, image_path):
        self.__init__(image_path)

    def saveImage(self, output_path):
        x, y, w, h = self.roi
        dst = self.dst[y:y + h, x:x + w]
        cv2.imwrite(output_path, dst)
