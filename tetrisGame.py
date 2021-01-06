# coding=UTF-8
#
#   File     :   tetrisGame.py
#
#   Authors     :   JHB
#
#   Description :   Tetris'outputs - abstract class 
#                   
#   Comment    :   min Python 3.xx
#
#   Version     :   0.6.2
#
#   Date        :   2021/01/06
#

import sharedConsts
from eventHandler import eventHandler
import board
from piece import PIECE_WIDTH, PIECE_HEIGHT, pieceStatus
from colorizer import colorizer, backColor, textColor, textAttribute

# tetrisGame - abstract class
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
    STATUS_CREATED = 0
    STATUS_INIT    = 1
    STATUS_RUNNING = 2
    STATUS_STOPPED = 4
    STATUS_CANCELED = 8
    
    # Members
    board_  = None
    status_ = STATUS_CREATED  # Just created
    currentPos_ = None

    itemTexts_     = ["Score", "Level", "Lines", "Next piece"]

    # Dimensions & position
    gameWidth_ , gameHeight_, gameLeft_, gameTop_ = 0, 0, 0, 0
    itemDims_ = None

    # Construction
    def __init__(self):
        self.status_ = self.STATUS_CREATED
        self.itemDims_  = [None] * 3

    # Destruction
    def __del__(self):
        self.clear()

    # Display "hall of fame"
    #   Basic display on console
    def showScores(self, me, currentScore, bestScores):
        if None == bestScores:
            return

        txtColours = colorizer(True, False)

        if me and len(me):
            print("\n Best scores for", txtColours.colored(me, formatAttr=[textAttribute.BOLD]), " :\n")
        else:
            print("\n Best scores :\n")
        
        currentPos = -1 if currentScore == None else bestScores[0][0]
        
        for index in range(len(bestScores)-1):
            score = bestScores[index+1]
            line = ">>>" if index == currentPos else " "
            line+= "\t" + str(index + 1) + " -" +  ("  " if index<9 else " ")
            line+=str(self._formatNumber(score[0]))
            line+="\t"
            if len(score[1]):
                line+="- "
                line+=score[1]
            if index == currentPos:
                line+=" <<<"
                print(txtColours.colored(line, textColor.RED))
            else:
                print(line)
        
        # and finally the current score
        if None != currentScore:
            print("\nYour score : ", txtColours.colored(str(self._formatNumber(currentScore)), formatAttr=[textAttribute.BOLD]))

    def isRunning(self):
        return self.STATUS_RUNNING == self.status_

    # Cancel the game
    #
    def cancel(self):
        # Already escaped ?
        if not self.isCancelled():
            self.status_ |= self.STATUS_CANCELED
        # stop the game
        self.end(True)
    # Escaped/canceled par the user ?
    def isCancelled(self):
        return ((self.status_ & self.STATUS_CANCELED) == self.STATUS_CANCELED)

    # Force the end of the game
    def end(self, force = False):
        if force:
            self.status_ |= self.STATUS_CANCELED
        else:
            self.status_ = self.STATUS_STOPPED

    # Finish ...
    def clear(self):
        pass

    def waitForEvent(self):
        pass
    
    # Non-blocking access to the keyboard
    #   return a char
    def checkKeyboard(self):
        return ''

    # Set a "pointer" to the game'board
    #
    def setBoard(self, currentBoard):
        self.board_ = currentBoard

    # Let's go
    #
    def start(self):
        # Check the object state
        if self.STATUS_INIT == self.status_ or self.STATUS_STOPPED == self.status_:
            # Initializations ...
            self.currentPos_ = None

            # Drawings
            self._drawBackGround()
            self.drawBoard()
            self.drawScore()
            self.drawLevel()
            self.drawLines()

            # Let's go
            self.status_ = self.STATUS_RUNNING
            self.board_.start()
            
            self._updateDisplay()
            return True

        return False

    # Helpers
    #
    def drawScore(self):
        self._drawNumValue(0, self.board_.score())
    def drawLevel(self):
        self._drawNumValue(1, self.board_.level())
    def drawLines(self):
        self._drawNumValue(2, self.board_.lines())
    def drawNextPiece(self):
        self._drawNextPiece(self.board_.nextPieceIndex())

    # Draw all
    #
    def drawBoard(self):
        if None == self.board_: # Anything to draw ?
            return

        leftFirst, top, w, h = self._changeCoordonateSystem(0,0,True)

        # Draw all the blocks (colored or not)
        for y in range(sharedConsts.PLAYFIELD_HEIGHT):
            left = leftFirst
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
    
    # Draw a line of text (and erase the prrevious value)
    def _drawText(self, index, text):
        pass

    # Draw borders
    def _drawBackGround(self):
        pass

    # Change the origin and the coordinate system
    #   (x,y) are to be translated
    #   inBoard : int he board (True) or in the "next piece" area
    #
    #   returns a tuple (x,y, dx, dy) in the new coordonate system
    #       dx, dy  are the width and height of the block in the screen
    # 
    def _changeCoordonateSystem(self, x, y, inBoard = True):
        return (x,y,1,1)

    # Draw a single colored block
    #
    def _drawBlock(self, left, top, colourID, inBoard, shadow = False):
        pass

    # Erase a tetramino
    #
    def _eraseBlocks(self, left, top, width, height, colourID, inBoard):
        pass

    # eventHandler overloads
    #

    # The position of  tetraminos has changed
    #   The piece must be erased from its previous pos and redrawwn at the new position
    #
    def piecePosChanged(self, newState):
        # Any changes (or rotation) ?
        if self.currentPos_ == None  or self.currentPos_ != newState: 
            # Erase the tetramino (and maybe it's shadow)
            if None != self.currentPos_:                    
                self._drawSinglePiece(self.board_.pieceDatas(self.currentPos_.index_, self.currentPos_.rotationIndex_), self.currentPos_.leftPos_, self.currentPos_.topPos_, sharedConsts.COLOUR_ID_BOARD)
                if -1 != self.currentPos_.shadowTopPos_:
                    # then the shadow
                    self._drawSinglePiece(self.board_.pieceDatas(self.currentPos_.index_, self.currentPos_.rotationIndex_), self.currentPos_.leftPos_, self.currentPos_.shadowTopPos_, sharedConsts.COLOUR_ID_BOARD)

            # ... redraw
            if -1 != newState.shadowTopPos_:
                # first : the shadow
                self._drawSinglePiece(self.board_.pieceDatas(newState.index_, newState.rotationIndex_), newState.leftPos_, newState.shadowTopPos_ , sharedConsts.COLOUR_ID_SHADOW, shadow = True)
            
            # and then the tetramino (can recover the shadow !!!!)
            self._drawSinglePiece(self.board_.pieceDatas(newState.index_, newState.rotationIndex_), newState.leftPos_, newState.topPos_ , self.board_.tetraminos_[newState.index_].colour())

            self._updateDisplay()
            
            self.currentPos_ = pieceStatus(other = newState)

    # A tetramino is at the lowest possible position
    #
    def pieceReachedLowerPos(self):
        # Don't erase this piece !!!
        self.currentPos_ = None

    # Increase the score
    #
    def incScore(self, inc):
        super().incScore(inc)
        self.board_.incScore(inc)
        self.drawScore()
        self._updateDisplay()
        
    # The game level just changed
    #
    def levelChanged(self, newLevel):
        super().levelChanged(newLevel)
        self.board_.setLevel(newLevel)
        self.drawLevel()
        self._updateDisplay()

    # ...
    # 
    def allLinesCompletedRemoved(self, rowCount, totalLines):
        super().allLinesCompletedRemoved(rowCount, totalLines)
        self.board_.setLines(totalLines)
        
        self.drawBoard()
        self.drawLines()
        self._updateDisplay()

    # New index for the "next piece"
    #
    def nextPieceIndexChanged(self, nextPieceIndex):
        super().nextPieceIndexChanged(nextPieceIndex)
        self._drawNextPiece(nextPieceIndex)
        self._updateDisplay()

    # The game is over
    #
    def gameFinished(self):
        super().gameFinished()
        self.status_ = self.STATUS_STOPPED
    
    #   "internal" methods
    #
    
    # Draw a tetramino using the given colour
    #   inBoard : True => draw in the board, False => draw "next" piece
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
    #
    def _drawNextPiece(self, pieceIndex):
        # Erase the previous piece 
        self._eraseBlocks(0, 0, 4, 4, sharedConsts.COLOUR_ID_BOARD, False)
        
        # ... and the new one
        if -1 != pieceIndex :     
            datas, colourIndex = self.board_.nextPieceDatas()
            self._drawSinglePiece(datas, 0, 0, colourIndex, False)

    # Format integer
    #
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