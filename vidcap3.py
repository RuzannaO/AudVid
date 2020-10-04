import cv2
import pyaudio
import threading
import wave
from mhmovie.code import *

class recVIdAud:
    def __init__(self, chunk=3024, frmat=pyaudio.paInt16, channels=2, rate=44100, py=pyaudio.PyAudio()):

        self.p = py
        self.frames = []
        self.st = 1

    def vidcap(self):
        self.status=1
        cap=cv2.VideoCapture(0)
        fourcc=cv2.VideoWriter_fourcc(*'mp4v')
        out=cv2.VideoWriter('Video.mp4',fourcc,20.0,(640,480))
        while(cap.isOpened()):
            ret,frame=cap.read()
            if ret==True:
                frame = cv2.GaussianBlur(frame, (15,15), cv2.BORDER_DEFAULT)
                out.write(frame)
                cv2.imshow('output',frame)
                if (cv2.waitKey(1) & 0xFF == ord('q')):
                    self.status=0
                    break
        cap.release()
        cv2.destroyAllWindows()


    def audcap(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.RECORD_SECONDS = 5
        self.WAVE_OUTPUT_FILENAME = "output.wav"
        self.status=1
        p = pyaudio.PyAudio()

        self.stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)

        print("* recording")
        frames = []
        while self.status == 1:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
            print("* recording Audio")

        print("* done recording")

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()


    def start_both(self):
        t1=threading.Thread(target=self.vidcap)
        t2=threading.Thread(target=self.audcap)
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


