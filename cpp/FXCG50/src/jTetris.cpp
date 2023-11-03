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

#include "tabs.h"
#include "tetrisGame.h"

#ifdef DEST_CASIO_FXCG50
#include <gint/gint.h>
#endif // #ifdef DEST_CASIO_FXCG50

// Program entry point
//
int main(){
    // Get parameters
    tetrisParameters params;

    tabManager tmanager;
    tmanager.clearScreen();

    // Create tabs
    tabValue tabAbout(TAB_ABOUT), tabLines(TAB_LINES);
    tab tabExit(TAB_QUIT, ACTION_QUIT);

    // add tabs ...
    tmanager.add(&tabAbout);    // should be 0 !
    tmanager.add(&tabLines);
    tmanager.add(&tabExit, 5);

    // Handle options
    bool useApp(true);
    uint car(0);
    int8_t sel(0);
    uint8_t action(ACTION_NONE);
#ifdef DEST_CASIO_FXCG50
    key_event_t evt;
#endif // #ifdef DEST_CASIO_FXCG50
    do{
#ifdef DEST_CASIO_FXCG50
        evt = pollevent();
        if (evt.type == KEYEV_DOWN){
            car = evt.key;

            drect(10, 10, 180, 30, C_WHITE);
            dprint(10, 10, C_BLACK, "code : %d", car);
            dupdate();
        }
        else{
            car = 0;
        }
#else
        car = getchar();
#endif // #ifdef DEST_CASIO_FXCG50

        if (car >= KEY_CODE_F1 && car <= KEY_CODE_F6){
            sel = car - KEY_CODE_F1;    // "F" key index

            // Update drawings
            action = tmanager.select(sel);

            // Specifics actions
            if (ACTION_OWNACTION == action){
                switch (sel){
                    // Launch the game
                    case 4 :
                    {
                        tetrisGame game(params);
                        game.start();
                        break;
                    }

                    default:
                        break;
                }
            }
            else{
                // End ?
                useApp = (action != ACTION_QUIT);
            }
        }else{
            if (KEY_CODE_QUIT == car){
                useApp = false;
            }
        }
    } while (useApp);

    // Free memory
#ifdef DEST_CASIO_FXCG50
    gint_setrestart(1);
#endif // #ifdef DEST_CASIO_FXCG50

    // Finished
    return 1;
}

// EOF
