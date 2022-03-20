import pygame, sys, random
import time

pygame.init()

win = pygame.display.set_mode((200, 201))
clock = pygame.time.Clock()

w = 10

cols = 20
rows = 20

grid = []
stack = []


def index(i, j):
    if i < 0 or j < 0 or i > cols - 1 or j > rows - 1:
        return None
    else:
        return i + j * cols


class Cell:
    def __init__(self, i, j):
        self.i, self.j = i, j
        self.walls = [True, True, True, True]  # 0 is top, 1 is right, 2 is bottom, 3 is left
        self.visited = False
        self.visited2 = False

    def show(self, win):
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

    def highlight(self, win):
        x = self.i * w
        y = self.j * w
        if self.visited:
            pygame.draw.rect(win, (0, 0, 255), (self.i * w, self.j * w, w, w))

    def highlight_green(self, win):
        x = self.i * w
        y = self.j * w
        if self.visited2:
            pygame.draw.rect(win, (255, 0, 0), (self.i * w + 3, self.j * w + 3 , 3, 3), 0, 2, 2)
            time.sleep(0.02)





    def checkNeighbors(self):
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

    def checking_walls(self):
        i, j = self.i, self.j
        my_current = grid[index(i,j)]
        neighbors = []
        shortest = []
        if index(i, j - 1):
            top = grid[index(i, j - 1)]
            if not my_current.walls[0] and not top.visited2:
                neighbors.append(top)

        if index(i + 1, j):
            right = grid[index(i + 1, j)]
            if not my_current.walls[1] and not right.visited2:
                neighbors.append(right)
                shortest.append(right)


        if index(i - 1, j):
            left = grid[index(i - 1, j)]
            if not my_current.walls[3] and not left.visited2:
                neighbors.append(left)

        if index(i, j + 1):
            bottom = grid[index(i, j + 1)]
            if not my_current.walls[2] and not bottom.visited2:
                neighbors.append(bottom)
                shortest.append(bottom)
        if len(neighbors) > 0:
            if len(shortest) > 0:
                return random.choice(shortest)
            else:
                return random.choice(neighbors)
        else:
            return None






def removeWalls(a, b):
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


for j in range(rows):
    for i in range(cols):
        cell = Cell(i, j)
        grid.append(cell)


# n = (cols*rows)//2 + (cols+rows)*2
start_time = time.time()
current = grid[0]
won = False
print("Generating maze...")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    win.fill((0, 0, 0))

    for cell in grid:
        cell.show(win)
        if won == True:
            if cell in stack:
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

        if current == grid[0]:
            print("Generation time = " + str(time.time()- start_time))
            print("Finding solution...")
            start_time = time.time()
            while current != grid[index(cols - 1, rows - 1)]:
                current.visited2 = True
                current.highlight_green(win)
                pygame.display.update()
                nextcell = current.checking_walls()
                if isinstance(nextcell, Cell):
                    nextcell.visited2 = True
                    stack.append(current)
                    current.show(win)
                    current = nextcell
                elif len(stack) > 0:
                    current.show(win)
                    current = stack.pop()
            won = True
            print("Solution time = " + str(time.time() - start_time))


    if won == True:
        font = pygame.font.Font(None, 25)
        text = font.render("I won!", True,(255,0,0))
        text_rect = text.get_rect(center=(cols*w/2, rows*w/2))
        win.blit(text, text_rect)
        pygame.display.update()

    pygame.display.update()









    pygame.display.flip()
