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
//--			Implementation of tetrisTab - The tetris Game
//--
//---------------------------------------------------------------------------

#include "tetrisTab.h"
#include "tetrisGame.h"

// The current tab is selected => let's play
//
void tetrisTab::select(TAB_STATUS& status){

    if (params_){
        tetrisGame game(params_);
        if (game.start()){
            _showScores(game.score());  // Show final score
        }

        // Ready for a new game !
        status.action = ACTION_REDRAW_TABS;
        status.exitKey = KEY_NONE;
    }
    else{
        // No parameters => no game
        status.action = ACTION_NONE;
        status.exitKey = KEY_CODE_F1;       // return to main screen
    }
}

// EOF
