# coding=UTF-8
#
#   File     :   board.py
#
#   Author      :   JHB
#
#   Description :   board class - gameplay
#                   The matrix with all the colored bloceked (ie dirty lines and / or posed tetraminos)
#
#   Comment    :    Python 3.xx needed
#

import random
import consts
import piece
import shapes
from eventHandler import eventHandler

# tetrisParameters
#   game's parameters
#
class tetrisParameters:

    # Members
    #
    startLevel_ = 1
    dirtyLines_ = 0
    shadow_ = False
    cursesAvailable_ = False
    useGUI_ = True
    showScores_ = False
    user_ = None

    # Constructor
    #
    def __init__(self, other = None):
        if None != other:
            # Check input parameters
            self.startLevel_ = other.startLevel_ 
            self.dirtyLines_ = other.dirtyLines_
            self.shadow_ = other.shadow_
            self.useGUI_ = other.useGUI_
            self.showScores_ = other.showScores_
            self.user_ = other.user_

# board
#   Handle the gameplay and the game (without display !)
#
class board(object):
    # Members
    #
    tetraminos_ = []    # Tetraminos (all diff. rotation states)

    playField_  = []
    
    parameters_ = None

    score_, lines_, level_ = 0, 0, 1
    
    currentPiece_ = piece.pieceStatus()   
    nextIndex_ = -1       # next piece index

    eventHandler_ = None  # Events handler

    # Methods
    #

    # Construction
    def __init__(self, handler = None):
        
        random.seed()

        # Events handler
        self.eventHandler_ = handler if not None == handler else eventHandler()

        # Build the tetraminos'list
        for shape in shapes.shapes_:
            self.tetraminos_.append(piece.piece(template = shape))

    # Game's paraeters
    def parameters(self):
        return self.parameters_ 

    def setParameters(self, params = None):   
        self.parameters_ = tetrisParameters(params)
        self.score = 0
        self.lines = 0
        self.level = self.parameters_.startLevel_
        self.setNextPieceIndex(-1)

        # Initialization of tetraminos (no rotation)
        for sPiece in self.tetraminos_:
            sPiece.rotateBack()
        
        self.playField_  = []
        
        # Add dirty lines ...
        maxLines = consts.PLAYFIELD_HEIGHT - piece.PIECE_HEIGHT - 1
        if self.parameters_.dirtyLines_ > maxLines:
            self.parameters_.dirtyLines_ = maxLines
        elif self.parameters_.dirtyLines_ < 0:
            self.parameters_.dirtyLines_ = 0

        for _ in range(self.parameters_.dirtyLines_):
            self._addDirtyLine()
        
        # other lines are empty 
        for _ in range(self.parameters_.dirtyLines_, consts.PLAYFIELD_HEIGHT):
            self.playField_.append([0] * consts.PLAYFIELD_WIDTH)

    # Let's play
    #
    def start(self):
        self.newPiece() # the first piece

    # Game level
    #
    @property
    def level(self):
        return self.level_
    @level.setter
    def level(self, value):
        self.level_ = value
    def incLevel(self):
        self.level += 1
        return self.level

    # Score
    #
    @property
    def score(self):
        return self.score_
    @score.setter
    def score(self, value):
        self.score_ = value
    def incScore(self, inc):    # +=
        self.score+=inc
        return self.score

    # Lines (done)
    #
    @property
    def lines(self):
        return self.lines_
    @lines.setter
    def lines(self, value = 0):
        self.lines_ = value
    def incLines(self, inc):    # +=
        self.lines+=inc
        return self.lines

    # Next piece
    #
    def nextPieceIndex(self):
        return self.nextIndex_
    def setNextPieceIndex(self, index):
        self.nextIndex_ = index
    
    # About a piece ...
    #  returns the tuple (blocks'datas, block colour)
    def nextPieceDatas(self):
        if self.nextPieceIndex() < 0 or self.nextPieceIndex() >= len(self.tetraminos_): # L'index doit être correct
            raise IndexError
        return (self.tetraminos_[self.nextPieceIndex()].datas(), self.tetraminos_[self.nextPieceIndex()].colour())

    # Datas of a piece
    #
    def pieceDatas(self, index, rotIndex):
        if index < 0 or index >= len(self.tetraminos_) or rotIndex < 0 or rotIndex >= self.tetraminos_[index].maxRotations(): # L'index doit être correct
            raise IndexError
        return self.tetraminos_[index][rotIndex]

    # New pièce
    #
    def newPiece(self):
        # New indexes
        self.currentPiece_.index_ = self._newPieceIndex() if -1 == self.nextPieceIndex() else self.nextPieceIndex()
        self.setNextPieceIndex(self._newPieceIndex())
        
        # The piece is a the top of the game play, centered horizontally
        self.currentPiece_.leftPos_ = int((consts.PLAYFIELD_WIDTH - piece.PIECE_WIDTH) / 2)
        self.currentPiece_.topPos_ = consts.PLAYFIELD_HEIGHT + self.tetraminos_[self.currentPiece_.index_].verticalOffset()
        self.currentPiece_.minHeight_ = -1          # no shadow
        self.currentPiece_.rotationIndex_ = 0       # no rotation
        self.tetraminos_[self.currentPiece_.index_].rotateBack()    

        # Notify the display manager
        self.eventHandler_.nextPieceIndexChanged(self.nextPieceIndex())

        # Can I go on line down ?
        if False == self._down(True):
            # No => the game is over
            self.eventHandler_.gameFinished()

    # Rotation(s)
    #

    # anti-clockwise
    def rotateLeft(self):
        
        # Rotate
        rotIndex = self.tetraminos_[self.currentPiece_.index_].rotateLeft()

        # Possible ?
        if True == self._canMove():
            self.currentPiece_.rotationIndex_ = rotIndex
            
            # Apply rotation 
            self.piecePosChanged()
            return True

        # No => cancel rotation
        self.tetraminos_[self.currentPiece_.index_].rotateRight()
        return False

    #
    # Piece movements
    #

    # Move left
    #
    def left(self):
        
        # Test position
        if True == self._canMove(leftPos = self.currentPiece_.leftPos_ - 1):
            # Correct
            self.currentPiece_.leftPos_ -= 1
            
            # apply chgmnt
            self.piecePosChanged()
            return True
        
        # Impossible
        return False

    # Move right
    #
    def right(self):
        
        # Test position
        if True == self._canMove(leftPos = self.currentPiece_.leftPos_ + 1):
            # Correct
            self.currentPiece_.leftPos_ += 1
            
            # apply chgmnt
            self.piecePosChanged()
            return True
        
        # Impossible
        return False

    # One line down
    def down(self):
       return self._down()

    def _down(self, newPiece = False):
        
        # Test position
        if True == self._canMove(topPos = self.currentPiece_.topPos_ - 1):
            # correct
            self.currentPiece_.topPos_ -= 1
            self.piecePosChanged()
            return True
        
        if not newPiece:
            self._reachLowerPos()
    
        return False

    # Go down (as many lines as possible)
    #
    def fall(self):
        
        bottom = self._minTopPosition()
        delta = self.currentPiece_.topPos_ - bottom
        self.currentPiece_.topPos_ = bottom

        # updates ...
        self.piecePosChanged()
        self._reachLowerPos(delta)
    
    # "private" methods
    #

    # Get a new index for the next piece
    #
    def _newPieceIndex(self):
        return random.randint(0, len(self.tetraminos_) - 1)

    # Can the current piece be at the given position ?
    #
    def _canMove(self, leftPos = None, topPos = None):

        # No coordinates => use current pos.
        if None == leftPos:
            leftPos = self.currentPiece_.leftPos_
        if None == topPos:
            topPos = self.currentPiece_.topPos_

        # Piece's datas
        datas = self.tetraminos_[self.currentPiece_.index_].datas()

        # Test all the contained blocks starting from bottom
        # ... to optimize a little ...
        for y in range(piece.PIECE_HEIGHT-1, -1, -1):
            for x in range(piece.PIECE_WIDTH):
                if not 0 == datas[y][x]:
                    # "real" position of the block 
                    realX = x + leftPos
                    realY = topPos - y 

                    # out of the gameplay's limits ?
                    if realX < 0 or realY < 0 or realX >= consts.PLAYFIELD_WIDTH : # or realY >= PLAYFIELD_HEIGHT
                        return False
                    
                    # Is there a block at this place ?
                    if realY < consts.PLAYFIELD_HEIGHT and not self.playField_[realY][realX] == 0:
                        return False

        # Yes => the position is valid
        return True

    # Get a piece min. pos. index (vertical value)
    #
    def _minTopPosition(self):
        currentTop = self.currentPiece_.topPos_

        # Try to move one line down
        while self._canMove(self.currentPiece_.leftPos_, currentTop):
            currentTop -= 1

        # current pos. is invalid => go up one line
        return currentTop+1

    # Put the tetramino a the current position
    #
    def _putPiece(self, colour = None):
        if None == colour:
            vertPos = self.currentPiece_.topPos_

            realColour = self.tetraminos_[self.currentPiece_.index_].colourIndex_
        else:
            vertPos = self.currentPiece_.shadowTopPos_
            realColour = colour

        datas = self.tetraminos_[self.currentPiece_.index_].datas()

        # Copuy all the colored blocks in the gameplay
        #
        maxY = 0 if consts.PLAYFIELD_HEIGHT - vertPos >= 1 else vertPos - consts.PLAYFIELD_HEIGHT + 1
        for y in range(maxY, piece.PIECE_HEIGHT):
            for x in range(piece.PIECE_WIDTH):
                if not 0 == datas[y][x] and (vertPos - y) < consts.PLAYFIELD_HEIGHT:
                    self.playField_[vertPos - y][x + self.currentPiece_.leftPos_] = realColour

    # Clear and remove a line (completed)
    #
    def _clearLine(self, index):
        if index < 0 or index >= consts.PLAYFIELD_HEIGHT:
            return
        
        # Remove the line from the screen
        self.playField_.pop(index)

        # Add a ne empty line 
        self.playField_.append([0] * consts.PLAYFIELD_WIDTH)

    # Add a randomly generated dirty line at the bottom of the gameplay
    #
    def _addDirtyLine(self):
        cubes = random.randint(1,2 ** consts.PLAYFIELD_WIDTH - 1)
        line = []
        sBit = 1 # 2 ^ 0
        for _ in range(consts.PLAYFIELD_WIDTH):
            # bit is set ?
            if cubes & sBit > 0:
                # yes => add a colored block
                line.append(random.randint(1,7))
            else:
                # no => empty space
                line.append(0)

            # next bit value
            sBit *= 2
        
        # Add the line
        self.playField_.append(line)
    
    # The piece is at the lowest possible level
    #
    def _reachLowerPos(self, downRowcount = 0):
        
        # put it
        self._putPiece()
        
        # Notify
        self.eventHandler_.pieceReachedLowerPos()
        
        # Are line(s) completed ?
        # Check the 4 possible lines
        completedLines = []
        maxY = self.currentPiece_.topPos_ + 1
        if maxY > consts.PLAYFIELD_HEIGHT:
            maxY = consts.PLAYFIELD_HEIGHT
        for line in range(self.currentPiece_.topPos_ - piece.PIECE_HEIGHT + 1, maxY):
            currentLineValue = 1
            for col in range(consts.PLAYFIELD_WIDTH):
                currentLineValue *= self.playField_[line][col]  # one empty block and the whole line "value" = 0

            # The line is complete
            if not 0 == currentLineValue:
                completedLines.insert(0,line)
                
        for lineIndex in completedLines:
            # Animate
            self.eventHandler_.lineCompleted(lineIndex)
            
            # update datas
            self._clearLine(lineIndex)

        # Update the score
        completedCount = len(completedLines)
        if completedCount >= 1:
            delta = 0
            if 1 == completedCount:
                delta += 100
            elif 2 == completedCount:
                delta += 300
            elif 3 == completedCount:
                delta += 500
            else:
                # 4 !
                delta += 800    # * 800 ?
            
            mult = 100 + consts.SCORE_SPEED_GAME * downRowcount + consts.SCORE_DIRTY_LINES * self.parameters_.dirtyLines_ + consts.SCORE_LEVEL_VALUATION * self.lines_
            if False == self.parameters_.shadow_:
                mult+=consts.SCORE_NO_SHADOW
            
            self.eventHandler_.incScore(int(delta*mult/100))

        if 0 != completedCount:
            self.eventHandler_.allLinesCompletedRemoved(completedCount, self.lines + completedCount)            

        # Get a new piece
        self.newPiece()

    # The piece has moved or rotated
    #
    def piecePosChanged(self):

        # Compute the pos ot the shadow ?
        if True == self.parameters_.shadow_:
            self.currentPiece_.shadowTopPos_ = self._minTopPosition()

        # Notification
        self.eventHandler_.piecePosChanged(self.currentPiece_)

# EOF