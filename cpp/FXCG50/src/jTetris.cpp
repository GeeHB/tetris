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

#ifdef DEST_CASIO_FXCG50
#include <gint/gint.h>
#endif // #ifdef DEST_CASIO_FXCG50

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

#ifdef DEST_CASIO_FXCG50
    gint_setrestart(1);
#endif // #ifdef DEST_CASIO_FXCG50

    // Finished
    return 1;
}

// EOF
