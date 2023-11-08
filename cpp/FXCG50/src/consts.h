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
#include <gint/kmalloc.h>
#else
#include <malloc.h>
#include <cstdint> // <stdint.h>
#include <cstdio>
#endif // #ifdef DEST_CASIO_FXCG50

#include <cstring>
#include <cstdlib>

#ifdef __cplusplus
extern "C" {
#endif // #ifdef __cplusplus

// App. infos
#define APP_NAME     "jTetris"
#define APP_VERSION  "0.1 - beta"
#define APP_AUTHORE "GeeHB"

// Playfield's dimensions (in box units)
//
#define PLAYFIELD_WIDTH     10
#define PLAYFIELD_HEIGHT    20

// Game status
//
enum GAME_STATUS{
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
enum VALUE_ID{
    SCORE_ID = 0,
    LEVEL_ID = 1,
    COMPLETED_LINES_ID = 2,
    VAL_COUNT = COMPLETED_LINES_ID + 1
};

#define SCORE_STR   "Score : "
#define LEVEL_STR   "Level : "
#define COMPLETED_LINES_STR "Lines : "

#define MAX_VALUE_LEN 30

//
// Colour IDs
//
enum COLOUR_ID{
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
// 24 bits RGB (for tests only)
#define C_RGB(r,g,b)      ((uint32_t)(((uint8_t)(r)|((uint16_t)((uint8_t)(g))<<8))|(((uint32_t)(uint8_t)(b))<<16)))
#endif // #ifndef DEST_CASIO_FXCG50

enum DEF_COLOUR{
    COLOUR_BLACK   = C_RGB(0, 0, 0),
    COLOUR_WHITE   = C_RGB(31, 31, 31),
    COLOUR_RED     = C_RGB(31, 0, 0),
    COLOUR_GREEN   = C_RGB(0, 31, 0),
    COLOUR_YELLOW  = C_RGB(31, 31, 0),
    COLOUR_BLUE    = C_RGB(0, 0, 31),
    COLOUR_LT_BLUE = C_RGB(6, 6, 31),
    COLOUR_PURPLE  = C_RGB(31, 0, 31),
    COLOUR_CYAN    = C_RGB(0, 31, 31),
    COLOUR_ORANGE  = C_RGB(31, 16, 0),
    COLOUR_LT_GREY = C_RGB(29, 29, 29),
    COLOUR_GREY    = C_RGB(16, 16, 16),
    COLOUR_DK_GREY = C_RGB(8, 8, 8),
    NO_COLOR       = -1
};

// Key codes
//
#ifdef DEST_CASIO_FXCG50
enum GAME_KEY{
    KEY_CODE_F1 = KEY_F1,     // !!!
    KEY_CODE_F6 = KEY_F6,
    KEY_CODE_UP = KEY_UP,
    KEY_CODE_DOWN = KEY_DOWN,
    KEY_CODE_LEFT = KEY_LEFT,
    KEY_CODE_RIGHT = KEY_RIGHT,
    KEY_CODE_FALL = KEY_0,
    KEY_CODE_PAUSE = KEY_OPTN,
    KEY_CODE_ROTATE_DISPLAY = KEY_XOT,
    KEY_CODE_EXIT = KEY_EXIT,
    KEY_CODE_ENTER = KEY_EXE
};
#else
enum GAME_KEY{
    KEY_CODE_F1 = '&',
    KEY_CODE_F6 = '-',
    KEY_CODE_LEFT = '4',
    KEY_CODE_RIGHT = '5',
    KEY_CODE_UP = '3',
    KEY_CODE_DOWN = '2',
    KEY_CODE_FALL = ' ',
    KEY_CODE_PAUSE = 'p',
    KEY_CODE_ROTATE_DISPLAY = 'r',
    KEY_CODE_EXIT = 'q',
    KEY_CODE_ENTER = '\13'
};
#endif // #ifdef DEST_CASIO_FXCG50

// Tab names
//
#define TAB_ABOUT   "Tetris"
#define TAB_LINES   "Lines"
#define TAB_LEVEL   "Level"
#define TAB_SHADOW  "Shadow"
#define TAB_PLAY    "Play"
#define TAB_QUIT    "Exit"

// Comments for tabs
#define TAB_LEVEL_STR   "Choose starting level"
#define TAB_DIRTY_LINES_STR   "Number of 'dirty' lines when starting game"
#define TAB_SHADOW_OFF_STR  "No shadows"
#define TAB_SHADOW_ON_STR   "Shadows will be drawn"

//
// Min / max values for parameters
//

#define MIN_LEVEL   1
#define MAX_LEVEL   9

#define MIN_DIRTY_LINES   0
#define MAX_DIRTY_LINES   8


#define TAB_RANGE_WIDTH         11
#define TAB_RANGE_POS_Y         200     // Vertical pos of scale

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
            startLevel_ = MIN_LEVEL;
            dirtyLines_ = MIN_DIRTY_LINES;
            shadow_ = true;
            rotatedDisplay_ = false;        // by default, no screen rotation
        }

        // recopy
        void copy(tetrisParameters* other) {
            if (other){
                startLevel_ = other->startLevel_;
                dirtyLines_ = other->dirtyLines_;
                shadow_ = other->shadow_;
                rotatedDisplay_ = other->rotatedDisplay_;
            }
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
typedef struct __point {
    // Construction
    __point(){
        x = y = 0;
    }

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
    uint32_t   value;
    int32_t    previous;
} UVALUE;

#ifdef __cplusplus
}
#endif // #ifdef __cplusplus

#endif // __J_TETRIS_CONSTS_h__

// EOF
