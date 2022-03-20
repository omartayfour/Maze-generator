import pygame, sys, random
import time

pygame.init()

win = pygame.display.set_mode((400,401))
clock = pygame.time.Clock()

w = 10

cols = 40
rows = 40

grid = []
stack = []
stack2 = []


def index(i, j):
    if i < 0 or j < 0 or i > cols - 1 or j > rows - 1:
        return None
    else:
        return i + j * cols


class Cell:
    def __init__(self, i, j):
        self.i, self.j = i, j
        self.walls = [True, True, True, True]  # 0 is top, 1 is right, 2 is bottom, 3 is left
        self.visited = False #used in generation A
        self.visited2 = False #used in solution 1
        self.visited3 = False #used in generation B
        self.visited4 = False #used in solution 2
        self.visited5 = False #used in solution 3

    def show(self, win): # used to draw the maze in generation and also to draw maze when solution nodes move
        x = self.i * w
        y = self.j * w
        if self.visited:
            pygame.draw.rect(win, (255, 255, 255), (self.i * w, self.j * w, w, w))
        if self.visited and (self.i == cols - 1) and (self.j == rows - 1):
            pygame.draw.rect(win, (255, 0, 0), (self.i * w, self.j * w, w, w))
        if self.walls[0]:
            pygame.draw.line(win, (0, 0, 0), (x, y), (x + w, y))
        if self.walls[1]:
            pygame.draw.line(win, (0, 0, 0), (x + w, y), (x + w, y + w))
        if self.walls[2]:
            pygame.draw.line(win, (0, 0, 0), (x + w, y + w), (x, y + w))
        if self.walls[3]:
            pygame.draw.line(win, (0, 0, 0), (x, y + w), (x, y))


    def highlight(self, win): # BLUE highlight when generating maze
        x = self.i * w
        y = self.j * w
        if self.visited:
            pygame.draw.rect(win, (0, 0, 255), (self.i * w, self.j * w, w, w))

    def highlight2(self, win): # RED highlight when generating maze
        x = self.i * w
        y = self.j * w
        if self.visited:
            pygame.draw.rect(win, (255, 0, 0), (self.i * w, self.j * w, w, w))

    def highlight_green(self, win): # GREEN solution
        x = self.i * w
        y = self.j * w
        if self.visited2 or self.visited5 or self.visited4:
            pygame.draw.rect(win, (0, 255, 0), (self.i * w + 3, self.j * w + 3 , 3, 3), 0, 2, 2)
           # time.sleep(0.02)

    def highlight_red(self, win): # RED solution
        x = self.i * w
        y = self.j * w
        if self.visited2 or self.visited5 or self.visited4:
            pygame.draw.rect(win, (255, 0, 0), (self.i * w + 3, self.j * w + 3 , 3, 3), 0, 2, 2)
           # time.sleep(0.02)

    def highlight_blue(self, win): # BLUE SOLUTION
        x = self.i * w
        y = self.j * w
        if self.visited2 or self.visited5 or self.visited4:
            pygame.draw.rect(win, (0, 0, 255), (self.i * w + 3, self.j * w + 3 , 3, 3), 0, 2, 2)
            time.sleep(0.02)






    def checkNeighbors(self): # Generation checking neighbors for open places to visit
        neighbors = []
        i, j = self.i, self.j
        if index(i, j - 1):
            top = grid[index(i, j - 1)]
            if not top.visited:
                neighbors.append(top)
        if index(i + 1, j):
            right = grid[index(i + 1, j)]
            if not right.visited:
                neighbors.append(right)
        if index(i - 1, j):
            left = grid[index(i - 1, j)]
            if not left.visited:
                neighbors.append(left)
        if index(i, j + 1):
            bottom = grid[index(i, j + 1)]
            if not bottom.visited:
                neighbors.append(bottom)

        if len(neighbors) > 0:
            return random.choice(neighbors)
        else:
            return None

    def checkPath(self): # Checking if path exists between generator A and generator B to be able to have path between two generators
        neighbors = []
        i, j = self.i, self.j
        my_current = grid[index(i,j)]
        if index(i, j - 1):
            top = grid[index(i, j - 1)]
            if top.visited and my_current.walls[0]:
                neighbors.append(top)
        if index(i + 1, j):
            right = grid[index(i + 1, j)]
            if right.visited and my_current.walls[1]:
                neighbors.append(right)
        if index(i - 1, j):
            left = grid[index(i - 1, j)]
            if left.visited and my_current.walls[3]:
                neighbors.append(left)
        if index(i, j + 1):
            bottom = grid[index(i, j + 1)]
            if bottom.visited and my_current.walls[2]:
                neighbors.append(bottom)

        if len(neighbors) > 0:
            return random.choice(neighbors)
        else:
            return None

    def checking_walls(self): # Checking walls when solving maze, returns shortest if possible(right or down path)
        i, j = self.i, self.j
        my_current = grid[index(i,j)]
        neighbors = []
        shortest = []
        if index(i, j - 1):
            top = grid[index(i, j - 1)]
            if (not my_current.walls[0] and not top.visited2):
                neighbors.append(top)

        if index(i + 1, j):
            right = grid[index(i + 1, j)]
            if (not my_current.walls[1] and not right.visited2):
                neighbors.append(right)
                shortest.append(right)

        if index(i - 1, j):
            left = grid[index(i - 1, j)]
            if (not my_current.walls[3] and not left.visited2):
                neighbors.append(left)

        if index(i, j + 1):
            bottom = grid[index(i, j + 1)]
            if (not my_current.walls[2] and not bottom.visited2):
                neighbors.append(bottom)
                shortest.append(bottom)

        if len(neighbors) > 0:
            if len(shortest) > 0:
                return random.choice(shortest)
            else:
                return random.choice(neighbors)
        else:
            return None

    def checking_walls2(self): # totally random checking walls to solve maze
        i, j = self.i, self.j
        my_current = grid[index(i,j)]
        neighbors = []
        shortest = []
        if index(i, j - 1):
            top = grid[index(i, j - 1)]
            if (not my_current.walls[0] and not top.visited4):
                neighbors.append(top)

        if index(i + 1, j):
            right = grid[index(i + 1, j)]
            if (not my_current.walls[1] and not right.visited4):
                neighbors.append(right)
                shortest.append(right)

        if index(i - 1, j):
            left = grid[index(i - 1, j)]
            if (not my_current.walls[3] and not left.visited4):
                neighbors.append(left)

        if index(i, j + 1):
            bottom = grid[index(i, j + 1)]
            if (not my_current.walls[2] and not bottom.visited4):
                neighbors.append(bottom)
                shortest.append(bottom)


        if len(neighbors) > 0:
            if len(shortest) > 0:
                return random.choice(shortest)
            else:
                return random.choice(neighbors)
        else:
            return None


    def checking_walls3(self): # totally random checking walls when solving maze
        i, j = self.i, self.j
        my_current = grid[index(i,j)]
        neighbors = []
        if index(i, j - 1):
            top = grid[index(i, j - 1)]
            if (not my_current.walls[0] and not top.visited5):
                neighbors.append(top)

        if index(i + 1, j):
            right = grid[index(i + 1, j)]
            if (not my_current.walls[1] and not right.visited5):
                neighbors.append(right)

        if index(i - 1, j):
            left = grid[index(i - 1, j)]
            if (not my_current.walls[3] and not left.visited5):
                neighbors.append(left)

        if index(i, j + 1):
            bottom = grid[index(i, j + 1)]
            if (not my_current.walls[2] and not bottom.visited5):
                neighbors.append(bottom)


        if len(neighbors) > 0:
            return random.choice(neighbors)
        else:
            return None







