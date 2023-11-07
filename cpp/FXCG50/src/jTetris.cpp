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
    tab::clearScreen();

    // Create tabs
    tabValue tabAbout(TAB_ABOUT), tabShadow(TAB_SHADOW, ACTION_OWNACTION);

    tabRangedValue tabLevel(TAB_LEVEL, MIN_LEVEL, MAX_LEVEL);
    TAB_VALUE level;
    level.uVal = params.startLevel_;
    tabLevel.setValue(level);
    tabLevel.setComment(TAB_LEVEL_STR);

    TAB_VALUE shadow;
    shadow.bVal = params.shadow_;
    tabShadow.setValue(shadow);
    tabShadow.setComment(params.shadow_?TAB_SHADOW_ON_STR:TAB_SHADOW_OFF_STR);

    tab tabExit(TAB_QUIT, ACTION_QUIT);

    // add tabs ...
    tmanager.add(&tabAbout);    // should be 0 !
    tmanager.add(&tabShadow);
    tmanager.add(&tabExit, 5);

    // Handle options
    bool useApp(true), readKey(true);
    uint car(0);
    int8_t sel(0);
    uint8_t action(ACTION_NONE);
#ifdef DEST_CASIO_FXCG50
    key_event_t evt;
#endif // #ifdef DEST_CASIO_FXCG50
    do{
        if (readKey){
#ifdef DEST_CASIO_FXCG50
            evt = pollevent();
            if (evt.type == KEYEV_DOWN){
                car = evt.key;
            }
            else{
                car = 0;    // ie. no char ...
            }
#else
            car = getchar();
#endif // #ifdef DEST_CASIO_FXCG50
        }
        else{
            readKey = true; // Next time read keyboard state
        }

        if (car >= KEY_CODE_F1 && car <= KEY_CODE_F6){
            sel = car - KEY_CODE_F1;    // "F" key index

            // Update drawings
            action = tmanager.select(sel);

            // Specifics actions
            if (ACTION_OWNACTION == action){
                switch (sel){
                    // Level
                    case 1:
                        car = tabLevel.changeValue();
                        readKey = (car == 0);   // Need to get the next key ?

                        // Uodate parameter
                        tabLevel.value(level);
                        params.startLevel_ = level.uVal;
                        break;

                    // A shadow ?
                    case 2:
                        // change value
                        shadow.bVal = (params.shadow_ = !params.shadow_);
                        tabShadow.setValue(shadow);
                        tabShadow.setComment(params.shadow_?TAB_SHADOW_ON_STR:TAB_SHADOW_OFF_STR);

                        // update
                        tabShadow.updateComment();

                        break;

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
            // The "Exit" key
            if (KEY_CODE_EXIT == car){
                useApp = false;
            }
        }
    } while (useApp);

    // Return to default state
    tmanager.select(0);

    // Free memory
#ifdef DEST_CASIO_FXCG50
    gint_setrestart(1);
#endif // #ifdef DEST_CASIO_FXCG50

    // Finished
    return 1;
}

// EOF
