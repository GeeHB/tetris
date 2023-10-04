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
//--			Definition of piece & pieceStatus objects : 
//--                a tetramino and all the informations for its drawing
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

/*
# Score valorisation (in %)
SCORE_NO_SHADOW     = 10        # +10% if no pieces'shadowing
SCORE_SPEED_GAME    = 2         # 2% * {piece's height} => quick play <=> more points
SCORE_DIRTY_LINES   = 0.1       # 0.1% per starting dirty-line
SCORE_LEVEL_VALUATION = 15      # 15% more for each level

#
# Timer & game's Levels
#
MAX_LEVEL_ACCELERATION = 15     # No more acceleration when this level is reached
ACCELERATION_STEP = 0.19        # Growing speed % per level
INITIAL_SPEED = 1200            # Level 1 speed (larger is slower)
MOVES_UPDATE_LEVEL = 250        # Change level criterium (# of pieces going down one step)
*/

//
// Colour IDs
//
#define COLOUR_ID_BOARD     0

// 1 -> 7 : Pieces colours (nCurses ID)
#define COLOUR_ID_SHADOW    8
#define COLOUR_ID_TEXT      9
#define COLOUR_ID_BORDER    10
#define COLOUR_ID_BKGRND    11
#define COLOUR_ID_ANIMATE   12     // animation When line if full

#define LAST_COLOUR_ID   = COLOUR_ID_ANIMATE

/*
#
# A few basic colours
#
COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)
COLOUR_RED = (255, 0, 0)
COLOUR_GREEN = (0, 255, 0)
COLOUR_YELLOW = (255, 255, 0)
COLOUR_BLUE = (0, 0, 255)
COLOUR_PURPLE = (255, 0, 255)
COLOUR_CYAN = (0, 255, 255)
COLOUR_ORANGE = (255, 128, 0)

COLOUR_LTGREY = ( 224, 224, 224)
COLOUR_GREY = ( 128, 128, 128)
COLOUR_DKGREY = ( 64, 64, 64)
*/

#endif // __J_TETRIS_CONSTS_h__

// EOF