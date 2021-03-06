#-------------------------------------------------------------------------------
# Name:        game-flood.py
# Purpose:
#
# Author:      andy
#
# Created:     24-04-2013
# Copyright:   (c) andy 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pygame
import sys
from random import seed,choice
from pygame.locals import *
from libun_find import UnionFind,node
import copy

FPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
SEED = 100
GRID_SIZE = 15
NUM_COLOR = 6
INTERSURFACE_SPACING = 5
BACK_BACK_COL = pygame.Color(255,128,0)
BACK_COL = pygame.Color(255,255,255)
GRID_SCREEN_Y = GRID_SCREEN_X = 0 + INTERSURFACE_SPACING
BOX_SIZE = WINDOWHEIGHT-50 #430
BLUE_POS = (BOX_SIZE + 20,100)
GRID_SCREEN = pygame.Rect(GRID_SCREEN_X,GRID_SCREEN_Y,BOX_SIZE,BOX_SIZE)
BUTTON_NAMES = ["blue","green","red","black","purple","yellow"]
COL = [pygame.Color(10,52,170),pygame.Color(90,187,12),pygame.Color(172,25,9),
        pygame.Color(80,80,80),pygame.Color(208,91,205),pygame.Color(237,235,88)]

CELL_SIZE = (BOX_SIZE / GRID_SIZE)
USER_MODE = True
TEST_MODE = False
RUNNING = 1 # game state
FINISHED = 2 #game state
un = UnionFind()
already_covered=set([]) # covered cells(frontier+non-frontier)
frontier = []
cell_table = []  # save the grid in 0=>RED,1=>GREEN,2=>YELLOW.... n*n-1=>BLUE
cell_nodes = [] # stores node object corresponding to each cell to be used in union-find
visited = [False for i in range(GRID_SIZE * GRID_SIZE)] # used in initializing frontier
totalmoves = 0 # counter for score[koto move lagse]


def heuristic_greedy():
        '''
        greedy heuristic: always pick the adjacent color with maximum count.
        '''
        next_frontier = get_next_frontier()
        color_count = {}
        for next_f in next_frontier:
                color = get_col_from_cell(next_f)
                if  color_count.get(color,0) == 0:
                        color_count[color] = 1
                else:
                        color_count[color] += 1

        maximum_count = sorted(color_count.items(), key = lambda x:x[1], reverse = True)[0]
        return maximum_count[0]

def get_next_frontier():
        '''
        input: none
        output: return a list of next frontier based on the variable frontier
        '''
        global visited
        next_frontier=set([])
        for cell in frontier:
                adjacent_cells = get_adjacent_cells(cell)
                for neighbour in adjacent_cells:
                        if not visited[neighbour]:
                                next_frontier = next_frontier.union\
                                (set(cell_nodes[neighbour].getchild()))
                                next_frontier = \
                                next_frontier.union(set([neighbour]))

        return next_frontier

# initialize frontier recursively. also initialize variable already_covered with globally visited cells.
def init_frontier(i):
        no_same_colored_neighbour = True
        same_colored_neighbour = []
        frontier.append(i)
        already_covered.add(i)
        visited[i] = True
        for neighbour in get_adjacent_cells(i):
                if is_same_col(neighbour, i) and not visited[neighbour]:
                        no_same_colored_neighbour = False
                        same_colored_neighbour.append(neighbour)
        if no_same_colored_neighbour:
                return
        for x in same_colored_neighbour:
                init_frontier(x)

# update score
def update_score(displaysurface, score):
   fontobj = pygame.font.SysFont(None, 40)
   scoretext = fontobj.render("Move: "+str(score), 1, (255,255,255))
   displaysurface.blit(scoretext, (BOX_SIZE+20, 380))

# update the grid when a color is choosen
def update_grid(color, displaysurface):
        '''
        input: color = name of a color like "blue","green" .must match a color in variable BUTTON_NAMES.
                displaysurface = display surface to update
        '''
        previosly_already_covered=copy.copy(already_covered)
        for cell in frontier:
                adjacent_cells = get_adjacent_cells(cell)
                print adjacent_cells
                for neighbour in adjacent_cells:
                        #print neighbour,"->",cell_table[neighbour]
                        #print cell,"->",cell_table[cell]

                        # jodi neighbour ta frontier othoba already flooded(unionfind e root different) na hoe thake.
                        if neighbour not in already_covered:
                                print "neighbour", neighbour
                                print un.findSet(cell_nodes[neighbour]).val
                                print un.findSet(cell_nodes[cell]).val
                                if get_col_from_cell(neighbour) == color:
                                        un.union(cell_nodes[cell], cell_nodes[neighbour])
                                        frontier.append(neighbour)
                                        visited[neighbour] = True
                                        already_covered.add(neighbour)
                                        print "appended", neighbour


        print "before atlast: ", frontier
        print "already covered", already_covered
        remove_set=[]
        for i in frontier:
                adjacent_cells = get_adjacent_cells(i)
                print i, "'s adjacent are", adjacent_cells
                if all(cell in already_covered for cell in adjacent_cells):
                        remove_set.append(i)
                        print "removed=>", i
        print "removeset",remove_set
        for i in remove_set:
                frontier.remove(i)
        print "atlast frontier: ", frontier
        #print "atlast visited: ",visited
        if previosly_already_covered == already_covered:
            #print 'no change'
            return False
        else:
            #print 'change'
            return True

