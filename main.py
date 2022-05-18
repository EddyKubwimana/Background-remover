import cv2
from moviepy import editor as mp
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from win32api import GetSystemMetrics
import datetime
width= GetSystemMetrics(0)
height=GetSystemMetrics(1)
import os
feed= cv2.VideoCapture(0)
feed.set(3,width)
feed.set(4,height)
segmentor = SelfiSegmentation()
image = os.listdir('image')
imglist = []
for impath in image:
    impath = cv2.imread(f'image/{impath}')
    imglist.append(impath)
indeximage = 0
filename=datetime.time.strftime()
filename=f'{filename}.mp4'
fourcc= cv2.VideoWriter_fourcc('m','p','4','v')
writer= cv2.VideoWriter('filename',fourcc,10,(width,height))
while True:
    success, img = feed.read()

    newim = cv2.resize(imglist[indeximage], (width, height))

    imgout =segmentor.removeBG(img,newim,threshold=0.8)
    cv2.imshow("image", imgout)
    writer.write(imgout)
    key = cv2.waitKey(1)
    try:
        if key == ord('a'):
            if indeximage<=17:
                indeximage += 1
        elif key == ord('q'):
            if indeximage >=1:
                indeximage -= 1
        elif key == ord('z'):
            break
        else:
            indeximage = indeximage
    except:
        indeximage = 0
video=mp.VideoFileClip('pythonProject11/filename')
audio=mp.AudioFileClip('pythonProject11/)