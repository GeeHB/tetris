//---------------------------------------------------------------------------
//--
//--	File	: casioScreen.h
//--
//--	Author	: Jérôme Henry-Barnaudière - GeeHB
//--
//--	Project	: jtetris - cpp version
//--
//---------------------------------------------------------------------------
//--
//--	Description:
//--
//--			Definition of casioScreen object and consts for casio fx-CG50
//--
//---------------------------------------------------------------------------

#ifndef __J_TETRIS_CASIO_h__
#define __J_TETRIS_CASIO_h__    1

#include "consts.h"

//---------------------------------------------------------------------------
//--
//-- Constants
//--
//---------------------------------------------------------------------------

// Screen dimensions in pixels
//
#define CASIO_WIDTH     384
#define CASIO_HEIGHT    192

// Box dimensions
//
#define CASIO_BOX_WIDTH_V   9       // playfield
#define CASIO_BOX_WIDTH_H   14

#define CASIO_BOX_WIDTH_NP_V   CASIO_BOX_WIDTH_V    // next piece preview
#define CASIO_BOX_WIDTH_NP_H   8

// Playfield
//
#define CASIO_PLAYFIELD_LEFT    100
#define CASIO_PLAYFIELD_BORDER  3
#define CASIO_BORDER_GAP        2

// Texts
//
#define CASIO_INFO_LEFT     250
#define CASIO_INFO_TOP      10
#define CASIO_INFO_GAP      4       // between border and text

//---------------------------------------------------------------------------
//--
//-- casioScreen object
//--
//--    coordinates, dimensionss for the casio fx-CG50 calculator
//--
//---------------------------------------------------------------------------

class casioScreen{

    // Public methods
    //
    public:
        // Construction
        casioScreen(){}

        // Vertical ?
        void setVert(bool vert = true){
            if (vert){
                boxWidth_ = CASIO_BOX_WIDTH_V;

                playfield_left_ = CASIO_PLAYFIELD_LEFT + CASIO_PLAYFIELD_BORDER + CASIO_BORDER_GAP;
                playfield_top_ = CASIO_PLAYFIELD_BORDER + CASIO_BORDER_GAP;

                NP_boxWidth_ = CASIO_BOX_WIDTH_NP_V;
                NP_width_ = 4 * NP_boxWidth_ + 2 * CASIO_INFO_GAP;

                NP_left_ = CASIO_INFO_LEFT + CASIO_INFO_GAP;
                NP_top_ = CASIO_INFO_TOP;
            }
            else {
                boxWidth_ = CASIO_BOX_WIDTH_H;

                playfield_left_ = CASIO_PLAYFIELD_BORDER + CASIO_BORDER_GAP;
                playfield_top_ = CASIO_PLAYFIELD_BORDER + CASIO_BORDER_GAP;

                NP_boxWidth_ = CASIO_BOX_WIDTH_NP_H;
                NP_width_ = 4 * NP_boxWidth_ + 2 * CASIO_INFO_GAP;

                NP_left_ = CASIO_HEIGHT -1 * CASIO_PLAYFIELD_BORDER - NP_width_;
                NP_top_ = CASIO_PLAYFIELD_BORDER;
            }
        }

        // (anticlockwise) Rotation for vertical drawings
        void rotate(uint16_t& x, uint16_t& y){
            uint16_t ny(CASIO_HEIGHT - x);
            x = y;
            y = ny;
        }

        // Members
        //
        uint8_t     boxWidth_, NP_boxWidth_;     // Width of a box
        uint16_t    playfield_left_, playfield_top_;

        uint16_t    NP_left_, NP_top_;          // Next piece preview
        uint16_t    NP_width_;
};

#endif // __J_TETRIS_CASIO_h__

// EOF