import cv2
import numpy as np
import math

def sins(a, b, c): 
    vect1 = [a[0] - b[0], a[1] - b[1]]
    vect2 = [c[0] - b[0], c[1] - b[1]]
    sin = abs(vect1[0] * vect2[0] + vect1[1] * vect2[1]) / math.sqrt(vect1[0] ** 2 + vect1[1] ** 2) / math.sqrt(vect2[0] ** 2 + vect2[1] ** 2)
    return abs(sin)

pic = np.array(cv2.imread('test.jpg'))
height = len(pic)
width = len(pic[0])

frame = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
ret, frame = cv2.threshold(frame, np.average(pic) + 50, 255, cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

mx = np.array([])
for i in contours:
    if len(i) > len(mx):
        mx = i

cont = []

n = len(mx)

for i in range(n):
    a, b = mx[i][0], mx[(i + 1) % n][0]
    if math.hypot(a[0] - b[0], a[1] - b[1]) > 1:
        cont.append([a])

cont = np.array(cont)

mx = cont
cont = []

n = len(mx)

for i in range(n):
    a, b, c = mx[i][0], mx[(i + 2) % n][0], mx[(i + 4) % n][0]
    if sins(a, b, c) < 0.8:
        cont.append([b])

cont = np.array(cont)

mx = cont
cont = []

n = len(mx)

for i in range(n):
    a, b = mx[i][0], mx[(i + 1) % n][0]
    if math.hypot(a[0] - b[0], a[1] - b[1]) > 20:
        cont.append([b])

cont = np.array(cont)
mx = cont

cont = []

n = len(mx)

for i in range(n):
    a, b, c = mx[i][0], mx[(i + 1) % n][0], mx[(i + 2) % n][0]
    if sins(a, b, c) < 0.8:
        cont.append([b])

cont = np.array(cont)
print(cont)

a3, a1, a2, a4 = cont[0][0], cont[1][0], cont[2][0], cont[3][0]
b, a = 1500, int(1500 * (math.hypot(a3[0] - a1[0], a3[1] - a1[1]) + math.hypot(a4[0] - a2[0], a4[1] - a2[1])) / (math.hypot(a2[0] - a1[0], a2[1] - a1[1]) + math.hypot(a3[0] - a4[0], a3[1] - a4[1])))
ans = np.zeros((a, b, 3))

for i in range(a):
    for j in range(b):
        x1, y1, x2, y2, x3, y3 = 0, 0, 0, 0, 0, 0
        x1 = (a1[0] * j + a2[0] * (b - j)) / b
        y1 = (a1[1] * j + a2[1] * (b - j)) / b
        x2 = (a3[0] * j + a4[0] * (b - j)) / b
        y2 = (a3[1] * j + a4[1] * (b - j)) / b
        x3 = (x1 * i + x2 * (a - i)) / a
        y3 = (y1 * i + y2 * (a - i)) / a
        ans[a - i - 1][j] = pic[int(y3)][int(x3)]

ans = np.array(ans) 

#вывод
cv2.imwrite('otput.png', ans)

#конец
cv2.waitKey(0)