#   File     :   casioPlotTetris.py
#
#   Author     :   JHB
#
#   Description :   casioPlotTetris object - Drawings using casioplot library
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

# casioplotTetris object - drawing of tertraminos using casioplot library
#
class casioplotTetris(tetrisGame.tetrisGame):

    #
    # overloads from tetrisGame
    #

    # Draw borders
    def drawBackGround(self):
        pass

    # Change the origin and the coordinate system
    #   (x,y) are to be translated
    #   inBoard : int he board (True) or in the "next piece" area (False)
    #
    #   returns a tuple (x,y, dx, dy) in the new coordonate system
    #       dx, dy  are the width and height of the block in the screen
    # 
    def _changeCoordonateSystem(self, x, y, inBoard = True):
        return (x,y,1,1)

    # Draw a single colored block
    #
    def _drawSingleBlock(self, left, top, colourID, shadow = False):
        self.__drawRectangle(left, top, CASIO_BOX_RWIDTH, CASIO_BOX_RWIDTH, self.colors_[colourID])

    # Erase a tetramino
    #
    def _eraseBlocks(self, left, top, width, height, colourID, inBoard):
        pass

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
    def __drawRectangle(x, y, width, height, fillColour = None, borderColour = None):
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

# Dessin d'un carre
#
#   x,y : coin superieur gauche
#   cote : longueur du côté
#   borderColour : Couleur de la bordure au format RGB (ou None si pas de bordure)
#   fillColour : Couleur de remplissage au format RGB (ou None si vide) 
# #
def draw_square(x, y, cote, fillColour, borderColour = None):
    # C'est un rectangle!!!
    draw_rectangle(x, y, cote, cote, fillColour, borderColour)


if __name__ == "__main__":      
    # Affichages ...
    draw_square(20,20, 10, BLEU)
    draw_square(20, 80, 30, ROUGE)

    draw_rectangle(150, 30, 80, 120, GRIS, VERT)

    # Mise a jour de l ecran
    show_screen()

# EOF