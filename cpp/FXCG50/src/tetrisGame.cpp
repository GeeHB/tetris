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

//---------------------------------------------------------------------------
//--
//-- tetrisGame object
//--
//--    Handle the gameplay and the game (without display !)
//--
//---------------------------------------------------------------------------

// Constrcution
//
tetrisGame::tetrisGame() {

    // Default values
    nextIndex_ = -1;

    strcpy(values_[SCORE_ID].name, SCORE_STR);
    values_[SCORE_ID].value = 0;

    strcpy(values_[LEVEL_ID].name, LEVEL_STR);
    values_[LEVEL_ID].value = 1;

    strcpy(values_[COMPLETED_LINES_ID].name, COMPLETED_LINES_STR);
    values_[COMPLETED_LINES_ID].value = 0;

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
    colours_[COLOUR_ID_SHADOW] = COLOUR_LT_GREY;
    colours_[COLOUR_ID_TEXT] = COLOUR_BLACK;
    colours_[COLOUR_ID_BORDER] = COLOUR_DK_GREY;
    colours_[COLOUR_ID_BKGRND] = COLOUR_WHITE;  // could be different from board !

    // Just created
    status_ = STATUS_INIT;      // Can't be started !!!
}

// setParameters() : Set game's parameters
//
//  @params : Struct. continaining parameters for the game
//  These parameters are choosen by the user
//
void tetrisGame::setParameters(tetrisParameters* params) {
    // Copy (and init) parameters
    parameters_.copy(params);

    values_[SCORE_ID].value = 0;
    values_[LEVEL_ID].value = parameters_.startLevel_;
    values_[COMPLETED_LINES_ID].value = 0;
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
    for (uint8_t index = 0; index < parameters_.dirtyLines_; index++) {
        _addDirtyLine(index);
    }

    // Ready for the game
    status_ = STATUS_READY;
}

// start() : Start the tetris game
//
//  The entore game is handled by this method.
//  It retuns on error or when the game is over
//
//  returns false on error(s)
//
bool tetrisGame::start() {
    // Check the object state
    if (STATUS_READY != status_ && STATUS_PAUSED != status_) {
        return false;
    }

    //Initializations ...
    currentPos_.valid(false);
    status_ = STATUS_RUNNING;

    _newPiece();

    // Set display's rotation mode
    _rotateDisplay(true);

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
            if (rLevel >= values_[LEVEL_ID].value){
                values_[LEVEL_ID].value = rLevel;
                seqDuration = _updateSpeed(seqDuration, rLevel, 1);

                _drawNumValue(LEVEL_ID);
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

// _rotateDisplay() : Rotate the display
//
//  @first : Game is starting ?
//
void tetrisGame::_rotateDisplay(bool first){

    // (new) rotation mode
    casioParams_.rotatedDisplay(first?parameters_.rotatedDisplay_:!casioParams_.rotatedDisplay_);

    // Clear the screen
#ifdef DEST_CASIO_FXCG50
    dclear(colours_[COLOUR_ID_BOARD]);
#endif // #ifdef DEST_CASIO_FXCG50

    _drawBackGround();
    _drawTetrisGame();

    _drawNumValue(SCORE_ID);
    _drawNumValue(LEVEL_ID);
    _drawNumValue(COMPLETED_LINES_ID);

    if (!first){
        // Redraw the piece and it's shadow
        if (-1 != nextPos_.shadowTopPos_) {
            // first : the shadow
            _drawSinglePiece(_pieceDatas(nextPos_.index_, nextPos_.rotationIndex_), nextPos_.leftPos_, nextPos_.shadowTopPos_, true, COLOUR_ID_SHADOW);
        }

        // and then the tetramino(can recover the shadow !!!!)
        _drawSinglePiece(_pieceDatas(nextPos_.index_, nextPos_.rotationIndex_), nextPos_.leftPos_, nextPos_.topPos_);
    }

    // The next pice
    _drawNextPiece(nextIndex_);

    // go !!!
    updateDisplay();
}


// _left() : Move left
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

// _right() : Move right
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

// _down() : Can the piece go down ?
//
//  Test wether the current piece can go down one row
//  When the piece has been added newly to the game and going down is
//  not possible, it means the game is over
//
//  @newPiece : The piece has just been added ?
//
//  Return true if the piece canmoive one row down
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

// _fall() : Go down (as many lines as possible)
//
void tetrisGame::_fall(){
    uint8_t bottom(_minTopPosition());
    uint8_t delta(nextPos_.topPos_ - bottom);
    nextPos_.topPos_ = bottom;

    // updates ...
    _piecePosChanged();
    _reachLowerPos(delta);
}

// _rotateLeft() : anti-clockwise rotation
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

// _piecePosChanged() : The position of the piece has just changed
//
//  Called when the screen needs to be updated
//
void tetrisGame::_piecePosChanged() {
    // Compute the pos or the shadow ?
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
        }

        // and then the tetramino(can recover the shadow !!!!)
        _drawSinglePiece(_pieceDatas(nextPos_.index_, nextPos_.rotationIndex_), nextPos_.leftPos_, nextPos_.topPos_);

        updateDisplay();
        currentPos_ = nextPos_;
    }
}

