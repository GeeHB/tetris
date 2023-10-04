//---------------------------------------------------------------------------
//--
//--	File	: board.h
//--
//--	Author	: Jérôme Henry-Barnaudière - GeeHB
//--
//--	Project	: jtetris - cpp version
//--
//---------------------------------------------------------------------------
//--
//--	Description:
//--
//--	    Definition of :
//--            - board : The matrix with all the colored blocks(ie dirty lines and / or putted tetraminos)
//--
//--            - tetrisParameters
//--
//---------------------------------------------------------------------------

#ifndef __J_TETRIS_BOARD_h__
#define __J_TETRIS_BOARD_h__	1

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
//-- board object
//--
//--    Handle the gameplay and the game(without display !)
//--
//---------------------------------------------------------------------------

class board {
    
    // Public methods
    //
    public:

        // Constrcution
        board();

        // Destruction
        virtual ~board() {

        }

        // Game level 
        uint8_t level() {
            return level_;
        }
        void setLevel(uint8_t value) {
            level_ = value;
        }
        uint8_t incLevel() {
            level_ += 1;
            return level_;
        }

        // Score
        uint16_t score() {
            return score_;
        }
        void setScore(uint16_t, value) {
            score_ = value;
        }
        uint16_t incScore(uint16_t inc) {
            score_ += inc;
            return score_;
        }

        // Next piece index
        uint8_t nextPieceIndex() {
            return nextIndex;
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
            return self.lines_;
        }

        // Game's parameters
        void setParameters(tetrisParameters & params);

        //
        // Pieces management
        //

        // Datas of a piece
        uint8_t** nextPieceDatas() {
            return (nextIndex_ < 0 || nextIndex_ >= TETRAMINOS_COUNT) ? nullptr : tetraminos_[nextIndex_].datas(0);
        }
        uint8_t** pieceDatas(uint8_t index, uint8_t  rotIndex) {
            return (index < 0 || index >= TETRAMINOS_COUNT || rotindex >= ? nullptr : tetraminos_[index].datas(rotIndex));
        }

        // New piece (in the game)
        void newPiece();

        // Let's play
        void start() {
            newPiece(); // the first piece
        }

        //
        // Mouvements
        //
        bool rotateLeft();
        bool left();
        bool right();
        bool down() {
            return _down();
        }
        bool fall();

        // The position of the piece just changed
        void piecePosChanged();

    // Internal methods
    //
    protected:

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

        // Clear and remove a completed line
        void _clearLine(uint8_t index);

        // Add a randomly generated dirty line at the bottom of the gameplay
        void _addDirtyLine(uint8_t line);

        // Put the tetramino at the current position
        void _putPiece(uint8_t colour = COLOUR_ID_SHADOW);

    // Members
    // 
    protected:
        uint8_t playField_[PLAYFIELD_HEIGHT][PLAYFIELD_WIDTH];      // The playfield
        piece   tetraminos_[TETRAMINOS_COUNT];                      // The tetraminos' list
        
        tetrisParameters parameters_;

        // Piece and next one
        pieceStatus currentPiece_;
        int8_t nextIndex_ = -1;

        // Game status
        uint16_t    score_;
        uint8_t lines_, level_;
};

#endif // __J_TETRIS_BOARD_h__

// EOF