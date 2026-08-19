#   File     :   consoleTetris.py
#
#   Author     :   JHB
#
#   Description :   consoleTetris object
#                   abstract class for console input handling
#
#   Comment    :   Python 3.xx
#

import sys, os, termios, fcntl
import tetrisGame

# consoleTetris object - Drawings with curses library
#
class consoleTetris(tetrisGame.tetrisGame):

    term_ = None      # curses term.

    # Construction
    def __init__(self):

        # Texts dims. (scores, lines and level)
        self.itemDims_  = [0] * 3

    # overloads of tetrisGame methods
    #

    # Wait for an event (a keyboard event on curses)
    #
    def waitForEvent(self):
        wait = True
        c = ''
        while wait:
            c = self.checkKeyboard()
            if len(c) :
                wait = False
        return (consoleTetris.EVT_KEYDOWN, c)

    # Read the keyboard (non-blocking)
    #   returns the char or ''
    def checkKeyboard(self):
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

        try:
            while True:
                try:
                    c = sys.stdin.read(1)
                    break
                except IOError:
                    pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
            fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        return c

# EOF
