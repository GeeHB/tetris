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

#ifdef DEST_CASIO_FXCG50
#include <gint/clock.h>
#else
#include <unistd.h>
#endif // #ifdef DEST_CASIO_FXCG50

#include <cstdio>
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

    _emptyTetrisGame();

    // Initialize rand num. generator
    srand((int)time(NULL));

    // Build the tetraminos'list
    //

    // S
    tetraminos_[0].addRotation(S_0);
    tetraminos_[0].addRotation(S_1);

    // Z
    tetraminos_[1].addRotation(Z_0);
    tetraminos_[1].addRotation(Z_1);

    // I
    tetraminos_[2].addRotation(I_0);
    tetraminos_[2].addRotation(I_1);

    // O
    tetraminos_[3].addRotation(O_0);

    // L
    tetraminos_[4].addRotation(L_0);
    tetraminos_[4].addRotation(L_1);
    tetraminos_[4].addRotation(L_2);
    tetraminos_[4].addRotation(L_3);

    // J
    tetraminos_[5].addRotation(J_0);
    tetraminos_[5].addRotation(J_1);
    tetraminos_[5].addRotation(J_2);
    tetraminos_[5].addRotation(J_3);

    // T
    tetraminos_[6].addRotation(T_0);
    tetraminos_[6].addRotation(T_1);
    tetraminos_[6].addRotation(T_2);
    tetraminos_[6].addRotation(T_3);

    // Colours
    //
    colours_[COLOUR_ID_BOARD] = COLOUR_WHITE;
    colours_[1] = COLOUR_RED;           // Pieces (1 to 7)
    colours_[2] = COLOUR_GREEN;
    colours_[3] = COLOUR_YELLOW;
    colours_[4] = COLOUR_BLUE;
    colours_[5] = COLOUR_PURPLE;
    colours_[6] = COLOUR_CYAN;
    colours_[7] = COLOUR_ORANGE;
    colours_[COLOUR_ID_SHADOW] = COLOUR_LTGREY;
    colours_[COLOUR_ID_TEXT] = COLOUR_BLACK;
    colours_[COLOUR_ID_BORDER] = COLOUR_DKGREY;
    colours_[COLOUR_ID_BKGRND] = COLOUR_WHITE;  // could be different from board !

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
    nextIndex_ = -1;

    // Initialization of tetraminos(no rotation)
    for (uint8_t index = 0; index < TETRAMINOS_COUNT; index++) {
        tetraminos_[index].rotateBack();
    }

    // Empty the playset
    _emptyTetrisGame();

    // Add dirty lines ...
    //
    uint8_t maxLines(PLAYFIELD_HEIGHT - PIECE_HEIGHT - 1);
    if (parameters_.dirtyLines_ > maxLines) {
        parameters_.dirtyLines_ = maxLines;
    }
    /*
    else
        if (parameters_.dirtyLines_ < 0) {
            parameters_.dirtyLines_ = 0;
        }
    */
    for (uint8_t index = 0; index < parameters_.dirtyLines_; index++) {
        _addDirtyLine(index);
    }

    // Casio specific datas.
    casioParams_.setVert(parameters_.vertical_);
}

// Let's play
//
bool tetrisGame::start() {
    // Check the object state
    if (STATUS_INIT != status_ && STATUS_STOPPED != status_) {
        return false;
    }

    //Initializations ...
    currentPos_.valid(false);
    status_ = STATUS_RUNNING;

    // Clear screen
#ifdef DEST_CASIO_FXCG50
    dclear(colours_[COLOUR_ID_BOARD]);
#endif // #ifdef DEST_CASIO_FXCG50

    //_drawBackGround();
    _drawTetrisGame();
    /*
    _drawScore();
    _drawLevel();
    _drawLines();
    */
    _newPiece();

    updateDisplay();

    // Initial 'speed' (ie. duration of a 'sequence' before moving down the piece)
    uint32_t seqCount(0);
    long diff, seqDuration(_updateSpeed(INITIAL_SPEED * 1000000, parameters_.startLevel_, parameters_.startLevel_ - 1));

#ifdef DEST_CASIO_FXCG50
    clock_t ts, now;
    now = clock();
#else
    struct timespec ts, now;
    clock_gettime(CLOCK_MONOTONIC, &now);
#endif // #ifdef DEST_CASIO_FXCG50

    // Game main loop
    while (isRunning()){
        diff = 0;
        ts = now;

        // During this short period, the piece can be moved or rotated
        while (isRunning() && diff < seqDuration){
            _handleGameKeys();
#ifdef DEST_CASIO_FXCG50
            sleep_us(SLEEP_DURATION);
            now = clock();
            diff = (now - ts) / CLOCKS_PER_SEC * 1000000000;
#else
            usleep(SLEEP_DURATION);
            clock_gettime(CLOCK_MONOTONIC, &now);
            diff = (now.tv_sec - ts.tv_sec) * 1000000000 + (now.tv_nsec - ts.tv_nsec);
#endif // #ifdef DEST_CASIO_FXCG50
        }

        // One line down ...
        _down();

        // Accelerate ?
        seqCount += 1;
        if (0 == (seqCount % MOVES_UPDATE_LEVEL)){
            // Real level (based on pieces movements)
            uint8_t rLevel = (uint8_t)floor(seqCount / MOVES_UPDATE_LEVEL) + 1;

            // Change level (if necessary) & accelerate
            if (rLevel >= level_){
                level_ = rLevel;
                seqDuration = _updateSpeed(seqDuration, level_, 1);

                //_drawLevel();
                updateDisplay();
            }
        }
    }

    // Game is Over
    return true;
}

