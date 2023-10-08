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
//--                a tetramino and all the informations for its drawing
//--
//---------------------------------------------------------------------------

#include "piece.h"

#ifdef _DEBUG
#include <iostream>
#endif // _DEBUG

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
    points_ = (uint8_t**)malloc(rotate_ * sizeof(uint8_t*));
    if (points_) {
        for (uint8_t index(0); index < other.maxRotate_; index++) {
            if (NULL != (points_[index] = (uint8_t*)malloc(PIECE_SIZE))) {
                memcpy(points_[index], other.points_[index], PIECE_SIZE);
                maxAllocated_ = other.maxAllocated_;
            }
        }
    }
}

// Add a new piece from a template
//
bool piece::addPiece(const char* tempPiece) {
    if (nullptr == tempPiece) {
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
    if (false == _addPiece(newRotation)) {
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

// Clear the current piece
//
void piece::clear() {
    if (points_) {
        // Free the differents pieces (rotations)
        for (uint8_t index(0); index < maxRotate_; index++) {
            free(points_[index]);
        }

        // Free the array
        free(points_);
        points_ = nullptr;
    }

    // Ensures all datas are initialized
    _init();
}

#ifdef _DEBUG
// Output to a console
//
void piece::print(uint8_t rotIndex) {
    if (rotIndex < maxRotate_) {
        std::cout << std::endl;
        for (uint8_t li(0); li < PIECE_HEIGHT; li++) {
            for (uint8_t col = 0; col < PIECE_WIDTH; col++) {
                std::cout << "  " << int(points_[rotIndex][li * PIECE_WIDTH + col]);
            }
            std::cout << std::endl;
        }
    }
}
#endif // _DEBUG

// Add a rotation to the current piece
//
bool piece::_addPiece(uint8_t* tempPiece) {
    if (nullptr == tempPiece) {
        return false;
    }

    // Size the "points" buffer
    if (maxRotate_ >= maxAllocated_) {
        // New size
        maxAllocated_ += ALLOCATE_STEP;
        if (NULL == (points_ = (uint8_t**)realloc(points_, maxAllocated_ * sizeof(uint8_t*)))) {
            return false;
        }
    }

    // Copy ...
    //return (NULL != memcpy(tempPiece, points_[maxRotate_++], sizeof(uint8_t));
    points_[maxRotate_++] = tempPiece;
    return true;
}

// Is the "line" empty ?
//
bool piece::_isLineEmpty(uint8_t pieceIndex, uint8_t lineIndex) {
    if (pieceIndex >= maxRotate_ || lineIndex >= PIECE_HEIGHT) {
        return false;
    }

    uint8_t total(0);
    //uint8_t* piece = points_[pieceIndex];
    for (uint8_t col(0); !total && col < PIECE_WIDTH; col++) {
        total += points_[pieceIndex][lineIndex * PIECE_WIDTH + col];
    }

    // Yes !
    return (!total);
}

// EOF
