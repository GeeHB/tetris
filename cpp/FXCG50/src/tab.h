//---------------------------------------------------------------------------
//--
//--	File	: tab.h
//--
//--	Author	: Jérôme Henry-Barnaudière - GeeHB
//--
//--	Project	: jtetris - cpp version
//--
//---------------------------------------------------------------------------
//--
//--	Description:
//--
//--			Definition of tab object
//--
//---------------------------------------------------------------------------

#ifndef __J_TETRIS_CASIO_TAB_h__
#define __J_TETRIS_CASIO_TAB_h__    1

#include "consts.h"

#ifdef __cplusplus
extern "C" {
#endif // #ifdef __cplusplus

//---------------------------------------------------------------------------
//--
//-- Constants
//--
//---------------------------------------------------------------------------

#define TAB_HEIGHT      10      # in pixels

#define TAB_NAME_LEN    10      # max char

//---------------------------------------------------------------------------
//--
//-- tab object
//--
//---------------------------------------------------------------------------

class tab{
public:
    // ctor and dtor
    tab(const char* tname){
        // Copy (and truncate) name
        size_t len(strlen(tname));
        if (len>TAB_NAME_LEN){
            len = TAB_NAME_LEN;
        }
        strncpy(tname, name_, len);
        name_[len] = 0;
    }
    virtual ~tab();

    // Draw.
    virtual void draw(int16_t cornerX, int16_t cornerY, bool selected = false);

    // access
    const char* name(){
        return name_;
    }
protected:
    // Members
    char    name_[TAB_NAME_LEN + 1];
};

#ifdef __cplusplus
}
#endif // #ifdef __cplusplus

#endif // __J_TETRIS_CASIO_TAB_h__

// EOF
