# coding=UTF-8
#
#   File     :   cursesTetris.py
#
#   Authors     :   JHB
#
#   Description :   cursesTetris obejct - Drawings using curses library
#
#   Comment    :   Python 3.xx
#

import curses, sys, os, termios, fcntl
import tetrisGame
import consts

# Public consts
#

# Dimensions & positions
BORDER_WIDTH    = 2
GAP_WIDTH       = 2
SHAPE_WIDTH     = tetrisGame.PIECE_WIDTH * 2
SHAPE_HEIGHT    = tetrisGame.PIECE_HEIGHT

BORDER_COLOR    = 0         # Terminal's default colour ID

# Char used for shadow
SHADOW_CHAR     = '\u2591'  # unicode

COLOUR_HILIGHT   = 9

# cursesTetris object - Drawings with curses library
#
class cursesTetris(tetrisGame.tetrisGame):

    term_ = None      # curses term.
    
    # Construction
    def __init__(self):

        # nCurses initialization
        self.term_ = curses.initscr()
        curses.cbreak()
        curses.noecho()
        self.term_.keypad(True)   # all chars
        self.term_.nodelay(True)  # non-blocking keyboard access
        curses.curs_set(0)        # no cursor

        # Texts dims. (scores, lines and level)
        self.itemDims_  = [0] * 3

    # overloads of tetrisGame methods
    #

    # Verifications
    #   Return error message ("" if none)
    #
    def checkEnvironment(self):

        errorMessage = ""

        if tetrisGame.tetrisGame.STATUS_INIT == self.status_:
            return ""   # Already done

        # Colors ?
        #
        if False == curses.has_colors():
            errorMessage = "Terminal dosen't accept colorized outputs"
            return errorMessage
        
        curses.start_color()
        for i in range(1,8):
            curses.init_pair(i, i, i) # colour ID = i <=>: text = i, bk = i
        
        # Shadow : white on black
        curses.init_pair(consts.COLOUR_ID_SHADOW, curses.COLOR_WHITE, curses.COLOR_BLACK)

        # Hilight : red
        curses.init_pair(COLOUR_HILIGHT, curses.COLOR_RED, curses.COLOR_BLACK)
    
        # Dimensions
        #
        height = consts.PLAYFIELD_HEIGHT
        self.gamePos_ = (2, curses.LINES - height, consts.PLAYFIELD_WIDTH * 2, height)
        #self.canDrawNextPiece_ = curses.COLS > (self.gamePos_[2]+ BORDER_WIDTH * 2 + GAP_WIDTH + SHAPE_WIDTH + 2)

        if curses.LINES < self.gamePos_[3]:
            errorMessage = f"Minimal height for the terminal is {str(self.gamePos_[3])} chars, actual is {curses.LINES}"
            return errorMessage
        
        if curses.COLS < self.gamePos_[2]+ 4:
            errorMessage = f"Minmal width for the terminal is {str(self.gamePos_[2]+ 4)} chars, actual is {curses.COLS}"
            return errorMessage
                
        # Ok
        self.status_ = tetrisGame.tetrisGame.STATUS_INIT
        return ""   # no message

    # Display "hall of fame"
    #   Basic display on console
    def showScores(self, me, currentScore, bestScores):
        self.clear()
        super().showScores(me, currentScore, bestScores)
    
    # Finish ...
    #
    def clear(self):
        self.term_.keypad(False)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

    # Wait for an event (a keyboard event on curses)
    #
    def waitForEvent(self):
        wait = True
        while wait:
            c = self.checkKeyboard()
            if len(c) :
                wait = False
        return (cursesTetris.EVT_KEYDOWN, c)

    # Read the keyboard (non-blocking)
    #   returns the char or ''
    def checkKeyboard(self):
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

        try:        
            while True:            
                try:
                    c = sys.stdin.read(1)
                    break
                except IOError: 
                    pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        return c

    def updateDisplay(self):
        self.term_.refresh()

    # Draw the text and erase previous if exists
    #
    def _drawNumValue(self, index, value):
        boxTop = self.gamePos_[1] + tetrisGame.PIECE_HEIGHT + 5 + 3 * index
        boxLeft = self.gamePos_[2]+ BORDER_WIDTH * 2 + GAP_WIDTH
        text = self.itemTexts_[index] + ": " +  str(value) + ' ' * self.itemDims_[index]
        self.term_.addstr(boxTop, boxLeft, text, curses.color_pair(0))
        self.itemDims_[index] = len(text) # text length

    # Draw the background
    #
    def drawBackGround(self):
         # top
        if self.gamePos_[1] >= 1:
            # Le charme de faire du Python !!!
            top = '\u250c' + '\u2500' * self.gamePos_[2] + '\u2510'
            self.term_.addstr(self.gamePos_[1] - 1, self.gamePos_[0] - 1, top, curses.color_pair(0))
        
        # Left & right
        if self.gamePos_[0] >= 2 and curses.COLS >= self.gamePos_[2]+ 4:

            self.term_.attron(curses.color_pair(BORDER_COLOR))
            
            for y in range(self.gamePos_[3]):
                self.term_.move(self.gamePos_[1] + y, self.gamePos_[0] - 2)
                self.term_.addch(' ')
                self.term_.addch('\u2502')

                self.term_.move(self.gamePos_[1] + y, self.gamePos_[0] + self.gamePos_[2])
                self.term_.addch('\u2502')
                self.term_.addch(' ')
            
            self.term_.attroff(curses.color_pair(BORDER_COLOR))

    # Change the origin and the coordinate system
    #   (x,y) are to be translated
    #   inBoard : int he board (True) or in the "next piece" area
    #
    #   returns a tuple (x,y, dx, dy) in the new coordonate system
    #       dx, dy  are the width and height of the block in the screen
    #
    def _changeCoordonateSystem(self, x, y, inBoard = True):
        
        if inBoard:
            left = self.gamePos_[0] + 2 * x
            top = self.gamePos_[1] + consts.PLAYFIELD_HEIGHT - 1 - y
        else:
            left = self.gamePos_[2]+ BORDER_WIDTH * 2 + GAP_WIDTH
            top = self.gamePos_[1] + 2
        
        return (left,top,2,1)    # 1 "cube" = 2 chars (double the width)

    # Draw a coloured block
    #
    def _drawBlock(self, left, top, colourID, inBoard, shadow = False):
        self.term_.addstr(top, left, (SHADOW_CHAR if shadow else ' ') * 2, curses.color_pair(colourID))

    # Erase a block
    #
    def _eraseBlocks(self, left, top, width, height, colourID, inBoard):
        x,y,w,_ = self._changeCoordonateSystem(0,0, False)
        for row in range(height):
            self.term_.addstr(y + row, x, ' ' * w * width, curses.color_pair(colourID))
# EOF