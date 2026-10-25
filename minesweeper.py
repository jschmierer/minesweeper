
import random
import turtle
import time

# customizable options!
MODE = "easy"
TILESIZE = 40
LIVES = 2

# other setup
lives = LIVES
lost = False
won = False
flagcount = 0
start_time = None
elapsed_time = 0
timer_generation = 0

#initialize board with r rows and c columns
if MODE == "super easy":
    r = 5
    c = 5
    mines = 5
elif MODE == "easy":
    r = 10
    c = 10
    mines = 20
elif MODE == "med":
    r = 15
    c = 15
    mines = 45
else:
    r = 20
    c = 20
    mines = 100

#turtle setup
# Very narrow boards need a taller HUD so the labels do not overlap.
HUD_ROWS = 5 if c * TILESIZE < 600 else 2
WINDOW_WIDTH = c * TILESIZE
WINDOW_HEIGHT = (r + HUD_ROWS) * TILESIZE

turtle.setup(WINDOW_WIDTH, WINDOW_HEIGHT)
screen = turtle.Screen()
screen.setworldcoordinates(0, WINDOW_HEIGHT, WINDOW_WIDTH, 0)
screen.tracer(0, 0)

t = turtle.Turtle()
t.penup()
t.shapesize(TILESIZE / 20)
t.hideturtle()

#on screen board creation
def drawBevelSquare(TILESIZE, t):
  squarescale = 20 / 28
  half = TILESIZE / 2
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
bg.penup()
bg.goto(c * TILESIZE / 2, (HUD_ROWS + r / 2) * TILESIZE)
drawBevelSquare(TILESIZE * 20 + 10, bg)

tilet = turtle.Turtle()
tilet.penup()
tilet.hideturtle()
tilet.goto(TILESIZE / 2, TILESIZE * (HUD_ROWS + 0.5))
for i in range(r):
  for j in range(c):
    drawBevelSquare(TILESIZE, tilet)
    tilet.goto(tilet.xcor() + TILESIZE, tilet.ycor())
  tilet.goto(TILESIZE / 2, tilet.ycor() + TILESIZE)

screen.update()

# HUD
hud = turtle.Turtle()
hud.hideturtle()
hud.penup()
hud.speed(0)

def formatTime(seconds):
    minutes = int(seconds) // 60
    seconds = int(seconds) % 60
    return f"{minutes:02}:{seconds:02}"

def getElapsedTime():
    if start_time is None:
        return elapsed_time
    if lost or won:
        return elapsed_time
    return int(time.monotonic() - start_time)

def drawHUD():
    hud.clear()
    hud.color("black")

    # Scale the text with the tiles, while keeping it readable.
    font_size = max(7, min(13, int(TILESIZE * 0.32)))
    font = ("Arial", font_size, "bold")

    if HUD_ROWS == 5:
        # On narrow boards, use separate lines to avoid overlapping labels.
        hud.goto(10, TILESIZE * 0.5)
        hud.write(f"Mines: {mines}", align="left", font=font)

        hud.goto(10, TILESIZE * 1.5)
        hud.write(f"Flags: {flagcount}", align="left", font=font)

        hud.goto(c * TILESIZE / 2, TILESIZE * 2.5)
        hud.color("blue")
        hud.write("Click to reset", align="center", font=font)

        hud.goto(10, TILESIZE * 3.5)
        hud.color("black")
        hud.write(f"Time: {formatTime(getElapsedTime())}",
                  align="left", font=font)

        hud.goto(10, TILESIZE * 4.5)
        hud.write(f"Lives left: {lives}", align="left", font=font)
    else:
        # Two-row HUD for wider boards.
        hud.goto(10, TILESIZE * 0.5)
        hud.write(f"Mines: {mines}", align="left", font=font)

        hud.goto(10, TILESIZE * 1.5)
        hud.write(f"Flags: {flagcount}", align="left", font=font)

        hud.goto(c * TILESIZE / 2, TILESIZE * 0.5)
        hud.color("blue")
        hud.write("Click to reset", align="center", font=font)

        hud.goto(c * TILESIZE - 10, TILESIZE * 0.5)
        hud.color("black")
        hud.write(f"Time: {formatTime(getElapsedTime())}",
                  align="right", font=font)

        hud.goto(c * TILESIZE - 10, TILESIZE * 1.5)
        hud.write(f"Lives left: {lives}", align="right", font=font)

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
    i = int(y / TILESIZE) - HUD_ROWS
    j = int(x / TILESIZE)
    return (i, j)

flags = []

