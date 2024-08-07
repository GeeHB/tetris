# coding=UTF-8
#
#   File     :   eventHandler.py
#
#   Author     :   JHB
#
#   Description :   Handle the notifications to update display
#
#                   This is an abstract class
#
#   Comment    :   Python 3.xx
#

# eventHandler object
#   Handle the notifications to update display
#
class eventHandler(object):

    # Members
    #

    # Other handler ?
    nextHandler_ = None

    def setNextHandler(self, next = None):
        self.nextHandler_ = next
    def nextHandler(self):
        return self.nextHandler_

    # Overloadable methods
    #

    # Resizable ?
    #
    @property
    def resizable(self) -> bool:
        return True
    @resizable.setter
    def resizable(self, value):
        pass

    # The position of  tetraminos has changed
    #   The piece must be erased from its previous pos and redrawwn at the new position
    #
    def piecePosChanged(self, newState):
        if self.nextHandler_ is not None:
            self.nextHandler_.piecePosChanged(newState)

    # A tetramino is at the lowest possible position
    #
    def pieceReachedLowerPos(self):
        if self.nextHandler_ is not None:
            self.nextHandler_.pieceReachedLowerPos()

    # Increase the score
    #
    def incScore(self, inc):
        if self.nextHandler_ is not None:
            self.nextHandler_.incScore(inc)

    # The game level just changed
    #
    def levelChanged(self, newLevel):
        self.level = newLevel
        if self.nextHandler_ is not None:
            self.nextHandler_.levelChanged(newLevel)

    # A line has just been completed (but is still visible)
    #
    def lineCompleted(self, rowIndex):
        if self.nextHandler_ is not None:
            self.nextHandler_.lineCompleted(rowIndex)

    # ...
    #
    def allLinesCompletedRemoved(self, rowCount, totalLines):
        if self.nextHandler_ is not None:
            self.nextHandler_.allLinesCompletedRemoved(rowCount)

    # New index for the "next piece"
    #
    def nextPieceIndexChanged(self, nextPieceIndex):
        if self.nextHandler_ is not None:
            self.nextHandler_.nextPieceIndexChanged(nextPieceIndex)

    # The game is over
    #
    def gameFinished(self):
        if self.nextHandler_ is not None:
            self.nextHandler_.gameFinished()
# EOF
