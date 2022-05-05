import cv2
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import os
feed= cv2.VideoCapture(0)
feed.set(3,1920)
feed.set(4,1080)
segmentor = SelfiSegmentation()
image = os.listdir('image')
imglist = []
for impath in image:
    impath = cv2.imread(f'image/{impath}')
    imglist.append(impath)
indeximage = 0
writer= cv2.VideoWriter('trialonvideo.avi',cv2.VideoWriter_fourcc('P','I','M','1'),10,(1920,1080))
while True:
    success, img = feed.read()

    newim = cv2.resize(imglist[indeximage], (1280, 720))

    imgout =segmentor.removeBG(img,newim,threshold=0.5)
    writer.write(img)
    cv2.imshow("image", imgout)
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