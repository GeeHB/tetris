//---------------------------------------------------------------------------
//--
//--	File	: tetrisTabs.h
//--
//--	Author	: Jérôme Henry-Barnaudière - GeeHB
//--
//--	Project	: jtetris - cpp version
//--
//---------------------------------------------------------------------------
//--
//--	Description:
//--
//--			Definition of tabs objects
//--
//---------------------------------------------------------------------------

#ifndef __J_TETRIS_TABS_h__
#define __J_TETRIS_TABS_h__    1

#include "tab.h"

#ifdef __cplusplus
extern "C" {
#endif // #ifdef __cplusplus

//---------------------------------------------------------------------------
//--
//-- Constants
//--
//---------------------------------------------------------------------------

// Tab names
TAB_ABOUT   "Tetris"
TAB_LINES   "Lines"
TAB_LEVEL   "Level"
TAB_SHADOW  "Shadow"
TAB_QUIT    "Exit"

//---------------------------------------------------------------------------
//--
//-- tab object - abstract class
//--
//---------------------------------------------------------------------------

class tab{
public:
    // Construction
    tab(uint8_t ID, const char* tname, uint_8 height = TAB_HEIGHT){
        // Tab pos
        rect_.x =   ID * TAB_WIDTH;
        rect_. y = CASIO_HEIGHT - height - 1;
        rect_.w = TAB_WIDTH;
        rect_.h = height,

        // Copy (and truncate) name
        size_t len(strlen(tname));
        if (len>TAB_NAME_LEN){
            len = TAB_NAME_LEN;
        }
        strncpy(tname, name_, len);
        name_[len] = 0;
    }

    // Destruction
    virtual ~tab();

    // Draw.
    virtual void draw(bool selected = false){
        _drawTabName(selected);
    }

    // Access
    const char* name(){
        return name_;
    }

    // Value
    void setValue(TAB_VALUE& val){
        // Any ...
        val_.iVal = val.iVal;
    }
    void value(TAB_VALUE& val){
        val.iVal = val_.iVal;
    }

    // "private" methods
protected:
    void _drawTabName(bool selected);
    void _clearScreen(){
#ifdef DEST_CASIO_FXCG50
        drec(0, 0, CASIO_WIDTH - 1, CASIO_HEIGHT - rect_.h - 1, C_WHITE)
#endif // #ifdef DEST_CASIO_FXCG50
    }

protected:
    // Members
    char        name_[TAB_NAME_LEN + 1];
    RECT        rect_;
    TAB_VALUE   val_;
};

#ifdef __cplusplus
}
#endif // #ifdef __cplusplus

#endif // __J_TETRIS_TABS_h__

// EOF

