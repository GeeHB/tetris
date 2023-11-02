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


#include "tetrisTabs.h"
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
    bool useApp(true);
    tabManager tmanager;

    // create tabs
    tab tabExit(TAB_QUIT, ACTION_QUIT);

    // add tabs ...
    tmanager.add(&tabExit, 5);

    tmanager.update();

    // Handle options
    char car(0);
    int8_t sel(0);
    int action;
    do{
#ifdef DEST_CASIO_FXCG50
        key_event_t evt = pollevent();
        if (evt.type == KEYEV_DOWN){
            car = evt.key;
        }
        else{
            car = 0;;
        }
    #else
        car = getchar();
    #endif // #ifdef DEST_CASIO_FXCG50

        if (car >= KEY_CODE_F1 && car <= (KEY_CODE_F1 + TAB_COUNT -1)){
            sel = car - KEY_CODE_F1;    // "F" key index

            // Update drawings and give control to tab
            action = tmanager.select(sel);

            // End ?
            useApp = (action != ACTION_QUIT);
        }
    } while (useApp);


	// Launch the game
	//tetrisGame game(params);
    	//game.start();

#ifdef DEST_CASIO_FXCG50
    gint_setrestart(1);
#endif // #ifdef DEST_CASIO_FXCG50

    // Finished
    return 1;
}

// EOF
