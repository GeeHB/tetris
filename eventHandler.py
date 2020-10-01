# coding=UTF-8
#
#   File     :   eventHandler.py
#
#   Authors     :   JHB
#
#   Description :   Handle the notifications to update display
#                   
#                   This is an abstract class
#
#   Remarque    :   Python 3.xx
#
#   Version     :   0.5.3-5
#
#   Date        :   2020/10/01
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

    # The position of  tetraminos has changed
    #   The piece must be erased from its previous pos and redrawwn at the new position
    #
    def piecePosChanged(self, newState):
        if None != self.nextHandler_:
            self.nextHandler_.piecePosChanged(newState)

    # A tetramino is at the lowest possible position
    #
    def pieceReachedLowerPos(self):
        if None != self.nextHandler_:
            self.nextHandler_.pieceReachedLowerPos()

    # Increase the score
    #
    def incScore(self, inc):
        if None != self.nextHandler_:
            self.nextHandler_.incScore(inc)

    # The game level just changed
    #
    def levelChanged(self, newLevel):
        self.level_ = newLevel
        if None != self.nextHandler_:
            self.nextHandler_.levelChanged(newLevel)

    # A line has just been completed (but is still visible)
    #
    def lineCompleted(self, rowIndex):
        if None != self.nextHandler_:
            self.nextHandler_.lineCompleted(rowIndex)

    # ...
    #
    def allLinesCompletedRemoved(self, rowCount, totalLines):
        if None != self.nextHandler_:
            self.nextHandler_.allLinesCompletedRemoved(rowCount)

    # New index for the "next piece"
    #
    def nextPieceIndexChanged(self, nextPieceIndex):
        if None != self.nextHandler_:
            self.nextHandler_.nextPieceIndexChanged(nextPieceIndex)

    # The game is over
    #
    def gameFinished(self):
        if None != self.nextHandler_:
            self.nextHandler_.gameFinished()
# EOF