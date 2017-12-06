##author: cindy guo
##date: 2017.12.6
##

import pano_stitcher
import cv2,os,sys
import numpy as np
import time

imagepath = '.../'##path to write
start = time.time()
image_list = sorted( [os.path.join(dp, f) for dp, dn, fs in os.walk(imagepath) for f in fs] )
# image_list = sorted(os.listdir(imagepath) )
# print image_list
image_num = len(image_list)
# print image_num
warp_image_list = []
origin_list = []
center = int(image_num/2) ### make sure image num is odd
for i in range(center):### change to be center
    image_a = cv2.imread(image_list[i],cv2.IMREAD_UNCHANGED)#cv2.IMREAD_UNCHANGED  cv2.CV_LOAD_IMAGE_COLOR
    image_b = cv2.imread(image_list[i + 1],cv2.IMREAD_UNCHANGED)
    
    image_a_gray = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
    image_b_gray = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

    image_a_alpha = cv2.cvtColor(image_a, cv2.COLOR_BGR2BGRA)

    # cv2.imshow("hi",image_a)
    # cv2.waitKey(0)
    H_translate = pano_stitcher.homography(image_a_gray, image_b_gray, bff_match=False)
    image_translated, origin = pano_stitcher.warp_image(image_a_alpha, H_translate)
    warp_image_list.append((image_translated))
    origin_list.append((origin))

image_center = cv2.imread(image_list[center],cv2.CV_LOAD_IMAGE_COLOR)
image_center = cv2.cvtColor(image_center, cv2.COLOR_BGR2BGRA)


warp_image_list.append((image_center))
origin_list.append((0,0))

for i in range(center):### change to be center
    # image_a = cv2.imread(image_list[image_num -1 - i],cv2.IMREAD_UNCHANGED)
    image_a = cv2.imread(image_list[image_num -1 - i],-1)
    
    # print "image shape is  ",image_a.shape
    
    image_b = cv2.imread(image_list[image_num -2 - i],cv2.IMREAD_UNCHANGED)
    
    image_a_gray = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
    image_b_gray = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

    image_a_alpha = cv2.cvtColor(image_a, cv2.COLOR_BGR2BGRA)
    
    # print "image_a_alpha shape 1 is  ",image_a_alpha.shape
    

    # cv2.imshow("hi",image_a)
    # cv2.waitKey(0)
    H_translate = pano_stitcher.homography(image_a_gray, image_b_gray, bff_match=False)
    image_translated, origin = pano_stitcher.warp_image(image_a_alpha, H_translate)
    warp_image_list.append((image_translated))
    origin_list.append((origin))
# print warp_image_list, origin_list
# print "origins is ",origin_list
pano = pano_stitcher.create_mosaic(warp_image_list, origin_list)
end = time.time()
during = end - start
print during 
cv2.imwrite("...", pano)### path to save
