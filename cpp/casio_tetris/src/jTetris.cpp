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

#ifndef DEST_CASIO_FXCG50
#include <iostream>
using namespace std;
#endif // #ifndef DEST_CASIO_FXCG50

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
    game.end();

    // Finished
    return 0;
}

// EOF
