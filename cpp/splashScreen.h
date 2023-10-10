//---------------------------------------------------------------------------
//--
//--	File	: splashScreen.h
//--
//--	Author	: Jérôme Henry-Barnaudière - GeeHB
//--
//--	Project	: jtetris - cpp version
//--
//---------------------------------------------------------------------------
//--
//--	Description:
//--
//--			Definition of splashScreen object - Game params & launching
//--
//---------------------------------------------------------------------------

#ifndef __J_TETRIS_SPLASH_h__
#define __J_TETRIS_SPLASH_h__    1

#include "consts.h"

//---------------------------------------------------------------------------
//--
//-- Constants
//--
//---------------------------------------------------------------------------


//---------------------------------------------------------------------------
//--
//-- splashScreen object
//--
//--    Game pres. + games parameters
//--
//---------------------------------------------------------------------------

class splashScreen{

    // Public methods
    //
    public:

        // Construction
        splashScreen(){}

        // Set / change parameters
        bool choose(tetrisParameters& params){
            return true;
        }
};

#endif // __J_TETRIS_SPLASH_h__

// EOF
