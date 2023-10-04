//---------------------------------------------------------------------------
//--
//--	File	: board.cpp
//--
//--	Author	: Jérôme Henry-Barnaudière - GeeHB
//--
//--	Project	: jtetris - cpp version
//--
//---------------------------------------------------------------------------
//--
//--	Description:
//--
//--	    Implementation of 
//--            - board : The matrix with all the colored blocks(ie dirty lines and / or putted tetraminos)
//--
//---------------------------------------------------------------------------

#include "board.h"

#include <time.h> 

im//---------------------------------------------------------------------------
//--
//-- board object
//--
//--    Handle the gameplay and the game(without display !)
//--
//---------------------------------------------------------------------------

// Constrcution
//
board::board() {

    // Default values
    nextIndex_ = -1;
    score_ = lines_ = 0;
    level_ = 1;

    // Initialize rand num. generator
    srand(time(NULL));

    // Build the tetraminos'list
    //

    // S
    tetraminos_[0].addPiece(S_0);
    tetraminos_[0].addPiece(S_1);

    // Z
    tetraminos_[1].addPiece(Z_0);
    tetraminos_[1].addPiece(Z_1);

    // I
    tetraminos_[2].addPiece(I_0);
    tetraminos_[2].addPiece(I_1);

    // O
    tetraminos_[3].addPiece(O_0);

    // L
    tetraminos_[4].addPiece(L_0);
    tetraminos_[4].addPiece(L_1);
    tetraminos_[4].addPiece(L_2);
    tetraminos_[4].addPiece(L_3);

    // J
    tetraminos_[5].addPiece(J_0);
    tetraminos_[5].addPiece(J_1);
    tetraminos_[5].addPiece(J_2);
    tetraminos_[5].addPiece(J_3);

    // T
    tetraminos_[6].addPiece(T_0);
    tetraminos_[6].addPiece(T_1);
    tetraminos_[6].addPiece(T_2);
    tetraminos_[6].addPiece(T_3);
}
    
// Game's parmaeters
//
void board::setParameters(tetrisParameters& params) {
    // Copy (and init) parameters
    parameters_.copy(params);

    score_ = 0;
    lines_ = 0;
    level_ = parameters_.startLevel_;
    setNextPieceIndex(-1);

    // Initialization of tetraminos(no rotation)
    for (uint8_t index = 0; index < TETRAMINOS_COUNT; index++) {
        tetraminos_[index].rotateBack();
    }

    // Empty the play-set
    memset(playField_, COLOUR_ID_BOARD, PLAYFIELD_HEIGHT * PLAYFIELD_WIDTH);

    // Add dirty lines ...
    //
    uint8_t maxLines(PLAYFIELD_HEIGHT - PIECE_HEIGHT - 1);
    if (parameters_.dirtyLines_ > maxLines) {
        parameters_.dirtyLines_ = maxLines
    }
    else
        if (parameters_.dirtyLines_ < 0) {
            parameters_.dirtyLines_ = 0;
        }

    for (uint8_t index = 0; index < parameters_.dirtyLines_; index++) {
        _addDirtyLine(index);
    }
}

// New piece (in the game)
//
void board::newPiece() {
    // Next piece => current
    currentPiece_.index_ = (-1 == nextPieceIndex()) ? _newPieceIndex() : nextPieceIndex();
    
    // Next one
    setNextPieceIndex(_newPieceIndex());

    // The piece is a the top of the game play, centered horizontally
    currentPiece_.leftPos_ = int((PLAYFIELD_WIDTH - PIECE_WIDTH) / 2);
    currentPiece_.topPos_ = PLAYFIELD_HEIGHT + tetraminos_[currentPiece_.index_].verticalOffset();
    currentPiece_.shadowTopPos_ = -1;
    currentPiece_.rotationIndex_ = 0;
    tetraminos_[currentPiece_.index_].rotateBack();

    // Notify the display manager
    //self.eventHandler_.nextPieceIndexChanged(self.nextPieceIndex())

    // Can I go on line down ?
    if (!_down(true)) {
        // No = > the game is over
        //self.eventHandler_.gameFinished()
    }
}

// anti-clockwise rotation
//
bool board::rotateLeft() {

    // Try to rotate
    rotIndex = tetraminos_[currentPiece_.index_].rotateLeft();

    // Possible ?
    if (_canMove(currentPiece_.leftPos_, currentPiece_.topPos_)){
        currentPiece_.rotationIndex_ = rotIndex;

        // Apply rotation
        piecePosChanged();
        return true;
     }

    // No = > cancel rotation
    tetraminos_[currentPiece_.index_].rotateRight();
    return false;
}

// Move left
//
bool board::left(){                    
    // Test position
    if (_canMove(currentPiece_.leftPos_ - 1, currentPiece_.topPos_)) {
        // Correct
        currentPiece_.leftPos_ -= 1;
        piecePosChanged();
        return true;
    }

    // Impossible
    return false;
}

// Move right
//
bool board::right(){
    // Test position
    if (_canMove(currentPiece_.leftPos_ + 1, currentPiece_.topPos_)){
        // Correct
        currentPiece_.leftPos_ += 1;
        piecePosChanged();
        return true;
    }

    // Impossible
    return false;
}

// Go down (as many lines as possible)
//
bool board::fall() {
    uint8_t bottom = _minTopPosition();
    uint8_t delta = currentPiece_.topPos_ - bottom;
    currentPiece_.topPos_ = bottom;

    // updates ...
    piecePosChanged();
    _reachLowerPos(delta);
}

