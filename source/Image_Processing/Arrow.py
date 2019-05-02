import cv2
#from matplotlib import pyplot as plt
import numpy as np

#Arrow Standard!
img = cv2.imread("key_type4.jpg",0)
BINARY_THRESH_MIN = 160
BINARY_THRESH_MAX = 255
DISTANCE_TO_FIRST_CUT = 0.265
DISTANCE_BETWEEN_CUT = 0.155
PIN_HEIGHT_INCREMENT = 0.014
WIDTH_OF_CUTS = 0.046
HEIGHT_OF_KEY = 0.312
NUMBER_OF_PIN = 5
MACS = 7
MAXIMUM_CUT_DEPTH = 9
DETECTION_WIDTH = 2
DETECTION_THRESHOLD = 10
RESOLUTION_WIDTH = 800
RESOLUTION_HEIGHT = 600
TEMPLETE_WIDTH = 5

# #Schlage Classic!
# img = cv2.imread("key3.jpg",0)
# BINARY_THRESH_MIN = 150
# BINARY_THRESH_MAX = 255
# DISTANCE_TO_FIRST_CUT = 0.231
# DISTANCE_BETWEEN_CUT = 0.156
# PIN_HEIGHT_INCREMENT = 0.015
# WIDTH_OF_CUTS = 0.031
# HEIGHT_OF_KEY = 0.335
# NUMBER_OF_PIN = 6
# MACS = 7
# MAXIMUM_CUT_DEPTH = 9
# DETECTION_WIDTH = 8
# DETECTION_THRESHOLD = 38

def calcAndDrawHist(image, color):
    hist = cv2.calcHist([image], [0], None, [256], [0.0, 255.0])
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)
    histImg = np.zeros([256, 256, 3], np.uint8)
    hpt = int(0.9 * 256)
    for h in range(256):
        intensity = int(hist[h] * hpt / maxVal)
        cv2.line(histImg, (h, 256), (h, 256 - intensity), color)
    return histImg



img = cv2.resize(img,(RESOLUTION_HEIGHT,RESOLUTION_WIDTH),interpolation=cv2.INTER_AREA)
img = np.rot90(img)
img = np.rot90(img)
img = np.rot90(img)

img = cv2.medianBlur(img,5)

ret,thresh1 = cv2.threshold(img,BINARY_THRESH_MIN,BINARY_THRESH_MAX,cv2.THRESH_BINARY)
# thresh1 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,551,5)

#
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5, 5))
#
thresh1 = cv2.dilate(thresh1,kernel)
thresh1 = cv2.erode(thresh1,kernel)

edges_inside = cv2.Canny(img, 30, 100, apertureSize = 3)
#plt.subplot(122),plt.imshow(img,)
#plt.xticks([]),plt.yticks([])

# img, contours,_= cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(img, contours, -1, (0, 0, 255), 3)
#
# cv2.imshow("img_Coutour", img)


cv2.imshow("Img_origin", img)
cv2.imshow("Img_thresh", thresh1)
cv2.imshow("Img_edge_inside", edges_inside)

