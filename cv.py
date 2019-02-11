import cv2
import sys
import numpy as np
import serial
import time

ser = serial.Serial('/dev/tty.usbmodem1411', 9600)
time.sleep(3)

# カメラの切り取る点
(x, y) = (200, 200)
# カメラの切り取る領域
(w, h) = (150, 150)

(w_thre, h_thre) = (80, 80)

nums = np.zeros(30)
cnt = 0
prev = 0

# ポイント(ピーナッツ, キャラメル, いちご)
point = np.zeros(3)
# 結果(0:ピーナッツ 1:キャラメル 2:いちご)
result = -1
pre_result = -1

# 判定画像読み込み
p_image = cv2.imread('./p.png')
c_image = cv2.imread('./c.png')
i_image = cv2.imread('./i.png')
cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE)

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FPS, 30)

if cap.isOpened() is False:
    print("can not open camera")
    sys.exit()

cv2.namedWindow("webcam", cv2.WINDOW_AUTOSIZE)

while True:
    ret, frame = cap.read()
    if ret is False:
        break

    #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255))
    #cv2.imshow("webcam", frame)
    dst_color = frame[y:y+h, x:x+w]
    dst_gray = cv2.cvtColor(dst_color, cv2.COLOR_BGR2GRAY)
    dst_canny = cv2.Canny(dst_gray, 100, 150)
 
    x2,y2,w2,h2 = cv2.boundingRect(dst_canny)
    dst = cv2.rectangle(dst_color, (x2, y2), (x2+w2, y2+h2), (0, 0, 255))
    if w2 > h2:
        num = w2
        num_min = h2
    else:
        num = h2
        num_min = w2
    diff = num - prev
    nums[cnt] = diff
    avg = np.average(nums)

    # 中心点
    mid_x = x2 + w2/2
    mid_y = y2 + h2/2
    
    #print("len : " + str(num) + " | len_min : " + str(num_min) +" | mid : (" + str(mid_x) + "," + str(mid_y) + ") | avg : " + str(avg))

    if num_min > 50 and mid_x > (w-w_thre)/2 and mid_x < (w+w_thre)/2 and mid_y > (h-h_thre)/2 and mid_y < (h+h_thre)/2 and avg > 0 and avg < 0.3:
        if dst[int(mid_x), int(mid_y)][2] > 150 and dst[int(mid_x), int(mid_y)][2]/dst[int(mid_x), int(mid_y)][0] > 1.0:
            print("いちご")
            point[2] += 1
            point[0] = 0
            point[1] = 0
        else:
            if num < 70:
                print("キャラメル")
                point[1] += 1
                point[0] = 0
                point[2] = 0
            else:
                print("ピーナッツ")
                point[0] += 1
                point[1] = 0
                point[2] = 0
        print("len : " + str(num) + " | len_min : " + str(num_min) +" | mid : (" + str(mid_x) + "," + str(mid_y) + ") | avg : " + str(avg))
        print(dst[int(mid_x), int(mid_y)])

    if point[0] > 3:
        #if (result != 0):
        #    result = 0
        print("これはピーナッツです")
        cv2.imshow("image", p_image)
        ser.write('1'.encode())
        point = np.zeros(3)
    elif point[1] > 3:
        #if (result != 1):
        #    result = 1
        print("これはキャラメルです")
        cv2.imshow("image", c_image)
        ser.write('2'.encode())
        point = np.zeros(3)
    elif point[2] > 3:
        #if (result != 2):
        #    result = 2
        print("これはいちごです")
        cv2.imshow("image", i_image)
        ser.write('3'.encode())
        point = np.zeros(3)

    prev = num
    cnt = (cnt+1)%30
    cv2.imshow("webcam", dst)
    if cv2.waitKey(30) == 27:
        break

time.sleep(1)
ser.close()
cap.release()
cv2.destroyAllWindows()
