# coding=UTF-8
#
#   File     :   eventHandler.py
#
#   Authors     :   JHB
#
#   Description :   Gestion / prise en compte des évènements
#                   Cette classe permet au gestionnaire de jeu d'appeler des méthodes du gestionnaire de rendu
#                   
#                   Cette classe est abstraite
#
#   Remarque    :   Nécessite Python 3.xx
#
#   Version     :   0.5.3-3
#
#   Date        :   2020/09/28
#

# Classe eventHandler
#   Gestion des évènements en provenance de l'espace de jeu et ayant une influence sur le rendu graphique
#
class eventHandler(object):

    # Members
    #

    # Chaînage
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