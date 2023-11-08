//---------------------------------------------------------------------------
//--
//--	File	: tabs.h
//--
//--	Author	: Jérôme Henry-Barnaudière - GeeHB
//--
//--	Project	: jtetris - cpp version
//--
//---------------------------------------------------------------------------
//--
//--	Description:
//--
//--			Definition of tetrisTab
//--
//---------------------------------------------------------------------------

#ifndef __J_TETRIS_CASIO_TETRIS_TAB_h__
#define __J_TETRIS_CASIO_TETRIS_TAB_h__    1

#include "tabs.h"

#ifdef __cplusplus
extern "C" {
#endif // #ifdef __cplusplus


//---------------------------------------------------------------------------
//--
//-- tetrisTab - Where the game is
//--
//---------------------------------------------------------------------------

class tetrisTab : public tab{
public:
    // Construction
    tetrisTab(const char* tname)
    :tab(tname, ACTION_NONE){
        params_ = NULL;     // No parameters
    }

    // Parameters
    void setParameters(tetrisParameters* params){
        params_ = params;
    }

    // The current tab is selected => let's play
    void select(TAB_STATUS& status);

    // Show best scores
    static void showScores(){
        _showScores();
    }

private:
    // Show best scores and current one (if in the list)
    static void _showScores(int32_t current = -1){}

private:
    // Members
    tetrisParameters* params_;
};

#ifdef __cplusplus
}
#endif // #ifdef __cplusplus

#endif // __J_TETRIS_CASIO_TETRIS_TAB_h__

// EOF