//
// "Private" methods
//

// anti-clockwise rotation
//
bool tetrisGame::_rotateLeft() {

    // Try to rotate
    uint8_t rotIndex = tetraminos_[nextPos_.index_].rotateLeft();

    // Possible ?
    if (_canMove(nextPos_.leftPos_, nextPos_.topPos_)){
        nextPos_.rotationIndex_ = rotIndex;

        // Apply rotation
        _piecePosChanged();
        return true;
     }

    // No = > cancel rotation
    tetraminos_[nextPos_.index_].rotateRight();
    return false;
}

// Move left
//
bool tetrisGame::_left(){
    // Test position
    if (_canMove(nextPos_.leftPos_ - 1, nextPos_.topPos_)) {
        // Correct
        nextPos_.leftPos_ -= 1;
        _piecePosChanged();
        return true;
    }

    // Impossible
    return false;
}

// Move right
//
bool tetrisGame::_right(){
    // Test position
    if (_canMove(nextPos_.leftPos_ + 1, nextPos_.topPos_)){
        // Correct
        nextPos_.leftPos_ += 1;
        _piecePosChanged();
        return true;
    }

    // Impossible
    return false;
}

// Go down (as many lines as possible)
//
void tetrisGame::_fall() {
    uint8_t bottom(_minTopPosition());
    uint8_t delta(nextPos_.topPos_ - bottom);
    nextPos_.topPos_ = bottom;

    // updates ...
    _piecePosChanged();
    _reachLowerPos(delta);
}

// The position of the piece has just changed
//
void tetrisGame::_piecePosChanged() {
    // Compute the pos ot the shadow ?
    if (parameters_.shadow_) {
        nextPos_.shadowTopPos_ = _minTopPosition();
    }

    // Any changes (or rotation) ?
    if (!currentPos_.isValid() || currentPos_ != nextPos_) {
        // Erase the tetramino(and maybe it's shadow)
        if (currentPos_.isValid()) {
            _drawSinglePiece(_pieceDatas(currentPos_.index_, currentPos_.rotationIndex_), currentPos_.leftPos_, currentPos_.topPos_, true, COLOUR_ID_BOARD);
            if (-1 != currentPos_.shadowTopPos_) {
                // then the shadow
                _drawSinglePiece(_pieceDatas(currentPos_.index_, currentPos_.rotationIndex_), currentPos_.leftPos_, currentPos_.shadowTopPos_, true, COLOUR_ID_BOARD);
            }
        }

        // redraw
        if (-1 != nextPos_.shadowTopPos_) {
            // first : the shadow
            _drawSinglePiece(_pieceDatas(nextPos_.index_, nextPos_.rotationIndex_), nextPos_.leftPos_, nextPos_.shadowTopPos_, true, COLOUR_ID_SHADOW);

            // and then the tetramino(can recover the shadow !!!!)
            _drawSinglePiece(_pieceDatas(nextPos_.index_, nextPos_.rotationIndex_), nextPos_.leftPos_, nextPos_.topPos_);

            updateDisplay();
            currentPos_ = nextPos_;
        }
    }
}

// Change the game speed
//
long tetrisGame::_updateSpeed(long currentDuration, uint8_t level, uint8_t incLevel){
        if (level >= MAX_LEVEL_ACCELERATION){
            // Already at the max speed
            return currentDuration;
        }

        // duration = currentDuration * acc ^ incLevel
        return currentDuration * ((incLevel == 1)? ACCELERATION_STEP : powl(ACCELERATION_STEP, incLevel));
}

// Handle keyboard events
//
void tetrisGame::_handleGameKeys() {
	char inChar(getchar());

	if(inChar != EOF) {
        if (casioParams_.keyQuit_ == inChar){
            end();
            return;
        }

        if (casioParams_.keyLeft_ == inChar){
            _left();
            return;
        }

        if (casioParams_.keyRight_ == inChar){
            _right();
            return;
        }

        if (casioParams_.keyRotate_ == inChar){
            _rotateLeft();
            return;
        }

        if (casioParams_.keyDown_ == inChar){
            _down();
            return;
        }

        if (casioParams_.keyFall_ == inChar){
            _fall();
            return;
        }
	}
}

