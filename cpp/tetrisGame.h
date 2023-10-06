//---------------------------------------------------------------------------
//--
//--	File	: tetrisGame.h
//--
//--	Author	: Jerome Henry-Barnaudiere - GeeHB
//--
//--	Project	: jtetris - cpp version
//--
//---------------------------------------------------------------------------
//--
//--	Description:
//--
//--	    Definition of :
//--
//--            - tetrisGame
//--
//--            - tetrisParameters
//--
//---------------------------------------------------------------------------

#ifndef __J_TETRIS_GAME_h__
#define __J_TETRIS_GAME_h__	1

#include "consts.h"
#include "piece.h"
#include "templates.h"

//---------------------------------------------------------------------------
//--
//-- tetrisParameters object
//--
//--    All the game's parameters
//--
//---------------------------------------------------------------------------

class tetrisParameters {
    public:
        // Construction
        //
        tetrisParameters() {
            // Set default parameters
            startLevel_ = 0;
            dirtyLines_ = 0;
            shadow_ = false;
        }

        // recopy
        void copy(tetrisParameters& other) {
            startLevel_ = other.startLevel_;
            dirtyLines_ = other.dirtyLines_;
            shadow_ = other.shadow_;
        }

    // Members
    //
    public:
        uint8_t startLevel_;
        uint8_t dirtyLines_;
        bool shadow_;
};

//---------------------------------------------------------------------------
//--
//-- tetrisGame object
//--
//--    Handle the gameplay and the game(without display !)
//--
//---------------------------------------------------------------------------

class tetrisGame {

    // Public methods
    //
    public:

        // Constrcution
        tetrisGame();

        // Destruction
        virtual ~tetrisGame() {

        }

        // Finish (end of displays)
        void clear(){}

#ifdef _DEBUG
        // Test ...
        void print();
#endif // _DEBUG

        // Status
        //
        bool isRunning() {
            return STATUS_RUNNING == status_;
        }

        // Cancel the game
        void cancel() {
            // Already escaped ?
            if (!isCancelled()) {
                status_ += STATUS_CANCELED;

                // stop the game
                end(true);
            }
        }

        // Escaped / canceled by the user ?
        bool isCancelled() {
            return ((status_ & STATUS_CANCELED) == STATUS_CANCELED);
        }

        // Force the end of the game
        void end(bool force = false) {
            if (force) {
                status_ |= STATUS_CANCELED;
            }
            else {
                status_ = STATUS_STOPPED;
            }
        }

        // Helpers for drawings
        //
        void drawScore() {
            _drawNumValue(0, score_);
        }
        void drawLevel() {
            _drawNumValue(1, level_);
        }
        void drawLines() {
            _drawNumValue(2, lines_);
        }
        void drawNextPiece() {
            _drawNextPiece(nextPieceIndex());
        }

        void updateDisplay(){}

        // Draw all
        void reDraw() {
            drawBackGround();
            drawtetrisGame();
            drawScore();
            drawLevel();
            drawLines();
        }

        // Draw the tetrisGame
        void drawtetrisGame();

        // Game level
        uint8_t level() {
            return level_;
        }

        // The game level just changed
        uint8_t levelChanged(uint8_t inc) {
            level_ += inc;
            drawLevel();
            updateDisplay();
            return level_;
        }

        // Score
        uint16_t score() {
            return score_;
        }
        void setScore(uint16_t value) {
            score_ = value;
        }
        uint16_t incScore(uint16_t inc) {
            score_ += inc;

            drawScore();
            updateDisplay();
            return score_;
        }

        // Next piece index
        int8_t nextPieceIndex() {
            return nextIndex_;
        }
        void setNextPieceIndex(uint8_t index) {
            nextIndex_ = index;
        }

        // Lines completed
        uint8_t lines() {
            return lines_;
        }
        void setLines(uint8_t value = 0) {
            lines_ = value;
        }
        uint8_t incLines(uint8_t inc) {
            lines_ += inc;
            return lines_;
        }

        // Game's parameters
        void setParameters(tetrisParameters & params);

        //
        // Pieces management
        //