def removeWalls(a, b): # breaking walls when generating maze
    x = a.i - b.i
    if x == 1:
        a.walls[3] = False
        b.walls[1] = False
    elif x == -1:
        a.walls[1] = False
        b.walls[3] = False
    y = a.j - b.j
    if y == 1:
        a.walls[0] = False
        b.walls[2] = False
    elif y == -1:
        a.walls[2] = False
        b.walls[0] = False



for j in range(rows): # initialization of grid
    for i in range(cols):
        cell = Cell(i, j)
        grid.append(cell)


# n = (cols*rows)//2 + (cols+rows)*2




current = grid[0]
current2 = grid[0]
current3 = grid[0]
stack3 = []
path = False
counter = 0
won = False

print("Generating maze....")
start_time = time.time()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    win.fill((0, 0, 0))
    for cell in grid:
        cell.show(win)
        if won == True:
            if current == grid[index(cols - 1, rows - 1)]:
                if cell in stack:
                    cell.highlight_blue(win)
            elif current2 == grid[index(cols - 1, rows - 1)]:
                if cell in stack2:
                    cell.highlight_red(win)
            elif current3 == grid[index(cols - 1, rows - 1)]:
                if cell in stack3:
                    cell.highlight_green(win)


    if won == False:

        current.visited = True
        current.highlight(win)
        # Step1
        nextcell = current.checkNeighbors()
        if isinstance(nextcell, Cell):
            nextcell.visited = True
            # Step2
            stack.append(current)
            # Step3
            removeWalls(current, nextcell)
            # Step4
            current = nextcell
        elif len(stack) > 0:
            current = stack.pop()

        current2.visited = True
        current2.visited3 = True
        current2.highlight2(win)
        nextcell2 = current2.checkNeighbors()
        if current2.checkPath() != None:
            if path == False and counter >= cols*rows/4:
                tempnext = current2.checkPath()
                if tempnext.visited3 == False:
                    print("Breaking")
                    path = True
                    nextcell2 = tempnext
        if isinstance(nextcell2, Cell):
            nextcell2.visited = True
            nextcell2.visited3 = True
            stack2.append(current2)
            removeWalls(current2, nextcell2)
            current2 = nextcell2
        elif len(stack2) > 0:
            current2 = stack2.pop()



        if current == grid[0] and current2 == grid[0]:
            print("Generation time = " + str(time.time()- start_time))
            print("Finding solution....")
            start_time = time.time()
            while current != grid[index(cols - 1, rows - 1)] and current2 != grid[index(cols-1, rows-1)] and current3 != grid[index(cols - 1, rows - 1)]:
                current.visited2 = True
                nextcell = current.checking_walls()
                if isinstance(nextcell, Cell):
                    nextcell.visited2 = True
                    stack.append(current)
                    current.show(win)
                    current = nextcell
                elif len(stack) > 0:
                    current.show(win)
                    current = stack.pop()

                current2.visited4 = True
                nextcell2 = current2.checking_walls2()
                if isinstance(nextcell2, Cell):
                    nextcell2.visited4 = True
                    stack2.append(current2)
                    current2.show(win)
                    current2 = nextcell2
                elif len(stack2) > 0:
                    current2.show(win)
                    current2 = stack2.pop()

                current3.visited5 = True
                nextcell3 = current3.checking_walls3()
                if isinstance(nextcell3, Cell):
                    nextcell3.visited5 = True
                    stack3.append(current3)
                    current3.show(win)
                    current3 = nextcell3
                elif len(stack3) > 0:
                    current3.show(win)
                    current3 = stack3.pop()

                current.highlight_blue(win)
                current2.highlight_red(win)
                current3.highlight_green(win)
                pygame.display.flip()




            won = True
            print("Solution time = " + str(time.time() - start_time))

    if won == True:
        font = pygame.font.Font(None, 25)
        text = font.render("I won!", True,(255,0,0))
        text_rect = text.get_rect(center=(cols*w/2, rows*w/2))
        win.blit(text, text_rect)
        pygame.display.update()


    pygame.display.update()

    counter +=1



    pygame.display.flip()
