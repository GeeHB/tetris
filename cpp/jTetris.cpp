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

#include <iostream>
using namespace std;

#include "../tetrisGame.h"

forward parametersScreen;

int main()
{
    // Get parameters
    //
    tetrisParameters params;
    parametersScreen splash(params);
    if (false == splash.choose()){
        // Canceled
        return 1;
    }

	// Launch the game
	tetrisGame game;
	game.setParameters(params);

	game.start();
    game.end();

    // Finished
    return 0;
}

// EOF
