# coding=UTF-8
#
#   File     :   pygameTetris.py
#
#   Author     :   JHB
#
#   Description :   pygameTetris object - Drawings using PYGame library
#                   
#   Comment    :   Python 3.xx
#

import pygame
import math
import consts
import tetrisGame
from sharedTools import systemInfos

# Public consts
#
BOX_SIZE       = 25    # Default dimensions of a small square

# Font for the text (and default size)
#
FONT_NAME       = 'helvetica'
FONT_SIZE       = 20
MAX_FONT_SIZE   = 25

# Max. percentage of screen size used by the window
WINDOW_SCREEN_PERCENT = 80

# A colour
#
class tetrisColour(object):
    base_, light_, dark_ = None, None, None

    def __init__(self, base, light = None, dark = None):
        self.base_ = base
        self.light_ = light
        self.dark_ = dark

# pygameTetris object - drawing of tertraminos using PYGame library
#
class pygameTetris(tetrisGame.tetrisGame):

    # PYGame events types
    EVT_KEYDOWN     = pygame.KEYDOWN
    EVT_QUIT        = pygame.QUIT
    
    # Key codes
    #
    KEY_LEFT        = pygame.K_LEFT
    KEY_RIGHT       = pygame.K_RIGHT
    KEY_ROTATE_LEFT = pygame.K_UP
    #KEY_ROTATE_RIGHT= '0'
    KEY_DOWN        = pygame.K_DOWN
    KEY_FALL        = pygame.K_SPACE
    KEY_START       = pygame.K_RETURN
    KEY_QUIT        = pygame.K_ESCAPE
    #KEY_QUIT        = pygame.K_q
    KEY_STOP        = KEY_QUIT
    KEY_SHADOW_MODE = pygame.K_o
    KEY_NORMAL_MODE = pygame.K_n
    KEY_SCORES      = pygame.K_h

    # Members
    win_            = None              # "Window"
    winDims         = (0, 0)            # (w,h)
    boxSize_        = BOX_SIZE
    fontSize_       = FONT_SIZE
    allowResize_    = True
    
    colours_        = []                # Table of tetrisColour objects

    itemDims_       = [None, None, None] # Texts dims. (scores, lines and level)
    allowResize_    = True      # The window can be resized !!!
    
    # Resizable ?
    #
    @property
    def resizable(self):
        return self.allowResize_
    @resizable.setter
    def resizable(self, value):
        self.allowResize_ = value
    
    # Construction
    #
    def __init__(self):
        
        # Table of colours
        #
        self.colours_ = [tetrisColour(consts.COLOUR_BLACK)] * (1 + consts.LAST_COLOUR_ID)
        
        self.colours_[1] = tetrisColour(consts.COLOUR_RED, (255, 128, 128), (128,0,0))
        self.colours_[2] = tetrisColour(consts.COLOUR_GREEN, (255, 128, 128), (0,128,0))
        self.colours_[3] = tetrisColour(consts.COLOUR_YELLOW, (255, 255, 128), (128,128,0))
        self.colours_[4] = tetrisColour(consts.COLOUR_BLUE, (128, 128, 255), (0,128,0))
        self.colours_[5] = tetrisColour(consts.COLOUR_PURPLE, (255, 128, 255), (128,0,128))
        self.colours_[6] = tetrisColour(consts.COLOUR_CYAN, (128, 255, 255), (0,128,128))
        self.colours_[7] = tetrisColour(consts.COLOUR_ORANGE, (255, 192, 128), (128,64,0))

        self.colours_[consts.COLOUR_ID_SHADOW] = tetrisColour((48,48,48))
        self.colours_[consts.COLOUR_ID_TEXT] = tetrisColour(consts.COLOUR_WHITE)
        self.colours_[consts.COLOUR_ID_BORDER] = tetrisColour((192,192,192))
        self.colours_[consts.COLOUR_ID_BOARD] = tetrisColour((32,32,32))
        self.colours_[consts.COLOUR_ID_ANIMATE] = tetrisColour((72, 72, 70), (92,92,95),(52,52,55))

        # Desktop dims.
        desktop = systemInfos.getDesktopSize()

        # OS type ?
        infos = systemInfos.getSystemInformations()
        # No resize on ChromeOS
        self.allowResize_ = False if infos[systemInfos.KEY_WM] == systemInfos.WM_CHROMEOS else True

        # Compute dimensions
        self.winDims_ = self._setSize()
        
        # Window is to high ?
        if desktop is not None:
            maxWindowHeight = int(desktop[1] * WINDOW_SCREEN_PERCENT / 100)
            if self.winDims_[1] > maxWindowHeight:
                # update box size
                self.boxSize_ = int(self.boxSize_ * maxWindowHeight / self.winDims_[1])

                # update fontsize
                self.fontSize_ = int(self.fontSize_ * maxWindowHeight / self.winDims_[1])

                # new dims
                self.winDims = self._setSize()

        height = consts.PLAYFIELD_HEIGHT * self.boxSize_
        self.gamePos_ = (2 * self.boxSize_, self.winDims_[1] - height  - 1, consts.PLAYFIELD_HEIGHT * self.boxSize_, height)

    #
    # Overloads from eventHandler
    #

    # A line has just been completed (but is still visible)
    #
    def lineCompleted(self, rowIndex):
        
        # Play ground coordinates (x,y)
        pos = (self.gamePos_[0], self.gamePos_[1])

        # animated block dimensions (w,h)
        dims = (consts.PLAYFIELD_WIDTH * self.boxSize_, (consts.PLAYFIELD_HEIGHT - rowIndex - 1) * self.boxSize_ + 1)

        # To control animation speed
        clock = pygame.time.Clock()
        
        # Draw / erase the line
        #
        
        # A grey piece ...
        tempPiece = pygame.Surface((self.boxSize_, self.boxSize_))

        # draw a single grey piece inside
        self._pyDrawBlock(tempPiece, 0, 0, consts.COLOUR_ID_ANIMATE, True)

        # replace blocks by the temp piece
        lineTop = pos[1] + dims[1] - 1
        for offset in range(self.boxSize_):
            for blockID in range(consts.PLAYFIELD_WIDTH):
                self.win_.blit(tempPiece, (pos[0] + blockID * self.boxSize_, lineTop), (0, 0, offset, self.boxSize_))
            self.updateDisplay()
            clock.tick(120)
        
        # Animate the surface (scroll down the memory surface into the playground)
        #

        # Create a "memory" surface
        tempSurface = pygame.Surface(dims)
        tempSurface.fill(self.colours_[consts.COLOUR_ID_BOARD].base_)

        # Copy blocks above the line to delete in memory surface
        tempSurface.blit(self.win_, (0, 1), (pos[0], pos[1], dims[0], dims[1]))

        # Animation
        for index in range(self.boxSize_):
            self.win_.blit(tempSurface, (pos[0], pos[1] + index))
            self.updateDisplay()
            clock.tick(60)  # not to quick !!!

        # Free the surfaces
        del tempPiece
        del tempSurface

    # overloads from gameRendering
    #

    # Verifications
    #   Return (Done, error message)
    #
    def checkEnvironment(self):
        
        # PYGame intialization (returns the tuple (#ok, #errors))
        rets = pygame.init()

        if 0 != rets[1] :
            return False, "PYGame initialization error. Returned " + str(rets[1]) + " error(s)"

        # Main window creation
        self.win_ = pygame.display.set_mode((self.winDims_[0], self.winDims_[1]), pygame.RESIZABLE if self.allowResize_ else pygame.SHOWN)
        #self.win_ = pygame.display.set_mode((self.winDims_[0], self.winDims_[1]), pygame.RESIZABLE)
        # pygame.NOFRAME
        pygame.display.set_caption('jTetris')
        
        # Ok
        self.status_ = tetrisGame.tetrisGame.STATUS_INIT
        return True, ""

    # End ...
    def clear(self):
        pygame.display.quit()

    # Wait for an event
    #
    def waitForEvent(self):
        finished = False
        
        try:
            while not finished:
                event = pygame.event.wait()
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN :
                    finished = True
                elif event.type == pygame.VIDEORESIZE:
                    if self.allowResize_:
                        # Update members
                        self._onResizeWindow(event.w, event.h)
                        
                        # Resize the surface
                        self.win_ = pygame.display.set_mode((self.winDims_[0], self.winDims_[1]), pygame.RESIZABLE if self.allowResize_ else 0)

                    # redraw (this event is sent at window creation)
                    self.reDraw()
                    self.updateDisplay()
        except KeyboardInterrupt:
            return pygame.QUIT, 0
        
        return (event.type, event.key)

    # Read the keyboard (non-blocking)
    #   returns the char or ''
    def checkKeyboard(self):
        try:
            evt = pygame.event.poll()
            if evt.type == pygame.KEYDOWN:
                # A digit
                if evt.key >= pygame.K_0 and evt.key <= pygame.K_9:
                    return (ord('0') + evt.key - pygame.K_0)
                else:
                    return evt.key
            elif evt.type == pygame.QUIT:
                # End the game
                self.end()
            else :
                return self.KEY_NOEVENT
        except KeyboardInterrupt:
            self.end()
            return ''
     
    #
    # Overloads of tetrisGame methods
    #

    def updateDisplay(self):
        pygame.display.update()

    # Draw the text and erase previous if exists
    #
    def _drawText(self, index, text):
        font = pygame.font.SysFont(FONT_NAME, self.fontSize_)
        label = font.render(text, 1, self.colours_[consts.COLOUR_ID_TEXT].base_)

        left = self.gamePos_[0] + (1 + consts.PLAYFIELD_WIDTH ) * self.boxSize_
        top = self.gamePos_[1] + self.boxSize_ * ( 2 * index + 1)
        
        # Erase 
        if None != self.itemDims_[index] and 2 == len(self.itemDims_[index]) :
            pygame.draw.rect(self.win_, self.colours_[consts.COLOUR_ID_BKGRND].base_, (left, top, self.itemDims_[index][0], self.itemDims_[index][1]))
    
        # Draw the text
        self.itemDims_[index] = font.size(text) # Get the size
        self.win_.blit(label, (left, top))
    
    # Draw the background
    #
    def drawBackGround(self):
        
        # Playfield frame
        left = self.gamePos_[0] - 1
        top = self.gamePos_[1] - 1
        width = consts.PLAYFIELD_WIDTH * self.boxSize_ + 2
        right = left + width - 1
        height = consts.PLAYFIELD_HEIGHT * self.boxSize_ + 2
        bottom = top + height - 1
        
        pygame.draw.line(self.win_, self.colours_[consts.COLOUR_ID_BORDER].base_, (left, top),(left, bottom))
        pygame.draw.line(self.win_, self.colours_[consts.COLOUR_ID_BORDER].base_, (left, bottom),(right, bottom))
        pygame.draw.line(self.win_, self.colours_[consts.COLOUR_ID_BORDER].base_, (right, top),(right, bottom))
        pygame.draw.line(self.win_, self.colours_[consts.COLOUR_ID_BORDER].base_, (left, top),(right, top))

        # background
        #x,y,w,h = self._changeCoordonateSystem(left, top, True)
        #pygame.draw.rect(self.win_, self.colours_[COLOUR_ID_BOARD].base_, (x, y, w * board.PLAYFIELD_WIDTH, h * board.PLAYFIELD_HEIGHT))
        
        # Next piece text
        left = self.gamePos_[0] + (1 + consts.PLAYFIELD_WIDTH ) * self.boxSize_
        top = self.gamePos_[1] + self.boxSize_ * 8
        font = pygame.font.SysFont(FONT_NAME, self.fontSize_)
        label = font.render(self.itemTexts_[3], 1, self.colours_[consts.COLOUR_ID_TEXT].base_)
        self.win_.blit(label, (left, top))

        # Next piece frame
        left-=2
        top = self.gamePos_[1] + self.boxSize_ * 10 -2
        width = 4 * self.boxSize_ + 4
        height = 4 * self.boxSize_ + 4
        pygame.draw.line(self.win_, self.colours_[consts.COLOUR_ID_BORDER].base_, (left, top),(left, top +  height - 1))
        pygame.draw.line(self.win_, self.colours_[consts.COLOUR_ID_BORDER].base_, (left + width - 1, top),(left + width - 1, top +  height - 1))
        pygame.draw.line(self.win_, self.colours_[consts.COLOUR_ID_BORDER].base_, (left, top),(left + width - 1, top))
        pygame.draw.line(self.win_, self.colours_[consts.COLOUR_ID_BORDER].base_, (left, top + height - 1),(left + width - 1, top + height - 1))

    # Draw a coloured block
    #
    
    # overloaded method ...
    #
    def _drawSingleBlock(self, left, top, width, height, colourID, shadow = False):
        self._pyDrawBlock(self.win_, left, top, width, height, colourID, shadow)

    # ... where the stuff is done !
    #   surface : Surface where to draw
    #
    def _pyDrawBlock(self, surface, left, top, width, height, colourID, shadow = False):
        paintColour = self.colours_[colourID]
        if None != paintColour.light_:
            # the single square
            pygame.draw.rect(surface, paintColour.base_, (left + 1, top + 1, width - 2, height -2))

            # 3D effect
            pygame.draw.line(surface, paintColour.light_, (left, top),(left, top + height - 1))
            pygame.draw.line(surface, paintColour.light_, (left, top),(left + width - 1, top))

            pygame.draw.line(surface, paintColour.dark_, (left + width - 1, top),(left + width - 1, top + height - 1))
            pygame.draw.line(surface, paintColour.dark_, (left, top + height - 1),(left + width - 1, top + height - 1))
        else:
            # Just a square
            pygame.draw.rect(surface, paintColour.base_, (left, top, width, height))

    # Erase a block
    #
    def _eraseBlocks(self, left, top, width, height, colourID):        
        x,y,w,h = self._changeCoordonateSystem(left, top, False)
        pygame.draw.rect(self.win_, self.colours_[colourID].base_, (x, y, w * width, h * height))

    # Change the origin and the coordinate system
    #
    #   (x,y) are to be translated
    #   inBoard : in the board (True) or in the "next piece" area
    #
    #   returns a tuple (x,y, dx, dy) in the new coordonate system
    #       dx, dy  are the width and height of the block in the screen
    #
    def _changeCoordonateSystem(self, x, y, inBoard = True):
        
        if inBoard:
            # For the game
            left = self.gamePos_[0] + x * self.boxSize_
            top = self.gamePos_[1] + (consts.PLAYFIELD_HEIGHT - 1 - y) * self.boxSize_
        else:
            # Next piece
            left = self.gamePos_[0] + (1 + consts.PLAYFIELD_WIDTH ) * self.boxSize_
            top = self.gamePos_[1] + self.boxSize_ * 10

        return (left, top, self.boxSize_, self.boxSize_)

    #
    # Internal methods
    #
    
    # Box size to window size
    #
    #   return a tuple (width, height)
    #
    def _setSize(self):
        return (2 * self.boxSize_ * consts.PLAYFIELD_WIDTH, (2 + self.boxSize_) * consts.PLAYFIELD_HEIGHT) 

    # Handle window's resize
    #
    def _onResizeWindow(self, newWidth, newHeight):

        self.winDims_ = (newWidth, newHeight)

        # Compute new "square" size
        self.boxSize_ = math.floor((newHeight - 1) / (consts.PLAYFIELD_HEIGHT+ 2))
        if self.boxSize_ < 8 :
            self.boxSize_ = 8

        # Other dims
        height = consts.PLAYFIELD_HEIGHT * self.boxSize_
        self.gamePos_ = (2 * self.boxSize_, self.winDims_[1] - height  - 1, consts.PLAYFIELD_HEIGHT * self.boxSize_, height)
        self.fontSize_ = int(self.boxSize_ / BOX_SIZE * FONT_SIZE)
        if self.fontSize_ > MAX_FONT_SIZE:
            self.fontSize_ = MAX_FONT_SIZE
        elif self.fontSize_ <= 8:
            self.fontSize_ = 8

# EOF