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

#ifndef LINUX_VER
#define DEST_CASIO_FXCG50        1   // Compile for Casio FX CG50 calculator
#endif // #ifndef LINX_VER

#ifdef DEST_CASIO_FXCG50
// Specific includes for calculators
#include <gint/display.h>
#include <gint/keyboard.h>
#else
#include <cstdint> // <stdint.h>
#include <cstdio>
#include <cstdlib>
#endif // #ifdef DEST_CASIO_FXCG50

#include <cstring>

#ifdef __cplusplus
extern "C" {
#endif // #ifdef __cplusplus

// Playfield's dimensions (in box units)
//
#define PLAYFIELD_WIDTH     10
#define PLAYFIELD_HEIGHT    20

// Game status
//
enum{
    STATUS_INIT		 = 0,
    STATUS_READY	 = 1,
    STATUS_RUNNING	 = 2,
    STATUS_PAUSED    = 4,
    STATUS_STOPPED	 = 8,
    STATUS_CANCELED  = 16
};

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

// Indicators
//
enum{
    SCORE_ID = 0,
    LEVEL_ID = 1,
    COMPLETED_LINES_ID = 2,
    VAL_COUNT = COMPLETED_LINES_ID + 1
};

#define SCORE_STR   "Score"
#define LEVEL_STR   "Level"
#define COMPLETED_LINES_STR "Lines"

#define FORMAT_STR  "%s : %d"

//
// Colour IDs
//
enum{
    COLOUR_ID_BOARD     = 0,
    // 1 -> 7 : Pieces colours (nCurses ID)
    COLOUR_ID_SHADOW    = 8,
    COLOUR_ID_TEXT      = 9,
    COLOUR_ID_BORDER    = 10,
    COLOUR_ID_BKGRND    = 11,
    //#define COLOUR_ID_ANIMATE   12     // animation When line if full
    LAST_COLOUR_ID		= COLOUR_ID_BKGRND,
    COLOUR_ID_NONE = 12
};


// A few basic colours
//

#ifndef DEST_CASIO_FXCG50
// 24 bits RGB
#define C_RGB(r,g,b)      ((uint32_t)(((uint8_t)(r)|((uint16_t)((uint8_t)(g))<<8))|(((uint32_t)(uint8_t)(b))<<16)))
#endif // #ifndef DEST_CASIO_FXCG50

enum{
    COLOUR_BLACK   = C_RGB(0, 0, 0),
    COLOUR_WHITE   = C_RGB(255, 255, 255),
    COLOUR_RED     = C_RGB(255, 0, 0),
    COLOUR_GREEN   = C_RGB(0, 255, 0),
    COLOUR_YELLOW  = C_RGB(255, 255, 0),
    COLOUR_BLUE    = C_RGB(0, 0, 255),
    COLOUR_PURPLE  = C_RGB(255, 0, 255),
    COLOUR_CYAN    = C_RGB(0, 255, 255),
    COLOUR_ORANGE  = C_RGB(255, 128, 0),

    COLOUR_LTGREY  = C_RGB(224, 224, 224),
    COLOUR_GREY    = C_RGB(128, 128, 128),
    COLOUR_DKGREY  = C_RGB(64, 64, 64),
    NO_COLOR       = -1
};

// Key codes
//
#ifdef DEST_CASIO_FXCG50
enum{
    KEY_CODE_UP = KEY_UP,
    KEY_CODE_DOWN = KEY_DOWN,
    KEY_CODE_LEFT = KEY_LEFT,
    KEY_CODE_RIGHT = KEY_RIGHT,
    KEY_CODE_FALL = KEY_0,
    KEY_ROTATE_DISPLAY = KEY_XOT,
    KEY_CODE_QUIT = KEY_EXIT,
    KEY_CODE_ENTER = KEY_EXE
};
#else
enum{
    KEY_CODE_LEFT = '4',
    KEY_CODE_RIGHT = '5',
    KEY_CODE_UP = '3',
    KEY_CODE_DOWN = '2',
    KEY_CODE_FALL = ' ',
    KEY_ROTATE_DISPLAY = 'r',
    KEY_CODE_QUIT = 'q',
    KEY_CODE_ENTER = '\13'
};
#endif // #ifdef DEST_CASIO_FXCG50

//---------------------------------------------------------------------------
//--
//-- tetrisParameters object
//--
//--    All the game's parameters
//--    could be a simple interface / struct
//--
//---------------------------------------------------------------------------

class tetrisParameters {
    public:
        // Construction
        //
        tetrisParameters() {
            // Set default parameters
            startLevel_ = 1;
            dirtyLines_ = 7;
            shadow_ = false;
            rotatedDisplay_ = false;        // by default, no rotation
        }

        // recopy
        void copy(tetrisParameters& other) {
            startLevel_ = other.startLevel_;
            dirtyLines_ = other.dirtyLines_;
            shadow_ = other.shadow_;
            rotatedDisplay_ = other.rotatedDisplay_;
        }

    // Members
    //
    public:
        uint8_t startLevel_;
        uint8_t dirtyLines_;
        bool shadow_;
        bool rotatedDisplay_;
};

// For lisibility ...
//

// Point coordinates
//
typedef struct{
    uint16_t    x;
    uint16_t    y;
} POINT;

// A single unsigned value (and its previous val if exists)
//
#define MAX_VALUE_NAME  20
typedef struct __uvalue{

    // Construction
    __uvalue(){
        name[0] = 0;
        value = 0;
        previous = -1; //  value is not (yet) used
    }

    char       name[MAX_VALUE_NAME+1];
    uint16_t   value;
    int16_t    previous;
} UVALUE;

#ifdef __cplusplus
}
#endif // #ifdef __cplusplus

#endif // __J_TETRIS_CONSTS_h__

// EOF