// _updateSpeed() : Change the game speed
//
//  Between each automatic down movement the system "waits" a given duration.
//  The greater this value, the lower the 'speed' will be.
//
//  This 'speed' is linked to the level in the game
//
//  @currentDuration : current 'speed'
//  @level : current level in the game
//  @incLevel : value of current increment for the level (1 by default)
//
//  Return the new duration in ns.
//
long tetrisGame::_updateSpeed(long currentDuration, uint8_t level, uint8_t incLevel){
        if (level >= MAX_LEVEL_ACCELERATION){
            // Already at the max speed
            return currentDuration;
        }

        // duration = currentDuration * acc ^ incLevel
        return currentDuration * ((incLevel == 1)? ACCELERATION_STEP : powl(ACCELERATION_STEP, incLevel));
}

// _handleGameKeys() : Handle keyboard events
//
//  This methods ends even if no event is in the queue
//
void tetrisGame::_handleGameKeys() {
    char car(0);
#ifdef DEST_CASIO_FXCG50
    key_event_t evt = pollevent();
    if (evt.type == KEYEV_DOWN){
        // A key has been pressed
        car = evt.key;
    }
    else{
        return;
    }
#else
	car = getchar();
#endif // #ifdef DEST_CASIO_FXCG50

	if(car != EOF) {
        if (casioParams_.keyQuit_ == car){
            end();
            return;
        }

        if (casioParams_.keyRotateDisplay_ == car){
            _rotateDisplay();
            return;
        }

        if (casioParams_.keyLeft_ == car){
            _left();
            return;
        }

        if (casioParams_.keyRight_ == car){
            _right();
            return;
        }

        if (casioParams_.keyRotatePiece_ == car){
            _rotateLeft();
            return;
        }

        if (casioParams_.keyDown_ == car){
            _down();
            return;
        }

        if (casioParams_.keyFall_ == car){
            _fall();
            return;
        }
	}
}

