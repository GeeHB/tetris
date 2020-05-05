# coding=UTF-8
#
#   Fichier     :   cursesTetris.py
#
#   Auteur      :   JHB
#
#   Description :   Gestion de l'interface du tetris en mode console avec la librairie ncurses
#                   
#
#   Remarque    :   Nécessite Python 3.xx
#
#   Version     :   0.4.8
#
#   Date        :   5 mai 2020
#

import curses, sys, time, os, termios, fcntl
from tetrisGame import *

# Quelques constantes
#

# Dimensions & positions
BORDER_WIDTH    = 2
GAP_WIDTH       = 2       # Espacement de la bordure
SHAPE_WIDTH     = PIECE_WIDTH * 2
SHAPE_HEIGHT    = PIECE_HEIGHT

BORDER_COLOR    = 0         # Couleur par défaut du term.

# Gestion de l'ombre
SHADOW_CHAR     = '\u2591'  # Caractère utilisé (en unicode)

# Mise en surbrillance
HILIGHT_COLOR   = 9

# Classe cursesTetris
#   Gestion des évènements ayant une influence sur le rendu graphique
#
class cursesTetris(tetrisGame):

    term_ = None      # Ecran curses
    
    # Dimensions & position
    gameLeft_, gameTop_, gameWidth_ , gameHeight_ = 0, 0, 0, 0
    
    # Construction
    def __init__(self):

        # Initialisation de nCurses
        self.term_ = curses.initscr()
        curses.cbreak()
        self.term_.keypad(True)   # Tous les caractères
        self.term_.nodelay(True)  # Lecture etat clavier non-bloquant
        curses.curs_set(0)        # Pas de curseur

    # Méthodes surchargées de gameRendering
    #

    # Vérifications
    #   Retourne un booléen qui indique si l'objet peut être initialisé
    def checkEnvironment(self):

        errorMessage = ""

        if tetrisGame.GAME_INIT == self.status_:
            # Déja fait
            return ""

        # Vérification et gestion des couleurs pour le terminal
        #
        if False == curses.has_colors():
            errorMessage = "Le terminal doit accepter les couleurs"
            return errorMessage
        
        # Initialisation des couleurs
        curses.start_color()
        # curses.init_pair(0, curses.COLOR_WHITE, curses.COLOR_BLACK)     # Par défaut
        for i in range(1,8):
            curses.init_pair(i, i, i) # La ieme couleur : text = i, bk = i
        
        # L'ombre est en blanc sur fond noir
        curses.init_pair(COLOUR_ID_SHADOW, curses.COLOR_WHITE, curses.COLOR_BLACK)

        # La couleur de surbrilance est le rouge
        curses.init_pair(HILIGHT_COLOR, curses.COLOR_RED, curses.COLOR_BLACK)
    
        # Dimensions
        #
        self.gameWidth_ = board.PLAYFIELD_WIDTH * 2
        self.gameHeight_ = board.PLAYFIELD_HEIGHT
        self.gameLeft_ = 2       # (curses.COLS - gameWidth_) / 2;
        self.gameTop_ = curses.LINES - self.gameHeight_
        #self.canDrawNextPiece_ = curses.COLS > (self.gameWidth_ + BORDER_WIDTH * 2 + GAP_WIDTH + SHAPE_WIDTH + 2)

        if curses.LINES < self.gameHeight_:
            # Pas assez haut
            errorMessage = "Le terminal doit avoir au moins " + str(self.gameHeight_) + " caractères de haut"
            return errorMessage
        
        if curses.COLS < self.gameWidth_ + 4:
            # Pas assez large
            errorMessage = "Le terminal doit avoir au moins " + str(self.gameWidth_ + 4) + " caractères de large"
            return errorMessage
                
        # Oui => tout est ok pour les affichages
        self.status_ = tetrisGame.GAME_INIT
        return ""

    
    # Fin ...
    def clear(self):
        # On remet le terminal dans l'état d'origine
        curses.endwin()

    # Lecture non bloquante du clavier
    # Retourne le caractère associé à la touche ou le caractère vide ('')
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

    # Affichage d'un message de texte
    #   le paramètre texte pointe sur une liste de lignes
    #
    #   idéalement on utiliserait les "windows" de curses, mais l'effacement le fonctionne pas
    def drawText(self, text, title="", highLight=-1):
        # Pas de texte ou trop?
        length = len(text)
        if 0 == length or length >= (board.PLAYFIELD_HEIGHT - 2):
            return
        
        # Ligne la plus large
        # on en profite pour sauter une ligne sur deux
        width = 0
        body = []
        for line in text:
            if len(line)>width:
                width = len(line)
            body.append(" ") # une ligne vide
            body.append(line)   # une ligne de texte
        body.append(" ") # On termine par une ligne vide
        
        if -1 != highLight:
            highLight=2*(highLight+1) -1 # Il y 2 fois plus de lignes
        
        # Titre
        wTitle = 4 + (len(title) if title!="" else 0)
        if wTitle > width :
            width = wTitle

        # Trop large
        if  width >= (curses.COLS - 2):
            width = curses.COLS - 2
        
        # Haut du cadre
        left = 1 + int((curses.COLS - 2 - width)/2)
        left = 5 if left > 5 else left
        top = 1 + int((curses.LINES - 2 - len(body))/2)
        string = '\u2552'
        if wTitle :
            offsetL = 1 + int((width - wTitle) /2)
            offsetR = width - wTitle - offsetL + 2
            string+='\u2550' * offsetL + ' ' + title + ' ' + '\u2550' * offsetR
        else :
            # pas de titre ...
            string+='\u2550' * width  
        string+= '\u2555'
        self.term_.addstr(top, left, string, curses.color_pair(0))
        top+=1

        # Affichage des lignes de texte
        index = 0
        for line in body:
            string = '\u2502'
            if len(line) <= width:
                # Le texte
                string+=line
                # Les espaces complémentaires
                string+=' '*(width - len(line))
            else:
                # on coupe la chaine
                string+=line[:width]
            string += '\u2502'
            
            if index == highLight :
                # Ligne sélectionnée
                self.term_.addstr(top, left, string[0], curses.color_pair(0))
                self.term_.addstr(top, left +1 , string[1:len(string)-1], curses.color_pair(HILIGHT_COLOR))
                self.term_.addstr(top, left + width + 1, string[len(string)-1], curses.color_pair(0))
            else :
                # Ligne "normale"
                self.term_.addstr(top, left, string, curses.color_pair(0))
            
            top+=1
            index+=1

        # et pour finir, bas du cadre
        string = '\u2514' + '\u2500' * width + '\u2518'
        self.term_.addstr(top, left, string, curses.color_pair(0))
        self.term_.refresh()

    # Effacement du texte
    def clearText(self):
        # On efface tout
        self.term_.clear()
        
        # puis on reaffiche tout ...
        self._drawBorders()
        self.drawBoard()
        self._drawNumValue(0, self.board_.score())
        self._drawNumValue(1, self.board_.level())
        self._drawNumValue(2, self.board_.lines())       
        self._drawNextPiece(self.board_.nextPieceIndex())

    # Affichage du tableau des meilleurs scores
    def drawScores(self):
        pass

    # Méthodes à surcharger
    #

    # L'écran doit être reactualisé
    def _updateDisplay(self):
        self.term_.refresh()

    # Affichage d'une valeur numérique avec effacement de l'ancienne valeur
    def _drawNumValue(self, index, value):
        boxTop = self.gameTop_ + PIECE_HEIGHT + 5 + 3 * index
        boxLeft = self.gameWidth_ + BORDER_WIDTH * 2 + GAP_WIDTH
        text = self.itemTexts_[index] + ": " +  str(value) + ' ' * self.itemDims_[index] # Affichage et effacement
        self.term_.addstr(boxTop, boxLeft, text, curses.color_pair(0))
        self.itemDims_[index] = len(text) # Longueur du texte

    # Dessin des bordures (esapde de jeu et éventuellement pièces suivantes)
    def _drawBorders(self):
         # en haut
        if self.gameTop_ >= 1:
            # Le charme de faire du Python !!!
            top = '\u250c' + '\u2500' * self.gameWidth_  + '\u2510'
            self.term_.addstr(self.gameTop_ - 1, self.gameLeft_ - 1, top, curses.color_pair(0))
        
        # Gauche et droite
        if self.gameLeft_ >= 2 and curses.COLS >= self.gameWidth_ + 4:

            self.term_.attron(curses.color_pair(BORDER_COLOR))
            
            for y in range(self.gameHeight_):
                self.term_.move(self.gameTop_ + y, self.gameLeft_ - 2)
                self.term_.addch(' ')
                self.term_.addch('\u2502')

                self.term_.move(self.gameTop_ + y, self.gameLeft_ + self.gameWidth_)
                self.term_.addch('\u2502')
                self.term_.addch(' ')
            
            self.term_.attroff(curses.color_pair(BORDER_COLOR))

    # Changement de repère (et de coordonnées)
    #   (x,y) sont les coordonnées à translater
    #   inBoard : Dans l'espace de jeu (True) ou dans la zone "pièce suivante"
    #   retourne le tuple (x,y, dx, dy) dans le nouveau système ou dx, dy 
    #   sont les incréments (ie la largeur reèlle des blocs à l'écran) 
    def _changeCoordonateSystem(self, x, y, inBoard = True):
        
        if inBoard:
            left = self.gameLeft_ + 2 * x
            top = self.gameTop_ + board.PLAYFIELD_HEIGHT - 1 - y
        else:
            left = self.gameWidth_ + BORDER_WIDTH * 2 + GAP_WIDTH
            top = self.gameTop_ + 2
        
        return (left,top,2,1)    # Chaque cube correspond à 2 car. en largeur

    # Affichage d'un bloc coloré aux coordonnées données (dans la zone donnée)
    def _drawBlock(self, left, top, colourID, inBoard, shadow = False):
        self.term_.addstr(top, left, (SHADOW_CHAR if shadow else ' ') * 2, curses.color_pair(colourID))

    # Effacement
    def _eraseBlocks(self, left, top, width, height, colourID, inBoard):
        x,y,w,h = self._changeCoordonateSystem(0,0, False)
        for row in range(height):
            self.term_.addstr(y + row, x, ' ' * w * width, curses.color_pair(colourID))
# EOF