houghimg1 = img.copy()
lines = cv2.HoughLines(edges_inside,1,np.pi/180,200)
theta1 = 0
for rho,theta in lines[0]:
    theta1 = theta
    a_w = np.cos(theta)
    b = np.sin(theta)
    x0 = a_w * rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000 * (a_w))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000 * (a_w))
    cv2.line(houghimg1,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imwrite('houghlines3.jpg',houghimg1)

rows, cols= img.shape
M = cv2.getRotationMatrix2D((cols/2,rows/2),-(np.pi/2-theta1)*180/np.pi,1)
dst = cv2.warpAffine(img,M,(cols,rows),borderValue=(255,255,255))

edges_inside = cv2.warpAffine(edges_inside,M,(cols,rows),borderValue=(0,0,0))

cv2.imshow("canny_new", edges_inside)

cv2.imwrite('houghlines4.jpg',dst)

ret,thresh1 = cv2.threshold(dst,BINARY_THRESH_MIN,BINARY_THRESH_MAX,cv2.THRESH_BINARY)

thresh1 = cv2.dilate(thresh1,kernel)
thresh1 = cv2.erode(thresh1,kernel)

edges_canny = cv2.Canny(thresh1, 30, 160, apertureSize = 3)
cv2.imshow("Img_edge", edges_canny)

thresh2 = thresh1.copy()

cv2.imwrite('houghlines5.jpg',thresh1)
cv2.imshow("Img_thresh2", thresh1)
(h, w) = thresh1.shape  # 返回高和宽
# print(h,w)#s输出高和宽
a_w = [0 for z in range(0, w)]
print(a_w)  # a = [0,0,0,0,0,0,0,0,0,0,...,0,0]初始化一个长度为w的数组，用于记录每一列的黑点个数

# 记录每一列的波峰
for j in range(0, w):  # 遍历一列
    for i in range(0, h):  # 遍历一行
        if thresh1[i, j] == 0:  # 如果改点为黑点
            a_w[j] += 1  # 该列的计数器加一计数
            thresh1[i, j] = 255  # 记录完后将其变为白色
    # print (j)

# cv2.imshow("Img_thresh1_purewhite", thresh1)

print(a_w)

#
for j in range(0, w):  # 遍历每一列
    for i in range((h - a_w[j]), h):  # 从该列应该变黑的最顶部的点开始向最底部涂黑
        thresh1[i, j] = 0  # 涂黑

cv2.imshow("Img_thresh_new", thresh1)

# 此时的thresh1便是一张图像向垂直方向上投影的直方图
# 如果要分割字符的话，其实并不需要把这张图给画出来，只需要的到a=[]即可得到想要的信息

(h, w) = thresh2.shape  # 返回高和宽
# print(h,w)#s输出高和宽
a_h = [0 for z in range(0, h)]
print(a_h)  # a1 = [0,0,0,0,0,0,0,0,0,0,...,0,0]初始化一个长度为h的数组，用于记录每一行的黑点个数

# 记录每一行的波峰
for j in range(0, h):  # 遍历一行
    for i in range(0, w):  # 遍历一列
        if thresh2[j, i] == 0:  # 如果改点为黑点
            a_h[j] += 1  # 该列的计数器加一计数
            thresh2[j, i] = 255  # 记录完后将其变为白色
    # print (j)

print(a_h)

#
for j in range(0, h):  # 遍历每一行
    for i in range((w - a_h[j]), w):  # 从该列应该变黑的最顶部的点开始向最底部涂黑
        thresh2[j, i] = 0  # 涂黑

cv2.imshow("Img_thresh2_new", thresh2)

first_h = a_h[h - 1]
last_h = a_h[h - 1]
curr_h = a_h[h - 1]
right_h = a_h[h - 1]
left_h = a_h[h - 1]
highest_h = a_h[h - 1]
highest_h_index = h - 1

for j in range(h-1,-1,-1):
    if(a_h[j]!=a_h[h-1]):
        last_h = j
        break

for j in range(0,h):
    if(a_h[j]!=a_h[0]):
        first_h = j
        break

for j in range(h-1,-1,-1):
    if(a_h[j]!=curr_h):
        curr_h = a_h[j]

    if(curr_h>highest_h):
        highest_h = curr_h
        highest_h_index = j
    if ((j+1)<=h-1) and (a_h[j + 1] != curr_h):
        right_h = a_h[j + 1]
    if (a_h[j - 1]!=curr_h):
        left_h = a_h[j - 1]



#plt.imshow(thresh1, cmap=plt.gray())
#plt.show()
count = NUMBER_OF_PIN
high_w = [0 for z in range(0, count)]

first_w = a_w[w - 1]
last_w = a_w[w - 1]
curr_w = a_w[w - 1]
right_w = a_w[w - 1]
left_w = a_w[w - 1]
highest_w = a_w[w - 1]
start_w = a_w[w-1]
end_w = a_w[w-1]

for j in range(w-1,-1,-1):
    if(a_w[j]!=a_w[w-1]):
        last_w = j
        break

for j in range(0,w):
    if(a_w[j]!=a_w[0]):
        first_w = j
        break

for j in range(w-1,-1,-1):
    if(a_w[j]!=curr_w):
        curr_w = a_w[j]
    if(curr_w>highest_w):
        highest_w = curr_w
    if ((j+1)<=w-1) and (a_w[j + 1] != curr_w):
        right_w = a_w[j + 1]
    if (a_w[j - 1]!=curr_w):
        left_w = a_w[j - 1]
    if((curr_w < left_w) and (curr_w < right_w)):
        high_w[count - 1] = curr_w
        count = count - 1
        if count == 0:
            break


#get key end index
key_cut_end_index = 0
for j in range(w-1,-1,-1):
    continu = 0
    for i in range(0,h):
        if(edges_inside[i,j]):
            key_cut_end_index = j
            continu = 1
            break
    if(continu == 1):
        break
print("key_cut_end_index", key_cut_end_index)


key_cut_start_high = 0
key_cut_start_index = w-1

#get the start of key
for j in range(w-1,-1,-1):
    if(j<(last_w - ((last_w-first_w)/3))):
        if((a_w[j-DETECTION_WIDTH] - a_w[j])>=DETECTION_THRESHOLD):
            key_cut_start_high = a_w[j]
            key_cut_start_index = j
            break


# SHOW OLD KEY CUT INDEX
canny_old_key_cut_start_index = edges_inside.copy()
for j in range(0, h):
    canny_old_key_cut_start_index[j, key_cut_start_index] = 255
cv2.imshow("OLD KEY CUT INDEX", canny_old_key_cut_start_index)

# find height of key!!!!!!
up = 0
down = 0
for j in range(0, h):
    if(edges_inside[j, key_cut_start_index] == 255):
        up = j
        break
for j in range(h-1,-1,-1):
    if(edges_inside[j, key_cut_start_index] == 255):
        down = j
        break
height_key = down - up

print("height_key = ",height_key)

# FIND key_cut_start_index OFFSET!!!!!
for j in range(0, h):
    if(edges_inside[j, key_cut_start_index] == 255):
        while((edges_inside[j, key_cut_start_index-1] == 255) or (edges_inside[j+1, key_cut_start_index-1] == 255) or (edges_inside[j-1, key_cut_start_index-1] == 255)):
            key_cut_start_index = key_cut_start_index - 1
        break

key_cut_start_index = key_cut_start_index - 3

print(high_w)
print("first_w = "+str(first_w))
print("last_w = "+str(last_w))
print("highest_w = "+str(highest_w))

print("first_h = "+str(first_h))
print("last_h = "+str(last_h))
print("highest_h = "+str(highest_h))
print("highest_h_index = " + str(highest_h_index))

print("key_cut_start_high = " + str(key_cut_start_high))
print("key_cut_start_index = " + str(key_cut_start_index))

for j in range(0, h):
    edges_inside[j, key_cut_start_index] = 255
for j in range(0, h):
    edges_inside[j, key_cut_end_index] = 255
#calculate length
img_key_lenth = key_cut_end_index - key_cut_start_index
total_len = DISTANCE_TO_FIRST_CUT + DISTANCE_BETWEEN_CUT * NUMBER_OF_PIN
cut_portion = [0 for z in range(0, NUMBER_OF_PIN)]
for n in range (0,NUMBER_OF_PIN):
    cut_portion[n] = (total_len - DISTANCE_BETWEEN_CUT * (NUMBER_OF_PIN - n))/total_len

cut_index = [0 for z in range(0, NUMBER_OF_PIN)]
high_cut = [0 for z in range(0, NUMBER_OF_PIN)]
for n in range(0,NUMBER_OF_PIN):
    cut_index[n] = int(key_cut_start_index + img_key_lenth * cut_portion[n])
    # cut_index[n] = int(last_w - img_key_lenth * cut_portion[n])
    high_cut[n] = a_w[cut_index[n]]

edges_new_temp_copy = edges_inside.copy()
edges_inside_copy = edges_inside.copy()
edges_canny_copy = edges_canny.copy()


#Templete Matching
template = np.zeros((1,5), np.uint8)
template.fill(255)
cv2.imshow('tmp', template)
meth = 'cv2.TM_CCORR_NORMED'
for i in range(0,NUMBER_OF_PIN):
    for j in range(0, h):
        if(edges_inside_copy[j,cut_index[i]] == 255):
            cropImg = edges_inside_copy[j-TEMPLETE_WIDTH:j+TEMPLETE_WIDTH,cut_index[i]-TEMPLETE_WIDTH:cut_index[i]+TEMPLETE_WIDTH]
            cv2.imshow('crop', cropImg)
            current_h = j
            method = eval(meth)
            res = cv2.matchTemplate(cropImg, template, method)
            threshold = 0.8
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            if(max_val > threshold):
                top_left = (cut_index[i] - TEMPLETE_WIDTH + max_loc[0]-10 ,j-TEMPLETE_WIDTH+ max_loc[1]-10)
                bottom_right = (top_left[0] + 20, top_left[1] + 20)
                cv2.rectangle(edges_inside_copy, top_left, bottom_right, (255,0,0), 3)
                cut_index[i] = int((cut_index[i] - 5 + max_loc[0]-10 + top_left[0] + 20)/2)
            else:
                for r in range(0,10):
                    c = 1
                    for l in range(0,10):
                        if(cropImg[l,r] == 255):
                            max_loc0 = r
                            max_loc1 = l
                            top_left = (cut_index[i] - 5 + max_loc0 - 10, j - 5 + max_loc1 - 10)
                            bottom_right = (top_left[0] + 20, top_left[1] + 20)
                            cv2.rectangle(edges_inside_copy, top_left, bottom_right, (255, 0, 0), 3)
                            cut_index[i] = int((cut_index[i] - 5 + max_loc0 - 10 + top_left[0] + 20) / 2)
                            c = 0
                            break
                    if(c == 0):
                        break
            break
for i in range(0,NUMBER_OF_PIN):
    for j in range(0,h):
        edges_new_temp_copy[j,cut_index[i]] = 255



cut_height = [0 for z in range(0, NUMBER_OF_PIN)]
# get CUT HEIGHT !!!!!
for n in range(0,NUMBER_OF_PIN):
    up = 0
    down = 0
    for j in range(0, h):
        if (edges_inside[j, cut_index[n]] == 255):
            up = j
            break
    for j in range(h - 1, -1, -1):
        if (edges_inside[j, cut_index[n]] == 255):
            down = j
            break
    cut_height[n] = down - up

print("cut_height = " + str(cut_height))



for i in range(0,NUMBER_OF_PIN):
    for j in range(0,h):
        edges_canny[j,cut_index[i]] = 255

for i in range(0,NUMBER_OF_PIN):
    for j in range(0,h):
        edges_inside[j,cut_index[i]] = 255

cv2.imshow("Img_canny_cut", edges_canny)
cv2.imshow("Img_canny_inside_cut", edges_inside)
cv2.imshow("Img_canny_inside_copy", edges_inside_copy)

current_x = 0
previous_h = 0
current_h = 0
max_length = 0


cv2.imshow("temp_cut_copy", edges_new_temp_copy)

cv2.imshow("templete", edges_inside_copy)

print("high_cut = " + str(high_cut))



# portion = [float(0) for z in range(0, 6)]
# for j in range(0,count):
#     a_w = float(high_w[j])
#     b = float(highest_w)
#     portion[j] = a_w / b





# NEW VERSION PART!!!!
high_s = height_key * ((PIN_HEIGHT_INCREMENT * MAXIMUM_CUT_DEPTH) / HEIGHT_OF_KEY)
high_1 = [height_key - float(i) for i in cut_height]
# highest_w = highest_w - high_s
print("Bitting Code")
# min_index = 0
for j in range(0, NUMBER_OF_PIN):
    div = high_1[j]/high_s
    min = abs(div - float(0/9))
    min_index = 0
    for n in range(0,MAXIMUM_CUT_DEPTH + 1):
        sub = abs(div - float(n/MAXIMUM_CUT_DEPTH))
        if(sub<min):
            min = sub
            min_index = n
    print(int(min_index))








# # OLD VERSION PART!!!!
# high_s = highest_w * ((PIN_HEIGHT_INCREMENT * MAXIMUM_CUT_DEPTH) / HEIGHT_OF_KEY)
# # highest_w = highest_w - high_s
# high_1 = [highest_w - float(i) for i in high_w]
# print("highest_key = " + str(highest_w))
#
# print("high1 = " + str(high_1))
# i = 1
#
# print("Bitting Code")
# # min_index = 0
# for j in range(0, NUMBER_OF_PIN):
#     div = high_1[j]/high_s
#     min = abs(div - float(0/9))
#     min_index = 0
#     for n in range(0,MAXIMUM_CUT_DEPTH + 1):
#         sub = abs(div - float(n/MAXIMUM_CUT_DEPTH))
#         if(sub<min):
#             min = sub
#             min_index = n
#     print(int(min_index))



cv2.waitKey(0)
cv2.destroyAllWindows()