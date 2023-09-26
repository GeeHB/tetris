#   File     :   casioplotTetris.py
#
#   Author     :   JHB
#
#   Description :   casioplotTetris object - Drawings using casioplot library
#                   
#   Comment    :   Python 3.xx
#

from casioplot import *
import consts
import tetrisGame

#
# CASIO calculator consts
# 

# Screen dimensions in pixels
#
CASIO_WIDTH = 384
CASIO_HEIGH = 192

# Single block dims in pixels (without borders)
CASIO_BOX_WIDTH = 8
CASIO_BOX_HEIGHT = CASIO_BOX_WIDTH

# SingleBlocks real dims (including borders)
CASIO_BOX_RWIDTH = (1 + CASIO_BOX_WIDTH)
CASIO_BOX_RHEIGHT = CASIO_BOX_RWIDTH

# Positions and dims.
CASIO_PLAYFIELD_BORDER = 3
CASIO_BORDER_GAP = 2
CASIO_PLAYFIELD_LEFT = CASIO_PLAYFIELD_BORDER + CASIO_BORDER_GAP
CASIO_PLAYFIELD_TOP = CASIO_PLAYFIELD_LEFT

# casioplotTetris object - drawing of tertraminos using casioplot library
#
class casioplotTetris(tetrisGame.tetrisGame):

    # Construction
    #
    def __init__(self):
        
        # Table of colours
        #
        self.colours_ = [consts.COLOUR_WHITE] * (1 + consts.LAST_COLOUR_ID)
        #self.colours_[consts.COLOUR_ID_BOARD] = consts.COLOUR_WHITE

        # Pieces
        self.colours_[1] = consts.COLOUR_RED
        self.colours_[2] = consts.COLOUR_GREEN
        self.colours_[3] = consts.COLOUR_YELLOW
        self.colours_[4] = consts.COLOUR_BLUE
        self.colours_[5] = consts.COLOUR_PURPLE
        self.colours_[6] = consts.COLOUR_CYAN
        self.colours_[7] = consts.COLOUR_ORANGE

        self.colours_[consts.COLOUR_ID_SHADOW] = consts.COLOUR_GREY
        self.colours_[consts.COLOUR_ID_TEXT] = consts.COLOUR_BLACK
        self.colours_[consts.COLOUR_ID_BORDER] = consts.COLOUR_DKGREY

    #
    # overloads from tetrisGame
    #

    def updateDisplay(self):
        show_screen()

    # Draw borders
    def drawBackGround(self):
        
        # Border around the playfield
        self.__drawRectangle(CASIO_PLAYFIELD_BORDER, CASIO_PLAYFIELD_BORDER, 
                             consts.PLAYFIELD_WIDTH * CASIO_BOX_RWIDTH + 2 * CASIO_BORDER_GAP, 
                             consts.PLAYFIELD_HEIGHT * CASIO_BOX_RHEIGHT + 2 * CASIO_BORDER_GAP, 
                             None, self.colours_[consts.COLOUR_ID_BORDER])

    # Change the origin and the coordinate system
    #   (x,y) are to be translated
    #   inBoard : int he board (True) or in the "next piece" area (False)
    #
    #   returns a tuple (x,y, dx, dy) in the new coordonate system
    #       dx, dy  are the width and height of the block in the screen
    # 
    def _changeCoordonateSystem(self, x, y, inBoard = True):
        if inBoard:
            # For the game
            left = CASIO_PLAYFIELD_LEFT + x * CASIO_BOX_RWIDTH
            top = CASIO_PLAYFIELD_TOP + (consts.PLAYFIELD_HEIGHT - 1 - y) * CASIO_BOX_RHEIGHT
        else:
            # Next piece
            left, top = 1, 1

        return (left, top, CASIO_BOX_RWIDTH, CASIO_BOX_RHEIGHT)

    # Draw a single colored block
    #
    def _drawSingleBlock(self, left, top, colourID, shadow = False):
        self.__drawRectangle(left, top, CASIO_BOX_RWIDTH, CASIO_BOX_RWIDTH, self.colours_[colourID])

    # Erase a tetramino
    #
    def _eraseBlocks(self, left, top, width, height, colourID):
        x,y,w,h = self._changeCoordonateSystem(left, top)
        self.__drawRectangle(x, y, w, h, self.colours_[colourID], None)

    # overloads from gameRendering
    #

    # Verifications
    #   Return (Done, error message)
    #
    def checkEnvironment(self):
        return True, ""
   
    # overloads from eventhandler
    # Resizable ?
    #
    @property
    def resizable(self):
        # No !!!
        # The "window" can't be resized
        return False

    #
    # Internal methods
    #

    # Draw a colored rectangle
    #
    #   x,y : top left starting point
    #   width, height : dimensions
    #   borderColour : Colour of the border in RGB format or None (if no border)
    #   fillColour : Filling colour in RGB format or None (if empty) 
    #
    def __drawRectangle(self, x, y, width, height, fillColour = None, borderColour = None):
        # A border ?
        if borderColour is not None:
            for px in range(width):
                set_pixel(x + px, y, borderColour)
                set_pixel(x + px, y + height - 1, borderColour)

            for py in range(height-2):
                set_pixel(x, y + py + 1, borderColour)
                set_pixel(x + width - 1, y + py + 1, borderColour)

        # Filling ?
        if fillColour is not None:
            for px in range(width - 1):
                for py in range(height - 1):
                    set_pixel(x + px, y + py, fillColour)


# EOF