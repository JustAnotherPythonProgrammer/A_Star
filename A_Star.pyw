import pygame
from pygame.locals import *
from sys import exit as sys_exit
from math import sqrt
from random import random
pygame.init()


WIDTH  = 700 + 1
HEIGHT = 500 + 1

BLOCKSIZE = 10

BOARDWIDTH  = WIDTH//BLOCKSIZE
BOARDHEIGHT = HEIGHT//BLOCKSIZE


display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A*    :P")




class Node:
    def __init__(self, row, col, type="SPOT"):
        self.row = row
        self.col = col
        self.type = "WALL" if random() < 0.4 else "SPOT"
        # self.type = "SPOT"
        self.g = 0
        self.h = 0
        self.f = 0
        self.parent = None



board = [[Node(j, i) for i in range(BOARDWIDTH)] for j in range(BOARDHEIGHT)]

START = board[ 0][ 0]
END   = board[-1][-1]
START.type = "START"
END.type = "TARGET"


GRAY   = (170, 170, 170)
BLACK  = (  0,   0,   0)
GREEN  = (  0, 255,   0)
RED    = (255,   0,   0)
BLUE   = (  0, 140, 255)
PURPLE = (255,   0, 255)
YELLOW = (255, 255,   0)




def drawGrid(width, height):

    for x in range(width + 1):
        pygame.draw.line(display, GRAY, (x * BLOCKSIZE, 0), (x * BLOCKSIZE, HEIGHT), 1)

    for y in range(height + 1):
        pygame.draw.line(display, GRAY, (0, y * BLOCKSIZE), (WIDTH, y * BLOCKSIZE), 1)


def drawBoard(board):
    for y, thing in enumerate(board):
        for x, spot in enumerate(thing):
            if spot.type == "START":
                pygame.draw.rect(display, RED, (x * BLOCKSIZE + 1, y * BLOCKSIZE + 1, BLOCKSIZE - 1, BLOCKSIZE - 1))
            elif spot.type == "TARGET":
                pygame.draw.rect(display, GREEN, (x * BLOCKSIZE + 1, y * BLOCKSIZE + 1, BLOCKSIZE - 1, BLOCKSIZE - 1))
            elif spot.type == "WALL":
                pygame.draw.rect(display, PURPLE, (x * BLOCKSIZE + 1, y * BLOCKSIZE + 1, BLOCKSIZE - 1, BLOCKSIZE - 1))


def drawPath(arr):
    pygame.draw.lines(display, BLUE, False, arr, 3)


def heuristic(p1, p2):
    x1, y1 = p1.row, p1.col
    x2, y2 = p2.row, p2.col
    return sqrt(((x2-x1)**2) + ((y2-y1)**2))


def leastF(arr):
    i = 0
    for index, node in enumerate(arr[1:], 1):
        if node.f < arr[i].f:
            i = index
    return i


def getNeighbors(node):
    arr = []
    for i in range(node.row - 1, node.row + 2):
        for j in range(node.col - 1, node.col + 2):
            if not (i == node.row and j == node.col):
                if (i >= 0 and i < BOARDHEIGHT and j >= 0 and j < BOARDWIDTH):
                    if not board[i][j].type == "WALL":
                        arr.append(board[i][j])
    return arr


def d(n1, n2):
    return sqrt(2) if n1.row != n2.row and n1.col != n2.col else 1


def aStar(start):


    def drawOpenList(arr):
        for n in openList:
            pygame.draw.rect(display, YELLOW, (n.col * BLOCKSIZE + 1, n.row * BLOCKSIZE + 1, BLOCKSIZE - 1, BLOCKSIZE - 1))

    openList = [start]
    closedList = []

    while openList:

        i = leastF(openList)
        current = openList[i]

        if current == END:
            return

        openList.pop(i)
        closedList.append(current)

        for n in getNeighbors(current):
            if not n in closedList:
                temp = current.g + d(current, n)

                improved = False
                if n in openList:
                    if temp < n.g:
                        n.g = temp
                        improved = True
                else:
                    n.g = temp
                    improved = True
                    openList.append(n)

                if improved:
                    n.h = heuristic(n, END)
                    n.f = n.g + n.h
                    n.parent = current

        drawGrid(BOARDWIDTH, BOARDHEIGHT)
        drawBoard(board)
        drawOpenList(openList)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys_exit()

        pygame.display.update()

    return "No path possible"


def getPath(node, arr=[]):
    if node.parent == None:
        return arr[::-1]
    arr.append([(node.col * BLOCKSIZE) + (BLOCKSIZE // 2), (node.row * BLOCKSIZE) + (BLOCKSIZE // 2)])
    return getPath(node.parent, arr)


def main():
    aStar(START)
    path = getPath(END)
    path.insert(0, [(START.col * BLOCKSIZE) + (BLOCKSIZE // 2), (START.row * BLOCKSIZE) + (BLOCKSIZE // 2)])

    while True:
        display.fill(BLACK)
        drawGrid(BOARDWIDTH, BOARDHEIGHT)
        drawBoard(board)
        drawPath(path)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys_exit()

        pygame.display.update()


if __name__ == "__main__":
    main()
