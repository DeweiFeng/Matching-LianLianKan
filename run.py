import windowToMatrix
import solve
import pyautogui

def pressBySolving(order, left, top):   
    # Box Width = 31, Height = 35
    # Box Center = 15.5, 17.5
    fbox = (left + 15.5 + 14, top + 17.5 + 181)
    for (row, col) in order:
        # Clicking each box in order
        pyautogui.click(x=fbox[0] + 31 * col, y=fbox[1] + 35 * row, interval=0.01)

def run():
    matrix, pos = windowToMatrix.windowToMatrix()
    order = solve.solve(matrix)
    pressBySolving(order, pos[0], pos[1])

if __name__ == '__main__':
    run()