from graphics import *
import random

############################################################
# BLOCK CLASS
############################################################

class Block(Rectangle):
    ''' Block class:
        Implement a block for a tetris piece
        Attributes: x - type: int
                    y - type: int
        specify the position on the tetris board
        in terms of the square grid
    '''

    BLOCK_SIZE = 30
    OUTLINE_WIDTH = 3

    def __init__(self, pos, color):
        self.x = pos.x
        self.y = pos.y
        
        p1 = Point(pos.x*Block.BLOCK_SIZE, pos.y*Block.BLOCK_SIZE)
        p2 = Point(p1.x + Block.BLOCK_SIZE, p1.y + Block.BLOCK_SIZE)

        Rectangle.__init__(self, p1, p2)
        self.setWidth(Block.OUTLINE_WIDTH)
        self.setFill(color)

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            checks if the block can move dx squares in the x direction
            and dy squares in the y direction
            Returns True if it can, and False otherwise
            HINT: use the can_move method on the Board object
        '''
        #MY CODE HERE
        x = self.x + dx
        y = self.y + dy
        return board.can_move(x, y)
    
    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int
                        
            moves the block dx squares in the x direction
            and dy squares in the y direction
        '''
        self.x += dx
        self.y += dy

        Rectangle.move(self, dx*Block.BLOCK_SIZE, dy*Block.BLOCK_SIZE)

############################################################
# SHAPE CLASS
############################################################

class Shape():
    ''' Shape class:
        Base class for all the tetris shapes
        Attributes: blocks - type: list - the list of blocks making up the shape
                    rotation_dir - type: int - the current rotation direction of the shape
                    shift_rotation_dir - type: Boolean - whether or not the shape rotates
    '''

    def __init__(self, coords, color):
        self.blocks = []
        self.rotation_dir = 1
        ### A boolean to indicate if a shape shifts rotation direction or not.
        ### Defaults to false since only 3 shapes shift rotation directions (I, S and Z)
        self.shift_rotation_dir = False
        self.new_coords = None

        for pos in coords:
            self.blocks.append(Block(pos, color))

    def get_blocks(self):
        '''returns the list of blocks
        '''
        #MY CODE HERE
        return self.blocks

    def draw(self, win):
        ''' Parameter: win - type: CanvasFrame

            Draws the shape:
            i.e. draws each block
        ''' 
        for block in self.blocks:
            block.draw(win)

    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            moves the shape dx squares in the x direction
            and dy squares in the y direction, i.e.
            moves each of the blocks
        '''
        for block in self.blocks:
            block.move(dx, dy)

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool
                        
            checks if the shape can move dx squares in the x direction
            and dy squares in the y direction, i.e.
            check if each of the blocks can move
            Returns True if all of them can, and False otherwise
           
        '''
        
        #MY CODE HERE
        for block in self.blocks:
            if block.can_move(board, dx, dy) == False:
                return False
        return True
    
    def get_rotation_dir(self):
        ''' Return value: type: int
        
            returns the current rotation direction
        '''
        return self.rotation_dir

    def can_rotate(self, board):
        ''' Parameters: board - type: Board object
            Return value: type : bool
            
            Checks if the shape can be rotated.
            
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation and check if
            the new position is valid
            3. If any of the blocks cannot be moved to their new position,
            return False
                        
            otherwise all is good, return True
        '''
        
        #MY CODE HERE
        self.new_coords = []
        center_block = self.blocks[0]
        cx = center_block.x
        cy = center_block.y
        rDir = self.get_rotation_dir()
        for i in range(4):
            if (self.blocks[i] != self.blocks[0]):
                x = cx - rDir*cy + rDir*self.blocks[i].y
                y = cy + rDir*cx - rDir*self.blocks[i].x

            else:
                x = self.blocks[0].x
                y = self.blocks[0].y

            self.new_coords.append((x, y))

            if board.can_move(x, y) == False:
                self.new_coords = []
                return False
        return True

    def rotate(self, board):
        ''' Parameters: board - type: Board object

            rotates the shape:
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation
            3. Move the block to the new position
            
        '''    

        ####  MY CODE HERE #####
        for i in range(4):
            x = self.new_coords[i][0]
            y = self.new_coords[i][1]
            dx = x - self.blocks[i].x
            dy = y - self.blocks[i].y
            self.blocks[i].move(dx, dy)
        ### This should be at the END of your rotate code. 
        ### DO NOT touch it. Default behavior is that a piece will only shift
        ### rotation direciton after a successful rotation. This ensures that 
        ### pieces which switch rotations definitely remain within their 
        ### accepted rotation positions.
        if self.shift_rotation_dir:
            self.rotation_dir *= -1


