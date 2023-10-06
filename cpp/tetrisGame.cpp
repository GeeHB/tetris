//---------------------------------------------------------------------------
//--
//--	File	: tetrisGame.cpp
//--
//--	Author	: Jérôme Henry-Barnaudière - GeeHB
//--
//--	Project	: jtetris / cpp version
//--
//---------------------------------------------------------------------------
//--
//--	Description:
//--
//--	    Implementation of tetrisGame object
//--
//---------------------------------------------------------------------------

#include "tetrisGame.h"

#include <cmath>
#include <time.h> 

#ifdef _DEBUG
#include <iostream>
using namespace std;
#endif // _DEBUG

//---------------------------------------------------------------------------
//--
//-- tetrisGame object
//--
//--    Handle the gameplay and the game(without display !)
//--
//---------------------------------------------------------------------------

// Constrcution
//
tetrisGame::tetrisGame() {

    // Default values
    nextIndex_ = -1;
    score_ = lines_ = 0;
    level_ = 1;

    _emptytetrisGame();

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

    // Just created
    status_ = STATUS_CREATED;
}

#ifdef _DEBUG
// Test ...
void tetrisGame::print() {
    cout << endl << "tetrisGame :" << endl;
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
void tetrisGame::setParameters(tetrisParameters& params) {
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

    // Empty the playset
    _emptytetrisGame();

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

// Let's play
//
bool tetrisGame::start() {
    // Check the object state
    if (STATUS_INIT == status_ || STATUS_STOPPED == status_) {
        //Initializations ...
        currentPos_.valid(false);

        // Drawings
        reDraw();

        status_ = STATUS_RUNNING;
        newPiece(); // the first piece

        updateDisplay();    // Redundant ???
        return true;
    }
    
    return false;
}

// New piece (in the game)
//
void tetrisGame::newPiece() {
    // Next piece => current
    nextPos_.index((-1 == nextPieceIndex()) ? _newPieceIndex() : nextPieceIndex());
    
    // Next one
    setNextPieceIndex(_newPieceIndex());

    // The piece is a the top of the game play, centered horizontally
    nextPos_.leftPos_ = int((PLAYFIELD_WIDTH - PIECE_WIDTH) / 2);
    nextPos_.topPos_ = PLAYFIELD_HEIGHT + tetraminos_[nextPos_.index_].verticalOffset();
    nextPos_.shadowTopPos_ = -1;
    nextPos_.rotationIndex_ = 0;
    tetraminos_[nextPos_.index_].rotateBack();

    nextPieceIndexChanged(nextPieceIndex());

    // Can I go on line down ?
    if (!_down(true)) {
        // No = > the game is over
        end(false);
    }
}

// Draw the tetrisGame
//
void tetrisGame::drawtetrisGame() {
    uint16_t left, leftFirst(0), top(0), w, h;
    _changeOrigin(true, leftFirst, top, w, h);

    // Draw all the blocks (coloured or not)
    for (uint8_t y = 0; y < PLAYFIELD_HEIGHT; y++) {
        left = leftFirst;
        for (uint8_t x = 0; x < PLAYFIELD_WIDTH; x++) {
            _drawSingleBlock(left, top, w, h, playField_[y][x]);
            left += w;
            top -= h;
        }
    }
}

// anti-clockwise rotation
//
bool tetrisGame::rotateLeft() {

    // Try to rotate
    uint8_t rotIndex = tetraminos_[nextPos_.index_].rotateLeft();

    // Possible ?
    if (_canMove(nextPos_.leftPos_, nextPos_.topPos_)){
        nextPos_.rotationIndex_ = rotIndex;

        // Apply rotation
        piecePosChanged();
        return true;
     }

    // No = > cancel rotation
    tetraminos_[nextPos_.index_].rotateRight();
    return false;
}

// Move left
//
bool tetrisGame::left(){                    
    // Test position
    if (_canMove(nextPos_.leftPos_ - 1, nextPos_.topPos_)) {
        // Correct
        nextPos_.leftPos_ -= 1;
        piecePosChanged();
        return true;
    }

    // Impossible
    return false;
}

// Move right
//
bool tetrisGame::right(){
    // Test position
    if (_canMove(nextPos_.leftPos_ + 1, nextPos_.topPos_)){
        // Correct
        nextPos_.leftPos_ += 1;
        piecePosChanged();
        return true;
    }

    // Impossible
    return false;
}

// Go down (as many lines as possible)
//
void tetrisGame::fall() {
    uint8_t bottom(_minTopPosition());
    uint8_t delta(nextPos_.topPos_ - bottom);
    nextPos_.topPos_ = bottom;

    // updates ...
    piecePosChanged();
    _reachLowerPos(delta);
}

// The position of the piece has just changed
//
void tetrisGame::piecePosChanged() {
    // Compute the pos ot the shadow ?
    if (parameters_.shadow_) {
        nextPos_.shadowTopPos_ = _minTopPosition();
    }

    // Any changes (or rotation) ?
    if (!currentPos_.isValid() || currentPos_ != nextPos_) {
        // Erase the tetramino(and maybe it's shadow)
        if (currentPos_.isValid()) {
            _drawSinglePiece(pieceDatas(currentPos_.index_, currentPos_.rotationIndex_), currentPos_.leftPos_, currentPos_.topPos_, true, COLOUR_ID_BOARD);
            if (-1 != currentPos_.shadowTopPos_) {
                // then the shadow
                _drawSinglePiece(pieceDatas(currentPos_.index_, currentPos_.rotationIndex_), currentPos_.leftPos_, currentPos_.shadowTopPos_, true, COLOUR_ID_BOARD);
            }
        }

        // redraw
        if (-1 != nextPos_.shadowTopPos_) {
            // first : the shadow
            _drawSinglePiece(pieceDatas(nextPos_.index_, nextPos_.rotationIndex_), nextPos_.leftPos_, nextPos_.shadowTopPos_, true, COLOUR_ID_SHADOW);

            // and then the tetramino(can recover the shadow !!!!)
            _drawSinglePiece(pieceDatas(nextPos_.index_, nextPos_.rotationIndex_), nextPos_.leftPos_, nextPos_.topPos_);

            updateDisplay();
            currentPos_ = nextPos_;
        }
    }
}

//
// "Private" methods
//

// Can the piece go down ?
//
bool tetrisGame::_down(bool newPiece) {
    // Test position
    if (_canMove(nextPos_.leftPos_, nextPos_.topPos_ - 1)) {
        // correct
        nextPos_.topPos_ -= 1;
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
bool tetrisGame::_canMove(uint8_t leftPos, uint8_t  topPos) {
    // Piece's datas (in its current state)
    uint8_t* datas = tetraminos_[nextPos_.index_].currentDatas();

    // Max index visible on desk
    uint8_t maxY = (topPos >= PLAYFIELD_HEIGHT) ? PIECE_HEIGHT - 1 + PLAYFIELD_HEIGHT - topPos : PIECE_HEIGHT - 1;
    
    // Test all the contained blocks starting from bottom
    uint8_t realX(0), realY(0);
    for (int8_t y = maxY; y >=0; y--){
        for (uint8_t x = 0; x < PIECE_WIDTH; x++) {
            if (COLOUR_ID_BOARD != datas[y * PIECE_WIDTH + x]) {
                // "real" position of the block 
                realX = x + leftPos;
                realY = topPos - y;

                // out of the gameplay's limits ?
                if (realX < 0 || realY < 0 || realX >= PLAYFIELD_WIDTH) {
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
uint8_t tetrisGame::_minTopPosition() {
    uint8_t currentTop(nextPos_.topPos_);

    // Try to move one line down
    while (_canMove(nextPos_.leftPos_, currentTop)){
        currentTop -= 1;
    }

    // current pos.is invalid = > go up one line
    return currentTop + 1;
}

// Clear and remove a completed line
//
void tetrisGame::_clearLine(uint8_t index) {
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
void tetrisGame::_addDirtyLine(uint8_t line) {
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
void tetrisGame::_putPiece(uint8_t colour) {
    uint8_t vertPos((COLOUR_ID_SHADOW == colour) ? nextPos_.shadowTopPos_ : nextPos_.topPos_);
    
    uint8_t* datas = tetraminos_[nextPos_.index_].currentDatas();
    uint8_t bColour(0);

    // Copy all the colored blocks in the gameplay
    uint8_t maxY = (PLAYFIELD_HEIGHT - vertPos >= 1) ? 0 : (vertPos - PLAYFIELD_HEIGHT + 1);
    for (uint8_t y = maxY; y < PIECE_HEIGHT; y++) {
        for (uint8_t x = 0; x < PIECE_WIDTH; x++) {
            bColour = datas[y * PIECE_WIDTH + x];
            if (COLOUR_ID_BOARD != bColour && (vertPos - y) < PLAYFIELD_HEIGHT) {
                playField_[vertPos - y][x + nextPos_.leftPos_] = ((COLOUR_ID_SHADOW == colour) ? colour : bColour);
            }
        }
    }
}
                                               
// The piece is at the lowest possible level
//
void tetrisGame::_reachLowerPos(uint8_t downRowcount){
    // put it
    _putPiece();

    // Notify
    //self.eventHandler_.pieceReachedLowerPos()

    // Are line(s) completed ?
    // Check the 4 possible lines
    uint8_t completedLines[4];
    uint8_t completedCount(0);       // # of completed lines

    uint8_t maxY(nextPos_.topPos_ + 1);
    if (maxY > PLAYFIELD_HEIGHT){
        maxY = PLAYFIELD_HEIGHT;
    }

    uint8_t currentLineValue(0);
    for (uint8_t line = nextPos_.topPos_ - PLAYFIELD_HEIGHT + 1; line < maxY; line++){
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
    for (int8_t line = (completedCount-1); line >=0; line--){
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

        incScore(uint32_t(delta * mult / 100.0));
        allLinesCompletedRemoved(completedCount, lines() + completedCount);
    }

    // Get a new piece
    newPiece();
}

// Change the origin and the coordinate system
//  and returns width and height of a block
//
void tetrisGame::_changeOrigin(bool intetrisGame,uint16_t& x, uint16_t& y, uint16_t& width, uint16_t& height) {
    width = height = 1;
}

// Draw a tetramino using the given colour
//   intetrisGame : True = > draw in the tetrisGame, False = > draw "next" piece
//
void tetrisGame::_drawSinglePiece(uint8_t* datas, uint16_t cornerX, uint16_t cornerY, bool intetrisGame, uint8_t colourID) {
    // First visible row ID
    int8_t rowFirst(0);
    if (intetrisGame) {
        rowFirst = PLAYFIELD_HEIGHT - 1 - cornerY;
        rowFirst = (rowFirst < 0) ? rowFirst * -1 : 0;
    }

    uint16_t x, xFirst(cornerX), y(cornerY - rowFirst), w, h;
    _changeOrigin(intetrisGame, xFirst, y, w, h);

    uint8_t colour; // Current block 's colour id

    for (uint8_t row = rowFirst; row < PIECE_HEIGHT; row++) {
        x = xFirst;
        for (uint8_t col = 0; col < PIECE_WIDTH; col++) {
            colour = datas[row * PIECE_WIDTH + col];
            if (colour != COLOUR_ID_BOARD) {
                _drawSingleBlock(x, y, w, h, (COLOUR_ID_NONE != colourID) ? colourID : colour);     // only non - empty squares
            }
            x += w;
        }
        y += h;
    }
}

// Display the next piece
//
void tetrisGame::_drawNextPiece(uint8_t pieceIndex) {
    // Erase the previous piece
    _eraseBlocks(0, 0, 4, 4, COLOUR_ID_BOARD);

    // ... and then draw the new one
    if (-1 != pieceIndex) {
        uint8_t* datas = nextPieceDatas();
        _drawSinglePiece(datas, 0, 0, false);
    }
}

// EOF