def drawFlag(x, y):
    global flagcount

    if lost or won:
        return

    if y < HUD_ROWS * TILESIZE:
        return

    spot = findTileFromPos(x, y)

    if not (0 <= spot[0] < r and 0 <= spot[1] < c):
        return

    tilex = spot[1] * TILESIZE + TILESIZE / 2
    tiley = (spot[0] + HUD_ROWS) * TILESIZE + TILESIZE / 2

    if spot in revealed:
        return

    if spot in flags:
        t.goto(tilex, tiley)
        t.shapesize(TILESIZE / 35)
        t.shape("square")
        t.color("#bdbdbd")
        t.stamp()
        t.shapesize(TILESIZE / 20)
        flags.remove(spot)
        flagcount -= 1
    else:
        t.setheading(0)
        t.goto(tilex, tiley)
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
        flagcount += 1

    drawHUD()

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
    t.shapesize(TILESIZE / 21)
    t.color("#7b7b7b", "#bdbdbd")
    x = j * TILESIZE + TILESIZE / 2
    y = (i + HUD_ROWS) * TILESIZE + TILESIZE / 2
    t.goto(x, y)
    t.stamp()
    t.shapesize(TILESIZE / 20)
    tile = board[i][j]
    if tile == "_":
        revealNeighboringBlanks(i, j)
    else:
        writeTileValue(i, j)
    screen.update()

# game messages
message = turtle.Turtle()
message.hideturtle()
message.penup()

# making board and clicking logic
board = None

def checkWin():
    global won, elapsed_time

    if board is None or lost or won:
        return

    safe_tiles = r * c - mines
    if sum(1 for i, j in revealed if board[i][j] != "M") == safe_tiles:
        won = True
        elapsed_time = getElapsedTime()
        message.clear()
        message.goto(c * TILESIZE / 2, (HUD_ROWS + r / 2) * TILESIZE)
        message.color("green")
        message.write(
            f"You Won! :D\nTime: {formatTime(elapsed_time)}",
            align="center",
            font=("Arial", max(12, min(30, int(TILESIZE * 0.75))), "bold")
        )
        drawHUD()

def updateTimer(generation):
    global elapsed_time

    if generation != timer_generation:
        return

    if start_time is not None and not lost and not won:
        elapsed_time = int(time.monotonic() - start_time)
        drawHUD()
        screen.ontimer(lambda: updateTimer(generation), 1000)

def resetGame():
    global board, lives, lost, won, flags, revealed
    global flagcount, start_time, elapsed_time, timer_generation

    timer_generation += 1

    t.clear()
    tilet.clear()
    bg.clear()
    message.clear()

    flags = []
    revealed = []
    board = None
    lives = LIVES
    lost = False
    won = False
    flagcount = 0
    start_time = None
    elapsed_time = 0

    # Redraw the background and tiles
    bg.penup()
    bg.goto(c * TILESIZE / 2, (HUD_ROWS + r / 2) * TILESIZE)
    drawBevelSquare(TILESIZE * 20 + 10, bg)

    tilet.penup()
    tilet.goto(TILESIZE / 2, TILESIZE * (HUD_ROWS + 0.5))
    for i in range(r):
        for j in range(c):
            drawBevelSquare(TILESIZE, tilet)
            tilet.goto(tilet.xcor() + TILESIZE, tilet.ycor())
        tilet.goto(TILESIZE / 2, tilet.ycor() + TILESIZE)

    drawHUD()
    screen.update()

def onClick(x, y):
    global board, lives, lost, won, start_time, elapsed_time

    # Clicking the top row resets the game
    if y < HUD_ROWS * TILESIZE:
        resetGame()
        return

    if lost or won:
        return

    tilei, tilej = findTileFromPos(x, y)

    if not (0 <= tilei < r and 0 <= tilej < c):
        return

    if board is None:
        board = makeBoard(tilei, tilej)
        for i in range(r):
            for j in range(c):
                print(board[i][j], end=" ")
            print()

    if (tilei, tilej) in flags or (tilei, tilej) in revealed:
        return

    if start_time is None:
        start_time = time.monotonic()
        generation = timer_generation
        screen.ontimer(lambda: updateTimer(generation), 1000)

    if board[tilei][tilej] == "M":
        lives -= 1

    revealTile(tilei, tilej)

    if lives == 0:
        lost = True
        elapsed_time = getElapsedTime()
        message.goto(c * TILESIZE / 2, (HUD_ROWS + r / 2) * TILESIZE)
        message.color("red")
        message.write("You Died! :(", align="center",
                      font=("Arial", max(12, min(36, int(TILESIZE * 0.9))), "bold"))
        drawHUD()
        screen.ontimer(resetGame, 3000)
        return

    checkWin()
    drawHUD()

screen.onscreenclick(onClick)

drawHUD()
screen.mainloop()