############################################################
# ALL SHAPE CLASSES
############################################################

 
class I_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x - 2, center.y),
                  Point(center.x + 1, center.y)]
        Shape.__init__(self, coords, 'blue')
        self.shift_rotation_dir = True

class J_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'orange')        

class L_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'cyan')

class O_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x   , center.y + 1),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'red')

    def can_rotate(self, board):
        # Override Shape's rotate method since O_Shape does not rotate
        return False

class S_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'green')
        self.shift_rotation_dir = True
        self.rotation_dir = -1


class T_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x    , center.y + 1)]
        Shape.__init__(self, coords, 'yellow')


class Z_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x - 1, center.y), 
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'magenta')
        self.shift_rotation_dir = True
        self.rotation_dir = -1


############################################################
# BOARD CLASS
############################################################

class Board():
    ''' Board class: it represents the Tetris board

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the pieces will be drawn
                    grid - type:Dictionary - keeps track of the current state of
                    the board; stores the blocks for a given position
    '''
    
    def __init__(self, title, width, height):
        self.width = width
        self.height = height

        # create a canvas to draw the tetris shapes on
        self.win = GraphWin(title, self.width * Block.BLOCK_SIZE + Block.OUTLINE_WIDTH - 0.8,
                            self.height * Block.BLOCK_SIZE + Block.OUTLINE_WIDTH - 0.8,
                            autoflush=False)
        self.win.setBackground('light grey')

        # create an empty dictionary
        # currently we have no shapes on the board
        self.grid = {}

    def draw_shape(self, shape):
        ''' Parameters: shape - type: Shape
            Return value: type: bool

            draws the shape on the board if there is space for it
            and returns True, otherwise it returns False
        '''
        if shape.can_move(self, 0, 0):
            shape.draw(self.win)
            self.win.flush()
            return True
        else:
            self.game_over()

    def can_move(self, x, y):
        ''' Parameters: x - type:int
                        y - type:int
            Return value: type: bool

            1. check if it is ok to move to square x,y
            if the position is outside of the board boundaries, can't move there
            return False

            2. if there is already a block at that postion, can't move there
            return False

            3. otherwise return True
            
        '''  
        #MY CODE HERE
        if (x < 0) or (y < 0) or (x >= self.width) or (y >= self.height):
            return False
        elif (x,y) in self.grid.keys():
            return False
        else:
            return True

    def add_shape(self, shape):
        ''' Parameter: shape - type:Shape
            
            add a shape to the grid, i.e.
            add each block to the grid using its
            (x, y) coordinates as a dictionary key

            Hint: use the get_blocks method on Shape to
            get the list of blocks
            
        '''
        #MY CODE HERE
        for block in shape.get_blocks():
            self.grid[(block.x, block.y)] = block

    def delete_row(self, y):
        ''' Parameters: y - type:int

            remove all the blocks in row y
            to remove a block you must remove it from the grid
            and erase it from the screen.
            If you dont remember how to erase a graphics object
            from the screen, take a look at the Graphics Library
            handout
            
        '''
        
        #MY CODE HERE
        for x in range(self.width):
            coords = (x, y)
            self.grid[coords].undraw()
            del self.grid[coords]
    
    def is_row_complete(self, y):        
        ''' Parameter: y - type: int
            Return value: type: bool

            for each block in row y
            check if there is a block in the grid (use the in operator) 
            if there is one square that is not occupied, return False
            otherwise return True
            
        '''
        #MY CODE HERE
        for x in range(self.width):
            if self.can_move(x, y):
                return False
        return True
    
    def move_down_rows(self, y_start):
        ''' Parameters: y_start - type:int                        

            for each row from y_start to the top
                for each column
                    check if there is a block in the grid
                    if there is, remove it from the grid
                    and move the block object down on the screen
                    and then place it back in the grid in the new position

        '''
        #MY CODE HERE
        grid = list(self.grid.keys())
        for y in range(y_start, -1, -1):
            for x in range(self.width):
                coords = (x, y)
                new_coords = (x, y + 1)
                if coords in grid:
                    self.grid[coords].undraw()
                    block = self.grid.pop(coords)
                    block.move(0, 1)
                    self.grid[new_coords] = block
                    self.grid[new_coords].draw(self.win)

    def remove_complete_rows(self):
        ''' removes all the complete rows
            1. for each row, y, 
            2. check if the row is complete
                if it is,
                    delete the row
                    move all rows down starting at row y - 1

        '''  
        #MY CODE HERE
        complete_rows = []
        for y in range(self.height):
            if self.is_row_complete(y):
                complete_rows.append(y)

        for y in complete_rows:
            self.delete_row(y)
            self.move_down_rows(y)

    def game_over(self):
        ''' display "Game Over !!!" message in the center of the board
            HINT: use the Text class from the graphics library
        '''
        
        #MY CODE HERE
        x = (self.width * Block.BLOCK_SIZE + Block.OUTLINE_WIDTH) / 2
        y = (self.height * Block.BLOCK_SIZE + Block.OUTLINE_WIDTH) / 2
        msg = Text(Point(x,y), "Game Over!!!")
        msg.setSize(35)
        msg.setStyle('bold')
        msg.setFill('black')
        msg.draw(self.win)
        
        msg = Text(Point(x,y), "Game Over!!!")
        msg.setSize(35)
        msg.setFill('red')
        msg.draw(self.win)        
        self.win.flush()


