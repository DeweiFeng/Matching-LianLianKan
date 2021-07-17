import cv2
import numpy as np
import win32gui
from PIL import ImageGrab
import time
import pyautogui

def get_window():
    window = None
    while not window:
        time.sleep(5)
        print("Start Finding Window")
        window = win32gui.FindWindow(None, "QQ游戏 - 连连看角色版")
        print("Window Not Found, waiting for 5 seconds to restart.")
    win32gui.SetForegroundWindow(window)
    (left, top, right, bottom) = win32gui.GetWindowRect(window)
    return (left, top, right, bottom)

def get_screenshot(pos):
    print("Getting screenshot")
    # (560, 220, 1360, 820)
    # (x=572, y=397, x=1159, y=783)
    # print(pos)
    left, top, right, bottom = pos
    screenshot = ImageGrab.grab(bbox = (left + 14, top + 181, left + 603, top + 566))
    # print((left + (right - left)/(67), top + (bottom - top)/3.37078652, right - (right - left) / 3.98, bottom - (bottom - top) / (16.216)))
    screenshot.save("screenshot.png")
    return cv2.imread("screenshot.png")

def process_screenshot(screenshot):
    # Horizontal: 19, Vertical: 11
    print("Processing Screenshot: Turning it into useful pixels")
    horizontal = 19
    vertical = 11
    all_square = []
    height, width, color = screenshot.shape 
    SQUARE_HEIGHT = round(height/11)
    SQUARE_WIDTH = round(width/19)
    for x in range(horizontal):
        for y in range(vertical):
            square = screenshot[y * SQUARE_HEIGHT : (y+1) * SQUARE_HEIGHT, x * SQUARE_WIDTH: (x+1) * SQUARE_WIDTH]
            all_square.append(square)
    SUB_LT_X = 8
    SUB_LT_Y = 8
    SUB_RB_X = 25
    SUB_RB_Y = 28
    new_all_square = []
    for square in all_square:
        s = square[SUB_LT_Y:SUB_RB_Y, SUB_LT_X:SUB_RB_X]
        # cv2.imwrite('color_img.jpg', s)
        # cv2.imshow('Color image', s)
        # cv2.waitKey(0)
        new_all_square.append(s)
    return new_all_square

def isImageExist(img,img_list):
    for existed_img in img_list:
        b = np.subtract(existed_img,img) # 图片数组进行比较，返回的是两个图片像素点差值的数组，
        if not np.any(b):   # 如果全部是0，说明两图片完全相同。
            return True
        else:
            continue
    return False

def getAllSquareTypes(all_square):
    print("Turning similar images into the same type")
    types = []
    # 先把空白添加到数组中，作为0号
    empty_img = cv2.imread('empty.png')
    empty_img = empty_img[8:28, 8:25]
    types.append(empty_img)
    for square in all_square:
        # If the image doesn't exist, store them in types
        if not isImageExist(square,types):
            types.append(square)
    return types

def findImage(img, types):
    for i in range(len(types)):
        b = np.subtract(types[i], img) # 图片数组进行比较，返回的是两个图片像素点差值的数组，
        if not np.any(b):   # 如果全部是0，说明两图片完全相同。
            return i

def pixelToImg(pixel, types):
    horizontal = 19
    vertical = 11
    res = [[''] * horizontal for _ in range(vertical)]
    counter = 0
    for col in range(len(res[0])):
        for row in range(len(res)):
            res[row][col] = findImage(pixel[counter], types)
            counter += 1
    return res

def windowToMatrix():
    pos = get_window()
    time.sleep(2)
    img = get_screenshot(pos)
    all_square = process_screenshot(img)
    types = getAllSquareTypes(all_square)
    array = pixelToImg(all_square, types)
    return (np.array(array), pos)

if __name__ == '__main__':
    # pos = get_window()
    # time.sleep(2)
    # img = get_screenshot(pos)
    # print(pyautogui.position())
    # all_square = process_screenshot(img)
    # all_square = process_screenshot(cv2.imread("screenshot.png"))
    # types = getAllSquareTypes(all_square)
    # print(pixelToImg(all_square, types))
    print(get_window())