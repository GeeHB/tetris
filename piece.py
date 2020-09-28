# coding=UTF-8
#
#   File     :   piece.py
#
#   Authors     :   JHB
#
#   Description :   Définition des objets piece et pieceStatus pour la modélistation d'un tetramino
#
#   Version     :   0.5.3-3
#
#   Date        :   2020/09/28
#

# Quelques "constantes"
#
PIECE_WIDTH = 4     # Dimensions du tetramino (en "carrés")
PIECE_HEIGHT = 4

# Définition de la classe piece
#
class piece(object):

    # Données membres
    #
    points_ = []        # Matrice définissant la piece et ses différentes états (rotations)
    rotate_ = 0         # Nombre de rotations effectuées (ie. indice de la pièce dans le tableau) 
    maxRotate_ = 0      # Nombre de rotations max.
    vertOffset_ = -1    # Décalage (ie. nombre de ligne vide) par rapport à la verticale basse
    colourIndex_ = 0    # Indice de la couleur (0 = invisible)

    # Méthodes
    #

    # Constructeur
    def __init__(self, other = None, template = None):
        if not other == None:
            # Constructeur par recopie
            self.rotate_ = other.rotate_
            self.maxRotate_ = other.maxRotate_
            self.vertOffset_ = other.vertOffset_
            
            # Copie de la pièce dans tous ses états
            for state in other.points_:
                self.points_.append(self._copy(state))
        elif not template == None:
            # Création à partir d'un modèle
            self.points_ = []
            self.rotate_ = 0
            
            # Transformation et intégration de tous les états de la pièce
            ordO = ord('0')
            for shape in template:
                points = self._new()
                j,i = 0,0
                if len(shape) == PIECE_HEIGHT:
                    for line in shape:
                        if len(line) == PIECE_WIDTH:
                            i = 0
                            for char in line:
                                if not char == '.':
                                    self.colourIndex_ = ord(char) - ordO
                                    points[j][i] = self.colourIndex_
                                i += 1
                        j +=  1
                    self.points_.append(points) # Nouvel état

            # Le nombre max. de rotation correspond au nombre reèl d'état(s)
            self.maxRotate_ = len(self.points_)

            # Calcul du décalage vertical
            self.vertOffset_ = 3
            while self.points_[0][self.vertOffset_] == [0,0,0,0] and self.vertOffset_ >= 0:
                self.vertOffset_-=1 # On remonte
        else:
            # Par défaut la pièce est "vide"
            self.points_ = self._new()

    # Indice de la couleur de la pièce
    def colour(self):
        return self.colourIndex_
    
    # Données dans l'état actuel (index = rotate_)
    def datas(self):
        if self.rotate_ < 0 or self.rotate_ >= self.maxRotate_:
            raise IndexError
        return self.points_[self.rotate_]

    # Décalage vertical de la pièce par rapport une l'horizontale (valable pour l'index 0)
    # ie. index de la dernière ligne non-vide
    def verticalOffset(self):
        return self.vertOffset_

    # Retour à la position initiale
    def rotateBack(self):
        self.rotate_ = 0

    # nombre maximal de rotations
    def maxRotations(self):
        return self.maxRotate_

    # Rotation dans le sens trigonométrique
    def rotateLeft(self):
        self.rotate_ += 1
        
        # Un tour complet ?
        if self.rotate_ >= self.maxRotate_:
            self.rotate_ = 0
        
        return self.rotate_

    # Rotation dans le sens des aiguilles d'une montre
    def rotateRight(self):
        if 0 == self.maxRotate_:
            self.rotate_ = 0
        else:
            self.rotate_ -= 1
            
            # Un tour complet ?
            if self.rotate_ < 0:
                self.rotate_ = self.maxRotate_ - 1

        return self.rotate_

    # Création d'un piece vierge
    def _new(self):
        datas =  [[0] * PIECE_WIDTH for _ in range(PIECE_HEIGHT)]
        return datas

    # Copie des points d'une piece
    def _copy(self, src):
        dest = []
        for line in src:
            dest.append(line)
        return dest

    #
    #   Surcharges
    #

    # Accès / self.[key]
    #
    #   retourne la pièce dans l'état de rotation demandé
    #
    def __getitem__(self, key):
        # key est un entier !
        if not type(key) == int:
            raise TypeError
        # key est dans le "bon" intervalle !
        if 0 == self.maxRotate_ or key < 0 or key >= self.maxRotate_:
            raise IndexError

        # On retourne la pièce dans l'état "key"
        return self.points_[key]

# Classe pieceStatus
#   Information sur la position et l'état d'une pièce
#   Suffisant, et nécessaire, pour afficher ou effacer une pièce à l'écran
#
class pieceStatus(object):
    index_ = -1              # Pièce non affichée (vient d'apparaitre)
    leftPos_ = 0
    topPos_  = 0
    rotationIndex_ = 0
    shadowTopPos_ = -1      # Ordonnée de l'ombre (-1 = pas d'ombre)

    # Construction
    def __init__(self, index = -1, x = 0, y = 0, rotation = 0, other = None):
        if not None == other:
            self.index_ = other.index_
            self.leftPos_ = other.leftPos_
            self.topPos_ = other.topPos_
            self.rotationIndex_ = other.rotationIndex_
            self.shadowTopPos_ = other.shadowTopPos_
        else:
            self.index_ = index
            self.leftPos_ = x
            self.topPos_ = y
            self.rotationIndex_ = rotation
            self.shadowTopPos_ = -1

    # Les status sont-ils équivalents ?
    def __eq__(self, other):
        return True if not other == None and self.index_ == other.index_ and self.leftPos_ == other.leftPos_ and self.topPos_ == other.topPos_ and self.rotationIndex_ == other.rotationIndex_ else False
# EOF