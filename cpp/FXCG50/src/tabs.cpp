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
//--
//--
//---------------------------------------------------------------------------

// Fonts
#ifdef DEST_CASIO_FXCG50
extern font_t font_horz;
#endif // #ifdef DEST_CASIO_FXCG50

//---------------------------------------------------------------------------
//--
//-- Constants
//--
//---------------------------------------------------------------------------

#define COLOUR_SELECTED     COLOUR_BLUE
#define COLOUR_UNSELECTED   COLOUR_GREY
#define COLOUR_BK_HILITE    COLOUR_LT_BLUE

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
    drect(anchor->x, anchor->y, anchor->x + anchor->w - 1, anchor->y + anchor->h - 1, COLOUR_WHITE);

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
        dline(anchor->x, anchor->y, anchor->x, anchor->y + anchor->h - 2, COLOUR_BLACK); // Left
        dline(anchor->x+1, anchor->y + anchor->h - 1, anchor->x + anchor->w -1 - TAB_ROUNDED_DIM, anchor->y + anchor->h - 1, COLOUR_BLACK);  // bottom
        dline(anchor->x + anchor->w -1 - TAB_ROUNDED_DIM, anchor->y + anchor->h - 1, anchor->x + anchor->w - 1, anchor->y + anchor->h - 1 - TAB_ROUNDED_DIM, COLOUR_BLACK);  // bottom
        dline(anchor->x + anchor->w - 1, anchor->y, anchor->x + anchor->w - 1, anchor->y + anchor->h - 1 - TAB_ROUNDED_DIM, COLOUR_BLACK);   // right
    }
    else{
        dline(anchor->x, anchor->y, anchor->x + anchor->w -1, anchor->y, COLOUR_BLACK);
    }
#endif // #ifdef DEST_CASIO_FXCG50
}

//
// tabValue: a tab holding a value (a parameter)
//

// Set or change comment
//
void tabValue::setComment(const char* comment, const char* ucomment){
    comment_ = _dup(comment_, comment);
    ucomment_ = _dup(ucomment_, ucomment);
}

// Duplicate a comment
//
char* tabValue::_dup(char* source, const char* val){
    // Free current string
    if (source){
        free(source);
    }

    // Duplicate comment
    return (val?strdup(val):NULL);
}

// The current tab is selected (and can take control of the keyboard)
//
void tabValue::select(TAB_STATUS& status){

    // Change the value
    value_.bVal = !value_.bVal;

    // update comment
    clearScreen();

#ifdef DEST_CASIO_FXCG50
    if (comment_){
        dtext(20, 20, COLOUR_BLACK, value_.bVal?comment_:(ucomment_?ucomment_:comment_));
    }

    dupdate();
#endif // #ifdef DEST_CASIO_FXCG50

    // Nothing special to do
    tab::select(status);
}

//
// tabRangedValue: A tab with a value in a range
//

// Range
//
void tabRangedValue::setRange(uint8_t minVal, uint8_t maxVal){
    // Set new values
    if (minVal < maxVal){
        minVal_ = minVal;
        maxVal_ = maxVal;
    }
    else{
        minVal_ = maxVal;
        maxVal_ = (minVal==maxVal?maxVal+1:minVal);
    }

    // Position
    xPos_ = (CASIO_WIDTH - TAB_RANGE_WIDTH * (maxVal_ - minVal_ + 1)) / 2;
    yPos_ = TAB_RANGE_POS_Y;

    // Current val must be in the range
    value_.uVal = (uint8_t)_inRange(value_.iVal);
}


// Change the value
//
void tabRangedValue::select(TAB_STATUS& status){

    int key(0);
    int8_t oldVal = -1;
    int8_t newVal = value_.uVal;
    bool stay(true);

    // Draw all possible numbers
    _drawRange();

    // Select current val
    _selectValue(newVal);

#ifdef DEST_CASIO_FXCG50
    dupdate();
    key_event_t evt;
#endif // #ifdef DEST_CASIO_FXCG50
    do{
#ifdef DEST_CASIO_FXCG50
        evt = pollevent();
        if (evt.type == KEYEV_DOWN){
            key = evt.key;
        }
        else{
            key = 0;    // ie. no char ...
        }
#else
        key = getchar();
#endif // #ifdef DEST_CASIO_FXCG50

        // Exit on "Exit" or F{n} key pressed
        if ((key >= KEY_CODE_F1 && key <= KEY_CODE_F6) || key == KEY_CODE_EXIT){
            stay = false;
        }
        else{
            // Change selection
            if (key == KEY_CODE_LEFT){
                newVal = _inRange(--newVal);
            }
            else{
                if (key == KEY_CODE_RIGHT){
                    newVal = _inRange(++newVal);
                }
            }

            // Any change ?
            if (newVal != oldVal){
                _selectValue(oldVal, false);
                _selectValue(newVal);

#ifdef DEST_CASIO_FXCG50
                dupdate();
#endif // #ifdef DEST_CASIO_FXCG50

                oldVal = newVal;
            }
        }

    }
    while (stay);

    // "return" key pressed (or 0 if none)
    status.action = ACTION_NONE;
    status.exitKey = key;
}

// Draw the range
void tabRangedValue::_drawRange(){
    uint8_t max = maxVal_ - minVal_;
    uint16_t x(xPos_);

    for (uint8_t index=0; index<max; index++){
#ifdef DEST_CASIO_FXCG50
        drect_border(x, yPos_, x + TAB_RANGE_WIDTH, yPos_ + TAB_RANGE_WIDTH, NO_COLOR, 1, COLOUR_BLACK);
        dprint(x + 3, yPos_ + 2, COLOUR_BLACK, "%d", (index+minVal_));
#endif // #ifdef DEST_CASIO_FXCG50
        x+=TAB_RANGE_WIDTH;
    }

#ifdef DEST_CASIO_FXCG50
    dupdate();
#endif // #ifdef DEST_CASIO_FXCG50
}

// Select a single value
//
void tabRangedValue::_selectValue(int8_t value, bool select){
    if (value >= minVal_ && value <= maxVal_){
        uint16_t x(xPos_ + (value - minVal_) * TAB_RANGE_WIDTH + 1);

#ifdef DEST_CASIO_FXCG50
        drect(x, yPos_ + 1 , x + TAB_RANGE_WIDTH - 1, yPos_ + TAB_RANGE_WIDTH - 1 , select?COLOUR_BK_HILITE:COLOUR_WHITE);
        dprint(x + 3, yPos_ + 2, select?COLOUR_WHITE:COLOUR_BLACK, "%d", value);
#else
        x++;    // for compiler
#endif // #ifdef DEST_CASIO_FXCG50
    }
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
tab* tabManager::select(int8_t ID){
    // Valid and different
    if (ID != active_ && ID < TAB_COUNT && tabs_[ID]){
        // Unselect
        _select(active_, false);

        // Select
        _select(ID, true);

        active_ = ID;

#ifdef DEST_CASIO_FXCG50
        dupdate();
#endif // DEST_CASIO_FXCG50

        return tabs_[ID];
    }

    // Not a valid tab
    return NULL;
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
