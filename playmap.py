#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from tkinter import *
import sys

CIRCLE_RADIUS = 12
CELL_WIDTH = 15
CELL_HEIGHT = 15
FILESAVE = "exo1.map"

def isInBoard(b, x, y):
    """Teste si une cellule est sur le plateau."""
    return not (x >= len(b[0]) or x < 0 or y >= len(b) or y < 0)


def getAdjacentCells(b, x, y):
    """Donne la liste des cellules voisines de la cellule "(x,y)"."""
    # on cree un vecteur qui determine les coordonnees des cellules voisines
    vector = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    adj = []
    cnt = 0
    # on l'applique a chaque cellule autour de la cible
    for v in vector:
        c = [x + v[0], y + v[1]]
        # si elle est comprise dans le plateau, on l'ajoute à la liste
        if isInBoard(b, c[0], c[1]) and b[c[1]][c[0]]:
            adj.append([c[0], c[1]])
            cnt += 1
    return cnt


def isInDict(x, y, dico):
    r = False
    for d in dico:
        r = (d[0] == x) and (d[1] == y)
        if r:
            break
    return r


def createBoard(h, w):
    global startState
    b = []
    for i in range(h):
        b.append([])
        for j in range(w):
            b[i].append(False)
    for v in startState:
        b[v[1]][v[0]] = True
    return b


def drawCell(cpyBoard, x, y, isStart):
    global board, cellW, cellH, grid, colorDying, colorBorn, colorEmpty, colorLiving, colorStart
    x1 = x * (cellW + 1) + 2
    y1 = y * (cellH + 1) + 2
    x2 = (x + 1) * (cellW + 1)
    y2 = (y + 1) * (cellH + 1)
    state = cpyBoard[y][x]
    if state:
        ct = getAdjacentCells(cpyBoard, x, y)
        if isStart:
            grid.create_rectangle(x1, y1, x2, y2, outline=colorStart, fill=colorStart)
        elif ct != 2 and ct != 3:
            board[y][x] = False
            grid.create_rectangle(x1, y1, x2, y2, outline=colorDying, fill=colorDying)
        else:
            grid.create_rectangle(x1, y1, x2, y2, outline=colorLiving, fill=colorLiving)
    else:
        if getAdjacentCells(cpyBoard, x, y) == 3 and not isStart:
            board[y][x] = True
            grid.create_rectangle(x1, y1, x2, y2, outline=colorBorn, fill=colorBorn)
        else:
            grid.create_rectangle(x1, y1, x2, y2, outline=colorDead, fill=colorDead)


def drawBoard(l):
    global board, width, height, grid, period, end, pause, generations, genAutoStop
    cpyBoard = []
    if not pause and not end and not (generations in genAutoStop):
        for y in range(height):
            cpyBoard.append([])
            for x in range(width):
                cpyBoard[y].append(board[y][x])
    #    if not ((generations - 1) in genAutoStop):
        generations += 1
        grid.delete(ALL)
        l.config(text="Generation : " + str(generations))
        for y in range(height):
            for x in range(width):
                drawCell(cpyBoard, x, y, False)
    grid.after(period, drawBoard, l)


def drawBoardStart():
    global grid, board, end, width, height
    cpyBoard = []
    for y in range(height):
        cpyBoard.append([])
        for x in range(width):
            cpyBoard[y].append(board[y][x])
    if not pause and not end:
        for y in range(height):
            for x in range(width):
                drawCell(cpyBoard, x, y, True)


def __action_p(e):
    global pause, generations, genAutoStop
    if generations in genAutoStop:
        generations += 1
    else:
        pause = not pause


def __action_q(e=None):
    global end, saveBoard, board
    if saveBoard:
        res = []
        for y in range(len(board)):
            for x in range(len(board[y])):
                if board[y][x]:
                    res.append([x, y])
        fd = open(FILESAVE, encoding="utf-8", mode="w")
        fd.write(str(res))
        fd.close()
    end = True
    root.destroy()


def __action_enter(e):
    global start, grid
    start = not start
    grid.unbind("<Button-1>")


def __action_echap(e):
    global root
    root.destroy()
    root = Tk()
    game()


def __action_clicGauche(clic):
    global cellW, cellH, board, grid, start, colorDead, colorStart
    x = clic.x // (cellW + 1)  # x et y contiennent les
    y = clic.y // (cellH + 1)  # coordonnées de la cellule
    if not isInBoard(board, x, y) or start:
        return
    board[y][x] = not board[y][x]
    x1 = x * (cellW + 1) + 2
    y1 = y * (cellH + 1) + 2
    x2 = (x + 1) * (cellW + 1)
    y2 = (y + 1) * (cellH + 1)
    if board[y][x]:
        grid.create_rectangle(x1, y1, x2, y2, outline=colorStart, fill=colorStart)
    else:
        grid.create_rectangle(x1, y1, x2, y2, outline=colorDead, fill=colorDead)


def getStartState(fd):
    if fd is None:
        return []
    f = open(fd, encoding='utf-8', mode='r')
    l = []
    s = f.read().replace(" ", "").replace("\n", "")
    f.close()
    length = len(s)
    i = 0
    tmp1 = 0
    tmp2 = 0
    tmp3 = 0
    while i < length:
        while i < length and not (s[i] in "0123456789"):
            i += 1
        tmp1 = i
        while i < length and s[i] in "0123456789":
            i += 1
        tmp2 = i
        while i < length and s[i] in ",. ;:-_\n":
            i += 1
        tmp3 = i
        while i < length and s[i] in "0123456789":
            i += 1
        if i < length:
            try:
                l.append([int(s[tmp1:tmp2]), int(s[tmp3:i])])
            except Exception:
                print("Invalid file : " + fd)
                return []
    return l


def getGens(l):
    i = 0
    tmp1 = 0
    res = []
    ll = len(l)
    while i < ll:
        while i < ll and not (l[i] in "0123456789"):
            i += 1
        tmp1 = i
        while i < ll and l[i] in "0123456789":
            i += 1
        try:
            res.append(int(l[tmp1:i]))
        except Exception:
            print("Invalid format string : " + l)
            return []
    return res

def game():
    global pause, start, replay, grid, board, end, cellH, cellW, width, bgColor, height, generations
    replay = False
    start = False
    pause = False
    generations = 0
    root.protocol("WM_DELETE_WINDOW", __action_q)
    root.title("Game of Life")
    root.resizable(width=False, height=False)
    l = Label(text="Generation : 0")
    l.pack()
    grid = Canvas(root, width=width * (cellW + 1) + 1, height=height * (cellH + 1) + 1, bg=bgColor)
    grid.pack()

    # les évènements à gérer
    root.bind("q", __action_q)
    root.bind("p", __action_p)
    root.bind("<Return>", __action_enter)
    root.bind("<Escape>", __action_echap)
    grid.bind("<Button-1>", __action_clicGauche)

    board = createBoard(height, width)
    drawBoardStart()
    while not start and not end:
        grid.update_idletasks()
        grid.update()
    drawBoard(l)
    grid.mainloop()

def getPath(arg):
    try:
        width = -1
        height = -1
        tab = []
        with open(arg, "r") as fd:
            s = f.read()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Donnez une map en argument")
    playmap = getPath(sys.argv[1])
    colorPath = '#11dd11'
    colorCircle = '#1111dd'
    colorObst = '#111111'
    board = []
    root = Tk()
    game()
