//---------------------------------------------------------------------------
//--
//--	File	: casioFX-CG50.h
//--
//--	Author	: Jérôme Henry-Barnaudière - GeeHB
//--
//--	Project	: jtetris - cpp version
//--
//---------------------------------------------------------------------------
//--
//--	Description:
//--
//--			Definition of casioFXCG50 object and consts for casio fx-CG50
//--
//---------------------------------------------------------------------------

#ifndef __J_TETRIS_CASIO_FXCG50_h__
#define __J_TETRIS_CASIO_FXCG50_h__    1

#ifdef __cplusplus
extern "C" {
#endif // #ifdef __cplucplus

#include "consts.h"

//---------------------------------------------------------------------------
//--
//-- Constants
//--
//---------------------------------------------------------------------------

// Screen dimensions in pixels
//
#ifdef DEST_CASIO_FXCG50
#define CASIO_WIDTH     DWIDTH
#define CASIO_HEIGHT    DHEIGHT
#else
#define CASIO_WIDTH     384
#define CASIO_HEIGHT    192
#endif // #ifdef DEST_CASIO_FXCG50

// Box dimensions in pixels
//
#define CASIO_BOX_WIDTH_V   9       // playfield
#define CASIO_BOX_WIDTH_H   14

#define CASIO_BOX_WIDTH_NP_V   CASIO_BOX_WIDTH_V    // next piece preview
#define CASIO_BOX_WIDTH_NP_H   8

// Playfield pos & dims
//
#define CASIO_PLAYFIELD_LEFT    100
#define CASIO_PLAYFIELD_BORDER  3
#define CASIO_BORDER_GAP        2

// Texts pos & dims
//
#define CASIO_INFO_LEFT     250
#define CASIO_INFO_TOP      10
#define CASIO_INFO_GAP      4       // between border and text

//---------------------------------------------------------------------------
//--
//-- casioFX-CG50 object
//--
//--    coordinates, dimensions for the casio fx-CG50 calculator
//--
//---------------------------------------------------------------------------

class casioFXCG50{

    // Public methods
    //
    public:
        // Construction
        casioFXCG50(){

            vert_ = true;

            // Default keys
            keyLeft_ = KEY_CODE_LEFT;
            keyRight_ = KEY_CODE_RIGHT;
            keyRotate_ = KEY_CODE_UP;
            keyDown_ = KEY_CODE_DOWN;
            keyFall_ = KEY_CODE_FALL;
            keyQuit_ = KEY_CODE_QUIT;
        }

        // Vertical ?
        void setVert(bool vert = true){
            vert_ = vert;
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
                // Horizontal mode
                //
                boxWidth_ = CASIO_BOX_WIDTH_H;

                playfield_left_ = CASIO_PLAYFIELD_BORDER + CASIO_BORDER_GAP;
                playfield_top_ = CASIO_PLAYFIELD_BORDER + CASIO_BORDER_GAP;

                NP_boxWidth_ = CASIO_BOX_WIDTH_NP_H;
                NP_width_ = 4 * NP_boxWidth_ + 2 * CASIO_INFO_GAP;

                NP_left_ = CASIO_HEIGHT -1 * CASIO_PLAYFIELD_BORDER - NP_width_;
                NP_top_ = CASIO_PLAYFIELD_BORDER;

                // Rotation of the keyboard
                keyLeft_ = KEY_CODE_UP;
                keyRight_ = KEY_CODE_DOWN;
                keyRotate_ = KEY_CODE_RIGHT;
                keyDown_ = KEY_CODE_LEFT;
            }
        }

        // (anticlockwise) Rotation for vertical drawings
        void rotate(uint16_t& x, uint16_t& y){
            uint16_t ny(CASIO_HEIGHT - x);
            x = y;
            y = ny;
        }

        //
        // Members
        //

        // Screen & display parameters
        //
        bool        vert_;                      // Vertical drawing (default) ?
        uint8_t     boxWidth_, NP_boxWidth_;    // Width of a box
        uint16_t    playfield_left_, playfield_top_;

        uint16_t    NP_left_, NP_top_;          // Next piece preview
        uint16_t    NP_width_;

        // Keyboard
        //
        char        keyLeft_, keyRight_, keyRotate_, keyDown_, keyFall_;
        char        keyQuit_;
};

#ifdef __cplusplus
}
#endif // #ifdef __cplucplus

#endif // __J_TETRIS_CASIO_FXCG50_h__

// EOF