############################################################
# TETRIS CLASS
############################################################

class Tetris():
    ''' Tetris class: Controls the game play
        Attributes:
            SHAPES - type: list (list of Shape classes)
            DIRECTION - type: dictionary - converts string direction to (dx, dy)
            BOARD_WIDTH - type:int - the width of the board
            BOARD_HEIGHT - type:int - the height of the board
            board - type:Board - the tetris board
            win - type:Window - the window for the tetris game
            delay - type:int - the speed in milliseconds for moving the shapes
            current_shapes - type: Shape - the current moving shape on the board
    '''
    
    SHAPES = [I_shape, J_shape, L_shape, O_shape, S_shape, T_shape, Z_shape]
    DIRECTION = {'Left':(-1, 0), 'Right':(1, 0), 'Down':(0, 1)}
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    
    def __init__(self):
        self.board = Board("Tetris", self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.delay = 1000 #ms

        # sets up the keyboard events
        # when a key is called the method key_pressed will be called
        self.board.win.bind_all('<Key>', self.key_pressed)

        # set the current shape to a random new shape
        self.current_shape = self.create_new_shape()

        # Draw the current_shape oan the board (take a look at the
        # draw_shape method in the Board class)
        ####  MY CODE HERE ####
        self.board.draw_shape(self.current_shape)

        # For Step 9:  animate the shape!
        ####  MY CODE HERE ####
        self.board.win.after(self.delay, self.animate_shape)

    def create_new_shape(self):
        ''' Return value: type: Shape
            
            Create a random new shape that is centered
             at y = 0 and x = int(self.BOARD_WIDTH/2)
            return the shape
        '''
        #MY CODE HERE
        center = Point(self.BOARD_WIDTH/2, 0)
        shape = random.choice(self.SHAPES)(center)
        return shape
    
    def animate_shape(self):
        ''' animate the shape - move down at equal intervals
            specified by the delay attribute
        '''
        self.do_move('Down')
        self.board.win.flush()
        self.board.win.after(self.delay, self.animate_shape)
    
    def do_move(self, direction):
        ''' Parameters: direction - type: string
            Return value: type: bool

            Move the current shape in the direction specified by the parameter:
            First check if the shape can move. If it can, move it and return True
            Otherwise if the direction we tried to move was 'Down',
            1. add the current shape to the board
            2. remove the completed rows if any 
            3. create a new random shape and set current_shape attribute
            4. If the shape cannot be drawn on the board, display a
               game over message

            return False

        '''
        
        #MY CODE HERE
        move = Tetris.DIRECTION[direction]
        can_move = self.current_shape.can_move(self.board, move[0], move[1])
        if can_move == True:
            self.current_shape.move(move[0], move[1])
        elif direction == 'Down':
            self.board.add_shape(self.current_shape)
            self.board.remove_complete_rows()
            self.current_shape = self.create_new_shape()
            self.board.draw_shape(self.current_shape)
        else:
            return False
            

    def do_rotate(self):
        ''' Checks if the current_shape can be rotated and
            rotates if it can
        '''
        
        #MY CODE HERE
        pass
    
    def key_pressed(self, event):
        ''' this function is called when a key is pressed on the keyboard
            it currenly just prints the value of the key

            Modify the function so that if the user presses the arrow keys
            'Left', 'Right' or 'Down', the current_shape will move in
            the appropriate direction

            if the user presses the space bar 'space', the shape will move
            down until it can no longer move and is added to the board

            if the user presses the 'Up' arrow key ,
                the shape should rotate.

        '''
            
        #MY CODE HERE
        key = event.keysym
        if key == 'space':
            move = Tetris.DIRECTION['Down']
            while self.current_shape.can_move(self.board, move[0], move[1]):
                self.do_move('Down')
            return
        elif key == 'Up':
            if self.current_shape.can_rotate(self.board):
                self.current_shape.rotate(self.board)
            return
        self.do_move(key)
       
################################################################
# Start the game
################################################################

game = Tetris()
