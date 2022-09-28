import cv2
import pyaudio
import wave
import time
from moviepy import editor as mp
from moviepy import tools as mt
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from win32api import GetSystemMetrics
from datetime import datetime
width = GetSystemMetrics(0)
height = GetSystemMetrics(1)
import os
#recording, the initiliazation of settings for pyaudio
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 2
fs = 8000 # Record at 44100 samples per second


p = pyaudio.PyAudio()  # Create an interface to PortAudio
stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                input=True,
                frames_per_buffer=chunk)
#initializations of values and variables for the settings of the camera.

feed = cv2.VideoCapture(0)
feed.set(3,width)
feed.set(4,height)
frame_rate= 33
prev= 0
segmentor = SelfiSegmentation()
image = os.listdir('image')
imglist = []
for impath in image:
    impath = cv2.imread(f'image/{impath}')
    imglist.append(impath)

timestamp = datetime.now().strftime('%y-%m-%d %H-%M-%S')
#Defining variables for video and audio recorded.

filename = f'{timestamp}.mp4'
record_name = f'{timestamp}.wav'
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
writer = cv2.VideoWriter(filename,fourcc,10,(width,height))


frames = []  # Initialize array to store frames
indeximage = 0
while True:
    #record images
    time_elapsed= time.time()-prev
    success, img = feed.read()
    if time_elapsed>1/frame_rate:
        prev= time.time()
    #resizing the images to fit the heigtht and width of the camera
        newim = cv2.resize(imglist[indeximage], (width, height))
        imgout = cv2.flip(segmentor.removeBG(img, newim, threshold=0.8), 1)
        cv2.imshow("image",imgout)

        writer.write(imgout)#
        key = cv2.waitKey(1)
    record = stream.read(chunk)
    frames.append(record)
    try:
            if key == ord('a'):
                    if indeximage <= 17:
                        indeximage += 1
            elif key == ord('q'):
                if indeximage >= 1:
                     indeximage -= 1
            elif key == ord('z'):
                stream.stop_stream()
                stream.close()
                p.terminate()
                sound_file = wave.open(record_name,'wb')
                sound_file.setnchannels(channels)
                sound_file.setsampwidth(p.get_sample_size(sample_format))
                sound_file.setframerate(fs)
                sound_file.writeframes(b''.join(frames))
                sound_file.close()
                break
            else:
               indeximage = indeximage
    except:
            indeximage = 0
cap=cv2.VideoCapture(filename)
frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
print(f'frames{frames} and fbs{fps}')
if frames==0:
    print(f'no frames rate in the video{filename}')
    writer=cv2.VideoWriter(filename,cv2.VideoWriter_fourcc(*'DIVX'),10,(width,height))
    while True:
        ret,frame= cap.read()
        if ret is True:
            writer.write(frame)
        else:
            cap.release()
            writer.release()
            writer= None
            break