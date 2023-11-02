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
    tab(uint8_t ID, const char* tname, uint8_t height = TAB_HEIGHT);

    // Destruction
    virtual ~tab(){}

    // Activate
    virtual int activate(bool setActivate = true){
        // Ok
        return ACTION_NONE;
    }

    // Draw.
    virtual void draw(bool selected = false){
        draw(rect_, selected, name);
    }

    // Access
    const char* name(){
        return name_;
    }

    // Value
    void setValue(TAB_VALUE& val){
        // Any ...
        val_.iVal = val.iVal;
    }
    void value(TAB_VALUE& val){
        val.iVal = val_.iVal;
    }

    // Dimensions & position
    void getRect(RECT& position);

    // static methods
    //

    // clear the whole screen (except tab lane)
    static void clearScreen(){
#ifdef DEST_CASIO_FXCG50
        drec(0, 0, CASIO_WIDTH - 1, CASIO_HEIGHT - rect_.h - 1, C_WHITE)
#endif // #ifdef DEST_CASIO_FXCG50
    }

    // Draw a single tab
    static void draw(const RECT* position, bool selected, const char* name = NULL);

    // "private" methods
protected:


protected:
    // Members
    char        name_[TAB_NAME_LEN + 1];
    RECT        rect_;
    TAB_VALUE   val_;
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
    bool add(const tab* ptab);

    // Set active tab
    void select(int8_t ID);

private:
    // Private methods
    int8_t _find(const tab* ptab);

    // Members
    tab*    tabs_[TAB_COUNT];
};

#ifdef __cplusplus
}
#endif // #ifdef __cplusplus

#endif // __J_TETRIS_CASIO_TABS_h__

// EOF
