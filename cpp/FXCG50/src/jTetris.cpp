//---------------------------------------------------------------------------
//--
//--	File	: jTetris.cpp
//--
//--	Author	: Jérôme Henry-Barnaudière - GeeHB
//--
//--	Project	: jtetris / cpp version
//--
//---------------------------------------------------------------------------
//--
//--	Description:
//--
//--	    Entry point
//--
//---------------------------------------------------------------------------


#include "splashScreen.h"
#include "tetrisGame.h"

int main()
{
    // Get parameters
    tetrisParameters params;

    /*
    splashScreen splash;
    if (false == splash.choose(params)){
        // Canceled
        return 1;
    }
    */

	// Launch the game
	tetrisGame game(params);
    game.start();

    /*
    tetrisGame* game = new tetrisGame(params);
	if (game){
	    game->start();
        delete game;
    }
    */
    // Finished
    return 1;
}

// EOF
