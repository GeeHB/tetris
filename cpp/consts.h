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

// Game status
//
#define STATUS_CREATED	0
#define STATUS_INIT		1
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
#define COLOUR_ID_ANIMATE   12     // animation When line if full

#define LAST_COLOUR_ID		COLOUR_ID_ANIMATE

#define COLOUR_ID_NONE		(LAST_COLOUR_ID +1)		// This is not a colour !!!

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