import cv2
import numpy as np
import win32gui
from PIL import ImageGrab
import time
import pyautogui

# Trying to find the application window by searching for the name "QQ游戏 - 连连看角色版"
def get_window():
    window = None
    while not window:
        print("Start Finding Window")
        window = win32gui.FindWindow(None, "QQ游戏 - 连连看角色版")
        if not window:
            print("Window Not Found, waiting for 5 seconds to restart.")
            time.sleep(5)
    win32gui.SetForegroundWindow(window)
    (left, top, right, bottom) = win32gui.GetWindowRect(window)
    return (left, top, right, bottom)

# Getting a screenshot of the application with an offset
def get_screenshot(pos):
    """
    14, 181, 603, 566 are the offset of the actual working space. This can be adjusted if needed. For example,
    if we are using a different version or change the size of the window, we need to change it. The offset can be found
    using pyautogui.
    """
    print("Getting screenshot")
    left, top, right, bottom = pos
    screenshot = ImageGrab.grab(bbox = (left + 14, top + 181, left + 603, top + 566))
    # print((left + (right - left)/(67), top + (bottom - top)/3.37078652, right - (right - left) / 3.98, bottom - (bottom - top) / (16.216)))
    screenshot.save("screenshot.png")
    return cv2.imread("screenshot.png")

# Process the screenshot by dividing into boxes.
def process_screenshot(screenshot):
    # Horizontal: 19, Vertical: 11
    print("Processing Screenshot: Turning it into useful pixels")
    horizontal = 19
    vertical = 11
    all_square = []
    height, width, color = screenshot.shape 

    # Each row, we assume that we have 19 boxes and each column, we have 11.
    SQUARE_HEIGHT = round(height/11)
    SQUARE_WIDTH = round(width/19)
    for x in range(horizontal):
        for y in range(vertical):
            # Grouping pixels into images
            square = screenshot[y * SQUARE_HEIGHT : (y+1) * SQUARE_HEIGHT, x * SQUARE_WIDTH: (x+1) * SQUARE_WIDTH]
            all_square.append(square)

    # Cropping the image since the edge might include other boxes.
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

# Given an image and a list of image, check if the image is in the list.
def isImageExist(img,img_list):
    for existed_img in img_list:
        b = np.subtract(existed_img,img) # Comparing two images by subtracting them 
        if not np.any(b): # If all the pixels are 0, that means the two images are the same
            return True
        else:
            continue
    return False

# Given all images, find all different images and store them in a image library
def getAllSquareTypes(all_square):
    print("Turning similar images into the same type")
    types = []
    # Assuming the empty image is 0. This will be useful when writing the matching algorithm.
    empty_img = cv2.imread('empty.png')
    empty_img = empty_img[8:28, 8:25]
    types.append(empty_img)
    for square in all_square:
        # If the image doesn't exist, store them in types
        if not isImageExist(square,types):
            types.append(square)
    return types

# Given an image library and an image, find the index corresponding to the image.
def findImage(img, types):
    for i in range(len(types)):
        b = np.subtract(types[i], img) # Comparing two images by subtracting them 
        if not np.any(b): # If all the pixels are 0, that means the two images are the same
            return i

# Given an image library, represent each image by an index. 0 is empty image.
def pixelToMatrix(pixel, types):
    print("Turning screenshot to matrix")
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
    array = pixelToMatrix(all_square, types)
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
    
    all_square = process_screenshot(cv2.imread("testing_img/test5.png"))
    types = getAllSquareTypes(all_square)
    array = pixelToMatrix(all_square, types)
    print(array)