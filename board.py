# coding=UTF-8
#
#   File     :   board.py
#
#   Authors     :   JHB
#
#   Description :   Espace de jeu
#                   Modélisation de la matrice avec l'ensemble des pavés colorés
#
#   Remarque    :   Nécessite Python 3.xx
#
#   Version     :   0.5.2
#
#   Date        :   2020/09/21
# 

import random

import sharedConsts
import piece
import shapes
from eventHandler import eventHandler

# tetrisParameters
#   game's parameters
#
class tetrisParameters:
    startLevel_ = 1
    dirtyLines_ = 0
    shadow_ = False
    pygameAvailable_ = False
    cursesAvailable_ = False
    useGUI_ = True
    user_ = None

    # Constructor
    #
    def __init__(self, other = None):
        if None != other:
            # Check input parameters
            self.startLevel_ = other.startLevel_ 
            self.dirtyLines_ = other.dirtyLines_
            self.shadow_ = other.shadow_
            self.pygameAvailable_ = other.pygameAvailable_
            self.cursesAvailable_ = other.cursesAvailable_
            self.useGUI_ = other.useGUI_
            self.user_ = other.user_

# board
#   Handle the gameplay and the game (without display !)
#
class board(object):
    # Members
    #
    tetraminos_ = []    # Listes des pièces (avec leurs états)

    playField_  = []    # Matrice de jeu
    
    parameters_ = None  # Paramètres du jeu

    score_, lines_, level_ = 0, 0, 1
    
    # Informations sur le tetramino courant
    currentPiece_ = piece.pieceStatus()   
    nextIndex_ = -1      # Index de la pièce suivante

    eventHandler_ = None  # Gestionnaire d'évènements

    # Méthodes
    #

    # Constructeur
    def __init__(self, handler = None):
        
        # Initialisation du générateur pseudo-aléatoire
        random.seed()

        # Si aucun gestionnaire d'evt => on en crée un bidon
        self.eventHandler_ = handler if not None == handler else eventHandler()

        # Construction de la liste des tetraminos à partir de leurs modèles respectifs
        for shape in shapes.shapes_:
            self.tetraminos_.append(piece.piece(template = shape))

    # (re)initialisation de l'espace de jeu
    #   lines : nombre de lignes "sales" à ajouter au bas de l'écran
    def setParameters(self, params = None):
        
        self.parameters_ = tetrisParameters(params)
        self.setScore(0)
        self.setLines(0)
        self.setLevel(self.parameters_.startLevel_)
        self.setNextPieceIndex(-1)

        # Initialization of tetraminos
        for sPiece in self.tetraminos_:
            sPiece.rotateBack()
        
        self.playField_  = []
        
        # Add dirty lines ...
        maxLines = sharedConsts.PLAYFIELD_HEIGHT - piece.PIECE_HEIGHT - 1
        if self.parameters_.dirtyLines_ > maxLines:
            self.parameters_.dirtyLines_ = maxLines
        elif self.parameters_.dirtyLines_ < 0:
            self.parameters_.dirtyLines_ = 0

        for _ in range(self.parameters_.dirtyLines_):
            self._addDirtyLine()
        
        # other lines are empty 
        for _ in range(self.parameters_.dirtyLines_, sharedConsts.PLAYFIELD_HEIGHT):
            self.playField_.append([0] * sharedConsts.PLAYFIELD_WIDTH)

    # Accès aux paramètres
    def parameters(self):
        return self.parameters_ 

    # C'est parti
    def start(self):
        # La première pièce
        self.newPiece()

    # Niveau du jeu
    #
    def level(self):
        return self.level_
    def setLevel(self, level):
        self.level_ = level
    def incLevel(self):
        self.level_ += 1
        return self.level_

    # Score
    def score(self):
        return self.score_
    def setScore(self, score):
        self.score_ = score
    def incScore(self, inc):
        self.score_+=inc

    # Lignes
    def lines(self):
        return self.lines_
    def setLines(self, value = 0):
        self.lines_ = value
    def incLines(self, inc):
        self.lines_+=inc

    # Pièce suivante
    def nextPieceIndex(self):
        return self.nextIndex_
    def setNextPieceIndex(self, index):
        self.nextIndex_ = index
    
    # Retourne le tuple (datas, couleur)
    def nextPieceDatas(self):
        if self.nextPieceIndex() < 0 or self.nextPieceIndex() >= len(self.tetraminos_): # L'index doit être correct
            raise IndexError
        return (self.tetraminos_[self.nextPieceIndex()].datas(), self.tetraminos_[self.nextPieceIndex()].colour())

    # Piece selon son index et selon son etat ...
    def pieceDatas(self, index, rotIndex):
        if index < 0 or index >= len(self.tetraminos_) or rotIndex < 0 or rotIndex >= self.tetraminos_[index].maxRotations(): # L'index doit être correct
            raise IndexError
        return self.tetraminos_[index][rotIndex]

    # Nouvelle pièce
    def newPiece(self):
        # Mise à jour des index de pièces
        self.currentPiece_.index_ = self._newPieceIndex() if -1 == self.nextPieceIndex() else self.nextPieceIndex()
        self.setNextPieceIndex(self._newPieceIndex())
        
        # La pièce est en haut, pas encore visible et centrée horizontalement
        self.currentPiece_.leftPos_ = int((sharedConsts.PLAYFIELD_WIDTH - piece.PIECE_WIDTH) / 2)
        self.currentPiece_.topPos_ = sharedConsts.PLAYFIELD_HEIGHT + self.tetraminos_[self.currentPiece_.index_].verticalOffset()
        self.currentPiece_.minHeight_ = -1  # Pas d'ombre
        self.currentPiece_.rotationIndex_ = 0
        self.tetraminos_[self.currentPiece_.index_].rotateBack()    # Réinitialisation du compteur de rotations
        
        # On previent le gestionnaire d'affichage
        self.eventHandler_.nextPieceIndexChanged(self.nextPieceIndex())

        # Si je ne peux pas descendre alors la partie est terminée
        if False == self._down(True):
            self.eventHandler_.gameFinished()

    # Rotations
    #

    # Sens trigonométrique
    def rotateLeft(self):
        
        # On fait tourner la pièce
        rotIndex = self.tetraminos_[self.currentPiece_.index_].rotateLeft()

        # Possible ?
        if True == self._canMove():
            # On conserve l'indice de rotation
            self.currentPiece_.rotationIndex_ = rotIndex
            
            # La pièce peut tourner
            self.piecePosChanged()
            return True

        # Non => on annule la rotation
        self.tetraminos_[self.currentPiece_.index_].rotateRight()
        return False

    # Déplacement de la pièce
    #

    # Vers la gauche
    def left(self):
        
        # Test de la position
        if True == self._canMove(leftPos = self.currentPiece_.leftPos_ - 1):
            # Oui => on conserve la position et on pose la pièce
            self.currentPiece_.leftPos_ -= 1
            
            # La pièce peut tourner
            self.piecePosChanged()
            return True
        
        # Impossible
        return False

    # Vers la droite
    def right(self):
        
        # Test de la position
        if True == self._canMove(leftPos = self.currentPiece_.leftPos_ + 1):
            # Oui => on conserve la position et on pose la pièce
            self.currentPiece_.leftPos_ += 1
            self.piecePosChanged()
            return True
        
        # Impossible
        return False

    # Un cran vers le bas
    def down(self):
       return self._down()

    def _down(self, newPiece = False):
        
        # Test de la position
        if True == self._canMove(topPos = self.currentPiece_.topPos_ - 1):
            # Oui => on conserve la position et on pose la pièce
            self.currentPiece_.topPos_ -= 1
            self.piecePosChanged()
            return True
        
        # La pièce est déja en bas
        if False == newPiece:
            self._reachLowerPos()   # La pièce est en mouvement
    
        return False

    # Le plus bas possible
    def fall(self):
        
        # Jusqu'ou puis je descendre ?
        bottom = self._minTopPosition()
        delta = self.currentPiece_.topPos_ - bottom
        self.currentPiece_.topPos_ = bottom

        # Je suis maintenant en bas ...
        self.piecePosChanged() # La pièce doit être affichée en bas
        self._reachLowerPos(delta)
    
    # Méthodes privées
    #

    # Index d'une nouvelle pièce
    def _newPieceIndex(self):
        return random.randint(0, len(self.tetraminos_) - 1)

    # La piece peut-elle être positionnée aux coordonnées données ?
    #
    def _canMove(self, leftPos = None, topPos = None):

        # Si les coordonnées ne sont pas renseignées on utilise la position actuelle
        if None == leftPos:
            leftPos = self.currentPiece_.leftPos_
        if None == topPos:
            topPos = self.currentPiece_.topPos_

        # Récupération des données de la pièce
        datas = self.tetraminos_[self.currentPiece_.index_].datas()

        # On analyse tous les points en partant du bas
        # ... pour optimiser un peu les traitements
        for y in range(piece.PIECE_HEIGHT-1, -1, -1):
            for x in range(piece.PIECE_WIDTH):
                if not 0 == datas[y][x]:
                    # Il y a un cube à afficher ...
                    # Quelle serait sa position reèlle ?
                    realX = x + leftPos
                    realY = topPos - y  # L'origine du playground est en bas de l'écran

                    # En dehors de la zone de jeu ?
                    if realX < 0 or realY < 0 or realX >= sharedConsts.PLAYFIELD_WIDTH : # or realY >= PLAYFIELD_HEIGHT
                        return False
                    
                    # Y a t'il déja qque chose à cette place ?
                    if realY < sharedConsts.PLAYFIELD_HEIGHT and not self.playField_[realY][realX] == 0:
                        return False

        # De toute évidence oui !
        return True

    # Jusqu'à quelle position la pièce peut-elle descendre ?
    # Utile pour accèlerer la descente et pour calculer la position de l'ombre sous la pièce
    def _minTopPosition(self):
        currentTop = self.currentPiece_.topPos_

        # On essaye de descendre
        while self._canMove(self.currentPiece_.leftPos_, currentTop):
            currentTop -= 1     # On descend

        # On retourne la dernière position valide
        return currentTop+1

    # Dépôt du tetramino à l'emplacement courant
    def _putPiece(self, colour = None):
        if None == colour:
            # Ajout de la pièce dans son état "normal"
            vertPos = self.currentPiece_.topPos_

            # ... et à sa couleur
            realColour = self.tetraminos_[self.currentPiece_.index_].colourIndex_
        else:
            vertPos = self.currentPiece_.shadowTopPos_
            realColour = colour

         # Récupération des données de la pièce
        datas = self.tetraminos_[self.currentPiece_.index_].datas()

        # Copie des carrés non vides les uns après les autres dans l'espace de jeu
        #
        maxY = 0 if sharedConsts.PLAYFIELD_HEIGHT - vertPos >= 1 else vertPos - sharedConsts.PLAYFIELD_HEIGHT + 1
        for y in range(maxY, piece.PIECE_HEIGHT):
            for x in range(piece.PIECE_WIDTH):
                if not 0 == datas[y][x] and (vertPos - y) < sharedConsts.PLAYFIELD_HEIGHT:
                    self.playField_[vertPos - y][x + self.currentPiece_.leftPos_] = realColour

    # Effacement d'une ligne (pleine)
    def _clearLine(self, index):
        if index < 0 or index >= sharedConsts.PLAYFIELD_HEIGHT:
            return
        
        # Suppression de la ligne
        self.playField_.pop(index)

        # Ajout d'une ligne vide
        self.playField_.append([0] * sharedConsts.PLAYFIELD_WIDTH)

    # Ajout d'une ligne aléatoire en bas de l'écran
    def _addDirtyLine(self):
        cubes = random.randint(1,2 ** sharedConsts.PLAYFIELD_WIDTH - 1)
        line = []
        for index in range(sharedConsts.PLAYFIELD_WIDTH):
            # Le bit est-il mis ?
            sBit = 2 ** index
            if cubes & sBit > 0:
                # Oui => ajout d'un carré coloré
                line.append(random.randint(1,7))
            else:
                # non => ajout d'un espace
                line.append(0)
        
        # Ajout de la ligne
        self.playField_.append(line)
    
    # La pièce a atteint le niveau le plus bas possible
    def _reachLowerPos(self, downRowcount = 0):
        
        # On l'ajoute à l'espace de jeu
        self._putPiece()
        
        self.eventHandler_.pieceReachedLowerPos()
        
        # A t'on complété des lignes ?
        # On regarde les 4 lignes concernées
        # Une ligne est vide lorsque le produit des valeurs = 0
        completedLines = []
        maxY = self.currentPiece_.topPos_ + 1
        if maxY > sharedConsts.PLAYFIELD_HEIGHT:
            maxY = sharedConsts.PLAYFIELD_HEIGHT
        for line in range(self.currentPiece_.topPos_ - piece.PIECE_HEIGHT + 1, maxY):
            currentLineValue = 1 # On reinitialise le compteur
            for col in range(sharedConsts.PLAYFIELD_WIDTH):
                currentLineValue *= self.playField_[line][col]  # Un seul emplacement vide et la ligne n'est pas pleine !

            # La ligne courante est effectivement pleine
            if not 0 == currentLineValue:
                # Une ligne de plus (on conserve l'ordre des lignes)
                completedLines.insert(0,line)
                self.eventHandler_.lineCompleted(line)

        # Effacement des lignes
        for lineIndex in completedLines:
            self._clearLine(lineIndex)

        # Mise à jour du score
        completedCount = len(completedLines)
        if completedCount >= 1:
            delta = 0
            if 1 == completedCount:
                delta += 100 * self.level_
            elif 2 == completedCount:
                delta += 300 * self.level_
            elif 3 == completedCount:
                delta += 500 * self.level_  # * 400 ?
            else:
                # Donc 4 !
                delta += 800 * self.level_    # * 800 ?
            
            # On valorise le fait qu'il n'y ait pas d'ombre, la vitesse du jeu ainsi que le nombre de ligne de handicap
            #
            mult = 100 + sharedConsts.SCORE_SPEED_GAME * downRowcount + sharedConsts.SCORE_DIRTY_LINES * self.parameters_.dirtyLines_
            if False == self.parameters_.shadow_:
                mult+=sharedConsts.SCORE_NO_SHADOW
            
            # Mise à jour du score
            self.eventHandler_.incScore(int(delta*mult/100))

        if 0 != completedCount:
            self.eventHandler_.allLinesCompletedRemoved(completedCount, self.lines() + completedCount)            

        # Nouvelle pièce
        self.newPiece()

    # La position (ou la rotation) de la pièce passée en param. a changée
    def piecePosChanged(self):

        # Calcul de l'ombre ?
        if True == self.parameters_.shadow_:
            self.currentPiece_.shadowTopPos_ = self._minTopPosition()

        # Notification
        self.eventHandler_.piecePosChanged(self.currentPiece_)

# EOF