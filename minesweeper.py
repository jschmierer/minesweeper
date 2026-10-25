
import random
import turtle

mode = "med"
tilesize = 40
lives = 2
game_over = False

#initialize board with r rows and c columns
if mode == "easy":
    r = 10
    c = 10
    mines = 20
elif mode == "med":
    r = 15
    c = 15
    mines = 45
else:
    r = 20
    c = 20
    mines = 100

#turtle setup
turtle.setup(c * tilesize, r * tilesize)
turtle.setworldcoordinates(0, r * tilesize, c * tilesize, 0)
t = turtle.Turtle()
screen = turtle.Screen()
screen.tracer(0, 0)
t.penup()
t.shapesize(tilesize / 20)
t.hideturtle()

#on screen board creation
def drawBevelSquare(tilesize, t):
  squarescale = 20 / 28
  half = tilesize / 2
  x = t.xcor()
  y = t.ycor()
  t.color("#ffffff")
  t.goto(x - half, y + half)
  t.begin_fill()
  t.goto(x - half, y - half)
  t.goto(x + half, y - half)
  t.goto(x - half, y + half)
  t.end_fill()
  t.color("#7b7b7b")
  t.begin_fill()
  t.goto(x + half, y + half)
  t.goto(x + half, y - half)
  t.goto(x - half, y + half)
  t.end_fill()
  leg = half * squarescale
  t.color("#bdbdbd")
  t.begin_fill()
  t.goto(x - leg, y + leg)
  t.goto(x + leg, y + leg)
  t.goto(x + leg, y - leg)
  t.goto(x - leg, y - leg)
  t.goto(x - leg, y + leg)
  t.end_fill()
  t.goto(x, y)

bg = turtle.Turtle()
bg.hideturtle()
bg.goto(c * tilesize / 2, r * tilesize / 2)
bg.penup()
drawBevelSquare(tilesize * 20 + 10, bg)

tilet = turtle.Turtle()
tilet.penup()
tilet.hideturtle()
tilet.goto(tilesize / 2, tilet.ycor() + tilesize / 2)
for i in range(r):
  for j in range(c):
    drawBevelSquare(tilesize, tilet)
    tilet.goto(tilet.xcor() + tilesize, tilet.ycor())
  tilet.goto(tilesize / 2, tilet.ycor() + tilesize)

screen.update()

# make the board logic
def allNeighborCheck(l, i, j):
    neighbors = []
    if i - 1 >= 0 and j - 1 >= 0:
        neighbors.append(l[i - 1][j - 1])
    if i - 1 >= 0:
        neighbors.append(l[i - 1][j])
    if i - 1 >= 0 and j + 1 < c:
        neighbors.append(l[i - 1][j + 1])
    if j - 1 >= 0:
        neighbors.append(l[i][j - 1])
    if j + 1 < c:
        neighbors.append(l[i][j + 1])
    if i + 1 < r and j - 1 >= 0:
        neighbors.append(l[i + 1][j - 1])
    if i + 1 < r:
        neighbors.append(l[i + 1][j])
    if i + 1 < r and j + 1 < c:
        neighbors.append(l[i + 1][j + 1])
    return neighbors

# parameters to ensure the passed in tile is blank
def makeBoard(blanki, blankj):
    board = []
    minecoords = []
    while len(minecoords) < mines:
        i = random.randint(0, r - 1)
        j = random.randint(0, c - 1)
        while (i, j) in minecoords or (abs(i - blanki) <= 1 and abs(j - blankj) <= 1):
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

    return board

# flag:
flagbottomshapecoords = ((-4, -5), (-4, -3), (-2, -3), (-2, -2), (0, -2), (0, 0),
                      (1, 0), (1, -3), (2, -2), (2, -3), (4, -3), (4, -5),
                      (-4, -5))
flagtopshapecoords = ((1, 0), (-1, 0), (-1, 1), (-3, 1), (-3, 2), (-4, 2),
                         (-4, 3), (-3, 3), (-3, 4), (-1, 4), (-1, 5), (1, 5),
                         (1, 0))
screen.register_shape("flagbottom", flagbottomshapecoords)
screen.register_shape("flagtop", flagtopshapecoords)

def findTileFromPos(x, y):
    i = int(y / tilesize)
    j = int(x / tilesize)
    return (i, j)

