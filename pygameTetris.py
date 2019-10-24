# coding=UTF-8
#
#   Fichier     :   pygameTetris.py
#
#   Auteur      :   JHB
#
#   Description :   Gestion de l'interface du tetris en mode graphique avec la bibliothèque pygame
#                   
#
#   Remarque    :   Nécessite Python 3.xx
#
#   Version     :   0.4.3
#
#   Date        :   22 octobre 2019
#

import pygame
from tetrisGame import *

# Constantes de l'application
#
BOX_WIDTH       = 35    # Dimensions d'un carré
BOX_HEIGHT      = BOX_WIDTH

# Palette de couleurs
#
COLOUR_BLACK        = (0, 0, 0)
COLOUR_WHITE        = (255, 255, 255)

# Police et taille du texte
#
FONT_NAME   = 'helvetica'
FONT_SIZE   = 25

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
class pygameTetris(tetrisGame):

    # Code des touches de contrôle par défaut
    #
    KEY_LEFT        = pygame.K_LEFT
    KEY_RIGHT       = pygame.K_RIGHT
    KEY_ROTATE_LEFT = pygame.K_UP
    #KEY_ROTATE_RIGHT= '0'
    KEY_DOWN        = pygame.K_DOWN
    KEY_FALL        = pygame.K_SPACE
    KEY_START       = pygame.K_RETURN
    #KEY_QUIT        = pygame.K_ESCAPE
    KEY_QUIT        = pygame.K_q
    KEY_STOP        = KEY_QUIT
    KEY_SHADOW_MODE = pygame.K_o
    KEY_NORMAL_MODE = pygame.K_n
    KEY_SCORES      = pygame.K_h

    # Données membres
    win_            = None          # "Fenêtre" d'affichage
    winHeight_, winWidth_ = 0,0     # Dimensions de la fenêtre
    colours_        = []            # Table des couleurs
    
    # Méthodes
    #

    # Construction
    def __init__(self):
        
        # Table des couleurs
        #
        self.colours_ = [tetrisColour(COLOUR_BLACK)] * (1 + LAST_COLOUR_ID)     # Par défaut tout est noir
        
        self.colours_[1] = tetrisColour((255, 0, 0), (255, 128, 128), (128,0,0))        # Rouge
        self.colours_[2] = tetrisColour((0, 255, 0), (255, 128, 128), (0,128,0))        # Vert
        self.colours_[3] = tetrisColour((255, 255, 0), (255, 255, 128), (128,128,0))    # Jaune
        self.colours_[4] = tetrisColour((0, 0, 255), (128, 128, 255), (0,128,0))        # Bleu
        self.colours_[5] = tetrisColour((255, 0, 255), (255, 128, 255), (128,0,128))    # Violet
        self.colours_[6] = tetrisColour((0, 255, 255), (128, 255, 255), (0,128,128))    # Cyan
        self.colours_[7] = tetrisColour((255, 128, 0), (255, 192, 128), (128,64,0))     # Orange

        self.colours_[COLOUR_ID_SHADOW] = tetrisColour((48,48,48))
        self.colours_[COLOUR_ID_TEXT] = tetrisColour(COLOUR_WHITE)
        self.colours_[COLOUR_ID_BORDER] = tetrisColour((192,192,192))
        self.colours_[COLOUR_ID_BOARD] = tetrisColour((32,32,32))

        # Calcul des dimensions
        self.winWidth_    = 2 * BOX_WIDTH * board.PLAYFIELD_WIDTH
        self.winHeight_   = (2 + BOX_HEIGHT) * board.PLAYFIELD_HEIGHT
        
        self.gameWidth_ = board.PLAYFIELD_HEIGHT * BOX_WIDTH
        self.gameHeight_ = board.PLAYFIELD_HEIGHT * BOX_HEIGHT
        self.gameLeft_ = 2 * BOX_WIDTH
        self.gameTop_ = self.winHeight_ - self.gameHeight_    # Aligné sur le bas

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
            # Des erreurs !
            return "L'initialisation de pygame a retournée " + str(rets[1]) + " erreur(s)"

        # Création de la fenêtre
        self.win_ = pygame.display.set_mode((self.winWidth_, self.winHeight_), pygame.RESIZABLE)
        pygame.display.set_caption('jTetris')
        
        # Ok
        self.status_ = tetrisGame.GAME_INIT
        return ""

    # Fin ...
    def clear(self):
        # Fermeture de l'environnement
        pygame.display.quit()

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
        else :
            return self.KEY_NOEVENT
     
    # Affichage d'un message de texte
    #   le paramètre texte pointe sur une liste de lignes
    def drawText(self, text, title="", highLight=-1):
        pass

    # Effacement du texte
    def clearText(self):
        pass

    # Affichage des scores
    def drawScores(self):
        pass

    # Méthodes surchargées de tetrisGame
    #

    # L'écran doit être reactualisé
    def _updateDisplay(self):
        pygame.display.update()

    # Affichage d'un texte avec effacement de l'ancienne valeur
    def _drawText(self, index, text):
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        label = font.render(text, 1, self.colours_[COLOUR_ID_TEXT].base_)

        left = self.gameLeft_ + board.PLAYFIELD_WIDTH * BOX_WIDTH + 45
        top = self.gameTop_ + 60 * (1 + index)
        
        # Effacer l'ancien
        if None != self.itemDims_[index] :
            pygame.draw.rect(self.win_, self.colours_[COLOUR_ID_BKGRND].base_, (left, top, self.itemDims_[index][0], self.itemDims_[index][1]))
    
        # Affichage
        self.itemDims_[index] = font.size(text) # Récupération de la taille ...
        self.win_.blit(label, (left, top))
    
    # Dessin des bordures
    def _drawBorders(self):
        # Dessin d'une simple bordure sur 3 côtés pour la zone de jeu
        left = self.gameLeft_ - 1
        top = self.gameTop_ - 1
        width = board.PLAYFIELD_WIDTH * BOX_WIDTH + 2
        height = board.PLAYFIELD_HEIGHT * BOX_HEIGHT + 2
        pygame.draw.line(self.win_, self.colours_[COLOUR_ID_BORDER].base_, (left, top),(left, top +  height - 1))
        pygame.draw.line(self.win_, self.colours_[COLOUR_ID_BORDER].base_, (left + width - 1, top),(left + width - 1, top +  height - 1))
        pygame.draw.line(self.win_, self.colours_[COLOUR_ID_BORDER].base_, (left, top),(left + width - 1, top))

        # Le fond ...
        x,y,w,h = self._changeCoordonateSystem(left, top, True)
        pygame.draw.rect(self.win_, self.colours_[COLOUR_ID_BOARD].base_, (x, y, w * board.PLAYFIELD_WIDTH, h * board.PLAYFIELD_HEIGHT))
        

        # Affichage du texte pour la piece suivante
        left = self.gameLeft_ + BOX_WIDTH * board.PLAYFIELD_WIDTH + 45
        top = self.gameTop_ + BOX_HEIGHT * (board.PLAYFIELD_HEIGHT - 5) - FONT_SIZE
        font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        label = font.render(self.itemTexts_[3], 1, self.colours_[COLOUR_ID_TEXT].base_)
        self.win_.blit(label, (left, top - 50))

        # Dessin de la bordure pour la pièce suivante
        left-=2
        top = self.gameTop_ + BOX_HEIGHT * (board.PLAYFIELD_HEIGHT - 5) - FONT_SIZE - 2
        width = 4 * BOX_WIDTH + 4
        height = 4 * BOX_HEIGHT + 4
        pygame.draw.line(self.win_, self.colours_[COLOUR_ID_BORDER].base_, (left, top),(left, top +  height - 1))
        pygame.draw.line(self.win_, self.colours_[COLOUR_ID_BORDER].base_, (left + width - 1, top),(left + width - 1, top +  height - 1))
        pygame.draw.line(self.win_, self.colours_[COLOUR_ID_BORDER].base_, (left, top),(left + width - 1, top))
        pygame.draw.line(self.win_, self.colours_[COLOUR_ID_BORDER].base_, (left, top + height - 1),(left + width - 1, top + height - 1))

    # Affichage d'un bloc coloré aux coordonnées données
    def _drawBlock(self, left, top, colourID, inBoard, shadow = False):
        paintColour = self.colours_[colourID]
        if None != paintColour.light_:
            # Le carré
            pygame.draw.rect(self.win_, paintColour.base_, (left + 1, top + 1, BOX_WIDTH - 2, BOX_HEIGHT -2))

            # l'effet ombré
            pygame.draw.line(self.win_, paintColour.light_, (left, top),(left, top + BOX_HEIGHT - 1))
            pygame.draw.line(self.win_, paintColour.light_, (left, top),(left + BOX_WIDTH - 1, top))

            pygame.draw.line(self.win_, paintColour.dark_, (left + BOX_WIDTH - 1, top),(left + BOX_WIDTH - 1, top + BOX_HEIGHT - 1))
            pygame.draw.line(self.win_, paintColour.dark_, (left, top + BOX_HEIGHT - 1),(left + BOX_WIDTH - 1, top + BOX_HEIGHT - 1))
        else:
            # Juste un carré
            pygame.draw.rect(self.win_, paintColour.base_, (left, top, BOX_WIDTH, BOX_HEIGHT))

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
            # Dans l'espace de jeu
            left = self.gameLeft_ + x * BOX_WIDTH
            top = self.gameTop_ + (board.PLAYFIELD_HEIGHT - 1 - y) * BOX_HEIGHT
        else:
            # Pièce suivante
            left = self.gameLeft_ + BOX_WIDTH * board.PLAYFIELD_WIDTH + 45
            top = self.gameTop_ + BOX_HEIGHT * (board.PLAYFIELD_HEIGHT - 5) - FONT_SIZE

        return (left, top, BOX_WIDTH, BOX_HEIGHT)

# EOF