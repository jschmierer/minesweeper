import random
import turtle

#initialize board with r rows and c columns
r = 20
c = 20
mode = "med"
if mode == "easy":
    mines = int(r * c * 0.15)
if mode == "med":
    mines = int(r * c * 0.18)
if mode == "hard":
    mines = int(r * c * 0.21)
print(mines)

#physical board creation
tilesize = 30
turtle.setup(r * tilesize, c * tilesize)
t = turtle.Turtle()
screen = turtle.Screen()
screen.bgcolor("#a2d149")
screen.tracer(0, 0)
t.penup()

t.color("#aad751")
t.shape("square")
t.shapesize(tilesize / 20, tilesize / 20)

startx = -c * tilesize / 2 + tilesize / 2
starty = r * tilesize / 2 - tilesize / 2
switch = True
y = starty
for i in range(r):
    t.goto(startx, y)
    for j in range(c):
        if switch:
            t.stamp()
        t.forward(tilesize)
        switch = not switch
    switch = not switch
    y -= tilesize
t.hideturtle()
screen.update()


# make the board!
def allNeighborCheck(l, i, j):
    neighbors = []
    if i - 1 >= 0 and j - 1 >= 0:
        neighbors.append(l[i - 1][j - 1])
    if i - 1 >= 0:
        neighbors.append(l[i - 1][j])
    if i - 1 >= 0 and j + 1 < len(l[0]):
        neighbors.append(l[i - 1][j + 1])
    if j - 1 >= 0:
        neighbors.append(l[i][j - 1])
    if j + 1 < len(l[0]):
        neighbors.append(l[i][j + 1])
    if i + 1 < len(l) and j - 1 >= 0:
        neighbors.append(l[i + 1][j - 1])
    if i + 1 < len(l):
        neighbors.append(l[i + 1][j])
    if i + 1 < len(l) and j + 1 < len(l[0]):
        neighbors.append(l[i + 1][j + 1])
    return neighbors

def makeBoard(blankx, blanky):
    board = []
    minecoords = []
    for x in range(mines):
        i = random.randint(0, r - 1)
        j = random.randint(0, c - 1)
        while (i, j) in minecoords or (i, j) == (blankx, blanky):
            i = random.randint(0, r - 1)
            j = random.randint(0, c - 1)
        minecoords.append((i, j))
        
    #make board with just mines and blanks
    for i in range(r):
        row = []
        for j in range(c):
            if (i, j) in minecoords:
                row.append("M")
            else:
                row.append("_")
        board.append(row)

 
        
    #load board with numbers
    for i in range(r):
        for j in range(c):
            surroundingmines = 0
            neighbors = allNeighborCheck(board, i, j)
            for el in neighbors:
                if el == "M":
                    surroundingmines += 1
            if board[i][j] == "_":
                if surroundingmines > 0:
                    board[i][j] = surroundingmines

for i in range(r):
    for j in range(c):
        print(board[i][j], end=" ")
    print()

#make game work
