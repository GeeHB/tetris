# coding=UTF-8
#
#   File     :   piece.py
#
#   Author     :   JHB
#
#   Description :   piece & pieceStatus objects : a tetramino and all the informations for its drawing
#

# Dimensions a the tetramino's matrix
#
PIECE_WIDTH     = 4
PIECE_HEIGHT    = 4

# piece obect - a tetramino and all it's rotation states
#
class piece(object):

    # Members
    #
    points_ = []        # Matrix of the piece whith all possible rotations
    rotate_ = 0         # rotation index (ie. index of the piece to draw)
    maxRotate_ = 0      # max. rotation(s) allowed for the piece ( = 360°)
    vertOffset_ = -1    # Initial vert. offset (ie. count of empty lines starting from bottom)
    
    # Construction
    #
    def __init__(self, other = None, template = None):
        if not other == None:
            # Recopy
            self.rotate_ = other.rotate_
            self.maxRotate_ = other.maxRotate_
            self.vertOffset_ = other.vertOffset_
            
            # Copy all the rotation states
            for state in other.points_:
                self.points_.append(self._copy(state))
        elif not template == None:
            # From a template
            self.points_ = []
            self.rotate_ = 0
            
            # Copy all the states
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
                                    points[j][i] = ord(char) - ordO
                                i += 1
                        j +=  1
                    self.points_.append(points) # It's a new state

            # #max rotation = # states !!!
            self.maxRotate_ = len(self.points_)

            # compute vertical offset
            self.vertOffset_ = 3
            while self.points_[0][self.vertOffset_] == [0,0,0,0] and self.vertOffset_ >= 0:
                self.vertOffset_-=1 # One line up
            
            # value = self.verticalOffset
        else:
            # By default the piece is empty
            self.points_ = self._new()

    # Piece's datas in the current rotation state (index = rotate_)
    #
    def datas(self):
        if self.rotate_ < 0 or self.rotate_ >= self.maxRotate_:
            raise IndexError
        return self.points_[self.rotate_]

    # Vertical offset (for rotationIndex = 0)
    #   ie. last non-empty line index
    def verticalOffset(self):
        return self.vertOffset_

    # Back to initial position
    #
    def rotateBack(self):
        self.rotate_ = 0

    # Max. rotation index for the piece
    #   (some pieces doen't rotate at all)
    #
    def maxRotations(self):
        return self.maxRotate_

    # Trigonometric rotation
    #
    def rotateLeft(self):
        self.rotate_ += 1
        
        # 360° ?
        if self.rotate_ >= self.maxRotate_:
            self.rotate_ = 0
        
        return self.rotate_

    # Clockwise rotation
    #
    def rotateRight(self):
        if 0 == self.maxRotate_:
            self.rotate_ = 0
        else:
            self.rotate_ -= 1
            
            # 360° ?
            if self.rotate_ < 0:
                self.rotate_ = self.maxRotate_ - 1

        return self.rotate_

    # New empty piece
    #
    def _new(self):
        datas =  [[0] * PIECE_WIDTH for _ in range(PIECE_HEIGHT)]
        return datas

    # Copy a single piece
    def _copy(self, src):
        dest = []
        for line in src:
            dest.append(line)
        return dest

    #   Overloads
    #

    # Acces / self[index]
    #
    #   return the piece in the "key" rotation index
    #
    def __getitem__(self, key):
        if not type(key) == int:
            raise TypeError
        if 0 == self.maxRotate_ or key < 0 or key >= self.maxRotate_:
            raise IndexError

        # done
        return self.points_[key]

#  pieceStatus object
#   All the informations concerning a tetramino : index, rotation, position ...
#
class pieceStatus(object):
    index_ = -1              # By default not drawn
    leftPos_ = 0
    topPos_  = 0
    rotationIndex_ = 0
    shadowTopPos_ = -1      # yPos of shadow (-1 = no shadow)

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

    # deep equal
    def __eq__(self, other):
        return True if not other == None and self.index_ == other.index_ and self.leftPos_ == other.leftPos_ and self.topPos_ == other.topPos_ and self.rotationIndex_ == other.rotationIndex_ else False
# EOF