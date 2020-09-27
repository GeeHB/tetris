# coding=UTF-8
#
#   File     :   pygameTetris.py
#
#   Authors     :   JHB
#
#   Description :   Gestion de l'interface du tetris en mode graphique avec la bibliothèque pygame
#                   
#
#   Remarque    :   Nécessite Python 3.xx
#
#   Version     :   0.5.3-2
#
#   Date        :   2020/09/21
#

import pygame
import math
import sharedConsts
import tetrisGame

# Constantes de l'application
#
BOX_WIDTH       = 25    # Dimensions d'un carré

# Palette de couleurs
#
COLOUR_BLACK        = (0, 0, 0)
COLOUR_WHITE        = (255, 255, 255)

# Police et taille du texte
#
FONT_NAME       = 'helvetica'
FONT_SIZE       = 20
MAX_FONT_SIZE   = 25

# Une couleur (avec sa version ombrée et sa version sur-exposée)
#
class tetrisColour(object):
    base_, light_, dark_ = None, None, None

    def __init__(self, base, light = None, dark = None):
        self.base_ = base
        self.light_ = light
        self.dark_ = dark

# Classe pygameTetris
#
class pygameTetris(tetrisGame.tetrisGame):

    # PYGame events types
    EVT_KEYDOWN         = pygame.KEYDOWN
    EVT_QUIT            = pygame.QUIT
    
    # Code des touches de contrôle par défaut
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

    """
    EVT_KEYDOWN     = pygame.KEYDOWN
    EVT_QUIT        = pygame.QUIT
    """

    # Données membres
    win_            = None          # "Fenêtre" d'affichage
    winHeight_, winWidth_ = 0,0     # Dimensions de la fenêtre
    boxWidth_       = BOX_WIDTH
    fontSize_       = FONT_SIZE
    
    colours_        = []            # Table des couleurs

    itemDims_      = [None, None, None]      # Dimensions de la zone de texte pour les scores, les lignes et le niveau
    
    # Méthodes
    #

    # Construction
    def __init__(self):
        
        # Table des couleurs
        #
        self.colours_ = [tetrisColour(COLOUR_BLACK)] * (1 + sharedConsts.LAST_COLOUR_ID)     # Par défaut tout est noir
        
        self.colours_[1] = tetrisColour((255, 0, 0), (255, 128, 128), (128,0,0))        # Rouge
        self.colours_[2] = tetrisColour((0, 255, 0), (255, 128, 128), (0,128,0))        # Vert
        self.colours_[3] = tetrisColour((255, 255, 0), (255, 255, 128), (128,128,0))    # Jaune
        self.colours_[4] = tetrisColour((0, 0, 255), (128, 128, 255), (0,128,0))        # Bleu
        self.colours_[5] = tetrisColour((255, 0, 255), (255, 128, 255), (128,0,128))    # Violet
        self.colours_[6] = tetrisColour((0, 255, 255), (128, 255, 255), (0,128,128))    # Cyan
        self.colours_[7] = tetrisColour((255, 128, 0), (255, 192, 128), (128,64,0))     # Orange

        self.colours_[sharedConsts.COLOUR_ID_SHADOW] = tetrisColour((48,48,48))
        self.colours_[sharedConsts.COLOUR_ID_TEXT] = tetrisColour(COLOUR_WHITE)
        self.colours_[sharedConsts.COLOUR_ID_BORDER] = tetrisColour((192,192,192))
        self.colours_[sharedConsts.COLOUR_ID_BOARD] = tetrisColour((32,32,32))

        # Calcul des dimensions
        self.winWidth_    = 2 * self.boxWidth_ * sharedConsts.PLAYFIELD_WIDTH
        self.winHeight_   = (2 + self.boxWidth_) * sharedConsts.PLAYFIELD_HEIGHT
        
        self.gameWidth_ = sharedConsts.PLAYFIELD_HEIGHT * self.boxWidth_
        self.gameHeight_ = sharedConsts.PLAYFIELD_HEIGHT * self.boxWidth_
        self.gameLeft_ = 2 * self.boxWidth_
        self.gameTop_ = self.winHeight_ - self.gameHeight_  - 1

    # Méthodes surchargées de eventHandler
    #

    # Une ligne est complête (mais encore dans l'espace de jeu)
    def lineCompleted(self, rowIndex):
        pass

    # Méthodes surchargées de gameRendering
    #

    # Vérifications
    #   Retourne un booléen qui indique si l'objet peut être initialisé
    def checkEnvironment(self):
        
        # Vérification de PYGame (retourne le tupe (#ok, #errors))
        rets = pygame.init()

        if 0 != rets[1] :
            return "PYGame initialization error. Returned " + str(rets[1]) + " error(s)"

        # Main window creation
        self.win_ = pygame.display.set_mode((self.winWidth_, self.winHeight_), pygame.RESIZABLE)
        pygame.display.set_caption('jTetris')
        
        # Ok
        self.status_ = tetrisGame.tetrisGame.GAME_INIT
        return ""

    # Fin ...
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

    # Lecture non bloquante du clavier
    # Retourne le caractère associé à la touche ou le caractère vide ('')
    def checkKeyboard(self):
        # Evènement en haut de la pile
        evt = pygame.event.poll()
        if evt.type == pygame.KEYDOWN:
            # Un chiffre
            if evt.key >= pygame.K_0 and evt.key <= pygame.K_9:
                return (ord('0') + evt.key - pygame.K_0)
            else:
                return evt.key
        elif evt.type == pygame.QUIT:
            # End the game
            self.end()
        else :
            return self.KEY_NOEVENT
     
    
    # Méthodes surchargées de tetrisGame
    #

    # L'écran doit être reactualisé
    def _updateDisplay(self):
        pygame.display.update()

    # Affichage d'un texte avec effacement de l'ancienne valeur
    def _drawText(self, index, text):
        font = pygame.font.SysFont(FONT_NAME, self.fontSize_)
        label = font.render(text, 1, self.colours_[sharedConsts.COLOUR_ID_TEXT].base_)

        left = self.gameLeft_ + (1 + sharedConsts.PLAYFIELD_WIDTH ) * self.boxWidth_
        top = self.gameTop_ + self.boxWidth_ * ( 2 * index + 1)
        
        # Effacer l'ancien
        if None != self.itemDims_[index] and 2 == len(self.itemDims_[index]) :
            pygame.draw.rect(self.win_, self.colours_[sharedConsts.COLOUR_ID_BKGRND].base_, (left, top, self.itemDims_[index][0], self.itemDims_[index][1]))
    
        # Affichage
        self.itemDims_[index] = font.size(text) # Récupération de la taille ...
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

    # Affichage d'un bloc coloré aux coordonnées données
    def _drawBlock(self, left, top, colourID, inBoard, shadow = False):
        paintColour = self.colours_[colourID]
        if None != paintColour.light_:
            # Le carré
            pygame.draw.rect(self.win_, paintColour.base_, (left + 1, top + 1, self.boxWidth_ - 2, self.boxWidth_ -2))

            # l'effet ombré
            pygame.draw.line(self.win_, paintColour.light_, (left, top),(left, top + self.boxWidth_ - 1))
            pygame.draw.line(self.win_, paintColour.light_, (left, top),(left + self.boxWidth_ - 1, top))

            pygame.draw.line(self.win_, paintColour.dark_, (left + self.boxWidth_ - 1, top),(left + self.boxWidth_ - 1, top + self.boxWidth_ - 1))
            pygame.draw.line(self.win_, paintColour.dark_, (left, top + self.boxWidth_ - 1),(left + self.boxWidth_ - 1, top + self.boxWidth_ - 1))
        else:
            # Juste un carré
            pygame.draw.rect(self.win_, paintColour.base_, (left, top, self.boxWidth_, self.boxWidth_))

    # Effacement
    def _eraseBlocks(self, left, top, width, height, colourID, inBoard):
        
        # Changement de repère
        x,y,w,h = self._changeCoordonateSystem(left, top, inBoard)

        # Dessin du rectangle
        pygame.draw.rect(self.win_, self.colours_[colourID].base_, (x, y, w * width, h * height))
        
        pass

    # Changement de repère (et de coordonnées)
    #   (x,y) sont les coordonnées à translater
    #   inBoard : Dans l'espace de jeu (True) ou dans la zone "pièce suivante"
    #   retourne le tuple (x,y, dx, dy) dans le nouveau système ou dx, dy 
    #   sont les incréments (ie la largeur reèlle des blocs à l'écran) 
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