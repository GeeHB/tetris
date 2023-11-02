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
#define TAB_HEIGHT      18
#define TAB_WIDTH       (CASIO_WIDTH / TAB_COUNT)

#define TAB_NAME_LEN    10      // max char


// Data handled by a tab
//
union TAB_VALUE{
    bool        bVal;
    int         iVal;
    uint16_t    uVal;
    void*       pVal;
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
    ACTION_QUIT
};

//---------------------------------------------------------------------------
//--
//-- tab object - abstract class
//--
//---------------------------------------------------------------------------

class tab{
public:
    // Construction
    tab(const char* tname, int action = ACTION_NONE);

    // Destruction
    ~tab(){}

    // Action to perform
    int action(){
        // Ok
        return action_;
    }

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

    // clear the whole screen (except tab lane)
    /*
    static void clearScreen(){
#ifdef DEST_CASIO_FXCG50
        drect(0, 0, CASIO_WIDTH - 1, CASIO_HEIGHT - rect_.height - 1, C_WHITE)
#endif // #ifdef DEST_CASIO_FXCG50
    }
    */

    // Draw a single tab
    static void draw(const RECT* position, bool selected, const char* name = NULL);

    // "private" methods
protected:


protected:
    // Members
    char        name_[TAB_NAME_LEN + 1];
    int         action_;        // What todo when pressed ?
    RECT        rect_;
};

//---------------------------------------------------------------------------
//--
//-- tabValue object : A tab with a value / parameter
//--
//---------------------------------------------------------------------------

class tabValue : public tab{
public:
    // Construction
    tabValue(const char* tname, int action = ACTION_NONE)
    :tab(tname, action){
        value_.iVal = 0;
    }

    // Destruction
    ~tabValue(){}

    // Action to perform
    uint8_t action(){
        // Ok
        return action_;
    }

    // Value
    void setValue(TAB_VALUE& val){
        // Any ...
        value_.iVal = val.iVal;
    }
    void value(TAB_VALUE& val){
        val.iVal = value_.iVal;
    }

protected:
    // Members
    TAB_VALUE   value_;
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
    uint8_t select(int8_t ID);
    int8_t activeTab(){
        return active_;
    }

    // Redraw all tabs
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