// Can the piece go down ?
//
bool tetrisGame::_down(bool newPiece) {
    // Test position
    if (_canMove(nextPos_.leftPos_, nextPos_.topPos_ - 1)) {
        // correct
        nextPos_.topPos_ -= 1;
        _piecePosChanged();
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
    int8_t realX(0), realY(0);
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

    // current pos is invalid = > go up one line
    return currentTop + 1;
}

// New piece (in the game)
//
void tetrisGame::_newPiece() {
    // Next piece => current
    nextPos_.index((-1 == nextIndex_) ? _newPieceIndex() : nextIndex_);

    // Next one
    nextIndex_ = _newPieceIndex();

    // The piece is a the top of the game play, centered horizontally
    nextPos_.leftPos_ = int((PLAYFIELD_WIDTH - PIECE_WIDTH) / 2);
    nextPos_.topPos_ = PLAYFIELD_HEIGHT + tetraminos_[nextPos_.index_].verticalOffset();
    nextPos_.shadowTopPos_ = -1;
    nextPos_.rotationIndex_ = 0;
    tetraminos_[nextPos_.index_].rotateBack();

    // Next piece
    _drawNextPiece(nextIndex_);

    // Can I go on line down ?
    if (!_down(true)) {
        // No = > the game is over
        end(false);
    }
}

// Clear and remove a completed line
//
void tetrisGame::_clearLine(uint8_t index) {
    if (/*index >= 0 && */index < PLAYFIELD_HEIGHT) {
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

// Add a randomly generated dirty line in the gameplay
//
void tetrisGame::_addDirtyLine(uint8_t lineID) {
    uint16_t cubes(rand() % int(pow(2, PLAYFIELD_WIDTH) - 1));
    uint16_t sBit(1); // 2 ^ 0

    // Convert 'cubes' bits into coloured blocks
    for (uint8_t col = 0; col < PLAYFIELD_WIDTH; col++) {
        // Is the bit set ?
        if ((cubes & sBit) > 0) {
            // yes = > add a colored block
            playField_[lineID][col] = 1 + rand() % TETRAMINOS_COUNT;
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

    // Don't erase this piece !!!
    currentPos_.valid(false);

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
    for (int8_t lineID = (completedCount-1); lineID >=0; lineID--){
        // Animate
        uint8_t line(completedLines[lineID]);
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

        // Updates
        score_+=uint32_t(delta * mult / 100.0);
        lines_+=completedCount;

        //_drawScore();
        //_drawLines();

        _drawTetrisGame();
    } // if (completedCount)

    // Get a new piece
    _newPiece();
    updateDisplay();
}

// Change the origin and the coordinate system
//  returns width and height of a block
//
void tetrisGame::_changeOrigin(bool inTetrisGame,uint16_t& x, uint16_t& y, uint16_t& width, uint16_t& height) {
    if (inTetrisGame){
        x = casioParams_.playfield_left_ + x * casioParams_.boxWidth_;
        y = casioParams_.playfield_top_ + (PLAYFIELD_HEIGHT - 1 - y) * casioParams_.boxWidth_;
        width = height = casioParams_.boxWidth_;
    }
    else{
        // Draw next piece
        x = casioParams_.NP_left_ + CASIO_INFO_GAP;
        y = casioParams_.NP_top_ + CASIO_INFO_GAP;
        width = height = casioParams_.NP_boxWidth_;
    }
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
void tetrisGame::_drawNextPiece(int8_t pieceIndex) {
    // Erase the previous piece
    _eraseNextPiece(0, 0, 4, 4, COLOUR_ID_BOARD);

    // ... and then draw the new one
    if (-1 != pieceIndex) {
        uint8_t* datas = _nextPieceDatas();
        _drawSinglePiece(datas, 0, 0, false);
    }
}

// Draw the tetrisGame
//
void tetrisGame::_drawTetrisGame() {
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

// Erase the "next piece" tetramino
//
void tetrisGame::_eraseNextPiece(uint16_t left, uint16_t  top, uint16_t  width, uint16_t  height, uint8_t colourID){

    uint16_t w, h;
    _changeOrigin(false, left, top, w, h);
    _drawRectangle(left, top, w * width, h * height, colours_[colourID]);
}

// Draw a single coloured rectangle
//
//   @x,@y : top left starting point
//   @width, @height : dimensions
//   @borderColour : Colour of the border in RGB format or -1 (if no border)
//   @fillColour : Filling colour in RGB format or -1 (if empty)
//
void tetrisGame::_drawRectangle(uint16_t x, uint16_t y, uint16_t width, uint16_t height, int16_t fillColour, int16_t borderColour){
#ifdef DEST_CASIO_FXCG50
    uint16_t xFrom(x), yFrom(y);
    uint16_t xTo, yTo;

    // Horizontal display ?
    if (!casioParams_.vert_){
        casioParams_.rotate(xFrom, yFrom);
        xTo = xFrom + height- 1;     // height should be equivalent to width
        yTo = yFrom + width -1;
    }
    else{
        xTo = xFrom + width- 1;
        yTo = yFrom + height -1;
    }

    // Draw the rect
    drect_border(xFrom, yFrom, xTo, yTo, colours_[fillColour], 1, -1 == borderColour ? -1 : colours_[borderColour]);
#endif // #ifdef DEST_CASIO_FXCG50
}

// EOF