def get_col_from_cell(cell):
        '''
        input: a cell number i.e an integer from 0 to GRID_SIZE**2-1
        output: the color-name of the cell at that point. the color name must be in BUTTON_NAMES
        '''
        return cell_table[un.findSet(cell_nodes[cell]).val]

def is_same_col(cell1, cell2):
        return cell_table[un.findSet(cell_nodes[cell1]).val]== \
                cell_table[un.findSet(cell_nodes[cell2]).val]


# true if cell1 is adjacent to cell2
def is_adjacent(cell1, cell2):
        return cell1 in get_adjacent_cells(cell2)

# return a set of adjacent cells for example <3,5,2> from a cell#
def get_adjacent_cells(i):
        adjacent_cells = set([])

        if (i/GRID_SIZE) == 0:
                if i+GRID_SIZE < GRID_SIZE*GRID_SIZE:
                        adjacent_cells.add(i+GRID_SIZE)
        else:
                adjacent_cells.add(i-GRID_SIZE)
                if i+GRID_SIZE < GRID_SIZE * GRID_SIZE:
                        adjacent_cells.add(i+GRID_SIZE)
        if i%GRID_SIZE == 0:
                adjacent_cells.add(i+1)
        else:
                adjacent_cells.add(i-1)

        if i/GRID_SIZE == GRID_SIZE-1:
                adjacent_cells.add(i-GRID_SIZE)
        else:
                if i+1 < GRID_SIZE:
                        adjacent_cells.add(i+1)

        if i%GRID_SIZE == GRID_SIZE-1:
                adjacent_cells.add(i-1)
        else:
                adjacent_cells.add(i+1)

        '''if i/GRID_SIZE != 0 and i%GRID_SIZE != 0:
                adjacent_cells.add(i+1)
                adjacent_cells.add(i-1)
                adjacent_cells.add(i+GRID_SIZE)
                adjacent_cells.add(i-GRID_SIZE)'''
        return adjacent_cells

def gen_grid():
                '''
                        choose random color, assign each color to each rectangle object, make node from each cell object
                        and construct variable un, union same colored cells.
                '''
                global cell_nodes
                cell_nodes = [0 for x in range(GRID_SIZE*GRID_SIZE)] # nodeobj if node object exist,otherwise 0
                for i in range(GRID_SIZE*GRID_SIZE):
                        x_pos, y_pos = getxy_from_index(i)
                        selected_pygamecol = choice(BUTTON_NAMES) #randomly pick a color
                        cell_rectobj = pygame.Rect(x_pos,y_pos, CELL_SIZE, CELL_SIZE) #create rectangular cell
                        cell_table.append(selected_pygamecol)
                        # populate union-find data structure
                        new_node = node(i)
                        un.makeSet(new_node)
                        cell_nodes[i] = new_node
                        adjacent_cells = get_adjacent_cells(i)

                        #print "new node:",new_node
                        #print adjacent_cells
                        #print cell_nodes
                        for anode in adjacent_cells:

                                if cell_nodes[anode] != 0 and cell_table[anode] == cell_table[i]:
                                        un.union(new_node,cell_nodes[anode])
                                        #print new_node,"unioned",anode
                                        #print new_node,"'s root",un.findSet(new_node)
                #un.print_set(cell_nodes)
                #pygame.draw.rect(self.DISPLAYSURF,selected_pygamecol,cell_rectobj)
                #self.modify_grid=False

        # convert a gridindex suppose 15 to x,y=3,3
def getxy_from_index(index):
                x = index / GRID_SIZE
                y = index % GRID_SIZE
                x_pos = GRID_SCREEN_X + y*CELL_SIZE
                y_pos = GRID_SCREEN_Y + x*CELL_SIZE
                return (x_pos, y_pos)

