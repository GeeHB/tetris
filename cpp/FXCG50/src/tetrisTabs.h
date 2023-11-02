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

#include "tabs.h"

#ifdef __cplusplus
extern "C" {
#endif // #ifdef __cplusplus

//---------------------------------------------------------------------------
//--
//-- Constants
//--
//---------------------------------------------------------------------------

// Tab names
#define TAB_ABOUT   "Tetris"
#define TAB_LINES   "Lines"
#define TAB_LEVEL   "Level"
#define TAB_SHADOW  "Shadow"
#define TAB_PLAY    "Play"
#define TAB_QUIT    "Exit"

//---------------------------------------------------------------------------
//--
//-- tabButton object : Initiate an action
//--
//---------------------------------------------------------------------------

class tabButton : public tab{
public:
    // Construction
    tabButton(uint8_t ID, const char* tname, int action = ACTION_NONE, uint8_t height = TAB_HEIGHT)
    :tab(ID, tname, height){
        action_ = action;
    }

    // Destruction
    ~tabButton(){}

    // Activate
    int activate(bool setActivate = true){
        // Ok
        return action_;
    }

protected:
    // Members
    int     action_;        // What todo when pressed ?
};

#ifdef __cplusplus
}
#endif // #ifdef __cplusplus

#endif // __J_TETRIS_TABS_h__

// EOF

