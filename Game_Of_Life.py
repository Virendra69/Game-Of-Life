import cv2
import numpy as np

frame = np.ones((360, 360))

# Getting the grid dimnesions
grid_dim = int(input("Enter the value: "))

# Creating the grid for the display
coordinates = []
for i in range(0, 360, 360//grid_dim):
    coord_n = []
    for j in range(0, 360, 360//grid_dim):
        coord_n.append(((j, i), (j + 360//grid_dim, i + 360//grid_dim)))
    coordinates.append(tuple(coord_n))
coordinates = tuple(coordinates)

# Creating the grid for generations
grid1 = []
grid2 = []
for i in range(grid_dim):
    grid1_temp = []
    grid2_temp = []
    for j in range(grid_dim):
        grid1_temp.append(1)
        grid2_temp.append(1)
    grid1.append(grid1_temp)
    grid2.append(grid2_temp)

# function to get the coordinates of different types
def getTypeCoordinates(type):
    type_coord = []

    if type == "blinker":
        type_coord = ((1, 2), (2, 2), (3, 2))
    elif type == "toad":
        type_coord = ((2, 2), (2, 3), (2, 4), (3, 1), (3, 2), (3, 3))
    elif type == "beacon":
        type_coord = ((1, 1), (1, 2), (2, 1), (2, 2), (3, 3), (3, 4), (4, 3), (4, 4))
    elif type == "glider":
        type_coord = ((1, 2), (2, 3), (3, 1), (3, 2), (3, 3))
    elif type == "light-weight spaceship":
        type_coord = ((1, 1), (1, 4), (2, 5), (3, 1), (3, 5), (4, 2), (4, 3), (4, 4), (4, 5))
    elif type == "gosper glider gun":
        type_coord = ((1, 25), (2, 23), (2, 25), (3, 13), (3, 14), (3, 21), (3, 22), (3, 35), (3, 36), (4, 12), (4, 16), (4, 21), (4, 22), (4, 35), (4, 36), (5, 1), (5, 2), (5, 11), (5, 17), (5, 21), (5, 22), (6, 1), (6, 2), (6, 11), (6, 15), (6, 17), (6, 18), (6, 23), (6, 25), (7, 11), (7, 17), (7, 25), (8, 12), (8, 16), (9, 13), (9, 14))
    else:
        print("Invalid Input")
    
    return type_coord

# Getting the input for the type of life to be implemented
type = input("Enter the type of life to implement: ")

# Placing the life on the grid
type_coord = getTypeCoordinates(type)
for i in range(len(type_coord)):
    grid1[type_coord[i][0]][type_coord[i][1]] = 0

# Counting the number lives cells around a 
def liveCount(i, j, grid):
    live = 0
    if i == 0 or j == 0 or i == grid_dim-1 or j == grid_dim-1:
        pass
    else:
        if grid[i - 1][j - 1] == 0:
            live += 1
        if grid[i - 1][j] == 0:
            live += 1
        if grid[i - 1][j + 1] == 0:
            live += 1
        if grid[i][j + 1] == 0:
            live += 1
        if grid[i + 1][j + 1] == 0:
            live += 1
        if grid[i + 1][j] == 0:
            live += 1
        if grid[i + 1][j - 1] == 0:
            live += 1
        if grid[i][j - 1] == 0:
            live += 1

    return live


def gridChanges():

    global grid1, grid2
    live = 0

    for i in range(grid_dim):
        for j in range(grid_dim):
            if grid1[i][j] == 0:
                live = liveCount(i, j, grid1)

                if live < 2:
                    grid2[i][j] = 1
                elif live > 3:
                    grid2[i][j] = 1
                else:
                    grid2[i][j] = 0
            elif grid1[i][j] == 1:
                live = liveCount(i, j, grid1)

                if live == 3:
                    grid2[i][j] = 0
                else:
                    grid2[i][j] = 1

    for i in range(grid_dim):
        for j in range(grid_dim):
            if grid2[i][j] == 0:
                cv2.rectangle(
                    frame, coordinates[i][j][0], coordinates[i][j][1], 0, -1)
            else:
                cv2.rectangle(
                    frame, coordinates[i][j][0], coordinates[i][j][1], 1, -1)

    for i in range(grid_dim):
        for j in range(grid_dim):
            grid1[i][j] = grid2[i][j]


def nothing(x):
    pass


cv2.namedWindow("Game Of Life")
cv2.createTrackbar("DecreaseSpeed", "Game Of Life", 0, 500, nothing)

while(1):

    gridChanges()
    cv2.imshow("Game Of Life", frame)
    spd_dec = int(cv2.getTrackbarPos("DecreaseSpeed", "Game Of Life"))
    if cv2.waitKey(500 - spd_dec) == 27:
        break

cv2.destroyAllWindows()