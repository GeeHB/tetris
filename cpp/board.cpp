//---------------------------------------------------------------------------
//--
//--	File	: board.cpp
//--
//--	Author	: Jérôme Henry-Barnaudière - GeeHB
//--
//--	Project	: jtetris / cpp version
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

#include <cmath>
#include <time.h> 

#ifdef _DEBUG
#include <iostream>
using namespace std;
#endif // _DEBUG

//---------------------------------------------------------------------------
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

    _emptyBoard();

    // Initialize rand num. generator
    srand((int)time(NULL));

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

#ifdef _DEBUG
// Test ...
void board::print() {
    cout << endl << "Board :" << endl;
    for (uint8_t line = 0; line < PLAYFIELD_HEIGHT; line++) {
        cout << int(PLAYFIELD_HEIGHT - line - 1) << "- \t";
        for (uint8_t col = 0; col < PLAYFIELD_WIDTH; col++) {
            cout << int(playField_[PLAYFIELD_HEIGHT - line -1][col]);
        }
        cout << endl;
    }
}
#endif // _DEBUG
    
// Game's parameters
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
    _emptyBoard();

    // Add dirty lines ...
    //
    uint8_t maxLines(PLAYFIELD_HEIGHT - PIECE_HEIGHT - 1);
    if (parameters_.dirtyLines_ > maxLines) {
        parameters_.dirtyLines_ = maxLines;
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
    uint8_t rotIndex = tetraminos_[currentPiece_.index_].rotateLeft();

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
void board::fall() {
    uint8_t bottom(_minTopPosition());
    uint8_t delta(currentPiece_.topPos_ - bottom);
    currentPiece_.topPos_ = bottom;

    // updates ...
    piecePosChanged();
    _reachLowerPos(delta);
}

// The position of the piece has just changed
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
        currentPiece_.topPos_ -= 1;
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
    uint8_t realX(0), realY(0);
    for (uint8_t y = PIECE_HEIGHT - 1; y >=0; y--){
        for (uint8_t x = 0; x < PIECE_WIDTH; x++) {
            if (COLOUR_ID_BOARD != datas[y * PIECE_WIDTH + x]) {
                // "real" position of the block 
                realX = x + leftPos;
                realY = topPos - y;

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
        for (uint8_t line = index; line < (PLAYFIELD_HEIGHT - 1); line++) {
            for (uint8_t col = 0; col < PLAYFIELD_WIDTH; col++) {
                playField_[line][col] = playField_[line + 1][col];
            }
        }

        // Add a new empty line
        for (uint8_t col=0; col<PLAYFIELD_WIDTH; col++){
            playField_[PLAYFIELD_HEIGHT-1][col] = COLOUR_ID_BOARD;    
        }
    }
}

// Add a randomly generated dirty line at the bottom of the gameplay
//
void board::_addDirtyLine(uint8_t line) {
    uint16_t cubes(rand() % int(pow(2, PLAYFIELD_WIDTH) - 1));
    uint16_t sBit(1); // 2 ^ 0

    // Convert 'cubes' bits into coloured blocks
    for (uint8_t col = 0; col < PLAYFIELD_WIDTH; col++) {
        // Is the bit set ?
        if ((cubes & sBit) > 0) {
            // yes = > add a colored block
            playField_[line][col] = 1 + rand() % TETRAMINOS_COUNT;
        }

        // next bit value
        sBit *= 2;
    }
}
 
// Put the tetramino at the current position
//
void board::_putPiece(uint8_t colour) {
    uint8_t vertPos((COLOUR_ID_SHADOW == colour) ? currentPiece_.shadowTopPos_ : currentPiece_.topPos_);
    
    uint8_t* datas = tetraminos_[currentPiece_.index_].currentDatas();
    uint8_t bColour(0);

    // Copy all the colored blocks in the gameplay
    uint8_t maxY = (PLAYFIELD_HEIGHT - vertPos >= 1) ? 0 : (vertPos - PLAYFIELD_HEIGHT + 1);
    for (uint8_t y = maxY; y < PLAYFIELD_HEIGHT; y++) {
        for (uint8_t x = 0; x < PLAYFIELD_WIDTH; x++) {
            bColour = datas[y * PLAYFIELD_WIDTH + x];
            if (COLOUR_ID_BOARD != bColour && (vertPos - y) < PLAYFIELD_HEIGHT) {
                playField_[vertPos - y][x + currentPiece_.leftPos_] = ((COLOUR_ID_SHADOW == colour) ? colour : bColour);
            }
        }
    }
}
                                               
// The piece is at the lowest possible level
//
void board::_reachLowerPos(uint8_t downRowcount){
    // put it
    _putPiece();

    // Notify
    //self.eventHandler_.pieceReachedLowerPos()

    // Are line(s) completed ?
    // Check the 4 possible lines
    uint8_t completedLines[4];
    uint8_t completedCount(0);       // # of completed lines

    uint8_t maxY(currentPiece_.topPos_ + 1);
    if (maxY > PLAYFIELD_HEIGHT){
        maxY = PLAYFIELD_HEIGHT;
    }

    uint8_t currentLineValue(0);
    for (uint8_t line = currentPiece_.topPos_ - PLAYFIELD_HEIGHT + 1; line < maxY; line++){
        currentLineValue = 1;
        for (uint8_t col = 0; col <PLAYFIELD_WIDTH; col++){
            // one empty block and the whole line "value" = 0
            currentLineValue *= playField_[line][col];
        }

        // The line is complete
        if (currentLineValue){
            completedLines[completedCount++] = line;
        }
    }

    // Remove lines in reverse order (max -> min)
    for (uint8_t line = (completedCount-1); line >=0; line--){
        // Animate
        //self.eventHandler_.lineCompleted(line)

        // Update datas
        _clearLine(line);
    }

    // Update the score
    if (completedCount){
        double delta(0.0);    
        switch(completedCount){
            case 1:
                delta = 100.0;
                break;

            case 2:
                delta = 300.0;
                break;

            case 3:
                delta = 500.0;
                break;

            // 4
            default:
                delta = 800.0;
                break;
        }

        double mult(100. + SCORE_SPEED_GAME * downRowcount + SCORE_DIRTY_LINES * parameters_.dirtyLines_ + SCORE_LEVEL_VALUATION * lines_);
        if (!parameters_.shadow_){
            mult += SCORE_NO_SHADOW;
        }

        // self.eventHandler_.incScore(uint32_t(delta * mult / 100.0))
        //self.eventHandler_.allLinesCompletedRemoved(completedCount, lines() + completedCount)
    }

    // Get a new piece
    newPiece();
}

// EOF