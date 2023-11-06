//---------------------------------------------------------------------------
//--
//--	File	: piece.cpp
//--
//--	Author	: Jérôme Henry-Barnaudière - GeeHB
//--
//--	Project	: jtetris - cpp version
//--
//---------------------------------------------------------------------------
//--
//--	Description:
//--
//--			Implementation of piece & pieceStatus objects :
//--            a tetramino and all the informations for its drawing
//--
//---------------------------------------------------------------------------

#include "piece.h"

//---------------------------------------------------------------------------
//--
//-- piece object
//--
//--    a tetramino and all it's rotation states
//--
//---------------------------------------------------------------------------

// Copy constructor (useless ????)
//
piece::piece(piece& other) {
    // Recopy
    rotate_ = other.rotate_;
    maxRotate_ = other.maxRotate_;
    vertOffset_ = other.vertOffset_;
    maxAllocated_ = other.maxAllocated_;

    // Copy the points
    if ((points_ = (uint8_t**)malloc(rotate_ * sizeof(uint8_t*)))) {
        for (uint8_t index(0); index < other.maxRotate_; index++) {
            if (NULL != (points_[index] = (uint8_t*)malloc(PIECE_SIZE))) {
                memcpy(points_[index], other.points_[index], PIECE_SIZE);
                maxAllocated_ = other.maxAllocated_;
            }
        }
    }
}

// addRotation() : Add a new piece from a template
//
//  @tempPiece : List a strings defining a tetramino from a template
//
//  Return true if the rotation has been successfully added
//
bool piece::addRotation(const char* tempPiece) {
    if (!tempPiece) {
        return false;
    }

    // Create an empty piece
    uint8_t* newRotation = (uint8_t*)malloc(PIECE_SIZE * sizeof(uint8_t));
    if (NULL == newRotation) {
        return false;
    }

    // By default, no colour (ie. the board colour)
    memset(newRotation, COLOUR_ID_BOARD, PIECE_SIZE);

    // Transfer values
    bool cont(true);
    char car(0);
    uint8_t pos(0);
    for (uint8_t li(0); cont && li < PIECE_HEIGHT; li++) {
        for (uint8_t col = 0; cont && col < PIECE_WIDTH; col++) {
            car = tempPiece[pos++];
            if (car){
                if (car != EMPTY_CHAR) {
                    newRotation[li * PIECE_WIDTH + col] = car - '0';
                }
            }
            else {
                // String is too short
                cont = false;
            }
        }
    }

    // Added ?
    if (false == _addRotation(newRotation)) {
        free(newRotation);
        return false;
    }

    // First piece => compute vertical offset
    if (1 == maxRotate_) {
        vertOffset_ = PIECE_HEIGHT - 1; // On line visible
        while (_isLineEmpty(0, vertOffset_) && vertOffset_ >= 0) {
            vertOffset_ -= 1;
        }
    }

    // Success
    return true;
}

// clear() : Clear the current piece
//
void piece::clear() {
    if (points_) {
        // Free the differents pieces (rotations)
        for (uint8_t index(0); index < maxRotate_; index++) {
            free(points_[index]);
        }

        // Free the array
        free(points_);
        points_ = NULL;
    }

    // Ensures all datas are initialized
    _init();
}

// _addRotation() : Add a rotation to the current piece
//
//  @tempPiece : List of blocks
//
//  Return true if the rotation is valid and has been successfully added
//
bool piece::_addRotation(uint8_t* tempPiece) {
    if (!tempPiece) {
        return false;
    }

    // Size the "points" buffer
    if (maxRotate_ >= maxAllocated_) {
        // New size
        maxAllocated_ += ALLOCATE_STEP;
        points_ = (uint8_t**)realloc(points_, maxAllocated_ * sizeof(uint8_t*));
        if (NULL == points_) {
            return false;
        }
    }

    // Copy ...
    points_[maxRotate_++] = tempPiece;
    return true;
}

// _isLineEmpty(): Is the "line" empty ?
//
//  @rotIndex : Index of the rotation to check
//  @lineIndex : Index of the line in the tetramino
//
//  Returns true if the tested line is empty (ie. no colored block)
//
bool piece::_isLineEmpty(uint8_t rotIndex, uint8_t lineIndex) {
    if (rotIndex >= maxRotate_ || lineIndex >= PIECE_HEIGHT) {
        return false;
    }

    uint8_t total(0);
    for (uint8_t col(0); !total && col < PIECE_WIDTH; col++) {
        total += points_[rotIndex][lineIndex * PIECE_WIDTH + col];
    }

    // Yes !
    return (!total);    // Sum of colors == 0 => empty line
}

// EOF
