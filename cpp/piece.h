//---------------------------------------------------------------------------
//--
//--	File	: piece.h
//--
//--	Author	: Jérôme Henry-Barnaudière - GeeHB
//--
//--	Project	: jtetris - cpp version
//--
//---------------------------------------------------------------------------
//--
//--	Description:
//--
//--			Definition of piece & pieceStatus objects : 
//--                a tetramino and all the informations for its drawing
//--
//---------------------------------------------------------------------------

#ifndef __J_TETRIS_PIECE_h__
#define __J_TETRIS_PIECE_h__    1

#include "consts.h"
#include <malloc.h>

// Public consts
//

// Tetramino max dims
#define PIECE_WIDTH     4
#define PIECE_HEIGHT    PIECE_WIDTH

// size in bytes
#define PIECE_SIZE      (PIECE_WIDTH * PIECE_HEIGHT)

// Allocation step
#define ALLOCATE_STEP   4

// Empty val in templates
#define EMPTY_CHAR      '.'

//---------------------------------------------------------------------------
//--
//-- pieceStatus object
//--
//--    All the informations concerning a tetramino : 
// --       index, rotation, position ...
//--
//---------------------------------------------------------------------------
class pieceStatus{

    // Public methods
    //
    public:

        // Constructors
        //
        pieceStatus(){
            // Use default values
            index_ = -1; 
            leftPos_ = topPos_  = 0;
            rotationIndex_ = 0;
            shadowTopPos_ = -1;
        }
        
        // Copy
        pieceStatus(pieceStatus& other){
            // Copy the values
            index_ = other.index_;
            leftPos_ = other.leftPos_;
            topPos_ = other.topPos_;
            rotationIndex_ = other.rotationIndex_;
            shadowTopPos_ = other.shadowTopPos_;
        }

        // Equal ?
        bool operator == (pieceStatus& right){
            return (index_ == right.index_ && leftPos_ == right.leftPos_ && topPos_ == right.topPos_ && rotationIndex_ == right.rotationIndex_);
        }

    // Members
    //
    public:
        uint8_t  index_;             // Index of the piece (-1 = don't draw)
        uint8_t  leftPos_;           // Initial pos. 
        uint8_t  topPos_;
    
        uint8_t  rotationIndex_;
        uint8_t  shadowTopPos_;      // yPos of shadow (-1 = no shadow)
};

//---------------------------------------------------------------------------
//--
//-- piece object
//--
//--    a tetramino and all it's rotation states
//--
//---------------------------------------------------------------------------

class piece{

    // Public methods
    //
    public:
        // Constructors
        //
        piece(){
            // Default values for members
            _init();
        }

        // recopy (useless ????)
        piece(piece& other);

        // Destructor
        virtual ~piece(){
            clear();
        }

        // Add from a template
        //
        bool addPiece(const char* tempPiece);

        // Clear the current piece
        //
        void clear();

#ifdef _DEBUG
        // Affichage en mode texte
        void print(uint8_t rotIndex);
#endif // _DEBUG

        // Access
        //

        // Piece's datas in the any rotation state (index = rotate_)
        uint8_t* datas(uint8_t index) {
            return (points_ == nullptr ||  index >= maxRotate_ ? NULL : points_[index]);
        }
        uint8_t* currentDatas() {
            return datas(rotate_);
        }

        // Vertical offset (when rotationIndex = 0)
        //   ie.last non-empty line index
        uint8_t verticalOffset() {
            return vertOffset_;
        }

        // Rotation(s)
        //

        // Back to initial position
        void rotateBack() {
            rotate_ = 0;
        }

        // Max.rotation index for the piece
        // (some pieces doen't rotate at all)
        uint8_t maxRotations() {
            return maxRotate_;
        }

        // Trigonometric rotation
        uint8_t rotateLeft() {
            // Rotate
            rotate_ += 1;

            // 360° ?
            if (rotate_ >= maxRotate_){
                rotate_ = 0;
            }

            return rotate_;
        }

        // Clockwise rotation
        uint8_t rotateRight() {
            return rotate_ = (!maxRotate_?0: (rotate_ == 0 ? maxRotate_ - 1 : rotate_ - 1));
        }

    // Private methods
    //
    protected:
        
        // Initialize members
        void _init(){
            
            points_ = nullptr;  // No rotation
            maxAllocated_ = 0;

            rotate_ = 0;
            maxRotate_ = 0;
            vertOffset_ = -1;
        }

        // Add a rotation to the current piece
        bool _addPiece(uint8_t* tempPiece);

        // Is the "line" empty ?
        bool _isLineEmpty(uint8_t pieceIndex, uint8_t lineIndex);

    // Members
    //
    protected:
        uint8_t** points_;      // Matrix of the piece whith all possible rotations
        uint8_t rotate_;        // rotation index (ie. index of the piece to draw)
        uint8_t maxRotate_;     // max. rotation(s) allowed for the piece ( = 360°)
        uint8_t maxAllocated_;  // Size of points_ in "rotation" count
        
        int8_t vertOffset_;     // Initial vert. offset (ie. count of empty lines starting from bottom)
        uint8_t colourIndex_;   // Colour ID (0 = invisible)
};

#endif __J_TETRIS_PIECE_h_
    
// EOF