flags = []
def drawFlag(x, y):
    if game_over:
        return
    spot = findTileFromPos(x, y)
    y = spot[0] * tilesize + tilesize / 2
    x = spot[1] * tilesize + tilesize / 2
    if spot in revealed:
        return
    if spot in flags:
        t.goto(x, y)
        t.shapesize(tilesize / 35)
        t.shape("square")
        t.color("#bdbdbd")
        t.stamp()
        t.shapesize(tilesize / 20)
        flags.remove(spot)
    else:
        t.setheading(0)
        t.goto(x, y)
        t.color("black")
        t.right(90)
        t.shape("flagbottom")
        t.stamp()
        t.setheading(0)
        t.color("red")
        t.shape("flagtop")
        t.right(90)
        t.stamp()
        flags.append(spot)
        screen.update()

screen.onclick(drawFlag, btn=3)

# drawing numbers
tile1coords = ((-3.5, -5), (-3.5, -3), (-1.5, -3), (-1.5, 1), (-3.5, 1), (-3.5, 2), (-2.5, 2), (-2.5, 3), (-1.5, 3), (-1.5, 4), (-0.5, 4), (-0.5, 5), (1.5, 5), (1.5, -3), (3.5, -3), (3.5, -5), (-3.5, -5))
screen.register_shape("1", tile1coords)
tile2coords = ((-5, -5), (-5, -2), (-4, -2), (-4, -1), (-2, -1), (-2, 0), (0, 0), (0, 1), (2, 1), (2, 3), (-2, 3), (-2, 2), (-5, 2), (-5, 4), (-4, 4), (-4, 5), (4, 5), (4, 4), (5, 4), (5, 1), (4, 1), (4, 0), (3, 0), (3, -1), (1, -1), (1, -2), (-1, -2), (-1, -3), (5, -3), (5, -5), (-5, -5))
screen.register_shape("2", tile2coords)
tile3coords = ((-5, -5), (-5, -3), (2, -3), (2, -1), (-2, -1), (-2, 1), (2, 1), (2, 3), (-5, 3), (-5, 5), (4, 5), (4, 4), (5, 4), (5, 1), (4, 1), (4, -1), (5, -1), (5, -4), (4, -4), (4, -5), (-5, -5))
screen.register_shape("3", tile3coords)
tile4coords = ((1, -5), (1, -1), (-5, -1), (-5, 1), (-4, 1), (-4, 3), (-3, 3), (-3, 5), (0, 5), (0, 3), (-1, 3), (-1, 1), (1, 1), (1, 5), (4, 5), (4, 1), (5, 1), (5, -1), (4, -1), (4, -5), (1, -5))
screen.register_shape("4", tile4coords)
tile5coords = ((-5, -5), (-5, -3), (2, -3), (2, -1), (-5, -1), (-5, 5), (5, 5), (5, 3), (-2, 3), (-2, 1), (4, 1), (4, 0), (5, 0), (5, -4), (4, -4), (4, -5), (-5, -5))
screen.register_shape("5", tile5coords)
tile6coords = ((-4, -5), (-4, -4), (-5, -4), (-5, 4), (-4, 4), (-4, 5), (4, 5), (4, 3), (-2, 3), (-2, 1), (4, 1), (4, 0), (5, 0), (5, -4), (4, -4), (4, -5), (-4, -5))
screen.register_shape("6", tile6coords)
tile6holecoords = ((-2, -3), (-2, -1), (2, -1), (2, -3), (-2, -3))
screen.register_shape("6hole", tile6holecoords)

mine1coords = ((-4.5, -4.5), (-4.5, -3.5), (-3.5, -3.5), (-3.5, -2.5), (-4.5, -2.5), (-4.5, -0.5), (-6.5, -0.5), (-6.5, 0.5), (-4.5, 0.5), (-4.5, 2.5), (-3.5, 2.5), (-3.5, 3.5), (-4.5, 3.5), (-4.5, 4.5), (-3.5, 4.5), (-3.5, 3.5), (-2.5, 3.5), (-2.5, 4.5), (-0.5, 4.5), (-0.5, 6.5), (0.5, 6.5), (0.5, 4.5), (2.5, 4.5), (2.5, 3.5), (3.5, 3.5), (3.5, 4.5), (4.5, 4.5), (4.5, 3.5), (3.5, 3.5), (3.5, 2.5), (4.5, 2.5), (4.5, 0.5), (6.5, 0.5), (6.5, -0.5), (4.5, -0.5), (4.5, -2.5), (3.5, -2.5), (3.5, -3.5), (4.5, -3.5), (4.5, -4.5), (3.5, -4.5), (3.5, -3.5), (2.5, -3.5), (2.5, -4.5), (0.5, -4.5), (0.5, -6.5), (-0.5, -6.5), (-0.5, -4.5), (-2.5, -4.5), (-2.5, -3.5), (-3.5, -3.5), (-3.5, -4.5), (-4.5, -4.5))
screen.register_shape("mine1", mine1coords)
mine2coords = ((-2.5, 0.5), (-2.5, 2.5), (-0.5, 2.5), (-0.5, 0.5), (-2.5, 0.5))
screen.register_shape("mine2", mine2coords)

