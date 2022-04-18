import cv2
from cvzone.SelfiSegmentationModule import SelfiSegmentation
feed= cv2.VideoCapture(0,)
feed.set(3,1920)
feed.set(4,1080)
segmentor=SelfiSegmentation()
image=cv2.imread("image/2022-03-02 (2).png")
newim= cv2.resize(image,(1280,720))
while True:
    success,img=feed.read()
    var = img.shape
    imgout =segmentor.removeBG(img,newim,threshold=0.5)
    cv2.imshow("image", imgout)
    cv2.waitKey(1)