//---------------------------------------------------------------------------
//--
//--	File	: consts.h
//--
//--	Author	: Jérôme Henry-Barnaudière - GeeHB
//--
//--	Project	: jtetris - cpp version
//--
//---------------------------------------------------------------------------
//--
//--	Description:
//--
//--			Shared types, objects and constants
//--
//---------------------------------------------------------------------------

#ifndef __J_TETRIS_CONSTS_h__
#define __J_TETRIS_CONSTS_h__    1

#include <cstdint> // <stdint.h>
#include <cstring>
#include <stdio.h>
#include <stdlib.h>

// Playfield's dimensions (in box unit)
//
#define PLAYFIELD_WIDTH     10
#define PLAYFIELD_HEIGHT    20

// Game status
//
#define STATUS_CREATED	1
#define STATUS_INIT		STATUS_CREATED
#define STATUS_RUNNING	2
#define STATUS_STOPPED	4
#define STATUS_CANCELED 8

// Scores valorisation (in %)
//
#define SCORE_NO_SHADOW         10.0    // +10% if no pieces'shadowing
#define SCORE_SPEED_GAME        2.0     // 2% * {piece's height} => quick play <=> more points
#define SCORE_DIRTY_LINES       0.1     // 0.1% per starting dirty-line
#define SCORE_LEVEL_VALUATION   15.0    // 15% more for each level

// Timer & game's Levels
//
#define SLEEP_DURATION          5000   // 5ms
#define MAX_LEVEL_ACCELERATION  15      // No more acceleration when this level is reached
#define ACCELERATION_STEP       0.19    // Growing speed % per level
#define INITIAL_SPEED           200     // Level 1 speed (larger is slower)
#define MOVES_UPDATE_LEVEL      250     // Change level criterium (# of pieces going down one step)

//
// Colour IDs
//
#define COLOUR_ID_BOARD     0

// 1 -> 7 : Pieces colours (nCurses ID)
#define COLOUR_ID_SHADOW    8
#define COLOUR_ID_TEXT      9
#define COLOUR_ID_BORDER    10
#define COLOUR_ID_BKGRND    11
//#define COLOUR_ID_ANIMATE   12     // animation When line if full

#define LAST_COLOUR_ID		COLOUR_ID_BKGRND

#define COLOUR_ID_NONE		(LAST_COLOUR_ID +1)		// This is not a colour !!!

// A few basic colours
//

#ifndef RGB
#define RGB(r,g,b)      ((uint32_t)(((uint8_t)(r)|((uint16_t)((uint8_t)(g))<<8))|(((uint32_t)(uint8_t)(b))<<16)))
#define LOBYTE(w)       ((uint8_t)(w))
#define GetRValue(rgb)  (LOBYTE(rgb))
#define GetGValue(rgb)  (LOBYTE(((uint16_t)(rgb)) >> 8))
#define GetBValue(rgb)  (LOBYTE((rgb)>>16))
#endif // RGB

#define COLOUR_BLACK   RGB(0, 0, 0)
#define COLOUR_WHITE   RGB(255, 255, 255)
#define COLOUR_RED     RGB(255, 0, 0)
#define COLOUR_GREEN   RGB(0, 255, 0)
#define COLOUR_YELLOW  RGB(255, 255, 0)
#define COLOUR_BLUE    RGB(0, 0, 255)
#define COLOUR_PURPLE  RGB(255, 0, 255)
#define COLOUR_CYAN    RGB(0, 255, 255)
#define COLOUR_ORANGE  RGB(255, 128, 0)

#define COLOUR_LTGREY  RGB(224, 224, 224)
#define COLOUR_GREY    RGB(128, 128, 128)
#define COLOUR_DKGREY  RGB(64, 64, 64)

// Key codes
//
#define KEY_LEFT        '4'
#define KEY_RIGHT       '5'
#define KEY_ROTATE_LEFT '3'
// #define KEY_ROTATE_RIGHT= '0'
#define KEY_DOWN        '2'
#define KEY_FALL        ' '
#define KEY_QUIT        'q'

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
            vertical_ = true;
        }

        // recopy
        void copy(tetrisParameters& other) {
            startLevel_ = other.startLevel_;
            dirtyLines_ = other.dirtyLines_;
            shadow_ = other.shadow_;
            vertical_ = other.vertical_;
        }

    // Members
    //
    public:
        uint8_t startLevel_;
        uint8_t dirtyLines_;
        bool shadow_;
        bool vertical_;
};

#endif // __J_TETRIS_CONSTS_h__

// EOF
