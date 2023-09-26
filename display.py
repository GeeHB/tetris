#
#   File     :   tetris.py
#
#   Author     :   JHB
#
#   Description :   display - Try to create the display object according to the selected mode
#
#   Comment    :
#
import consts

# display object
#
class display(object):

    # Construction
    def __init__(self):
        pass

    # Create (try to) an object
    #
    #   mode : type of object
    #
    #   return the object or None on error
    #
    def create(self, mode):
        obj = None
        if consts.MODE_AUTO == mode:
            # Try to create
            obj = self._pygameTetrisObject()
            if obj is None:
                obj =  self._cursesTetrisObject()
                if obj is None:
                    obj =  self._casioplotTetrisObject()
        else:
            if consts.MODE_CONSOLE == mode:
                return self._cursesTetrisObject()
            else:
                if consts.MODE_CASIOPLOT == mode:
                    return self._casioplotTetrisObject()
                else:
                    if consts.MODE_PYGAME == mode:
                        return self._pygameTetrisObject()
                    
        # ???
        return obj

    #
    # Internal methods
    #

    #   Create a pygameTetris object
    #
    #   return the object or None
    #
    def _pygameTetrisObject(self):
        try:
            from pygameTetris import pygameTetris
            return pygameTetris()
        except ModuleNotFoundError:
            return None
    
    #   Create a cursesTetris object
    #
    #   return the object or None
    #
    def _cursesTetrisObject(self):
        try:
            from cursesTetris import cursesTetris
            return cursesTetris()
        except ModuleNotFoundError:
            return None
    
    #   Create a casioplotTetris object
    #
    #   return the object or None
    #
    def _casioplotTetrisObject(self):
        try:
            from casioplotTetris import casioplotTetris
            return casioplotTetris()
        except ModuleNotFoundError:
            return None

# EOF