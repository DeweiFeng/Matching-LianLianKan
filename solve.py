from collections import defaultdict
from itertools import combinations
import numpy as np
columns = 19
rows = 11

# Check if the given matrix is a valid matrix by checking if everything is in pair
def checkValid(matrix):
    valid = defaultdict(int)
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 0:
                continue
            else:
                valid[matrix[i][j]] += 1
    
    for key in valid:
        if valid[key] % 2 != 0:
            return False
    return True

# Creating a dictionary for each image. The key is a list of coordinates corresponding to that image.
def create_dictionary(matrix):
    points = defaultdict(set)
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            if matrix[x][y] != 0:
                points[matrix[x][y]].add((x, y))
    return points

# Checking if two points are connected in a matrix
def checkConnection(matrix, pt1, pt2):
    y1, x1 = pt1
    y2, x2 = pt2
    # check veritical
    if y1 == y2:
        small_x = min(x1, x2)
        big_x = max(x1, x2)
        temp = matrix[y1: y1 + 1,small_x: big_x + 1]
        if np.all(temp == 0):
            return True
    else:
        small_y = min(y1, y2) + 1
        big_y = max(y1, y2) - 1
        for col in range(columns):
            temp = matrix[small_y:big_y + 1, col:col+1]
            # Find a column where everything in that column is 0
            if temp.size == 0 or np.all(temp == 0):
                # Check if the row from the current column to the points are 0
                if x1 < col:
                    temp1 = matrix[y1: y1+1, x1+1: col+1]
                elif x1 == col:
                    temp1 = np.array([0])
                else:
                    temp1 = matrix[y1: y1+1, col: x1]
                if x2 < col:
                    temp2 = matrix[y2: y2+1, x2+1: col+1]
                elif x2 == col:
                    temp2 = np.array([0])
                else:
                    temp2 = matrix[y2: y2+1, col: x2]
                if np.all(temp1 == 0) and np.all(temp2 == 0):
                    return True

            # if temp.size == 0:
            #     if x1 < col:
            #         temp1 = matrix[y1: y1+1, x1+1: col+1]
            #     elif x1 == col:
            #         temp1 = np.array([0])
            #     else:
            #         temp1 = matrix[y1: y1+1, col: x1]
            #     if x2 < col:
            #         temp2 = matrix[y2: y2+1, x2+1: col+1]
            #     elif x2 == col:
            #         temp2 = np.array([0])
            #     else:
            #         temp2 = matrix[y2: y2+1, col: x2]
            #     if np.all(temp1 == 0) and np.all(temp2 == 0):
            #         return True
            # elif np.all(temp == 0):
            #     if x1 < col:
            #         temp1 = matrix[y1: y1+1, x1+1: col+1]
            #     elif x1 == col:
            #         temp1 = np.array([0])
            #     else:
            #         temp1 = matrix[y1: y1+1, col: x1]
            #     if x2 < col:
            #         temp2 = matrix[y2: y2+1, x2+1: col+1]
            #     elif x2 == col:
            #         temp2 = np.array([0])
            #     else:
            #         temp2 = matrix[y2: y2+1, col: x2]
            #     if np.all(temp1 == 0) and np.all(temp2 == 0):
            #         return True

    # check horizontal
    if x1 == x2:
        small_y = min(y1, y2)
        big_y = max(y1, y2)
        temp = matrix[small_y: big_y + 1,x1: x1 + 1]
        if np.all(temp == 0):
            return True
    else:
        small_x = min(x1, x2) + 1
        big_x = max(x1, x2) - 1
        for row in range(rows):
            temp = matrix[row:row+1, small_x:big_x + 1]
            # Find a row where everything is 0
            if temp.size == 0 or np.all(temp == 0):
                # Check if the column from the current row to the points are 0
                if y1 < row:
                    temp1 = matrix[y1+1: row+1, x1: x1+1]
                elif y1 == row:
                    temp1 = np.array([0])
                else:
                    temp1 = matrix[row: y1, x1: x1+1]
                if y2 < row:
                    temp2 = matrix[y2+1: row+1, x2: x2+1]
                elif y2 == row:
                    temp2 = np.array([0])
                else:
                    temp2 = matrix[row: y2, x2: x2+1]
                if np.all(temp1 == 0) and np.all(temp2 == 0):
                    return True
            # if temp.size == 0:
            #     if y1 < row:
            #         temp1 = matrix[y1+1: row+1, x1: x1+1]
            #     elif y1 == row:
            #         temp1 = np.array([0])
            #     else:
            #         temp1 = matrix[row: y1, x1: x1+1]
            #     if y2 < row:
            #         temp2 = matrix[y2+1: row+1, x2: x2+1]
            #     elif y2 == row:
            #         temp2 = np.array([0])
            #     else:
            #         temp2 = matrix[row: y2, x2: x2+1]
            #     if np.all(temp1 == 0) and np.all(temp2 == 0):
            #         return True
            # elif np.all(temp == 0):
            #     if y1 < row:
            #         temp1 = matrix[y1+1: row+1, x1: x1+1]
            #     elif y1 == row:
            #         temp1 = np.array([0])
            #     else:
            #         temp1 = matrix[row: y1, x1: x1+1]
            #     if y2 < row:
            #         temp2 = matrix[y2+1: row+1, x2: x2+1]
            #     elif y2 == row:
            #         temp2 = np.array([0])
            #     else:
            #         temp2 = matrix[row: y2, x2: x2+1]
            #     if np.all(temp1 == 0) and np.all(temp2 == 0):
            #         return True
    return False