class Pymanmain():
        def __init__(self):
                pygame.init()
                self.init_global_vars()
                self.__gen_color()
                gen_grid()
                self.FPSCLOCK = pygame.time.Clock()
                self.DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
                pygame.display.set_caption('Flood It!')
                self.totalmoves = 0
                init_frontier(0)  # initialize game from cell# 0
                self.state = RUNNING
                self.mode = USER_MODE

        def init_global_vars(self):
                '''
                        initialize global variables GRID_SIZE,CELL_SIZE according to user input
                '''
                global CELL_SIZE,GRID_SIZE
                GRID_SIZE = int(raw_input("PLEASE ENTER GRID SIZE: "))
                CELL_SIZE=(BOX_SIZE/GRID_SIZE)

        def __gen_color(self):
                self.button = []  # [(buttonimage,buttonposition),...]
                for col in range(NUM_COLOR):
                        name = "button"+str(col+1)
                        if col < 3:
                                pos = (BLUE_POS[0]+col*48,BLUE_POS[1])
                        else:
                                pos = (BLUE_POS[0]+(col%3)*48,BLUE_POS[1]+(col/3)*48)

                        btn = pygame.image.load(name+".png")
                        self.button.append((btn,pos))


        def mainloop(self):

                while True:
                        self.DISPLAYSURF.fill(BACK_BACK_COL)
                        self.draw_background_rects()
                        self.draw_buttons()
                        self.draw_gridbyun()
                        self.checkforquit()
                        update_score(self.DISPLAYSURF,self.totalmoves)

                        for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN and self.mode == USER_MODE:
                                        if self.state == RUNNING:
                                                for index,btn in enumerate(self.button):
                                                        buttonobj = self.get_exact_buttonrect(btn[0].get_rect(),index)
                                                        if buttonobj.collidepoint(pygame.mouse.get_pos()):
                                                                print BUTTON_NAMES[index],'clicked' # handle change in grid

                                                                #print pycolor ,'clicked'
                                                                grid_updated=update_grid(BUTTON_NAMES[index], self.DISPLAYSURF) #update grid
                                                                #update_grid(BUTTON_NAMES[index],self.DISPLAYSURF)
                                                                if grid_updated:                                                    
                                                                    self.totalmoves+=1
                                                                update_score(self.DISPLAYSURF, self.totalmoves)
                                                                if len(already_covered) == GRID_SIZE**2 and self.state==RUNNING:
                                                                        self.state = FINISHED



                                if event.type == KEYDOWN:
                                        if hasattr(event,'key'):
                                                if event.key == K_SPACE:
                                                        if self.state == RUNNING:
                                                                # solve the grid in heuristic-test mode
                                                                #print "hi"
                                                                color_choice = heuristic_greedy() # here get a colorchoice from a heuristic algo
                                                                        # update grid accordingly

                                                                #pycolor = pygame.Color(color_choice)
                                                                grid_updated=update_grid(color_choice,self.DISPLAYSURF)
                                                                
                                                                if grid_updated:                                                    
                                                                    self.totalmoves+=1
                                                                update_score(self.DISPLAYSURF, self.totalmoves)
                                                                if len(already_covered) == GRID_SIZE**2 and self.state==RUNNING:
                                                                        self.state = FINISHED

                        pygame.display.update()

        # find exact x,y co-ordinate (with respect to pygame surface) from cell-index  and return rect object
        def get_exact_buttonrect(self, rect, index):
                if index < 3:
                        rect.x, rect.y = (BLUE_POS[0] + index*48, BLUE_POS[1])
                else:
                        rect.x, rect.y = (BLUE_POS[0] + (index%3)*48, BLUE_POS[1] + (index/3)*48)
                return rect

        def draw_background_rects(self): # draws white-SQUARE surface
                pygame.draw.rect(self.DISPLAYSURF, BACK_COL, GRID_SCREEN)

        def draw_buttons(self): # draw 6 buttons on the right
                for btn in self.button:
                        self.DISPLAYSURF.blit(btn[0], btn[1])

        '''
        def draw_grid(self):
                for key,value in enumerate(cell_table):
                        x_pos,y_pos=getxy_from_index(key)
                        cell_rectobj=pygame.Rect(x_pos,y_pos,CELL_SIZE,CELL_SIZE)
                        pygame.draw.rect(self.DISPLAYSURF,value,cell_rectobj)
        '''

        # draw the game grid using uniion-find
        def draw_gridbyun(self):
                for key,obj in enumerate(cell_nodes):
                        idx = un.findSet(obj).val
                        x_pos, y_pos = getxy_from_index(key)
                        cell_rectobj = pygame.Rect(x_pos,y_pos,CELL_SIZE,CELL_SIZE)
                        color = self.get_pycolor_from_colorname(cell_table[idx])
                        pygame.draw.rect(self.DISPLAYSURF,color,cell_rectobj) # this line is importane
                                        # we could have used cell_table[key] but didn't.

        def get_pycolor_from_colorname(self,colorname):
                '''
                input: a color name like "purple" "green" . name must be in the variable BUTTON_SIZE
                output: a pycolor object from that color-name
                '''
                global COL,BUTTON_NAMES
                return COL[BUTTON_NAMES.index(colorname)]





        # check if ESC button is pressed.
        def checkforquit(self):
                for event in pygame.event.get(QUIT): # get all the QUIT events
                        self._terminate()
                for event in pygame.event.get(KEYUP): # get all the KEYUP events
                        if event.key == K_ESCAPE:
                                self._terminate() # terminate if the KEYUP event was for the Esc key
                        pygame.event.post(event) # put the other KEYUP event objects back

        # terminate pygame
        def _terminate(self):
                pygame.quit()
                import sys
                sys.exit()

def main():
        seed(SEED)
        #print sys.argv
        mainwindow = Pymanmain()
        #print mainwindow
        mainwindow.mainloop()

if __name__ == '__main__':
        main()
