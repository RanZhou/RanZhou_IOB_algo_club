import pygame
import random
import sys


# Pygame set up 
# Screen size
SX, SY = 800, 600
# margins
horizontal_mar = 100
vertical_mar = 100

# define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PINK = (255, 182, 193)
BLUE = (0,34,230)
DR = (105, 0, 0)

# This is for large recursion
sys.setrecursionlimit(15000)

plt_x_size = SX-horizontal_mar
plt_y_size = SY-vertical_mar

#Centered plot ## not really working well
plt_x_start = int(horizontal_mar/2)
plt_y_start = int(vertical_mar/2)

pygame.init()
screen = pygame.display.set_mode((SX, SY))
clock = pygame.time.Clock()


# set up grid size of maze
grid_x, grid_y = 7, 7
cx = grid_x+1
cy = grid_y+1
lwd = 1
cell_size = min(int(plt_x_size /grid_x),int(plt_y_size /grid_y))
plt_x_size = grid_x*cell_size+cx*lwd
plt_y_size = grid_y*cell_size+cy*lwd

#Set up the turtle
#turtle_x, turtle_y = 0, 0
#turtle_heading = 0  # in degrees
#turtle_speed = 1  # in grid per frame
#turtle_path = [(turtle_x, turtle_y)]

## Set up the stack ##
unvisited_nodes = []
for i in range(0,grid_x):
    for j in range(0,grid_y):
        unvisited_nodes.append([i,j])

visited_nodes = []

## Symbolization ##
bricks = []
for i in range(0,grid_y*2+1):
    row = []
    for j in range(0,grid_x*2+1):
        row.append("#")
    bricks.append(row)

random.seed(259)
carvar_x = random.randint(0,grid_x)

random.seed(260)
carvar_y = random.randint(0,grid_y)

carve_path = []
carve_path_full = []
link_array = []
backnodes = []
print ("Start from", carvar_x, carvar_y)
#backtracking
carve_dir = 1
def carve_pas_from(cxr_x, cxr_y,grid_x, grid_y):
    global carve_dir
    nbsig = neighborScan(cxr_x,cxr_y)
    print("@",cxr_x,cxr_y)
    if len(carve_path)<1:
        carve_path.append([cxr_x, cxr_y])
        visited_nodes.append([cxr_x, cxr_y])
        bricks[cxr_y*2+1][cxr_x*2+1] = " "
        unvisited_nodes.remove([cxr_x, cxr_y])
    if nbsig == 0:
        if len(unvisited_nodes) == 0:
            carve_path_full.append(carve_path)
            print(bricks)
            return 2
        else:  
            if carve_dir == 1 :
                carve_path_full.append(carve_path)
                carve_dir = -1
            backnodes.append(carve_path.pop())
            back_node=carve_path[-1]
            carve_pas_from(back_node[0],back_node[1],grid_x,grid_y)
    else:
        # Please notice I take shortcut by converting coded neighborSginal into binary bits and use that
        # to simplify the coordinate delta
        # https://stackoverflow.com/questions/13081090/convert-binary-to-list-of-digits-python
        operationlist = [int(d) for d in str(format(nbsig,'#06b'))[2:]]
        #print(str(format(nbsig,'#06b'))[2:])
        #print("OPL:",operationlist)
        choicelist = []
        if operationlist[3] == 1:
            choicelist.append([0,-1])
        if operationlist[2] == 1:
            choicelist.append([0,1])
        if operationlist[1] == 1:
            choicelist.append([1,0])
        if operationlist[0] == 1:
            choicelist.append([-1,0])
        #print(choicelist)
        del_mv = random.choice(choicelist)
        #print("Choose:", del_mv)
        new_x = cxr_x + del_mv[0]
        new_y = cxr_y + del_mv[1]
        bricks[new_y*2+1][new_x*2+1] = " "
        bricks[cxr_y*2+1+del_mv[1]][cxr_x*2+1+del_mv[0]]= " "
        if carve_dir == -1:
            carve_dir = 1
            carve_path_full.append(backnodes)
        carve_path.append([new_x, new_y])
        visited_nodes.append([new_x, new_y])
        unvisited_nodes.remove([new_x, new_y])
        link_array.append([cxr_x, cxr_y, del_mv[0], del_mv[1]])
        if len(unvisited_nodes) >0:
            carve_pas_from(new_x, new_y, grid_x, grid_y)