def drawMine():
    t.color("black")
    t.shape("mine1")
    t.stamp()
    t.color("white")
    t.shape("mine2")
    t.stamp()

def drawSix():
    t.shape("6")
    t.color("#008080")
    t.stamp()
    t.shape("6hole")
    t.color("#bdbdbd")
    t.stamp()

def writeTileValue(i, j):
    tile = board[i][j]
    t.setheading(-90)
    if tile == "M":
        drawMine()
    elif tile <= 6: # eventually remove conditional when all shapes set
        t.shape(str(tile))
        if tile == 1:
            t.color("#0101ff")
        elif tile == 2:
            t.color("#008301")
        elif tile == 3:
            t.color("#fe0300")
        elif tile == 4:
            t.color("#01037f")
        elif tile == 5:
            t.color("#810101")
        elif tile == 6:
            drawSix()
        elif tile == 7:
            t.color("#000000")
        elif tile == 8:
            t.color("#808080")
        t.stamp()
    screen.update()

# reveal tile logic
def revealNeighboringBlanks(i, j):
    if i - 1 >= 0 and j - 1 >= 0:
        revealTile(i - 1, j - 1)
    if i - 1 >= 0:
        revealTile(i - 1, j)
    if i - 1 >= 0 and j + 1 < c:
        revealTile(i - 1, j + 1)
    if j - 1 >= 0:
        revealTile(i, j - 1)
    if j + 1 < c:
        revealTile(i, j + 1)
    if i + 1 < r and j - 1 >= 0:
        revealTile(i + 1, j - 1)
    if i + 1 < r:
        revealTile(i + 1, j)
    if i + 1 < r and j + 1 < c:
        revealTile(i + 1, j + 1)

revealed = []
def revealTile(i, j):
    if (i, j) in flags or (i, j) in revealed:
        return
    revealed.append((i, j))
    t.setheading(0)
    t.shape("square")
    t.shapesize(tilesize / 21)
    t.color("#7b7b7b", "#bdbdbd")
    x = j * tilesize + tilesize / 2
    y = i * tilesize + tilesize / 2
    t.goto(x, y)
    t.stamp()
    t.shapesize(tilesize / 20)
    tile = board[i][j]
    if tile == "_":
        revealNeighboringBlanks(i, j)
    else:
        writeTileValue(i, j)
    screen.update()

# making board and clicking logic
board = None

# Death message
deathtext = turtle.Turtle()
deathtext.hideturtle()
deathtext.penup()
deathtext.color("red")

def resetGame():
    global board, lives, game_over, flags, revealed

    t.clear()
    tilet.clear()
    bg.clear()
    deathtext.clear()

    flags = []
    revealed = []
    board = None
    lives = 1
    game_over = False

    # Redraw the background and tiles
    bg.penup()
    bg.goto(c * tilesize / 2, r * tilesize / 2)
    drawBevelSquare(tilesize * 20 + 10, bg)

    tilet.penup()
    tilet.goto(tilesize / 2, tilesize / 2)
    for i in range(r):
        for j in range(c):
            drawBevelSquare(tilesize, tilet)
            tilet.goto(tilet.xcor() + tilesize, tilet.ycor())
        tilet.goto(tilesize / 2, tilet.ycor() + tilesize)

    screen.update()

def onClick(x, y):
    global board, lives, game_over

    if game_over:
        return

    tilei, tilej = findTileFromPos(x, y)

    if not (0 <= tilei < r and 0 <= tilej < c):
        return

    if board == None:
        board = makeBoard(tilei, tilej)
        for i in range(r):
            for j in range(c):
                print(board[i][j], end=" ")
            print()

    if (tilei, tilej) in flags or (tilei, tilej) in revealed:
        return

    if board[tilei][tilej] == "M":
        lives -= 1

    revealTile(tilei, tilej)

    if lives == 0:
        game_over = True
        deathtext.goto(c * tilesize / 2, r * tilesize / 2)
        deathtext.write("You Died! :(", align="center",
                        font=("Arial", 36, "bold"))
        screen.update()
        screen.ontimer(resetGame, 3000)

screen.onscreenclick(onClick)

screen.mainloop()