        // Datas of a piece
        uint8_t* nextPieceDatas() {
            return ((nextIndex_ < 0 || nextIndex_ >= TETRAMINOS_COUNT) ? nullptr : tetraminos_[nextIndex_].datas(0));
        }
        uint8_t* pieceDatas(uint8_t index, uint8_t  rotIndex) {
            return ((index < 0 || index >= TETRAMINOS_COUNT || rotIndex >= tetraminos_[index].maxRotations()) ? nullptr : tetraminos_[index].datas(rotIndex));
        }

        // Verifications
        bool checkEnvironment() {
            status_ = STATUS_INIT;
            return true;
        }

        // Let's play
        bool start();

        // New piece (in the game)
        void newPiece();

        //
        // Mouvements
        //
        bool rotateLeft();
        bool left();
        bool right();
        bool down() {
            return _down();
        }
        void fall();

        // The position of the piece just changed
        void piecePosChanged();

        // Update drawings after removing lines
        void allLinesCompletedRemoved(uint8_t rowCount, uint8_t totalLines) {
            lines_ = totalLines;

            drawtetrisGame();
            drawLines();
            updateDisplay();
        }

        // New index for the "next piece"
        void nextPieceIndexChanged(uint8_t nextPieceIndex){
            _drawNextPiece(nextPieceIndex);
            updateDisplay();
        }

    // Internal methods
    //
    protected:

        // The tetrisGame is empty ...
        void _emptytetrisGame() {
            memset(playField_, COLOUR_ID_BOARD, PLAYFIELD_HEIGHT * PLAYFIELD_WIDTH);
        }

        // Get a new index for the next piece
        uint8_t _newPieceIndex() {
            return (rand() % TETRAMINOS_COUNT);
        }

        // Can the piece go down ?
        bool _down(bool newPiece = false);

        // Can the current piece be at the given position ?
        bool _canMove(uint8_t leftPos, uint8_t  topPos);

        // Get a piece min.pos.index (vertical value)
        uint8_t _minTopPosition();

        // Add a randomly generated dirty line at the bottom of the gameplay
        void _addDirtyLine(uint8_t line);

        // Clear and remove a completed line
        void _clearLine(uint8_t index);

        // Put the tetramino at the current position
        void _putPiece(uint8_t colour = COLOUR_ID_NONE);

        // The piece is at the lowest possible level
        void _reachLowerPos(uint8_t downRowcount = 0);

        // Change origin for drawing
        void _changeOrigin(bool intetrisGame, uint16_t& x, uint16_t& y, uint16_t& width, uint16_t& height);

        // Drawings
        //

        // Display the next piece
        void _drawNextPiece(uint8_t pieceIndex);

        // Numeric value
        void _drawNumValue(uint8_t index, uint16_t value){}

        // Draw a line of text(and erase the prrevious value)
        void _drawText(uint8_t index, const char* value){}

        // Draw borders
        void drawBackGround(){}

        // Draw a tetramino using the given colour
        void _drawSinglePiece(uint8_t* datas, uint16_t cornerX, uint16_t cornerY, bool intetrisGame = true, uint8_t colourID = COLOUR_ID_NONE);

        // Draw a single coloured block
        void _drawSingleBlock(uint16_t left, uint16_t  top, uint16_t  width, uint16_t  height,uint8_t colourID){}

        // Erase a tetramino
        void _eraseBlocks(uint16_t left, uint16_t  top, uint16_t  width, uint16_t  height, uint8_t colourID){}


    // Members
    //
    protected:

        uint8_t status_; // Game status

        uint8_t playField_[PLAYFIELD_HEIGHT][PLAYFIELD_WIDTH];      // The playfield
        piece   tetraminos_[TETRAMINOS_COUNT];                      // The tetraminos' list

        tetrisParameters parameters_;

        // Piece and next one
        int8_t nextIndex_ = -1;
        pieceStatus nextPos_, currentPos_;

        // Indicators
        uint16_t    score_;
        uint8_t lines_, level_;
};

#endif // __J_TETRIS_GAME_h__

// EOF