def neighborScan(cxr_x, cxr_y):
    neighborSignal = 0
    #N
    tp_y =cxr_y-1
    if [cxr_x, tp_y] in unvisited_nodes:
        neighborSignal = neighborSignal + 1
    #S
    tp_y =cxr_y+1
    if [cxr_x, tp_y] in unvisited_nodes:
        neighborSignal = neighborSignal + 2
    #E
    tp_x =cxr_x+1
    if [tp_x, cxr_y] in unvisited_nodes:
        neighborSignal = neighborSignal + 4
    #W
    tp_x =cxr_x-1
    if [tp_x, cxr_y] in unvisited_nodes:
        neighborSignal = neighborSignal + 8
    return neighborSignal

# running
carve_pas_from(carvar_x, carvar_y, grid_x, grid_y)
print(len(visited_nodes),"Visited:", visited_nodes)
print(len(unvisited_nodes),"UnVisited:", unvisited_nodes)
print(bricks)
for i in bricks:
    print("".join(i))

## Visual in Pygame ##

# generate grid
def grid_gen():
    for x in range(plt_x_start, plt_x_start+plt_x_size, cell_size+lwd):
        pygame.draw.line(screen, WHITE, (x, plt_y_start), (x, plt_y_start+plt_y_size-lwd))
    for y in range(plt_y_start, plt_y_start+plt_y_size, cell_size+lwd):
        pygame.draw.line(screen, WHITE, (plt_x_start, y), (plt_x_start+plt_x_size-lwd, y))

def carvar_recol(carvar_x,carvar_y,COLOR):
    pygame.draw.rect(screen, COLOR,(plt_x_start+carvar_x*(cell_size+lwd),plt_y_start+carvar_y*(cell_size+lwd),cell_size+1,cell_size+1))


