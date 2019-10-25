# coding=UTF-8
#
#   Fichier     :   eventHandler.py
#
#   Auteur      :   JHB
#
#   Description :   Gestion / prise en compte des évènements
#                   Cette classe permet au gestionnaire de jeu d'appeler des méthodes du gestionnaire de rendu
#                   
#                   Cette classe est abstraite
#
#   Remarque    :   Nécessite Python 3.xx
#
#   Version     :   0.4.7
#
#   Date        :   25 octobre 2019
#

# Classe eventHandler
#   Gestion des évènements en provenance de l'espace de jeu et ayant une influence sur le rendu graphique
#
class eventHandler(object):

    # Chaînage
    nextHandler_ = None

    def setNextHandler(self, next = None):
        self.nextHandler_ = next
    def nextHandler(self):
        return self.nextHandler_

    # Méthodes à surcharger
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
    def scoreChanged(self, newScore):
        if None != self.nextHandler_:
            self.nextHandler_.scoreChanged(newScore)

    # Changement de niveau
    def levelChanged(self, newLevel):
        if None != self.nextHandler_:
            self.nextHandler_.levelChanged(newLevel)

    # Une ligne est complête (mais encore dans l'espace de jeu)
    def lineCompleted(self, rowIndex):
        if None != self.nextHandler_:
            self.nextHandler_.lineCompleted(rowIndex)

    # Toutes les lignes complêtes ont été retirées
    def allLinesCompletedRemoved(self, rowCount, totalRows):
        if None != self.nextHandler_:
            self.nextHandler_.allLinesCompletedRemoved(rowCount, totalRows)

    # L'index  de la pièce suivante vient d'être modifié
    def nextPieceIndexChanged(self, nextPieceIndex):
        if None != self.nextHandler_:
            self.nextHandler_.nextPieceIndexChanged(nextPieceIndex)

    # La partie est terminée
    def gameFinished(self):
        if None != self.nextHandler_:
            self.nextHandler_.gameFinished()
# EOF