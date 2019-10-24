# coding=UTF-8
#
#   Fichier     :   tetrisGame.py
#
#   Auteur      :   JHB
#
#   Description :   Gestion et affichage complet du jeu Tetris - Classe abstraite 
#                   
#
#   Remarque    :   Nécessite Python 3.xx
#
#   Version     :   0.4.3
#
#   Date        :   22 octobre 2019
#

from eventHandler import eventHandler
import board
from piece import PIECE_WIDTH, PIECE_HEIGHT, pieceStatus

# Constantes de l'application
#

# Indices des couleurs
#
COLOUR_ID_BOARD        = 0      # Fond de l'espace de jeu
# 1 -> 7 : couleurs des pièces
COLOUR_ID_SHADOW       = 8
COLOUR_ID_TEXT         = 9
COLOUR_ID_BORDER       = 10
COLOUR_ID_BKGRND       = 11      # Fond de la fenêtre

LAST_COLOUR_ID   = COLOUR_ID_BKGRND


# Classe tetrisGame
#
class tetrisGame(eventHandler):

    # Code des touches de contrôle par défaut
    # peuvent être surchargées
    KEY_LEFT        = '4'
    KEY_RIGHT       = '6'
    KEY_ROTATE_LEFT = '5'
    KEY_ROTATE_RIGHT= '0'
    KEY_DOWN        = '2'
    KEY_FALL        = ' '
    KEY_START       = chr(13)   # Touche "enter"
    KEY_QUIT        = 'q'
    KEY_STOP        = KEY_QUIT
    KEY_SHADOW_MODE = 'o'
    KEY_NORMAL_MODE = 'n'
    KEY_SCORES      = 'h'
    KEY_NOEVENT     = ''

    # Etats du jeu
    GAME_CREATED = 0
    GAME_INIT    = 1
    GAME_RUNNING = 2
    GAME_STOPPED = 3
    
    # Données membres
    board_  = None          # Espace de jeu
    status_ = GAME_CREATED  # Par défaut l'objet est "juste" crée
    currentPos_ = None      # Ou se trouve la pièce actuelle (pour pouvoir l'effacer ...)

    itemTexts_     = ["Score", "Niveau", "Lignes", "Pièce suivante"]
    itemDims_      = [None, None, None]      # Dimensions de la zone de texte pour les scores, les lignes et le niveau

    # Dimensions & position
    gameWidth_ , gameHeight_, gameLeft_, gameTop_ = 0, 0, 0, 0

    # Méthodes
    #  

    # Construction
    def __init__(self):
        self.status_ = self.GAME_CREATED

    # Destruction
    def __del__(self):
        self.clear()

    # Jeu en cours ?
    def isRunning(self):
        return self.GAME_RUNNING == self.status_

    # Forcer la fin de partie
    def end(self):
        self.status_ = self.GAME_STOPPED

    # Fin ...
    def clear(self):
        pass

    # Lecture non bloquante du clavier
    # Retourne le caractère associé à la touche ou le caractère vide ('')
    def checkKeyboard(self):
        return ''

    # L'espace de jeu
    def setBoard(self, currentBoard):
        self.board_ = currentBoard

    # C'est parti !
    def start(self):
        # L'objet doit au minimum avoir été initialisé
        if self.GAME_INIT == self.status_ or self.GAME_STOPPED == self.status_:
            # Initialisations ...
            self.currentPos_ = None

            # Dessin du cadre
            self._drawBorders()

            # Dessin de l'espace de jeu
            self.drawBoard()

            # Affichage du score et du niveau
            self._drawNumValue(0, self.board_.score())
            self._drawNumValue(1, self.board_.level())
            self._drawNumValue(2, self.board_.lines())

            # C'est parti
            self.status_ = self.GAME_RUNNING
            self.board_.start()
            
            # Dessin de la pièce suivante
            self._drawNextPiece(self.board_.nextPieceIndex())

            # Ok
            self._updateDisplay()
            return True
        
        # Sinon on ne fait rien
        return False

    # Affichage de tout l'espace de jeu
    def drawBoard(self):
        if None == self.board_:
            # Pas de données !!!
            return

        # Changement de repère
        leftFirst, top, w, h = self._changeCoordonateSystem(0,0,True)

        # Affichage de tous les blocs (colorés ou pas)
        for y in range(board.PLAYFIELD_HEIGHT):
            left = leftFirst    # A chaque nouvelle ligne on replace le "curseur"
            for x in range(board.PLAYFIELD_WIDTH):        
                self._drawBlock(left, top, self.board_.playField_[y][x], True)
                left+=w
            top-=h
        
        self._updateDisplay()


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

    # L'écran doit être reactualisé
    def _updateDisplay(self):
        pass

    
    def _drawNumValue(self, index, value):
               
        text = self.itemTexts_[index] + " : " + self._formatNumber(value)
        
        # Appel de la méthode surchargée
        self._drawText(index, text)
    
    # Affichage d'un texte avec effacement de l'ancienne valeur
    def _drawText(self, index, text):
        pass

    # Dessin des bordures (esapde de jeu et éventuellement pièces suivantes)
    def _drawBorders(self):
        pass

    # Changement de repère (et de coordonnées)
    #   (x,y) sont les coordonnées à translater
    #   inBoard : Dans l'espace de jeu (True) ou dans la zone "pièce suivante"
    #   retourne le tuple (x,y, dx, dy) dans le nouveau système ou dx, dy 
    #   sont les incréments (ie la largeur et la hauteur reèlles des blocs à l'écran) 
    def _changeCoordonateSystem(self, x, y, inBoard = True):
        return (x,y,1,1)

    # Affichage d'un bloc coloré aux coordonnées données (dans la zone donnée)
    def _drawBlock(self, left, top, colourID, inBoard, shadow = False):
        pass

    # Effacement
    def _eraseBlocks(self, left, top, width, height, colourID, inBoard):
        pass

    # Méthodes surchargées de eventHandler
    #

    # Un pièce vient de bouger (elle doit donc être effacée à son ancienne position et affichée à la nouvelle)
    def piecePosChanged(self, newState):
        # Y at'il eu une changement de position et/ou de rotation ?
        if self.currentPos_ == None  or self.currentPos_ != newState: 
            # On peut effacer la pièce et son ombre
            #
            if None != self.currentPos_:                    
                # Effacer = reafficher avec la couleur du fond
                self._drawSinglePiece(self.board_.pieceDatas(self.currentPos_.index_, self.currentPos_.rotationIndex_), self.currentPos_.leftPos_, self.currentPos_.topPos_, COLOUR_ID_BOARD)
                if -1 != self.currentPos_.shadowTopPos_:
                    # puis l'ombre
                    self._drawSinglePiece(self.board_.pieceDatas(self.currentPos_.index_, self.currentPos_.rotationIndex_), self.currentPos_.leftPos_, self.currentPos_.shadowTopPos_, COLOUR_ID_BOARD)

            ## ... puis on l'affiche à la nouvelle position
            if -1 != newState.shadowTopPos_:
                # d'abord l'ombre
                self._drawSinglePiece(self.board_.pieceDatas(newState.index_, newState.rotationIndex_), newState.leftPos_, newState.shadowTopPos_ , COLOUR_ID_SHADOW, shadow = True)
            # puis la pièce (qui peut recouvrir l'ombre !!!!)
            self._drawSinglePiece(self.board_.pieceDatas(newState.index_, newState.rotationIndex_), newState.leftPos_, newState.topPos_ , self.board_.tetraminos_[newState.index_].colour())

            # Mise à jour de l'affichage
            self._updateDisplay()
            
            # On conserve la position de la pièce
            self.currentPos_ = pieceStatus(other = newState)

    # Une pièce a atteint le plus bas niveau possible de l'espace de jeu
    def pieceReachedLowerPos(self):
        # Je ne dois plus l'effacer
        self.currentPos_ = None

    # Le score vient de changer
    def scoreChanged(self, newScore):
        self._drawNumValue(0, newScore)
        self._updateDisplay()

    # Changement de niveau
    def levelChanged(self, newLevel):
        self._drawNumValue(1, newLevel)
        self._updateDisplay()

    # Toutes les lignes complêtes ont été retirées
    def allLinesCompletedRemoved(self, rowCount, totalRows):
        # Réaffichage de l'espace de jeu
        self.drawBoard()
        self._drawNumValue(2, totalRows)
        self._updateDisplay()

    # L'index de la pièce suivante vient d'être modifié
    def nextPieceIndexChanged(self, nextPieceIndex):
        self._drawNextPiece(nextPieceIndex)
        self._updateDisplay()

    # La partie est terminée
    def gameFinished(self):
        # dont acte !
        self.status_ = self.GAME_STOPPED
    
    #   Méthodes à usage interne
    #
    
    # Dessin de tous les "carrés" non vide d'une pièce donné avec la couleur fournie
    #   le paramètre inBoard indique si les coordonnées correspondent à l'espace de jeu
    #
    def _drawSinglePiece(self, datas, cornerX, cornerY, colourID, inBoard = True, shadow = False):
        
        # Indice de la première rangée visible
        if True == inBoard:
            rowFirst =  board.PLAYFIELD_HEIGHT -1 - cornerY
            rowFirst = rowFirst* -1 if rowFirst < 0 else 0
        else:
            rowFirst = 0    # On affiche tout ...
        
        # Changement de repère
        xFirst,y,w,h = self._changeCoordonateSystem(cornerX, cornerY - rowFirst, inBoard)
        
        for row in range(rowFirst, PIECE_HEIGHT):
            x = xFirst
            for col in range(PIECE_WIDTH):
                colour = datas[row][col]
                if colour != COLOUR_ID_BOARD:
                    self._drawBlock(x, y, colourID, inBoard, shadow)  # Affichage des cubes non-vides
                x+=w
            y+=h

    # Affichage de la pièce suivante
    def _drawNextPiece(self, pieceIndex):
        # On efface l'ancienne piece
        self._eraseBlocks(0, 0, 4, 4, COLOUR_ID_BOARD, False)
        
        # puis la nouvelle
        if -1 != pieceIndex : 
            # Affichage de la nouvelle pièce
            datas, colourIndex = self.board_.nextPieceDatas()
            self._drawSinglePiece(datas, 0, 0, colourIndex, False)

    # Mise en forme d'un nombre avec séparateur de milliers
    def _formatNumber(self, number):
        current = str(number)
        text = ''
        pos = len(current) - 1
        while pos > 2 :
            text = ' ' + current[pos-2:pos+1] + text
            pos-=3
        text = current[:pos+1] + text
        return text
# EOF