## Want to add a player
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super(Player, self).__init__()
        self.pos = pos
        self.image = pygame.image.load('bulldog2.png')
        self.image = pygame.transform.smoothscale(self.image,(cell_size*0.8,cell_size*0.8)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left = plt_x_start+self.pos[0]*(cell_size+lwd)+cell_size*0.1
        self.rect.top = plt_y_start+self.pos[1]*(cell_size+lwd)+cell_size*0.1
    def move(self, target_del):
        self.pos = [self.pos[0]+target_del[0],self.pos[1]+target_del[1]]
        self.rect.left = plt_x_start+self.pos[0]*(cell_size+lwd)+cell_size*0.1
        self.rect.top = plt_y_start+self.pos[1]*(cell_size+lwd)+cell_size*0.1
        #print(self.pos)

## Goal ##
class TargetPoint(pygame.sprite.Sprite):
    def __init__(self, x, y, col):
        super(TargetPoint, self).__init__()
        self.x = x
        self.y = y
        self.col = col
    def show(self):
        pygame.draw.circle(screen, self.col, (plt_x_start+self.x*(cell_size+lwd)+cell_size*0.5, 
                                              plt_y_start+self.y*(cell_size+lwd)+cell_size*0.5) , cell_size*0.1)
    def update(self):
        self.x = random.randint(0,grid_x-1)
        self.y = random.randint(0,grid_y-1)

#Pygame main loop
running = True
step_c  = 0
vv_c = 0
screen.fill(BLACK)
grid_gen()
automate_draw = False
PlayMode = False
MyPlayer = Player([1,1])
GameGoal = TargetPoint(random.randrange(0,grid_x),random.randrange(0,grid_y),DR)
mv_delta = [0,0]
while running:
    # handle events
    draw_path = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if vv_c < len(visited_nodes):
                    #print("#",vv_c)
                    for i in range(0,vv_c):
                        draw_path.append(visited_nodes[i])
                    print("@",visited_nodes[vv_c][0],visited_nodes[vv_c][1])
                vv_c = vv_c + 1
                for i in draw_path:
                    pygame.draw.rect(screen, PINK,(plt_x_start+i[0]*(cell_size+lwd),plt_y_start+i[1]*(cell_size+lwd),cell_size,cell_size))
                if step_c < len(visited_nodes):
                    pygame.draw.rect(screen, BLUE,(plt_x_start+visited_nodes[step_c][0]*(cell_size+lwd),plt_y_start+visited_nodes[step_c][1]*(cell_size+lwd),cell_size,cell_size))
                    link_x = plt_x_start+link_array[step_c][0]*(cell_size+lwd)+0.2*cell_size
                    link_y = plt_y_start+link_array[step_c][1]*(cell_size+lwd)+0.2*cell_size
                    link_w = cell_size
                    link_h = cell_size
                    if link_array[step_c][2] == -1:
                        link_x = plt_x_start+(link_array[step_c][0]-1)*(cell_size+lwd)+0.1*cell_size
                    if link_array[step_c][3] == -1:
                        link_y = plt_y_start+(link_array[step_c][1]-1)*(cell_size+lwd)+0.1*cell_size
                    if link_array[step_c][2] == 0:
                        link_h = cell_size*0.8
                    if link_array[step_c][3] == 0:
                        link_w = cell_size*0.8
                    pygame.draw.rect(screen, PINK,(link_x, link_y,
                                                    link_h, link_w))
                    if len(visited_nodes) - step_c == 1:
                        pygame.draw.rect(screen, PINK,(plt_x_start+visited_nodes[-1][0]*(cell_size+lwd),plt_y_start+visited_nodes[-1][1]*(cell_size+lwd),cell_size,cell_size))
                    step_c = step_c+1
            if event.key == pygame.K_a:
                screen.fill(BLACK)
                grid_gen()
                step_c  = 0
                vv_c = 0
                automate_draw = True
            if event.key == pygame.K_p:
                PlayMode = True
            if PlayMode is True:
                if event.key == pygame.K_RIGHT:
                    mv_delta =[1,0]   
                if event.key == pygame.K_LEFT:
                    mv_delta =[-1,0]
                if event.key == pygame.K_UP:
                    mv_delta =[0,-1]
                if event.key == pygame.K_DOWN:
                    mv_delta =[0,1]
                next_pos = [MyPlayer.pos[0] + mv_delta[0],MyPlayer.pos[1] + mv_delta[1]]
                #try:
                sym_x = MyPlayer.pos[0]*2 + 1 + mv_delta[0]
                sym_y = MyPlayer.pos[1]*2 + 1 + mv_delta[1]
                print(sym_x,sym_y, bricks[sym_y][sym_x])
                if bricks[sym_y][sym_x] == " ":
                    MyPlayer.move(mv_delta)
                #except:
                #    print("Something is wrong!")

    if automate_draw is True:
        for i in visited_nodes:
           pygame.draw.rect(screen, PINK,(plt_x_start+i[0]*(cell_size+lwd),plt_y_start+i[1]*(cell_size+lwd),cell_size,cell_size))
        if step_c < len(visited_nodes)-1:
            pygame.draw.rect(screen, BLUE,(plt_x_start+visited_nodes[step_c][0]*(cell_size+lwd),plt_y_start+visited_nodes[step_c][1]*(cell_size+lwd),cell_size,cell_size))
            link_x = plt_x_start+link_array[step_c][0]*(cell_size+lwd)+0.1*cell_size
            link_y = plt_y_start+link_array[step_c][1]*(cell_size+lwd)+0.1*cell_size
            link_w = cell_size
            link_h = cell_size
            if link_array[step_c][2] == -1:
                link_x = plt_x_start+(link_array[step_c][0]-1)*(cell_size+lwd)+0.1*cell_size
            if link_array[step_c][3] == -1:
                link_y = plt_y_start+(link_array[step_c][1]-1)*(cell_size+lwd)+0.1*cell_size
            if link_array[step_c][2] == 0:
                link_h = cell_size*0.8
            if link_array[step_c][3] == 0:
                link_w = cell_size*0.8
            pygame.draw.rect(screen, PINK,(link_x, link_y,
                                            link_h, link_w))
            if len(visited_nodes) - step_c == 1:
                pygame.draw.rect(screen, PINK,(plt_x_start+visited_nodes[-1][0]*(cell_size+lwd),plt_y_start+visited_nodes[-1][1]*(cell_size+lwd),cell_size,cell_size))
            step_c = step_c+1

    if PlayMode is True:
        GameGoal.show()
        if MyPlayer.pos[0] == GameGoal.x and MyPlayer.pos[1] == GameGoal.y :
            GameGoal.update()
        screen.blit(MyPlayer.image, MyPlayer.rect)
        print(MyPlayer.pos)
    # Update the display
    pygame.display.flip()
    clock.tick(30)

pygame.image.save(screen, 'test_maze.png')
pygame.quit()