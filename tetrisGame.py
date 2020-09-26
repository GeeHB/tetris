# coding=UTF-8
#
#   File     :   tetrisGame.py
#
#   Authors     :   JHB
#
#   Description :   Tetris'outputs - bastrct class 
#                   
#
#   Remarque    :   Nécessite Python 3.xx
#
#   Version     :   0.5.2
#
#   Date        :   2020/09/21
#

import sharedConsts
from eventHandler import eventHandler
import board
from piece import PIECE_WIDTH, PIECE_HEIGHT, pieceStatus

# Classe tetrisGame
#
class tetrisGame(eventHandler):

    EVT_KEYDOWN     = 1  # By default the event doesn't exist
    EVT_QUIT        = 2
    
    # Default keys
    # can (must) be overloaded
    KEY_LEFT        = '4'
    KEY_RIGHT       = '6'
    KEY_ROTATE_LEFT = '5'
    KEY_ROTATE_RIGHT= '0'
    KEY_DOWN        = '2'
    KEY_FALL        = ' '
    KEY_START       = chr(13)   # "enter"
    KEY_QUIT        = 'q'
    KEY_STOP        = KEY_QUIT
    KEY_SHADOW_MODE = 'o'
    KEY_NORMAL_MODE = 'n'
    KEY_SCORES      = 'h'
    KEY_NOEVENT     = ''

    # Game status
    GAME_CREATED = 0
    GAME_INIT    = 1
    GAME_RUNNING = 2
    GAME_STOPPED = 3
    
    # Members
    board_  = None          # Espace de jeu
    status_ = GAME_CREATED  # Par défaut l'objet est "juste" crée
    currentPos_ = None      # Ou se trouve la pièce actuelle (pour pouvoir l'effacer ...)

    itemTexts_     = ["Score", "Level", "Lines", "Next piece"]

    # Dimensions & position
    gameWidth_ , gameHeight_, gameLeft_, gameTop_ = 0, 0, 0, 0
    itemDims_ = None

    # Construction
    def __init__(self):
        self.status_ = self.GAME_CREATED
        self.itemDims_  = [None] * 3

    # Destruction
    def __del__(self):
        self.clear()

    # Display "hall of fame"
    #   Basic display on console
    def showScores(self, me, currentScore, bestScores):
        if None == bestScores:
            return

        if me and len(me):
            print("\n Best scores of ", me, " :\n")
        else:
            print("\n Best scores :\n")
        
        currentPos = bestScores[0]
        currentPos[0] += 1

        for index in range(len(bestScores)-1):
            score = bestScores[index+1]
            line = ">>>" if index == currentPos[0] else " "
            line+= "\t" + str(index + 1) + " -" +  ("  " if index<9 else " ")
            line+=str(score[0])
            line+="\t"
            if len(score[1]):
                line+="- "
                line+=score[1]
            if index == currentPos[0]:
                line+="<<<"
            print(line)
        
        # and finally the current score
        print("\nYour score : ", currentScore)

    # Jeu en cours ?
    def isRunning(self):
        return self.GAME_RUNNING == self.status_

    # Force the end of the game
    def end(self):
        self.status_ = self.GAME_STOPPED

    # Finish ...
    def clear(self):
        pass

    def waitForEvent(self):
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
            self._drawBackGround()

            # Dessin de l'espace de jeu
            self.drawBoard()

            # Affichage du score et du niveau
            self.drawScore()
            self.drawLevel()
            self.drawLines()

            # C'est parti
            self.status_ = self.GAME_RUNNING
            self.board_.start()
            
            # Dessin de la pièce suivante
            #self._drawNextPiece(self.board_.nextPieceIndex())

            # Ok
            self._updateDisplay()
            return True
        
        # Sinon on ne fait rien
        return False

    # Helpers
    def drawScore(self):
        self._drawNumValue(0, self.board_.score())

    def drawLevel(self):
        self._drawNumValue(1, self.board_.level())

    def drawLines(self):
        self._drawNumValue(2, self.board_.lines())

    def drawNextPiece(self):
        self._drawNextPiece(self.board_.nextPieceIndex())

    # Affichage de tout l'espace de jeu
    def drawBoard(self):
        if None == self.board_:
            # Pas de données !!!
            return

        # Changement de repère
        leftFirst, top, w, h = self._changeCoordonateSystem(0,0,True)

        # Affichage de tous les blocs (colorés ou pas)
        for y in range(sharedConsts.PLAYFIELD_HEIGHT):
            left = leftFirst    # A chaque nouvelle ligne on replace le "curseur"
            for x in range(sharedConsts.PLAYFIELD_WIDTH):        
                self._drawBlock(left, top, self.board_.playField_[y][x], True)
                left+=w
            top-=h
        
        self._updateDisplay()

    def _updateDisplay(self):
        pass
    
    def _drawNumValue(self, index, value):           
        text = self.itemTexts_[index] + " : " + self._formatNumber(value)
        self._drawText(index, text)
    
    # Affichage d'un texte avec effacement de l'ancienne valeur
    def _drawText(self, index, text):
        pass

    # Dessin des bordures (espace de jeu et éventuellement pièces suivantes)
    def _drawBackGround(self):
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
                self._drawSinglePiece(self.board_.pieceDatas(self.currentPos_.index_, self.currentPos_.rotationIndex_), self.currentPos_.leftPos_, self.currentPos_.topPos_, sharedConsts.COLOUR_ID_BOARD)
                if -1 != self.currentPos_.shadowTopPos_:
                    # puis l'ombre
                    self._drawSinglePiece(self.board_.pieceDatas(self.currentPos_.index_, self.currentPos_.rotationIndex_), self.currentPos_.leftPos_, self.currentPos_.shadowTopPos_, sharedConsts.COLOUR_ID_BOARD)

            ## ... puis on l'affiche à la nouvelle position
            if -1 != newState.shadowTopPos_:
                # d'abord l'ombre
                self._drawSinglePiece(self.board_.pieceDatas(newState.index_, newState.rotationIndex_), newState.leftPos_, newState.shadowTopPos_ , sharedConsts.COLOUR_ID_SHADOW, shadow = True)
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

    # Increase the score
    def incScore(self, inc):
        super().incScore(inc)
        self.board_.incScore(inc)
        self.drawScore()
        self._updateDisplay()
        
    # Change game level
    def levelChanged(self, newLevel):
        super().levelChanged(newLevel)
        self.board_.setLevel(newLevel)
        self.drawLevel()
        self._updateDisplay()

    # Toutes les lignes complêtes ont été retirées
    def allLinesCompletedRemoved(self, rowCount, totalLines):
        super().allLinesCompletedRemoved(rowCount, totalLines)
        self.board_.setLines(totalLines)
        # Réaffichage de l'espace de jeu
        self.drawBoard()
        self.drawLines()
        self._updateDisplay()

    # L'index de la pièce suivante vient d'être modifié
    def nextPieceIndexChanged(self, nextPieceIndex):
        super().nextPieceIndexChanged(nextPieceIndex)
        self._drawNextPiece(nextPieceIndex)
        self._updateDisplay()

    # La partie est terminée
    def gameFinished(self):
        super().gameFinished()
        # dont acte !
        self.status_ = self.GAME_STOPPED
    
    #   Méthodes à usage interne
    #
    
    # Dessin de tous les "carrés" non vide d'une pièce donné avec la couleur fournie
    #   le paramètre inBoard indique si les coordonnées correspondent à l'espace de jeu
    #
    def _drawSinglePiece(self, datas, cornerX, cornerY, colourID, inBoard = True, shadow = False):
        
        # First visible row ID
        if True == inBoard:
            rowFirst =  sharedConsts.PLAYFIELD_HEIGHT -1 - cornerY
            rowFirst = rowFirst* -1 if rowFirst < 0 else 0
        else:
            rowFirst = 0    # all rows are visible
        
        xFirst,y,w,h = self._changeCoordonateSystem(cornerX, cornerY - rowFirst, inBoard)
        
        for row in range(rowFirst, PIECE_HEIGHT):
            x = xFirst
            for col in range(PIECE_WIDTH):
                colour = datas[row][col]
                if colour != sharedConsts.COLOUR_ID_BOARD:
                    self._drawBlock(x, y, colourID, inBoard, shadow)  # only non-empty squares
                x+=w
            y+=h

    # Display the next piece
    def _drawNextPiece(self, pieceIndex):
        # Erase the previous piece 
        self._eraseBlocks(0, 0, 4, 4, sharedConsts.COLOUR_ID_BOARD, False)
        
        # ... and the new one
        if -1 != pieceIndex :     
            datas, colourIndex = self.board_.nextPieceDatas()
            self._drawSinglePiece(datas, 0, 0, colourIndex, False)

    # Format integer
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