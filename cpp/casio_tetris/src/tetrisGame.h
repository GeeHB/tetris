//---------------------------------------------------------------------------
//--
//--	File	: tetrisGame.h
//--
//--	Author	: Jérôme Henry-Barnaudière - GeeHB
//--
//--	Project	: jtetris - cpp version
//--
//---------------------------------------------------------------------------
//--
//--	Description:
//--
//--	    Definition of tetrisGame
//---------------------------------------------------------------------------

#ifndef __J_TETRIS_GAME_h__
#define __J_TETRIS_GAME_h__	1

#include "consts.h"
#include "piece.h"
#include "templates.h"
#include "casioFX-CG50.h"

#include <cstdlib>

#ifdef __cplusplus
extern "C" {
#endif // #ifdef __cpluscplus

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

        // Constructions
        tetrisGame();
        tetrisGame(tetrisParameters& params)
        :tetrisGame(){
            setParameters(params);
        }

        // Destruction
        ~tetrisGame() {}

        // Game's parameters
        void setParameters(tetrisParameters & params);

        // Start the game
        bool start();

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

        // Update the display
        void updateDisplay(){
        #ifdef DEST_CASIO_FXCG50
            dupdate();
        #endif // #ifdef DEST_CASIO_FXCG50
        }

    // Internal methods
    //
    protected:

        // The tetrisGame is empty ...
        void _emptyTetrisGame() {
            memset(playField_, COLOUR_ID_BOARD, PLAYFIELD_HEIGHT * PLAYFIELD_WIDTH);
        }

        // Change the game speed
        long _updateSpeed(long currentDuration, uint8_t level, uint8_t incLevel = 1);

       // Change origin for drawing
        void _changeOrigin(bool inTetrisGame, uint16_t& x, uint16_t& y, uint16_t& width, uint16_t& height);

        // Handle keyboard events
        void _handleGameKeys();

        //
        // Pieces management
        //

        // Datas of a piece
        uint8_t* _nextPieceDatas() {
            return ((nextIndex_ < 0 || nextIndex_ >= TETRAMINOS_COUNT) ? nullptr : tetraminos_[nextIndex_].datas(0));
        }
        uint8_t* _pieceDatas(int8_t index, uint8_t  rotIndex) {
            return ((index < 0 || index >= TETRAMINOS_COUNT || rotIndex >= tetraminos_[index].maxRotations()) ? nullptr : tetraminos_[index].datas(rotIndex));
        }

        // New piece (in the game)
        void _newPiece();

        // The position of the piece just changed
        void _piecePosChanged();

        // Get a new index for the next piece
        uint8_t _newPieceIndex() {
            return (rand() % TETRAMINOS_COUNT);
        }

        //
        // Mouvements
        //
        bool _rotateLeft();
        bool _left();
        bool _right();
        bool _down(bool newPiece = false);
        void _fall();

        // Can the current piece be at the given position ?
        bool _canMove(uint8_t leftPos, uint8_t  topPos);

        // Get a piece min.pos.index (vertical value)
        uint8_t _minTopPosition();

        // Add a randomly generated dirty line in the gameplay
        void _addDirtyLine(uint8_t lineID);

        // Clear and remove a completed line
        void _clearLine(uint8_t index);

        // Put the tetramino at the current position
        void _putPiece(uint8_t colour = COLOUR_ID_NONE);

        // The piece is at the lowest possible level
        void _reachLowerPos(uint8_t downRowcount = 0);

        // Display the next piece
        void _drawNextPiece(int8_t pieceIndex);

        // Erase the "next piece" tetramino
        void _eraseNextPiece(uint16_t left, uint16_t  top, uint16_t  width, uint16_t  height, uint8_t colourID);

        // Numeric value
        void _drawNumValue(uint8_t index, uint16_t value){}

        // Draw a line of text(and erase the prrevious value)
        void _drawText(uint8_t index, const char* value){}

        // Draw entire background
        void _drawBackGround();

        // Draw a tetramino using the given colour
        void _drawSinglePiece(uint8_t* datas, uint16_t cornerX, uint16_t cornerY, bool intetrisGame = true, uint8_t colourID = COLOUR_ID_NONE);

        // Draw a single coloured block
        void _drawSingleBlock(uint16_t left, uint16_t  top, uint16_t  width, uint16_t  height,uint8_t colourID){
            _drawRectangle(left, top, width, height, colours_[colourID]);
        }

        // Draw the tetrisGame
        void _drawTetrisGame();

        // Helpers for drawings
        //
        /*
        void _drawScore() {
            _drawNumValue(TEXT_SCORE_ID, score_);
        }
        void _drawLevel() {
            _drawNumValue(TEXT_LEVEL_ID, level_);
        }
        void _drawLines() {

        }
        */

        // Draw a coloured rectangle
        void _drawRectangle(uint16_t x, uint16_t y, uint16_t width, uint16_t height, int16_t fillColour = NO_COLOR, int16_t borderColour = NO_COLOR);

    // Members
    //
    protected:

        uint8_t status_; // Game status

        uint8_t playField_[PLAYFIELD_HEIGHT][PLAYFIELD_WIDTH];      // The playfield
        piece   tetraminos_[TETRAMINOS_COUNT];                      // The tetraminos' list

        tetrisParameters parameters_;

        uint32_t colours_[LAST_COLOUR_ID+1];     // Colours in rgb

        casioFXCG50 casioParams_;

        // Piece and next one
        int8_t nextIndex_;  // -1 = None
        pieceStatus nextPos_, currentPos_;

        // Indicators
        uint16_t score_;
        uint8_t lines_, level_;
};

#ifdef __cplusplus
}
#endif // #ifdef __cpluscplus

#endif // __J_TETRIS_GAME_h__

// EOF