// _canMove : Can the current piece be at the given position ?
//
//  Since a tetramino doesn't fill the whole 4x4 matrix,
//  leftPos can be negative (ie empty spaces are on the left of the screen)
//
//  @leftPos, @topPos : Position to test
//
//  Return true if the position is free and can be used by the tetramino
//
bool tetrisGame::_canMove(int8_t leftPos, uint8_t  topPos) {
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

// _minTopPosition() : Get a piece min.pos.index(vertical value)
//
//  Return the index of the lowest possible position foir the current piece
//
uint8_t tetrisGame::_minTopPosition(){
    uint8_t currentTop(nextPos_.topPos_);

    // Try to move one line down
    while (_canMove(nextPos_.leftPos_, currentTop)){
        currentTop -= 1;
    }

    // current pos is invalid = > go up one line
    return currentTop + 1;
}

// _newPiece() : New piece (in the game)
//
//  The piece in the preview area will appear in the playfield
//  A new "next piece" will be shown in the preview area
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

// _clearLine() : Clear and remove a completed line
//
//  When a line is completed (ie. all horizontal boxes are colored)
//  it disapperas from the game. All lines "below" will move down.
//
//  @index : index of the line to clear  in [0 , PLAYFIELD_HEIGHT[
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

// _addDirtyLine() : Add a randomly generated dirty line in the gameplay
//
//  @lineID : Index of the line to fill in [0 , PLAYFIELD_HEIGHT[
//
void tetrisGame::_addDirtyLine(uint8_t lineID) {
    uint16_t cubes(1 + rand() % int(pow(2, PLAYFIELD_WIDTH) - 1));
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

// _putPiece : Put the tetramino at the current position
//
//  This methods is used to put a tetramino on the playing area.
//  The tetramino is no longer mobile.
//
void tetrisGame::_putPiece() {
    uint8_t vertPos(nextPos_.topPos_);

    uint8_t* datas = tetraminos_[nextPos_.index_].currentDatas();
    uint8_t bColour(0);

    // Copy all the colored blocks in the gameplay
    uint8_t maxY = (PLAYFIELD_HEIGHT - vertPos >= 1) ? 0 : (vertPos - PLAYFIELD_HEIGHT + 1);
    for (uint8_t y = maxY; y < PIECE_HEIGHT; y++) {
        for (uint8_t x = 0; x < PIECE_WIDTH; x++) {
            bColour = datas[y * PIECE_WIDTH + x];
            if (COLOUR_ID_BOARD != bColour && (vertPos - y) < PLAYFIELD_HEIGHT) {
                playField_[vertPos - y][x + nextPos_.leftPos_] = bColour;
            }
        }
    }
}

// _reachLowerPos() : Update the datas when a tetramino is down
//
//  @downRowCount : count of down'rows
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

    bool foundEmpty(false);
    for (uint8_t line = nextPos_.topPos_ - PIECE_HEIGHT + 1; line < maxY; line++){
        foundEmpty = false;
        for (uint8_t col = 0; col <PLAYFIELD_WIDTH && !foundEmpty; col++){
            if (!playField_[line][col]){
                foundEmpty = true;
            }
        }

        // The line is complete
        if (!foundEmpty){
            completedLines[completedCount++] = line;
        }
    }

    // Remove lines in reverse order (max -> min)
    for (int8_t lineID = (completedCount-1); lineID >=0; lineID--){
        // Update datas
        _clearLine(completedLines[lineID]);
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

        double mult(100. + SCORE_SPEED_GAME * downRowcount + SCORE_DIRTY_LINES * parameters_.dirtyLines_ + SCORE_LEVEL_VALUATION * values_[COMPLETED_LINES_ID].value);
        if (!parameters_.shadow_){
            mult += SCORE_NO_SHADOW;
        }

        // Updates
        values_[SCORE_ID].value+=uint32_t(delta * mult / 100.0);
        values_[COMPLETED_LINES_ID].value+=completedCount;

        _drawNumValue(SCORE_ID);
        _drawNumValue(COMPLETED_LINES_ID);
        _drawTetrisGame();
    } // if (completedCount)

    // Get a new piece
    _newPiece();
    updateDisplay();
}

// _changeOrigin() : Change the origin and the coordinate system
//
//  @inTetrisGame : if true coordinates are changed to playfield area.
//   if false, coordinates are changed to the preview area
//  @x, @y : coordinates to change
//  @width, @height : Dimensions in pixels of a single block in the choosen area
//
void tetrisGame::_changeOrigin(bool inTetrisGame,uint16_t& x, uint16_t& y, uint16_t& width, uint16_t& height) {
    if (inTetrisGame){
        x = casioParams_.playfield_pos_.x + x * casioParams_.boxWidth_;
        y = casioParams_.playfield_pos_.y + (PLAYFIELD_HEIGHT - 1 - y) * casioParams_.boxWidth_;
        width = height = casioParams_.boxWidth_;
    }
    else{
        // Draw next piece
        x = casioParams_.NP_pos_.x + CASIO_INFO_GAP;
        y = casioParams_.NP_pos_.y + CASIO_INFO_GAP;
        width = height = casioParams_.NP_boxWidth_;
    }
}

// _drawTetrisGame() : Draw a whole tetramino using the given colour
//
//  @datas is the piece'datas in its current rotation state
//  @cornerX, @cornerY are the coordinates of the upper left corner in blocks coordinates
//  @inTetrisGame : True = > draw in the tetrisGame, False = > draw "next" piece
//  @specialColourID is the colour to use for the tetramino.
//   If set to COLOUR_ID_NONE the tetramini's colour will be used
//
void tetrisGame::_drawSinglePiece(uint8_t* datas, uint16_t cornerX, uint16_t cornerY, bool inTetrisGame, uint8_t specialColourID) {
    // First visible row ID
    int8_t rowFirst(0);
    if (inTetrisGame) {
        rowFirst = PLAYFIELD_HEIGHT - 1 - cornerY;
        rowFirst = (rowFirst < 0) ? rowFirst * -1 : 0;
    }

    uint16_t x, xFirst(cornerX), y(cornerY - rowFirst), w, h;
    _changeOrigin(inTetrisGame, xFirst, y, w, h);

    uint8_t colourID;
    for (uint8_t row = rowFirst; row < PIECE_HEIGHT; row++) {
        x = xFirst;
        for (uint8_t col = 0; col < PIECE_WIDTH; col++) {
            colourID = datas[row * PIECE_WIDTH + col];
            if (colourID != COLOUR_ID_BOARD) {
                _drawRectangle(x, y, w, h, colours_[(COLOUR_ID_NONE != specialColourID) ? specialColourID : colourID]);
            }
            x += w;
        }
        y += h;
    }
}

// _drawTetrisGame() : Display the next piece
//
//  The next piece will be drawn in the preview box.
//  This zone, prior to drawinings, will be erased
//
//  @pieceIndex is the index of the piece
//
void tetrisGame::_drawNextPiece(int8_t pieceIndex) {
    // Erase the previous piece
    _eraseNextPiece();

    // ... and then draw the new one
    if (-1 != pieceIndex) {
        uint8_t* datas = _nextPieceDatas();
        _drawSinglePiece(datas, 0, 0, false);
    }
}

// _drawTetrisGame() : Draw the tetrisGame
//
void tetrisGame::_drawTetrisGame() {
    uint16_t left, leftFirst(0), top(0), w, h;
    _changeOrigin(true, leftFirst, top, w, h);

    // Draw all the blocks (coloured or not)
    for (uint8_t y = 0; y < PLAYFIELD_HEIGHT; y++) {
        left = leftFirst;
        for (uint8_t x = 0; x < PLAYFIELD_WIDTH; x++) {
            //_drawSingleBlock(left, top, w, h, playField_[y][x]);
            _drawRectangle(left, top, w, h, colours_[playField_[y][x]]);
            left += w;
        }
        top -= h;
    }
}

// _eraseNextPiece() : Erase the "next piece" tetramino
//
//  @left, @top : top left corner of next-piece preview
//  @width, @height : dimensions of the preview (in box units)
//  @colourID : ID of the colour to use
//
void tetrisGame::_eraseNextPiece(){
    uint16_t x(0), y(0), w, h;
    _changeOrigin(false, x, y, w, h);
    _drawRectangle(x, y, w * PIECE_WIDTH, h * PIECE_HEIGHT, colours_[COLOUR_ID_BOARD], colours_[COLOUR_ID_BOARD]);
}

// _drawBackGround() : Draw entire background
//
//  This methods will redraw all the window except the next piece preview and
//  the tetris game playfield
//
void tetrisGame::_drawBackGround(){
    // Border around the playfield
    _drawRectangle(casioParams_.playfield_pos_.x - CASIO_BORDER_GAP,
        casioParams_.playfield_pos_.y - CASIO_BORDER_GAP,
        casioParams_.playfield_width, casioParams_.playfield_height,
        NO_COLOR, colours_[COLOUR_ID_BORDER]);

    // Border for 'Next piece'
    _drawRectangle(casioParams_.NP_pos_.x + CASIO_BORDER_GAP,
                casioParams_.NP_pos_.y + CASIO_BORDER_GAP,
                casioParams_.NP_width_, casioParams_.NP_width_,
                NO_COLOR, colours_[COLOUR_ID_BORDER]);
}

// _drawRectangle() : Draw a single coloured rectangle
//
//   @x,@y : top left starting point
//   @width, @height : dimensions
//   @borderColour : Colour of the border in RGB format or -1 (if no border)
//   @fillColour : Filling colour in RGB format or -1 (if empty)
//
void tetrisGame::_drawRectangle(uint16_t x, uint16_t y, uint16_t width, uint16_t height, int32_t fillColour, int32_t borderColour){
    int16_t xFrom(x), yFrom(y);
    int16_t xTo(xFrom + width - 1), yTo(yFrom + height - 1);

    // Horizontal display ?
    if (casioParams_.rotatedDisplay_){
        casioParams_.rotate(xFrom, yFrom, xTo, yTo);
    }

    // Draw the rect
#ifdef DEST_CASIO_FXCG50
    drect_border(xFrom, yFrom, xTo, yTo, fillColour, 1, borderColour);
#endif // #ifdef DEST_CASIO_FXCG50
}

// _drawNumValue() : Draw a value and its name
//
//  @index of the VALUE object to be drawn
//
void tetrisGame::_drawNumValue(uint8_t index){
    char valStr[MAX_VALUE_LEN + 1];

    // Erase previous value ?
    if (-1 != values_[index].previous){
        __valtoa(values_[index].previous, values_[index].name, valStr);

#ifdef DEST_CASIO_FXCG50
        if (casioParams_.rotatedDisplay_){
            _dtextV(casioParams_.textsPos_[index].x, casioParams_.textsPos_[index].y, colours_[COLOUR_ID_BKGRND], valStr);
        }
        else{
            dtext(casioParams_.textsPos_[index].x, casioParams_.textsPos_[index].y, colours_[COLOUR_ID_BKGRND], valStr);
        }
#endif // #ifdef DEST_CASIO_FXCG50
    }

    // print new value
    __valtoa(values_[index].value, values_[index].name, valStr);

#ifdef DEST_CASIO_FXCG50
    if (casioParams_.rotatedDisplay_){
        _dtextV(casioParams_.textsPos_[index].x, casioParams_.textsPos_[index].y, colours_[COLOUR_ID_TEXT], valStr);
    }
    else{
        dtext(casioParams_.textsPos_[index].x, casioParams_.textsPos_[index].y, colours_[COLOUR_ID_TEXT], valStr);
    }
#endif // #ifdef DEST_CASIO_FXCG50

    values_[index].previous = values_[index].value;
}

// _dtextV() : Draw a line of text vertically
//
//  @x, @y : Anchor point coordinates
//  @fg : font colour
//  @test : string to draw
//
void tetrisGame::_dtextV(int x, int y, int fg, const char* text){
    if (strlen(text) > 0){
        int16_t xFrom(x), yFrom(y), xTo, yTo;

        // dimensions of the first char.
        char* current = (char*)text;
        int w, h;
#ifdef DEST_CASIO_FXCG50
        dnsize(current, 1, casioParams_.vFont_, &w, &h);
#else
        w = h = 10; // for debug tests
#endif // #ifdef DEST_CASIO_FXCG50

        // Get new coordinates of the anchor
        xTo = xFrom + w;
        yTo = yFrom + h;
        casioParams_.rotate(xFrom, yFrom, xTo, yTo);

        // Draw the string (char. by char.)
        while (*current){
#ifdef DEST_CASIO_FXCG50
            dtext_opt(xFrom, yFrom,  fg, C_NONE, DTEXT_RIGHT, DTEXT_BOTTOM, current, 1);
            dnsize(current, 1, casioParams_.vFont_, &w, &h);
#endif // #ifdef DEST_CASIO_FXCG50

            // Update anchor pos.
            yFrom-=h;

            // Next char
            current++;
        }
    }
}

// __valtoa() : Transform a numeric value into a string
//
//  This specific method creates a string composed of the name of the value
//  and the value it self. It is equivalent to a sprintf(out, "%s : %d", name, value)
//
//  The base can't be changed it is always equal to 10
//
//  This method assumes the output buffer - ie. the str - is large enough to contain
//  the name and the formated value.
//
//  @num : Numeric value to transform
//  @name : Name of the value (can be NULL)
//  @str : Pointer to output string
//
//  Return the formated string
//
char* tetrisGame::__valtoa(int num, const char* name, char* str){
    char* strVal(str); // Num. part starts here

    // Insert name
	if (name){
	    strcpy(str, name);
	    strVal+=strlen(str);
	}

	// Add num. value
	int sum ((num < 0)?-1*num:num);
	uint8_t i(0), digit, dCount(0);
	do{
		digit = sum % 10;
		strVal[i++] = '0' + digit;
		if (!(++dCount % 3)){
		    strVal[i++] = ' ';  // for large numbers lisibility
		}

		sum /= 10;
	}while (sum);

	// A sign ?
	if (num < 0){
	    strVal[i++] = '-';
	}
	strVal[i] = '\0';

	// Reverse the string (just the num. part)
	__strrev(strVal);
	return str;
}

// __strrev() : Reverse a string
//
//  @str : String to reverse
//
void tetrisGame::__strrev(char *str){
	int i, j;
	unsigned char a;
	size_t len = strlen((const char *)str);
	for (i = 0, j = len - 1; i < j; i++, j--){
		a = str[i];
		str[i] = str[j];
		str[j] = a;
	}
}

// EOF
