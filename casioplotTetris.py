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
#import tetrisGame
import consoleTetris

#
# CASIO calculator consts
# 

# casioplotTetris object - drawing of tertraminos using casioplot library
#
#class casioplotTetris(tetrisGame.tetrisGame):
class casioplotTetris(consoleTetris.consoleTetris):

    KEY_START       = 'w'
    
    # Screen dimensions in pixels
    #
    CASIO_WIDTH = 384
    CASIO_HEIGHT = 192

    # Single block dims in pixels (without borders)
    CASIO_BOX_WIDTH = 8
    CASIO_BOX_HEIGHT = CASIO_BOX_WIDTH

    # SingleBlocks real dims (including borders)
    CASIO_BOX_RWIDTH = (1 + CASIO_BOX_WIDTH)
    CASIO_BOX_RHEIGHT = CASIO_BOX_RWIDTH

    # Playfield positions and dims.
    CASIO_PLAYFIELD_BORDER = 3
    CASIO_BORDER_GAP = 2
    CASIO_PLAYFIELD_LEFT = 100 + CASIO_PLAYFIELD_BORDER + CASIO_BORDER_GAP
    CASIO_PLAYFIELD_TOP = CASIO_PLAYFIELD_BORDER + CASIO_BORDER_GAP

    # Next piece and value info box
    CASIO_TEXT_SIZE = "small"
    CASIO_INFO_GAP = 4
    CASIO_INFO_LEFT = 250
    CASIO_INFO_TOP = CASIO_PLAYFIELD_BORDER

    CASIO_NP_TOP = 100

    # Construction
    #
    def __init__(self):
        
        # Call parent constructor
        super().__init__()

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

        # Dims. & pos.
        self.gamePos_ = [self.CASIO_PLAYFIELD_LEFT - self.CASIO_BORDER_GAP,
                         self.CASIO_PLAYFIELD_TOP - self.CASIO_BORDER_GAP,
                         consts.PLAYFIELD_WIDTH * self.CASIO_BOX_RWIDTH + 2 * self.CASIO_BORDER_GAP,
                         consts.PLAYFIELD_HEIGHT * self.CASIO_BOX_RHEIGHT + 2 * self.CASIO_BORDER_GAP]

    #
    # overloads from tetrisGame
    #

    def updateDisplay(self):
        show_screen()

    # Draw borders
    def drawBackGround(self):
        
        # Border around the playfield
        self._drawRectangle(self.gamePos_[0], self.gamePos_[1],
                             self.gamePos_[2], self.gamePos_[3],
                             None, self.colours_[consts.COLOUR_ID_BORDER])
        
        # Next piece
        draw_string(self.CASIO_INFO_LEFT + self.CASIO_INFO_GAP, self.CASIO_NP_TOP, self.itemTexts_[3], self.colours_[consts.COLOUR_ID_TEXT], "medium")

        self._drawRectangle(self.CASIO_INFO_LEFT + self.CASIO_INFO_GAP, 
                             self.CASIO_NP_TOP + 10,
                             self.CASIO_BOX_RWIDTH * 4 + self.CASIO_BORDER_GAP * 2, 
                             self.CASIO_BOX_RHEIGHT * 4 + self.CASIO_BORDER_GAP * 2, 
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
            left = self.CASIO_PLAYFIELD_LEFT + x * self.CASIO_BOX_RWIDTH
            top = self.CASIO_PLAYFIELD_TOP + (consts.PLAYFIELD_HEIGHT - 1 - y) * self.CASIO_BOX_RHEIGHT
        else:
            # Next piece
            left = self.CASIO_INFO_LEFT + self.CASIO_INFO_GAP + self.CASIO_BORDER_GAP
            top = self.CASIO_NP_TOP + 10 + self.CASIO_BORDER_GAP

        return (left, top, self.CASIO_BOX_RWIDTH, self.CASIO_BOX_RHEIGHT)

    # Draw a single colored block
    #
    def _drawSingleBlock(self, left, top, colourID, shadow = False):
        self._drawRectangle(left, top, self.CASIO_BOX_RWIDTH, self.CASIO_BOX_RWIDTH, self.colours_[colourID])

    # Erase a tetramino
    #
    def _eraseBlocks(self, left, top, width, height, colourID):
        x,y,w,h = self._changeCoordonateSystem(left, top, False)
        self._drawRectangle(x, y, w, h, self.colours_[colourID], None)

    # overloads from gameRendering
    #

    # Verifications
    #   Return (Done, error message)
    #
    def checkEnvironment(self):
        self.status_ = self.STATUS_INIT
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
    def _drawRectangle(self, x, y, width, height, fillColour = None, borderColour = None):
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