// The position of the piece just changed
//
void board::piecePosChanged() {
    // Compute the pos ot the shadow ?
    if (parameters_.shadow_) {
        currentPiece_.shadowTopPos_ = _minTopPosition();
    }

     // Notification
     //self.eventHandler_.piecePosChanged(self.currentPiece_);
}

//
// "Private" methods
//

// Can the piece go down ?
//
bool board::_down(bool newPiece) {
    // Test position
    if (_canMove(currentPiece_.leftPos_, currentPiece_.topPos_ - 1)) {
        // correct
        currentPiece_.topPos_ -= 1
        piecePosChanged();
        return true;
    }

    if (!newPiece) {
        _reachLowerPos();
    }

    return false;
}

// Can the current piece be at the given position ?
//
bool board::_canMove(uint8_t leftPos, uint8_t  topPos) {
    // Piece's datas (in its current state)
    uint8_t* datas = tetraminos_[currentPiece_.index_].currentDatas();

    // Test all the contained blocks starting from bottom
    for (uint8_t y = PIECE_HEIGHT - 1; y >=0; y--){
        for (uint8_t x = 0; x < PIECE_WIDTH; x++) {
            if (COLOUR_ID_BOARD != datas[y * PIECE_WIDTH + x]) {
                // "real" position of the block 
                realX = x + leftPos
                realY = topPos - y

                // out of the gameplay's limits ?
                if (realX < 0 || realY < 0 || realX >= PLAYFIELD_WIDTH || realY >= PLAYFIELD_HEIGHT) {
                    return false;
                }

                // Is there a block at this place ?
                if (realY < PLAYFIELD_HEIGHT && playField_[realY][realX] != COLOUR_ID_BOARD) {
                    return false;
                }
            }
        }
    }
    
    // Yes = > the position is valid
    return true;
}

// Get a piece min.pos.index(vertical value)
//
uint8_t board::_minTopPosition() {
    uint8_t currentTop(currentPiece_.topPos_);

    // Try to move one line down
    while (_canMove(currentPiece_.leftPos_, currentTop)){
        currentTop -= 1;
    }

    // current pos.is invalid = > go up one line
    return currentTop + 1;
}

// Clear and remove a completed line
//
void board::_clearLine(uint8_t index) {
    if (index >= 0 && index < PLAYFIELD_HEIGHT) {
        // Remove the line from the screen
        playField_.pop(index);

        // Add a ne empty line
        playField_.append([0] * PLAYFIELD_WIDTH);
    }
}

// Add a randomly generated dirty line at the bottom of the gameplay
//
void board::_addDirtyLine(uint8_t line) {
    uint16_t cubes(rand() % (2 * *consts.PLAYFIELD_WIDTH - 1));
    uint16_t sBit(1); // 2 ^ 0

    // Convert 'cubes' bits into coloured blocks
    for (uint8_t col = 0; col < PLAYFIELD_WIDTH; col++) {
        // Is the bit set ?
        if ((cubes & sBit) > 0) {
            // yes = > add a colored block
            playField_[line][col] = 1 + rand() % 6;
        }

        // next bit value
        sBit *= 2
    }
}
 
// Put the tetramino at the current position
//
void board::_putPiece(uint8_t colour) {
    if (COLOUR_ID_SHADOW == colour) {
        vertPos = currentPiece_.shadowTopPos_;
    }
    else {
        vertPos = currentPiece_.topPos_;
    }

    uint8_t* datas = tetraminos_[currentPiece_.index_].currentDatas();
    uint8 - t bColour(0);

    // Copy all the colored blocks in the gameplay
    uint8_t maxY = (PLAYFIELD_HEIGHT - vertPos >= 1) ? 0 : (vertPos - PLAYFIELD_HEIGHT + 1);
    for (uint8_t y = maxY; y < PIECE_HEIGHT; y++) {
        for (uint8_t x = 0; x < PIECE_WIDTH; x++) {
            bColour = datas[y * PIECE_WIDTH + x];
            if (COLOUR_ID_BOARD != bColour && (vertPos - y) < PLAYFIELD_HEIGHT) {
                playField_[vertPos - y][x + currentPiece_.leftPos_] = ((COLOUR_ID_SHADOW == colour) ? colour : bColour);
            }
        }
    }
}
                                               
                                                        # The piece is at the lowest possible level
#
                                                        def _reachLowerPos(self, downRowcount = 0) :

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
for line in range(self.currentPiece_.topPos_ - piece.PIECE_HEIGHT + 1, maxY) :
    currentLineValue = 1
    for col in range(consts.PLAYFIELD_WIDTH) :
        currentLineValue *= self.playField_[line][col]  # one empty block and the whole line "value" = 0

        # The line is complete
        if not 0 == currentLineValue:
completedLines.insert(0, line)

for lineIndex in completedLines :
# Animate
self.eventHandler_.lineCompleted(lineIndex)

# update datas
self._clearLine(lineIndex)

# Update the score
completedCount = len(completedLines)
if completedCount >= 1:
delta = 0
if 1 == completedCount :
    delta += 100
    elif 2 == completedCount :
    delta += 300
    elif 3 == completedCount :
    delta += 500
else:
# 4 !
delta += 800    #  * 800 ?

mult = 100 + consts.SCORE_SPEED_GAME * downRowcount + consts.SCORE_DIRTY_LINES * self.parameters_.dirtyLines_ + consts.SCORE_LEVEL_VALUATION * self.lines_
if False == self.parameters_.shadow_ :
    mult += consts.SCORE_NO_SHADOW

    self.eventHandler_.incScore(int(delta * mult / 100))

    if 0 != completedCount :
        self.eventHandler_.allLinesCompletedRemoved(completedCount, self.lines + completedCount)

        # Get a new piece
        self.newPiece()

        # The piece has moved or rotated
#
        

// EOF