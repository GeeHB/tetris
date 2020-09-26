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
#   Version     :   0.5.2
#
#   Date        :   2020/09/21
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

    # Un pièce vient de bouger (elle doit donc être effacée à son ancienne position et affichée à la nouvelle)
    def piecePosChanged(self, newState):
        if None != self.nextHandler_:
            self.nextHandler_.piecePosChanged(newState)

    # Une pièce a atteint le plus bas niveau possible de l'espace de jeu
    def pieceReachedLowerPos(self):
        if None != self.nextHandler_:
            self.nextHandler_.pieceReachedLowerPos()

    # Le score vient de changer
    def incScore(self, inc):
        if None != self.nextHandler_:
            self.nextHandler_.incScore(inc)

    # Changement de niveau
    def levelChanged(self, newLevel):
        self.level_ = newLevel
        if None != self.nextHandler_:
            self.nextHandler_.levelChanged(newLevel)

    # Une ligne est complête (mais encore dans l'espace de jeu)
    def lineCompleted(self, rowIndex):
        if None != self.nextHandler_:
            self.nextHandler_.lineCompleted(rowIndex)

    # Toutes les lignes complêtes ont été retirées
    def allLinesCompletedRemoved(self, rowCount, totalLines):
        if None != self.nextHandler_:
            self.nextHandler_.allLinesCompletedRemoved(rowCount)

    # L'index  de la pièce suivante vient d'être modifié
    def nextPieceIndexChanged(self, nextPieceIndex):
        if None != self.nextHandler_:
            self.nextHandler_.nextPieceIndexChanged(nextPieceIndex)

    # La partie est terminée
    def gameFinished(self):
        if None != self.nextHandler_:
            self.nextHandler_.gameFinished()
# EOF