//---------------------------------------------------------------------------
//--
//--	File	: templates.h
//--
//--	Author	: Jérôme Henry-Barnaudière - GeeHB
//--
//--	Project	: jtetris - cpp version
//--
//---------------------------------------------------------------------------
//--
//--	Descritpion:
//--
//--                 Definition of the 7 tetraminos templates
//--
//--                 The num. value is the colour ID. Colours'IDs are based on nCurses index
//--
//--                 A piece is given with all its postions after rotations in trignometric direction
//--                 Each "rotation", to be precise, is a combination of a rotation and a translation
//--
//--                 Based on Nintendo for pieces and rotation.
//--
//---------------------------------------------------------------------------

#ifndef __J_TETRIS_PIECE_TEMPLATE_h__
#define __J_TETRIS_PIECE_TEMPLATE_h__    1

#ifdef __cplusplus
extern "C" {
#endif // #ifdef __cplusplus

// Different pieces and their rotations
//

#define TETRAMINOS_COUNT    7

// "S" tetramino x 2 - green
#define S_0     ".2.."\
                ".22."\
                "..2."\
                "...."

#define S_1     "...."\
                ".22."\
                "22.."\
                "..."

// "Z" x 2 - red
#define Z_0     "..1."\
                ".11."\
                ".1.."\
                "....'"

#define Z_1     "...."\
                "11.."\
                ".11."\
                "...."

// "I" x 2 - Cyan
#define I_0     "..6."\
                "..6."\
                "..6."\
                "..6."

#define I_1     "...."\
                "...."\
                "6666"\
                "...."

// "O" x 1 - Yellow
#define O_0     "...."\
                ".33."\
                ".33."\
                "...."

// "L"  x 4 - Orange
#define L_0     "77.."\
                ".7.."\
                ".7.."\
                "...."

#define L_1     "...."\
                "777."\
                "7..."\
                "...."

#define L_2     ".7.."\
                ".7.."\
                ".77."\
                "...."

#define L_3     "..7."\
                "777."\
                "...."\
                "...."

// "J" x 4 -  Blue
#define J_0     ".4.."\
                ".4.."\
                "44.."\
                "...."

#define J_1     "...."\
                "444."\
                "..4."\
                "...."

#define J_2     ".44."\
                ".4.."\
                ".4.."\
                "...."

#define J_3     "4..."\
                "444."\
                "...."\
                "...."

// "T" x 4 - Violet
#define T_0     ".5.."\
                "55.."\
                ".5.."\
                "...."

#define T_1     "...."\
                "555."\
                ".5.."\
                "...."

#define T_2     ".5.."\
                ".55."\
                ".5.."\
                "...."

#define T_3     ".5.."\
                "555."\
                "...."\
                "...."

#ifdef __cplusplus
}
#endif // #ifdef __cplusplus


#endif // __J_TETRIS_PIECE_TEMPLATE_h__

// EOF
