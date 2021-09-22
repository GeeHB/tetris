# coding=UTF-8
#
#   File     :   pygameTetris.py
#
#   Authors     :   JHB
#
#   Description :   pygameTetris object - Drawings using PYGame library
#                   
#   Comment    :   Python 3.xx
#
#   Version     :   0.7.1
#
#   Date        :   2021/09/22
#

import pygame
import math
import sharedConsts
import tetrisGame

# Public consts
#
BOX_WIDTH       = 25    # Default dimensions of a small square

# A few colours
#
COLOUR_BLACK        = (0, 0, 0)
COLOUR_WHITE        = (255, 255, 255)

# Font for the text (and default size)
#
FONT_NAME       = 'helvetica'
FONT_SIZE       = 20
MAX_FONT_SIZE   = 25

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
    winHeight_, winWidth_ = 0,0         # dimensions
    boxWidth_       = BOX_WIDTH
    fontSize_       = FONT_SIZE
    
    colours_        = []                # Table of colours

    itemDims_      = [None, None, None] # Texts dims. (scores, lines and level)
    
    # Construction
    #
    def __init__(self):
        
        # Table of colours
        #
        self.colours_ = [tetrisColour(COLOUR_BLACK)] * (1 + sharedConsts.LAST_COLOUR_ID)
        
        self.colours_[1] = tetrisColour((255, 0, 0), (255, 128, 128), (128,0,0))        # Red
        self.colours_[2] = tetrisColour((0, 255, 0), (255, 128, 128), (0,128,0))        # Green
        self.colours_[3] = tetrisColour((255, 255, 0), (255, 255, 128), (128,128,0))    # Yellow
        self.colours_[4] = tetrisColour((0, 0, 255), (128, 128, 255), (0,128,0))        # Blue
        self.colours_[5] = tetrisColour((255, 0, 255), (255, 128, 255), (128,0,128))    # Purple
        self.colours_[6] = tetrisColour((0, 255, 255), (128, 255, 255), (0,128,128))    # Cyan
        self.colours_[7] = tetrisColour((255, 128, 0), (255, 192, 128), (128,64,0))     # Orange

        self.colours_[sharedConsts.COLOUR_ID_SHADOW] = tetrisColour((48,48,48))
        self.colours_[sharedConsts.COLOUR_ID_TEXT] = tetrisColour(COLOUR_WHITE)
        self.colours_[sharedConsts.COLOUR_ID_BORDER] = tetrisColour((192,192,192))
        self.colours_[sharedConsts.COLOUR_ID_BOARD] = tetrisColour((32,32,32))

        # Compute dimensions
        self.winWidth_    = 2 * self.boxWidth_ * sharedConsts.PLAYFIELD_WIDTH
        self.winHeight_   = (2 + self.boxWidth_) * sharedConsts.PLAYFIELD_HEIGHT
        
        self.gameWidth_ = sharedConsts.PLAYFIELD_HEIGHT * self.boxWidth_
        self.gameHeight_ = sharedConsts.PLAYFIELD_HEIGHT * self.boxWidth_
        self.gameLeft_ = 2 * self.boxWidth_
        self.gameTop_ = self.winHeight_ - self.gameHeight_  - 1

    # overloards from eventHandler
    #

    # A line has just been completed (but is still visible)
    #
    def lineCompleted(self, rowIndex):
        pass

    # overloads from gameRendering
    #

    # Verifications
    #   Return True (init done) or False (errors)
    #
    def checkEnvironment(self):
        
        # PYGame intialization (returns the tuple (#ok, #errors))
        rets = pygame.init()

        if 0 != rets[1] :
            return "PYGame initialization error. Returned " + str(rets[1]) + " error(s)"

        # Main window creation
        self.win_ = pygame.display.set_mode((self.winWidth_, self.winHeight_), pygame.RESIZABLE)
        pygame.display.set_caption('jTetris')
        
        # Ok
        self.status_ = tetrisGame.tetrisGame.STATUS_INIT
        return ""

    # End ...
    def clear(self):
        pygame.display.quit()

    # Wait for an event
    #
    def waitForEvent(self):
        finished = False
        while not finished:
            event = pygame.event.wait()
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN :
                finished = True
            elif event.type == pygame.VIDEORESIZE:
                # Update members
                self._onResizeWindow(event.w, event.h)
                
                # Resize the surface
                self.win_ = pygame.display.set_mode((self.winWidth_, self.winHeight_), pygame.RESIZABLE)

                # redraw
                self._drawBackGround()
                self.drawBoard()
                self.drawScore()
                self.drawLevel()
                self.drawLines()
                
                self._updateDisplay()
        return (event.type, event.key)

    # Read the keyboard (non-blocking)
    #   returns the char or ''
    def checkKeyboard(self):
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
     
    
    # overloads of tetrisGame methods
    #

    def _updateDisplay(self):
        pygame.display.update()

    # Draw the text and erase previous if exists
    #
    def _drawText(self, index, text):
        font = pygame.font.SysFont(FONT_NAME, self.fontSize_)
        label = font.render(text, 1, self.colours_[sharedConsts.COLOUR_ID_TEXT].base_)

        left = self.gameLeft_ + (1 + sharedConsts.PLAYFIELD_WIDTH ) * self.boxWidth_
        top = self.gameTop_ + self.boxWidth_ * ( 2 * index + 1)
        
        # Erase 
        if None != self.itemDims_[index] and 2 == len(self.itemDims_[index]) :
            pygame.draw.rect(self.win_, self.colours_[sharedConsts.COLOUR_ID_BKGRND].base_, (left, top, self.itemDims_[index][0], self.itemDims_[index][1]))
    
        # Draw the text
        self.itemDims_[index] = font.size(text) # Get the size
        self.win_.blit(label, (left, top))
    
    # Draw the background
    #
    def _drawBackGround(self):
        
        # Playfield frame
        left = self.gameLeft_ - 1
        top = self.gameTop_ - 1
        width = sharedConsts.PLAYFIELD_WIDTH * self.boxWidth_ + 2
        right = left + width - 1
        height = sharedConsts.PLAYFIELD_HEIGHT * self.boxWidth_ + 2
        bottom = top + height - 1
        
        pygame.draw.line(self.win_, self.colours_[sharedConsts.COLOUR_ID_BORDER].base_, (left, top),(left, bottom))
        pygame.draw.line(self.win_, self.colours_[sharedConsts.COLOUR_ID_BORDER].base_, (left, bottom),(right, bottom))
        pygame.draw.line(self.win_, self.colours_[sharedConsts.COLOUR_ID_BORDER].base_, (right, top),(right, bottom))
        pygame.draw.line(self.win_, self.colours_[sharedConsts.COLOUR_ID_BORDER].base_, (left, top),(right, top))

        # background
        #x,y,w,h = self._changeCoordonateSystem(left, top, True)
        #pygame.draw.rect(self.win_, self.colours_[COLOUR_ID_BOARD].base_, (x, y, w * board.PLAYFIELD_WIDTH, h * board.PLAYFIELD_HEIGHT))
        
        # Next piece text
        left = self.gameLeft_ + (1 + sharedConsts.PLAYFIELD_WIDTH ) * self.boxWidth_
        top = self.gameTop_ + self.boxWidth_ * 8
        font = pygame.font.SysFont(FONT_NAME, self.fontSize_)
        label = font.render(self.itemTexts_[3], 1, self.colours_[sharedConsts.COLOUR_ID_TEXT].base_)
        self.win_.blit(label, (left, top))

        # Next piece frame
        left-=2
        top = self.gameTop_ + self.boxWidth_ * 10 -2
        width = 4 * self.boxWidth_ + 4
        height = 4 * self.boxWidth_ + 4
        pygame.draw.line(self.win_, self.colours_[sharedConsts.COLOUR_ID_BORDER].base_, (left, top),(left, top +  height - 1))
        pygame.draw.line(self.win_, self.colours_[sharedConsts.COLOUR_ID_BORDER].base_, (left + width - 1, top),(left + width - 1, top +  height - 1))
        pygame.draw.line(self.win_, self.colours_[sharedConsts.COLOUR_ID_BORDER].base_, (left, top),(left + width - 1, top))
        pygame.draw.line(self.win_, self.colours_[sharedConsts.COLOUR_ID_BORDER].base_, (left, top + height - 1),(left + width - 1, top + height - 1))

    # Draw a coloured block
    #
    def _drawBlock(self, left, top, colourID, inBoard, shadow = False):
        paintColour = self.colours_[colourID]
        if None != paintColour.light_:
            # the single square
            pygame.draw.rect(self.win_, paintColour.base_, (left + 1, top + 1, self.boxWidth_ - 2, self.boxWidth_ -2))

            # 3D effect
            pygame.draw.line(self.win_, paintColour.light_, (left, top),(left, top + self.boxWidth_ - 1))
            pygame.draw.line(self.win_, paintColour.light_, (left, top),(left + self.boxWidth_ - 1, top))

            pygame.draw.line(self.win_, paintColour.dark_, (left + self.boxWidth_ - 1, top),(left + self.boxWidth_ - 1, top + self.boxWidth_ - 1))
            pygame.draw.line(self.win_, paintColour.dark_, (left, top + self.boxWidth_ - 1),(left + self.boxWidth_ - 1, top + self.boxWidth_ - 1))
        else:
            # Just a squere
            pygame.draw.rect(self.win_, paintColour.base_, (left, top, self.boxWidth_, self.boxWidth_))

    # Erase a block
    #
    def _eraseBlocks(self, left, top, width, height, colourID, inBoard):
        
        x,y,w,h = self._changeCoordonateSystem(left, top, inBoard)
        pygame.draw.rect(self.win_, self.colours_[colourID].base_, (x, y, w * width, h * height))

    # Change the origin and the coordinate system
    #
    #   (x,y) are to be translated
    #   inBoard : int he board (True) or in the "next piece" area
    #
    #   returns a tuple (x,y, dx, dy) in the new coordonate system
    #       dx, dy  are the width and height of the block in the screen
    #
    def _changeCoordonateSystem(self, x, y, inBoard = True):
        
        if inBoard:
            # For the game
            left = self.gameLeft_ + x * self.boxWidth_
            top = self.gameTop_ + (sharedConsts.PLAYFIELD_HEIGHT - 1 - y) * self.boxWidth_
        else:
            # Next piece
            left = self.gameLeft_ + (1 + sharedConsts.PLAYFIELD_WIDTH ) * self.boxWidth_
            top = self.gameTop_ + self.boxWidth_ * 10

        return (left, top, self.boxWidth_, self.boxWidth_)

    # Handle window's resize
    #
    def _onResizeWindow(self, newWidth, newHeight):

        self.winWidth_ = newWidth
        self.winHeight_ = newHeight

        # Compute new "square" size
        self.boxWidth_ = math.floor((newHeight - 1) / (sharedConsts.PLAYFIELD_HEIGHT+ 2))
        if self.boxWidth_ < 8 :
            self.boxWidth_ = 8

        # other dims
        self.gameWidth_ = sharedConsts.PLAYFIELD_HEIGHT * self.boxWidth_
        self.gameHeight_ = sharedConsts.PLAYFIELD_HEIGHT * self.boxWidth_
        self.gameLeft_ = 2 * self.boxWidth_
        self.gameTop_ = self.winHeight_ - self.gameHeight_  - 1
        self.fontSize_ = int(self.boxWidth_ / BOX_WIDTH * FONT_SIZE)
        if self.fontSize_ > MAX_FONT_SIZE:
            self.fontSize_ = MAX_FONT_SIZE
        elif self.fontSize_ <= 8:
            self.fontSize_ = 8

# EOF