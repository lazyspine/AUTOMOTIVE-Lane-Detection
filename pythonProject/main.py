import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import math
from PIL import Image
def half_image(image):
  height, width = image.shape[:2]
  return height // 2 , width // 2

def max_line_right_left(image):
  line = cv2.HoughLinesP(edge,1,np.pi/180,50,maxLineGap=50)
  line_left , line_right = 0 , 0
  x , y = half_image(image)
  coordinate_left = []
  coordinate_right =  []
  if line is not None:
    for line in line:
      x1,y1,x2,y2 = line[0]
      length_line = math.sqrt(pow(x1-x2,2)+pow(y1-y2,2))
      if(x1 > x):
        if line_left < length_line:
          coordinate_left = line[0]
          line_left = length_line
      else:
         if line_right < length_line:
          coordinate_right = line[0]
          line_right = length_line

  return coordinate_right,coordinate_left

def length_x_y(coordinate):
    x1,y1,x2,y2 = coordinate
    length_line = math.sqrt(pow(x1-x2,2)+pow(y1-y2,2))
    return length_line

def pytago(x,y):
    pytago_line = math.sqrt(((x)**2+(y)**2))
    return pytago_line


def nearLine(image,coordinate):
    line = cv2.HoughLinesP(edge,1,np.pi/180,50,maxLineGap=50)
    nearLine,vector_tmp = [] , []
    norm_vector = length_x_y(coordinate)
    if line is not None:
      for line in line:
        x1,y1,x2,y2 = line[0]
        vector_tmp = coordinate[2],coordinate[3],x2,y2
        norm_tmp = length_x_y(vector_tmp)
        if(norm_tmp != 0):
          hypotenuse = pytago(x2-coordinate[0],y2-coordinate[1])
          cosin = (norm_tmp**2+norm_vector**2-hypotenuse**2)/(2*norm_tmp*norm_vector)
          angle_radian = np.arccos(cosin)

          angle_degree = np.degrees(angle_radian)

          if  175< angle_degree <= 180:
            nearLine.append(line[0])
            print(angle_degree,line[0])

    return nearLine

def angle(x1,y1,width):
  if (y1 < 0):
    y1 = -y1 + 720
  else:
    y1 = 720 - y1
  goc_radian = math.atan2((abs(width-x1)),y1)
  goc_do = math.degrees(goc_radian)
  return goc_do


video=cv2.VideoCapture("5314944507048.mp4")
count = 0
while True:
    ret, or_frame = video.read()
    count += 1
    if not ret:
        video=cv2.VideoCapture("5314944507048.mp4")
        continue
    print(count)
    half_bottom = or_frame[int(or_frame.shape[0]/2):, :]

    gray = cv2.cvtColor(half_bottom,cv2.COLOR_BGR2GRAY)

    frame = cv2.GaussianBlur(gray,(5,5),0)

    _, thresholded = cv2.threshold(frame, 170, 250, 1)

    kernel = np.ones((3, 3), np.uint8)
    dilated = cv2.dilate(thresholded, kernel, iterations=1)
    erode = cv2.erode(dilated, kernel, iterations=1)

    edge = cv2.Canny(erode, 100, 200)

    key = cv2.waitKey(25)

    black_image = np.zeros_like(or_frame)
    black_image_test = np.zeros_like(or_frame)
    line = cv2.HoughLinesP(edge, 1, np.pi / 180, 50, maxLineGap=50)
    if line is not None:
        for line in line:
            x1, y1, x2, y2 = line[0]
            cv2.line(black_image, (x1, y1), (x2, y2), (0, 255, 0), 5)
    coordinate_right, coordinate_left = max_line_right_left(black_image)

    x, y = half_image(black_image)
    print(coordinate_right, coordinate_left)

    if len(coordinate_right) != 0:
        x1, y1, x2, y2 = coordinate_right
        cv2.line(black_image_test, (x1, y1), (x2, y2), (0, 255, 0), 5)
    else:
        x1, y1, x2, y2 = 1280, 0, 1280, 720
        cv2.line(black_image_test, (x1, y1), (x2, y2), (0, 255, 0), 5)

    if len(coordinate_left) != 0:
        x1, y1, x2, y2 = coordinate_left
        cv2.line(black_image_test, (x1, y1), (x2, y2), (0, 0, 255), 5)
    else:
        x1, y1, x2, y2 = 0, 0, 0, 720
        cv2.line(black_image_test, (x1, y1), (x2, y2), (0, 0, 255), 5)

    if len(coordinate_right) != 0 and len(coordinate_left) != 0:
        x1, y1, x2, y2 = coordinate_right
        x3, y3, x4, y4 = coordinate_left
    else:
        if len(coordinate_right) == 0 and len(coordinate_left) == 0:
            continue
        elif len(coordinate_right) == 0:
            x1, y1, x2, y2 = 1280, 0, 1280, 720
            x3, y3, x4, y4 = coordinate_left
        else:
            x3, y3, x4, y4 = 0, 0, 0, 720
            x1, y1, x2, y2 = coordinate_right

    # if len(coordinate_right) != 0:
    #   tmp = nearLine(black_image,coordinate_right)
    #   if tmp is not None:
    #     for line in tmp:
    #       x1,y1,x2,y2 = line
    #       cv2.line(black_image_test,(x1,y1),(x2,y2),(0,255,0),5)

    # if len(coordinate_left) != 0:
    #   tmp = nearLine(black_image,coordinate_left)
    #   if tmp is not None:
    #     for line in tmp:
    #       x1,y1,x2,y2 = line
    #       cv2.line(black_image_test,(x1,y1),(x2,y2),(0,0,255),5)

    A1, B1, C1 = (y2 - y1), (x1 - x2), (x1 * y2 - x2 * y1)
    A2, B2, C2 = (y4 - y3), (x3 - x4), (x3 * y4 - x4 * y3)

    det = A1 * B2 - A2 * B1
    if (det != 0):
        x_g = int((B2 * C1 - B1 * C2) / det)
        y_g = int((A1 * C2 - A2 * C1) / det)

    print(det, x_g, y_g)

    # cv2.line(black_image_test, (x2, y2), (x_g, y_g), (0, 0, 255), 5)
    # cv2.line(black_image_test, (x4, y4), (x_g, y_g), (0, 0, 255), 5)

    angle_result = angle(x_g, y_g, y)
    if angle_result >= 80:
        continue
    if (x_g < 640):
        print("RE TRAI: " + str(angle_result))
    else:
        print("RE PHAI: " + str(angle_result))

    cv2.imshow("Frame",frame)
    cv2.imshow("TEST",black_image_test  )
    if (key == 27):
        break
