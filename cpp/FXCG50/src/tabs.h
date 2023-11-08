//---------------------------------------------------------------------------
//--
//--	File	: tabs.h
//--
//--	Author	: Jérôme Henry-Barnaudière - GeeHB
//--
//--	Project	: jtetris - cpp version
//--
//---------------------------------------------------------------------------
//--
//--	Description:
//--
//--			Definition of tabManager and tab objects
//--
//---------------------------------------------------------------------------

#ifndef __J_TETRIS_CASIO_TABS_h__
#define __J_TETRIS_CASIO_TABS_h__    1

#include "casioFX-CG50.h"

#ifdef __cplusplus
extern "C" {
#endif // #ifdef __cplusplus

//---------------------------------------------------------------------------
//--
//-- Constants
//--
//---------------------------------------------------------------------------

#define TAB_COUNT       6

// Dimensions in pixels
#define TAB_HEIGHT      22
#define TAB_WIDTH       (CASIO_WIDTH / TAB_COUNT)

#define TAB_ROUNDED_DIM     4

#define TAB_NAME_LEN    10      // max char

#define KEY_NONE        0       // No key pressed

// Data handled by a tabValue object
//
union TAB_VALUE{
    bool        bVal;
    uint8_t     uVal;
    int         iVal;
    /*
    void*       pVal;
    */
};

// Position of a tab
typedef struct __rect{
    uint16_t    x,y;    // top left
    uint16_t    w, h;   // width and height
} RECT;

// Actions
//
enum TAB_ACTIONS{
    ACTION_NONE	 = 0,
    ACTION_REDRAW_TABS = 1,
    ACTION_QUIT = 2            // The app should quit
    // Other possible actions ???
};

// Status of a tab
//
typedef struct __tabStatus{
    // Construction
    __tabStatus(){
        action = ACTION_NONE;
        exitKey = KEY_NONE;
    }

    int action;         // Action to perform
    int exitKey;        // Code of last keyboard event or KEY_NONE
}TAB_STATUS;

//---------------------------------------------------------------------------
//--
//-- tab object - base class for tab objects
//--
//---------------------------------------------------------------------------

class tab{
public:
    // Construction
    tab(const char* tname, int action = ACTION_NONE);

    // Destruction
    ~tab(){}

    // The current tab is selected (and can take control of the keyboard)
    virtual void select(TAB_STATUS& status){
        // Nothing todo
        status.action = action_;
        status.exitKey = KEY_NONE;
    }

    /*
    // Unselect the current tab
    void unSelect(){}
    */

    // Draw
     void draw(bool selected = false){
        draw(&rect_, selected, name_);
    }

    // Access
    const char* name(){
        return name_;
    }

    // Dimensions & position
    void getRect(RECT& position);
    void setRect(RECT& position);

    // static methods
    //

    // Draw a single tab
    static void draw(const RECT* position, bool selected, const char* name = NULL);

    // clear the whole screen (except tab lane)
    static void clearScreen(){
#ifdef DEST_CASIO_FXCG50
        drect(0, 0, CASIO_WIDTH - 1, CASIO_HEIGHT - TAB_HEIGHT - 1, C_WHITE);
#endif // #ifdef DEST_CASIO_FXCG50
    }

protected:
    // Members
    char        name_[TAB_NAME_LEN + 1];
    int         action_;        // What todo when pressed ?
    RECT        rect_;
};

//---------------------------------------------------------------------------
//--
//-- tabValue object : A tab with a value / parameter
//--            by default the tabValue works as a 2 state button to
//--            set ou unset the internal boolean value
//--
//---------------------------------------------------------------------------

class tabValue : public tab{
public:
    // Construction
    tabValue(const char* tname, int action = ACTION_NONE)
    :tab(tname, action){
        value_.iVal = 0;
        comment_ = ucomment_ = NULL;
    }

    // Destruction
    virtual ~tabValue(){
        setComment(NULL, NULL);   // Free the resource
    }

    // Value
    void setValue(TAB_VALUE& val){
        // Any ...
        value_.iVal = val.iVal;
    }
    void value(TAB_VALUE& val){
        val.iVal = value_.iVal;
    }

    // Comment
    void setComment(const char* comment, const char* ucomment = NULL);

    // The current tab is selected (and can take control of the keyboard)
    void select(TAB_STATUS& status);

protected :
    char* _dup(char* source, const char* value);

protected:
    // Members
    TAB_VALUE   value_;
    char       *comment_, *ucomment_;
};

//---------------------------------------------------------------------------
//--
//-- tabRangedValue object : A tab with a value in a range
//--
//---------------------------------------------------------------------------

class tabRangedValue : public tabValue{
public:
    // Construction
    tabRangedValue(const char* tname, uint8_t minVal, uint8_t maxVal)
    :tabValue(tname, ACTION_NONE){
        setRange(minVal, maxVal);
    }

    // Destruction
    ~tabRangedValue(){
        setComment(NULL);   // should be useless with virtual methods ...
    }

    // Range
    void setRange(uint8_t minVal, uint8_t maxVal);

    // The current tab is selected (and can take control of the keyboard)
    void select(TAB_STATUS& status);

private:
    // Ensure value is in the range
    int8_t _inRange(int8_t val){
        return ((val < minVal_)?minVal_:((value_.uVal > maxVal_)?maxVal_:val));
    }

    // Draw the range
    void _drawRange();

    // Select a single value
    void _selectValue(int8_t value, bool select = true);

protected:
    uint8_t minVal_, maxVal_;   // Range
    uint16_t xPos_, yPos_;      // Origin for range
};

//
// tabManager - Manages the 6 possibles tabs
//
class tabManager{
public:
    // Constructor
    tabManager();

    // Destructor
    ~tabManager(){}

    // Add a tab
    bool add(tab* ptab, int8_t ID = -1);

    // Set active tab
    tab* select(int8_t ID);
    int8_t activeTab(){
        return active_;
    }

    // (Re)draw all tabs
    void update();

    // Private methods
    //
private:
    // Set a tab position
    void _ID2Rect(uint8_t ID, RECT& rect);

    // Search in the tab list
    int8_t _find(const tab* ptab);
    int8_t _findFreeID();

    // (de)activate a tab
    void _select(int8_t ID, bool activate);

    // Members
    tab*    tabs_[TAB_COUNT];
    int8_t  active_;    // ID of active tab
};

#ifdef __cplusplus
}
#endif // #ifdef __cplusplus

#endif // __J_TETRIS_CASIO_TABS_h__

// EOF
