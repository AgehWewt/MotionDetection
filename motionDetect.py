from imutils.video import VideoStream
from motionRecord import CaptureVideo
from motionUpload import GDrive
import datetime, imutils, time, cv2

class DetectMotion():
    def __init__(self):
        self.writer = None
        print("\n[INFO] Opening page to login to Google")
        self.googleDrive = GDrive()
        print("[INFO] starting up...")
        self.vs = VideoStream(0).start()
        print("[INFO] stream started")
        print("[INFO] one minute until starting")
        print("[INFO] escape while you still can")
        delayTime = 60
        for x in range(delayTime):
            time.sleep(1.0)
            print("[INFO] " + str(delayTime-x) + " seconds remaining...")
        print("[INFO] Motion detection starting...")
        self.checkMotionLoop()

    def getFrame(self):
        self.frame = self.vs.read()
        self.frame = imutils.resize(self.frame, width=640)
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_RGB2GRAY)
        self.gray = cv2.GaussianBlur(self.gray, (21, 21), 0)
        return self.gray

    def checkFrames(self, frame1, frame2):
        frameDelta = cv2.absdiff(frame1, frame2)
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        for c in cnts:
                if cv2.contourArea(c) < 500:
                    continue
                self.motion = True

    def checkMotionLoop(self):
        while True:
            self.motion = False
            frame1 = self.getFrame()
            time.sleep(2)
            frame2 = self.getFrame()
            self.checkFrames(frame1, frame2)

            if self.motion:
                print("[INFO] motion detected")
                CaptureVideo(self.vs, self.googleDrive)
                self.googleDrive.upload()

if __name__ == '__main__':
    DetectMotion()
