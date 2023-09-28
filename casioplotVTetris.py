#   File     :   casioplotVTetris.py
#
#   Author     :   JHB
#
#   Description :   casioplotTetris object - Drawings using casioplot library, vertical way
#                   
#   Comment    :   Python 3.xx
#

from casioplot import *
import consts
import casioplotTetris


# casioplotVTetris object - drawing of tertraminos using casioplot library
#
#class casioplotTetris(tetrisGame.tetrisGame):
class casioplotVTetris(casioplotTetris.casioplotTetris):    
     
    # Construction
    #
    def __init__(self):
        
        self.CASIO_BOX_WIDTH = 13
        self.CASIO_BOX_HEIGHT = self.CASIO_BOX_WIDTH

        # SingleBlocks real dims (including borders)
        self.CASIO_BOX_RWIDTH = (1 + self.CASIO_BOX_WIDTH)
        self.CASIO_BOX_RHEIGHT = self.CASIO_BOX_RWIDTH

        self.CASIO_PLAYFIELD_LEFT = self.CASIO_PLAYFIELD_BORDER + self.CASIO_BORDER_GAP
        #self.CASIO_PLAYFIELD_TOP = self.CASIO_WIDTH - self.CASIO_PLAYFIELD_BORDER - self.CASIO_BORDER_GAP - (consts.PLAYFIELD_HEIGHT - 1) * self.CASIO_BOX_RHEIGHT

        # Next-Piece
        self.CASIO_NP_LEFT = self.CASIO_HEIGHT - self.CASIO_PLAYFIELD_BORDER - 4 * self.CASIO_NP_BOX_WIDTH
        self.CASIO_NP_TOP = self.CASIO_PLAYFIELD_BORDER

        # Call parent constructor
        super().__init__()

    #
    # overloads from tetrisGame
    #

    # Draw borders
    def drawBackGround(self):
        # Border around the playfield
        self._drawRectangle(self.gamePos_[0], self.gamePos_[1],
                             self.gamePos_[2], self.gamePos_[3],
                             None, self.colours_[consts.COLOUR_ID_BORDER])
        
        # Next piece
        #draw_string(self.CASIO_INFO_LEFT + self.CASIO_INFO_GAP, self.CASIO_NP_TOP, self.itemTexts_[3], self.colours_[consts.COLOUR_ID_TEXT], "medium")
        self._drawRectangle(self.CASIO_NP_LEFT, self.CASIO_NP_TOP,
                            self.CASIO_NP_WIDTH, self.CASIO_NP_HEIGHT, 
                            None, self.colours_[consts.COLOUR_ID_BORDER])
    
    # Change the origin and the coordinate system
    #   (x,y) are to be translated
    #   inBoard : int he board (True) or in the "next piece" area (False)
    #
    #   returns a tuple (x,y, dx, dy) in the new coordonate system
    #       dx, dy  are the width and height of the block in the screen
    # 
    """
    def _changeCoordonateSystem(self, x, y, inBoard = True):
        if inBoard:
            # For the game
            return super()._changeCoordonateSystem(x,y, True)
        
        # Next piece
        left = self.CASIO_INFO_LEFT + self.CASIO_INFO_GAP + self.CASIO_BORDER_GAP
        top = self.CASIO_NP_TOP + 10 + self.CASIO_BORDER_GAP

        return (left, top, self.CASIO_BOX_SWIDTH, self.CASIO_BOX_SHEIGHT)
    """
    
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
        
        # anticlockwise rotation
        nx = y + 1
        ny = self.CASIO_HEIGHT - x

        # A border ?
        if borderColour is not None:
            for px in range(width):
                #set_pixel(x + px, y, borderColour)
                set_pixel(nx - 1, ny - px, borderColour)
                #set_pixel(x + px, y + height - 1, borderColour)
                set_pixel(nx + height - 2, ny - px, borderColour)

            for py in range(height-2):
                #set_pixel(x, y + py + 1, borderColour)
                set_pixel(nx + py, ny, borderColour)
                #set_pixel(x + width - 1, y + py + 1, borderColour)
                set_pixel(nx + py, ny -width + 1, borderColour)
                pass

        # Filling ?
        nx+=(self.CASIO_BOX_WIDTH - self.CASIO_BORDER_GAP)
        if fillColour is not None:
            for px in range(width - 1):
                for py in range(height - 1):
                    #set_pixel(x + px, y + py, fillColour)
                    set_pixel(nx - px, ny - py, fillColour)

# EOF