# Find a working order for the matrix
def solution(matrix, points):
    order = []
    while points:
        keysToRemove = []
        for key in points:

            comb = combinations(points[key], 2)
            used = set()
            for pt1, pt2 in comb:
                if pt1 in used or pt2 in used:
                    continue
                if checkConnection(matrix, pt1, pt2):
                    # Adding to used to make sure not using two keys at the same time
                    used.add(pt1)
                    used.add(pt2)
                    # Changing the used cells to 0
                    matrix[pt1[0]][pt1[1]] = 0
                    matrix[pt2[0]][pt2[1]] = 0
                    order.append(pt1)
                    order.append(pt2)
                    points[key].remove(pt1)
                    points[key].remove(pt2)
            if not points[key]:
                keysToRemove.append(key)
        for key in keysToRemove:
            del points[key]
        

    return order
            
def solve(matrix):
    if not checkValid(matrix):
        print("This is not a valid matrix.")
        return
    points = create_dictionary(matrix)
    print("Creating the order")
    order = solution(matrix, points)
    return order
                
if __name__ == '__main__':
    # matrix = np.array([[1, 2, 3, 4, 5, 6, 7, 0, 0, 0, 0, 0, 7, 6, 5, 4, 3, 2, 1], 
    #                 [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], 
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    #                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

    matrix1 = np.array([[1,     8,  16, 23, 14, 22, 11, 9,  36, 22, 0,  40, 38, 34, 13, 32, 41, 9,  33], 
                        [0,     9,  17, 1,  26, 29, 19, 0,  0,  0,  0,  39, 20, 35, 23, 10, 39, 4,  0], 
                        [0,     0,  12, 24, 27, 18, 0,  0,  0,  0,  0,  0,  2,  26, 20, 8,  32, 0,  0], 
                        [2,     0,  0,  1,  14, 23, 0,  0,  17, 0,  26, 0,  38, 29, 17, 13, 0,  0,  10], 
                        [3,     10, 0,  0,  23, 30, 0,  0,  0,  0,  0,  0,  1,  12, 29, 0,  0,  7,  27], 
                        [4,     9,  18, 0,  0,  24, 0,  15, 0,  0,  0,  0,  0,  41, 0,  0,  35, 20, 40], 
                        [5,     11, 10, 13, 0,  0,  34, 35, 0,  0,  18, 0,  8,  0,  0,  14, 21, 41, 12], 
                        [6,     12, 19, 25, 8,  0,  0,  30, 37, 39, 11, 31, 0,  0,  28, 6,  22, 30, 15], 
                        [7,     13, 20, 5,  28, 21, 0,  0,  0,  0,  0,  0,  0,  7,  25, 27, 34, 33, 34], 
                        [4,     14, 21, 19, 17, 0,  0,  0,  0,  0,  0,  0,  27, 30, 11, 37, 28, 29, 19], 
                        [7,     15, 22, 3,  28, 15, 4,  18, 0,  0,  0,  36, 21, 41, 35, 26, 39, 16, 31]])

    
    # print(checkConnection(matrix, (0, 1), (0, 17)))
    print(solve(matrix1))