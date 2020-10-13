import cv2
import pyaudio
import threading
import wave
from mhmovie.code import *
import time

class recVIdAud:

    def vidcap(self):
        self.status=1
        cap=cv2.VideoCapture(0)
        fourcc=cv2.VideoWriter_fourcc(*'mp4v')
        out=cv2.VideoWriter('Video.mp4',fourcc,20.0,(640,480))
        while(cap.isOpened()):
            ret,frame=cap.read()
            if ret==True:
                frame = cv2.GaussianBlur(frame, (15,15), cv2.BORDER_DEFAULT,100)
                # frame = cv2.GaussianBlur(frame,(19,19),sigmaX=0,borderType=cv2.BORDER_DEFAULT)
                # frame = cv2.blur(frame,(39,39))
                out.write(frame)
                cv2.imshow('output',frame)
                if (cv2.waitKey(1) & 0xFF == ord('q')):
                    self.status=0
                    break
        cap.release()
        cv2.destroyAllWindows()


    def audcap(self):
        self.CHUNK = 3024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.RECORD_SECONDS = 5
        self.WAVE_OUTPUT_FILENAME = "output.wav"
        self.frames=[]
        self.status=1
        # time.sleep(3)
        self.py = pyaudio.PyAudio()

        self.stream = self.py.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        print("* recording")
        while self.status == 1:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
            print("* recording Audio")

        print("* done recording")

        self.stream.stop_stream()
        self.stream.close()
        self.py.terminate()

        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.py.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()


    def start_both(self):


        t2=threading.Thread(target=self.audcap)
        t1=threading.Thread(target=self.vidcap)
        t1.start()
        t2.start()


    def combine(self):
        m = movie("Video.mp4")
        mu = music('output.wav')
        mu.Aconvert()  # convert wav to mp3
        final = m + mu
        final.save("./final1.mp4")

a = recVIdAud()
a.start_both()
# a.combine()


