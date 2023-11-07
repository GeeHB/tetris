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
#define CASIO_BOX_WIDTH_NP_ROTATED  7

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

#define CASIO_VERT_TEXT_OFFSET  15

//---------------------------------------------------------------------------
//--
//-- casioFX-CG50 object
//--
//--    Coordinates, dimensions for the casio fx-CG50 calculator
//--
//---------------------------------------------------------------------------

class casioFXCG50{

    // Public methods
    //
    public:
        // Construction
        casioFXCG50();

        // Update members on rotation
        void rotatedDisplay(bool doRotate);

        // (trigonometric) rotations
        //  ... of a single point
        void rotate(int16_t& x, int16_t& y){
            int16_t ny(CASIO_HEIGHT - x);
            x = y;
            y = ny;
        }

        // ... of a rect
        void rotate(int16_t& xFrom, int16_t& yFrom, int16_t& xTo, int16_t& yTo){
            rotate(xFrom, yFrom);
            rotate(xTo, yTo);

            // The rect (xFrom, yFrom) -> (xTo, yTo)
            // turns and becomes (xTo, yFrom) -> (xFrom, yTo)
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

#ifdef DEST_CASIO_FXCG50
        font_t     *hFont_, *vFont_;     // Fonts
#endif //#ifdef DEST_CASIO_FXCG50
};

#ifdef __cplusplus
}
#endif // #ifdef __cplusplus

#endif // __J_TETRIS_CASIO_FXCG50_h__

// EOF
