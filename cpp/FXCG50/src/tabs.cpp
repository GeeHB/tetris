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

#define COLOUR_SELECTED     COLOUR_BLUE
#define COLOUR_UNSELECTED   COLOUR_GREY

//---------------------------------------------------------------------------
//--
//-- tab object - A simple basic tab - abstract class
//--
//---------------------------------------------------------------------------

// Construction
//
tab::tab(const char* tname, int action){

    action_ = action;

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

void tab::setRect(RECT& rect){
    rect_.x =  rect.x;
    rect_. y = rect.y;
    rect_.w = rect.w;
    rect_.h = rect.h;
}

// Draw a single tab
//
void tab::draw(const RECT* anchor, bool selected, const char* name){
#ifdef DEST_CASIO_FXCG50
    // Draw back ground
    drect(anchor->x, anchor->y, anchor->x + anchor->w - 1, anchor->y + anchor->h - 1, C_WHITE);

    // Text
    if (name){
        int x,y, w, h;
        dsize(name, NULL, &w, &h);

        // center text
        x = anchor->x + (anchor->w - w) / 2;
        y = anchor->y + (anchor->h - h) / 2;

        // text too large ?

        // draw the text
        dtext(x, y, selected?COLOUR_SELECTED:COLOUR_UNSELECTED, name);
    }

    // frame
    if (selected){
        dline(anchor->x, anchor->y, anchor->x, anchor->y + anchor->h - 2, C_BLACK); // Left
        dline(anchor->x+1, anchor->y + anchor->h - 1, anchor->x + anchor->w -1 - TAB_ROUNDED_DIM, anchor->y + anchor->h - 1, C_BLACK);  // bottom
        dline(anchor->x + anchor->w -1 - TAB_ROUNDED_DIM, anchor->y + anchor->h - 1, anchor->x + anchor->w - 1, anchor->y + anchor->h - 1 - TAB_ROUNDED_DIM, C_BLACK);  // bottom
        dline(anchor->x + anchor->w - 1, anchor->y, anchor->x + anchor->w - 1, anchor->y + anchor->h - 1 - TAB_ROUNDED_DIM, C_BLACK);   // right
    }
    else{
        dline(anchor->x, anchor->y, anchor->x + anchor->w -1, anchor->y, C_BLACK);
    }
#endif // #ifdef DEST_CASIO_FXCG50
}



//
// tabManager - Manages the 6 possibles tabs
//

// Constructor
//
tabManager::tabManager(){
    // Initialize members
    memset(tabs_, 0, sizeof(tabs_));
    active_ = -1;
}

// Add a tab
//
bool tabManager::add(tab* ptab, int8_t ID){
    if (!ptab || ID >= TAB_COUNT || -1 != _find(ptab)){
        return false;
    }

    int8_t index = ((ID==-1)?_findFreeID():ID);
    if (-1 == index){
        return false;   // no free place
    }

    // Add the new tab
    tabs_[index] = ptab;

    // set its position
    RECT pos;
    _ID2Rect(index, pos);
    ptab->setRect(pos);

    // Automatically select the first added tab.
    if (-1 == active_){
        select(index);
    }

    // Ok
    update();
    return true;
}

// Set active tab
//
uint8_t tabManager::select(int8_t ID){
    // Valid and different
    bool valid(false);
    if (ID != active_ && ID < TAB_COUNT && tabs_[ID]){
        // Unselect
        _select(active_, false);

        // Select
        _select(ID, true);

        valid = true;
        active_ = ID;

#ifdef DEST_CASIO_FXCG50
        dupdate();
#endif // DEST_CASIO_FXCG50
    }

    // "action" of the tab
    return (valid ? tabs_[ID]->action():(uint8_t)ACTION_NONE);
}

// Redraw all tabs
//
void tabManager::update(){
    tab* ptab;
    RECT anchor;
    for (uint8_t index(0); index < TAB_COUNT; index++){
        ptab = tabs_[index];
        if (ptab){
            ptab->draw(index == active_);
        }
        else{
            _ID2Rect(index, anchor);
            tab::draw(&anchor, index==active_);
        }
    }
#ifdef DEST_CASIO_FXCG50
    dupdate();
#endif // DEST_CASIO_FXCG50
}

// Set a tab position
//
void tabManager::_ID2Rect(uint8_t ID, RECT& rect){
    if (ID < TAB_COUNT){
        rect.x = ID * TAB_WIDTH;
        rect. y = CASIO_HEIGHT - TAB_HEIGHT;
        rect.w = TAB_WIDTH;
        rect.h = TAB_HEIGHT;
    }
}

// Search the current tab.
//
int8_t tabManager::_find(const tab* ptab){
    if (!ptab){
        return -1;
    }

    for (uint index(0); index < TAB_COUNT; index++){
        if (tabs_[index] == ptab){
            return index;   // found
        }
    }

    // Not found
    return -1;
}

// Search first free place
//
int8_t tabManager::_findFreeID(){
    uint index(0);
    while (tabs_[index] && index < TAB_COUNT){
        index++;
    }

    // ID of first free place or -1
    return (index>=TAB_COUNT)?-1:index;
}

// (de)activate a tab
//
void tabManager::_select(int8_t ID, bool activate){
    if (-1 != ID){
        tab* ptab = tabs_[ID];

        if (ptab){
            ptab->draw(activate);
        }
        else{
            RECT rect;
            _ID2Rect(ID, rect);
            tab::draw(&rect, activate);
        }
    }
}

// EOF
