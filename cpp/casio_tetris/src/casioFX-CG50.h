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

#include "consts.h"

#ifdef __cplusplus
extern "C" {
#endif // #ifdef __cplusplus

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
#define CASIO_BOX_WIDTH           9
#define CASIO_BOX_WIDTH_ROTATED   14

#define CASIO_BOX_WIDTH_NP          CASIO_BOX_WIDTH    // next piece preview
#define CASIO_BOX_WIDTH_NP_ROTATED  8

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

            rotatedDisplay_ = false;

            // Default keys
            keyFall_ = KEY_CODE_FALL;
            keyPause_ = KEY_CODE_PAUSE;
            keyRotateDisplay_ = KEY_CODE_ROTATE_DISPLAY;
            keyQuit_ = KEY_CODE_QUIT;

            // set parameters
            rotatedDisplay(rotatedDisplay_);
        }

        // Rotate ?
        void rotatedDisplay(bool doRotate){
            if (false == (rotatedDisplay_ = doRotate)){
                boxWidth_ = CASIO_BOX_WIDTH;

                playfield_pos_.x = CASIO_PLAYFIELD_LEFT + CASIO_PLAYFIELD_BORDER + CASIO_BORDER_GAP;
                playfield_pos_.y = CASIO_PLAYFIELD_BORDER + CASIO_BORDER_GAP;

                playfield_width = PLAYFIELD_WIDTH * boxWidth_ + 2 * CASIO_BORDER_GAP;
                playfield_height = PLAYFIELD_HEIGHT * boxWidth_ + 2 * CASIO_BORDER_GAP;

                NP_boxWidth_ = CASIO_BOX_WIDTH_NP;
                NP_width_ = 4 * NP_boxWidth_ + 2 * CASIO_INFO_GAP;

                NP_pos_.x = CASIO_INFO_LEFT + CASIO_INFO_GAP;
                if (NP_pos_.x <= (playfield_pos_.x + playfield_width)){
                    NP_pos_.x = playfield_pos_.x + playfield_width + 2 * CASIO_INFO_GAP;
                }

                NP_pos_.y = CASIO_INFO_TOP;

                // Values indicators
                textsPos_[0].x = textsPos_[1].x = textsPos_[2].x = NP_pos_.x;
                for (uint8_t id(0); id <VAL_COUNT; id++){
                    textsPos_[id].y = NP_pos_.y + NP_width_ + boxWidth_ * ( 2 * id + 1);
                }

                // Keys
                keyLeft_ = KEY_CODE_LEFT;
                keyRight_ = KEY_CODE_RIGHT;
                keyRotatePiece_ = KEY_CODE_UP;
                keyDown_ = KEY_CODE_DOWN;
            }
            else {
                // "rotated" mode
                //
                boxWidth_ = CASIO_BOX_WIDTH_ROTATED;    // Larger box

                playfield_pos_.x = CASIO_PLAYFIELD_BORDER + CASIO_BORDER_GAP;
                playfield_pos_.y = CASIO_PLAYFIELD_BORDER + CASIO_BORDER_GAP;

                playfield_width = PLAYFIELD_WIDTH * boxWidth_ + 2 * CASIO_BORDER_GAP;
                playfield_height = PLAYFIELD_HEIGHT * boxWidth_ + 2 * CASIO_BORDER_GAP;

                NP_boxWidth_ = CASIO_BOX_WIDTH_NP_ROTATED;  // ... but preview is smaller
                NP_width_ = 4 * NP_boxWidth_ + 2 * CASIO_INFO_GAP;

                //NP_pos_.x = CASIO_HEIGHT -2 * CASIO_PLAYFIELD_BORDER - NP_width_;
                NP_pos_.x = playfield_pos_.x + playfield_width + 3 * CASIO_BORDER_GAP;
                NP_pos_.y = CASIO_INFO_TOP;

                // Keys
                keyLeft_ = KEY_CODE_DOWN;
                keyRight_ = KEY_CODE_UP;
                keyRotatePiece_ = KEY_CODE_LEFT;
                keyDown_ = KEY_CODE_RIGHT;
            }
        }

        // (anticlockwise) Rotations for vertical drawings
        //  for a single point
        void rotate(int16_t& x, int16_t& y){
            int16_t ny(CASIO_HEIGHT - x);
            x = y;
            y = ny;
        }

        // a rect
        void rotate(int16_t& xFrom, int16_t& yFrom, int16_t& xTo, int16_t& yTo){
            rotate(xFrom, yFrom);
            rotate(xTo, yTo);

            // The rect (xFrom, yFrom) -> (xTo, yTo)
            // turns and becomes (xTo, yFrom, xFrom, yTo)
            int16_t oFrom(xFrom);
            xFrom = xTo;
            xTo = oFrom;
        }

        //
        // Members
        //

        // Screen & display parameters
        bool        rotatedDisplay_;    // Rotate all displays (default = False) ?
        uint8_t     boxWidth_;
        POINT       playfield_pos_;
        uint16_t    playfield_width, playfield_height;

        // Next piece
        POINT       NP_pos_;
        uint16_t    NP_width_, NP_boxWidth_;

        // Texts
        POINT       textsPos_[VAL_COUNT];      // Positions of texts

        // Keyboard
        char        keyLeft_, keyRight_, keyRotatePiece_, keyDown_, keyFall_;
        char        keyPause_, keyRotateDisplay_;
        char        keyQuit_;
};

#ifdef __cplusplus
}
#endif // #ifdef __cplusplus

#endif // __J_TETRIS_CASIO_FXCG50_h__

// EOF
