//---------------------------------------------------------------------------
//--
//--	File	: tabs.cpp
//--
//--	Author	: Jérôme Henry-Barnaudière - GeeHB
//--
//--	Project	: jtetris - cpp version
//--
//---------------------------------------------------------------------------
//--
//--	Description:
//--
//--			Implementation of tabManager and tab objects
//--
//---------------------------------------------------------------------------

#include "tabs.h"

//---------------------------------------------------------------------------
//--
//-- Constants
//--
//---------------------------------------------------------------------------


//---------------------------------------------------------------------------
//--
//-- tab object - A simple basic tab - abstract class
//--
//---------------------------------------------------------------------------

// Construction
//
tab::tab(uint8_t ID, const char* tname, uint8_t height = TAB_HEIGHT){
    // Tab pos
    rect_.x =   ID * TAB_WIDTH;
    rect_. y = CASIO_HEIGHT - height - 1;
    rect_.w = TAB_WIDTH;
    rect_.h = height;

    // Copy (and truncate) name
    size_t len(strlen(tname));
    if (len>TAB_NAME_LEN){
        len = TAB_NAME_LEN;
    }
    strncpy(name_, tname, len);
    name_[len] = 0;
}

// Dimensions & position
//
void tab::getRect(RECT& position){
    position.x = rect_.x;
    position.y = rect_.y;
    position.w = rect_.w;
    position.h = rect_.h;
}


// Draw a single tab
//
void tab::draw(const RECT* position, bool selected, const char* name = NULL){
#ifdef DEST_CASIO_FXCG50
    // Draw back ground

    // frame

    // text

#endif // #ifdef DEST_CASIO_FXCG50
}



//
// tabManager - Manages the 6 possibles tabs
//

    // Constructor
    tabManager();

    // Destructor
    ~tabManager(){}

    // Add a tab
    bool add(const tab* ptab);

    // Set active tab
    void select(int8_t ID);

    // Private methods
    int8_t _find(const tab* ptab);

    // Members
    tab*    tabs_[TAB_COUNT];

// EOF
