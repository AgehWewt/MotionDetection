from imutils.video import VideoStream
import datetime, imutils, time, cv2

class CaptureVideo():
    def __init__(self, vs, driveObj=None):
        self.vs = vs
        self.driveObj = driveObj
        self.output = 'test.mp4'
        self.writer = None
        self.targetTime = 1
        self.setTime(self.targetTime)
        self.setName()
        self.record()

    def setName(self):
        now = datetime.datetime.now()
        date = str(now.month) + '-' + str(now.day) + '-' + str(now.year)
        timeCon = str(now.hour) + '-' + str(now.minute) + '-' + str(now.second)
        self.output = './zMotion/' + date + '_' + timeCon + '.mp4'
        if self.driveObj != None:
            self.driveObj.setPath(self.output)

    def createWriter(self):
        self.fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.fps = 20
        self.writer = cv2.VideoWriter(self.output, self.fourcc, self.fps,
                                      (640, 480), True)

    def setTime(self, target):
        now = datetime.datetime.now()
        self.targetMin = now.minute + self.targetTime
        if self.targetMin >= 60:
            self.targetMin = 10
        print(now.minute, self.targetMin)
        
    def record(self):
        while True:
            self.now = datetime.datetime.now()
            if self.now.minute >= self.targetMin:
                print("[INFO] video time reached")
                self.writer.release()
                
                break;
            
            self.frame = self.vs.read()

            if __name__ == '__main__':
                cv2.imshow('Stream', self.frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    cv2.destroyAllWindows()
                    self.vs.stop()
                    self.writer.release()
                    break

            if self.writer == None:
                self.createWriter()

            self.writer.write(self.frame)

def testSetup():
    print("\n[INFO] Warming up...")
    vs = VideoStream(0).start()
    time.sleep(2.0)
    print("[INFO] Stream started")
    CaptureVideo(vs)
    vs.stop()

if __name__ == '__main__':
    testSetup()
