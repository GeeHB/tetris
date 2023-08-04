#!/usr/bin/python3
#
# coding=UTF-8
#
#   File     :   tetris.py
#
#   Authors     :   JHB
#
#   Description :   The "tetris" game 
#
#   Comment    :   Need Python 3.xx or higher
#

import sys, math, argparse
import consts
from sharedTools import colorizer as color
from tetrisGame import tetrisGame
from board import tetrisParameters
from scores import scores

# Public consts
#

# tetris object
#   Handles game and scores 
#
class tetris(object):
    # Données membres
    #
    gameData_       = None        # Game's datas
    displayMgr_     = None        # Display manager
    txtColours_     = color.colorizer(True)

    params_ = tetrisParameters()

    # Construction
    #
    def __init__(self, params):
        self.params_ = params

    # Parse the command line
    #
    #   return True if no error where found
    #
    def parseCmdLine(self):
        
        parser = argparse.ArgumentParser(epilog = self.version())
 
        # Define parameters
        #
         
        # High scores
        parser.add_argument(consts.ARG_TOP_S, consts.ARG_TOP, action='store_true', help = consts.COMMENT_TOP, required = False)
        
        # Console display mode ?
        parser.add_argument(consts.ARG_CONSOLE_S, consts.ARG_CONSOLE, action='store_true', help = consts.COMMENT_CONSOLE, required = False)

        # Console display mode ?
        parser.add_argument(consts.ARG_SHADOW_S, consts.ARG_SHADOW, action='store_true', help = consts.COMMENT_SHADOW, required = False)

        # Start level
        parser.add_argument(consts.ARG_STARTLEVEL_S, consts.ARG_STARTLEVEL, help = consts.COMMENT_STARTLEVEL, required = False, nargs=1, default = [consts.DEF_LEVEL], type=int, choices=range(consts.MIN_LEVEL, consts.MAX_LEVEL))
        
        # dirty lines
        parser.add_argument(consts.ARG_DIRTY_S, consts.ARG_DIRTY, help = consts.COMMENT_DIRTY, required = False, nargs=1, default = [0], type=int, choices=range(0, consts.PLAYFIELD_HEIGHT - 1))
        
        # User name
        parser.add_argument(consts.ARG_USER_S, consts.ARG_USER, help = consts.COMMENT_USER, required = False, nargs=1)

        # Parse the command line
        #
        args = parser.parse_args()

        # Display high-scores
        self.params_.showScores_ = args.top
        
        # Console mode (forced if displaying scores)
        self.useGUI_ = False if self.params_.showScores_ else (False == args.console)

        # Display high-scores
        self.params_.shadow_ = args.shadow

        # Starting level
        self.params_.startLevel_ = args.level[0]

        # Dirty lines
        self.params_.dirtyLines_ = args.dirty[0]

        # User name
        if args.user is not None:
            self.params_.user_ = args.user[0]
        
        # Ok
        return True
        
    # Can we start the game ?
    #
    def isReady(self):

        # Display mode
        #
        if self.params_.useGUI_:
            if self.params_.pygameAvailable_:
                self.displayMgr_ = pygameTetris()
            else:
                # GUI wanted but no pygame => try curses
                print("Error - pygame not installed. Try with curses")
                params.useGUI_ = False

        if False == params.useGUI_:
            if self.params_.cursesAvailable_:
                self.displayMgr_ = cursesTetris()
            else:
                print("Error - curses not installed")
                
        # No display ?
        if not self.displayMgr_:
            print("Error - no display handler. Ending the game")
            return False

        # Check display manager
        if False == self.params_.showScores_:
            error = self.displayMgr_.checkEnvironment()
            if len(error) > 0:
                print(f"Display init. error. Message : {error}")
                return False

        self.gameData_ = board(self.displayMgr_)
        self.displayMgr_.setBoard(self.gameData_)

        # yes !
        return True

    # Starting the game
    #
    def start(self):
        self.gameData_.setParameters(self.params_)
        self._newGame()

    # Game ending
    def end(self):
        if self.displayMgr_:
            self.displayMgr_.end()

    # A new game
    #
    def _newGame(self):

        # Initial speed
        seqCount = 0
        seqDuration = self._updateSpeed(consts.INITIAL_SPEED * 1000000, self.params_.startLevel_, self.params_.startLevel_ - 1)
        ts, now = 0, 0
        uWait = 5 / 1000.0   # in ms.

        # start !
        self.gameData_.setParameters(self.params_)
        self.displayMgr_.start()
        
        # Cancel the game ?
        cont = True
        while cont :
            evt = self.displayMgr_.waitForEvent()
            if evt[0] == self.displayMgr_.EVT_QUIT or (evt[0] == self.displayMgr_.EVT_KEYDOWN and evt[1] == self.displayMgr_.KEY_QUIT):
                exit(1) 

            if evt[1] == self.displayMgr_.KEY_START:
                cont = False

        self.displayMgr_.drawNextPiece()

        # Game main loop
        while self.displayMgr_.isRunning():
            diff = 0
            ts = now

            # During this short period, the piece can be moved or rotated
            while self.displayMgr_.isRunning() and diff < seqDuration :
                self._handleGameKeys()
                time.sleep(uWait) # usleep(5000)
                now = time.monotonic_ns()
                diff = now - ts

            # One line down ...
            self.gameData_.down()

            # Accelerate ?
            seqCount += 1
            if 0 == (seqCount % consts.MOVES_UPDATE_LEVEL):
                # Real level (based on pieces movements)
                rLevel = math.floor(seqCount / consts.MOVES_UPDATE_LEVEL) + 1
                
                # Change level (if necessary) & accelerate
                if rLevel >= self.gameData_.level():
                    self.displayMgr_.levelChanged(self.gameData_.incLevel())
                    seqDuration = self._updateSpeed(seqDuration, self.gameData_.level(), 1)

        # the game is over
        # wait for gamer to exit
        cont = True
        while cont:
            evt = self.displayMgr_.waitForEvent()
            if evt[0] == self.displayMgr_.EVT_QUIT or (evt[0] == self.displayMgr_.EVT_KEYDOWN and (evt[1] == self.displayMgr_.KEY_QUIT or evt[1] == self.displayMgr_.KEY_START)):
                cont = False

        # Close display
        self.displayMgr_.clear()

        if not self.displayMgr_.isCancelled():
            # Score handling
            bestScores = scores(self.params_.user_)
            myScore = self.gameData_.score()
            if False != myScore:
                self.displayMgr_.showScores(self.params_.user_, myScore, bestScores.add(myScore))

    
    # Display app version infos
    #
    #   return a string
    #
    def version(self, verbose = True):
        if None == self.txtColours_:
            self.txtColours_ = color.colorizer(True)

        return f"{self.txtColours_.colored(consts.APP_NAME, formatAttr=[color.textAttribute.BOLD], datePrefix=(False == verbose))} by {consts.APP_AUTHOR} - release {consts.APP_CURRENT_VERSION} - {consts.APP_RELEASE_DATE}"
    
    #
    # Private methods
    #   
    
    # Handle keyboard inputs
    #
    def _handleGameKeys(self):
        inputChar = self.displayMgr_.checkKeyboard()
        if self.displayMgr_.KEY_STOP == inputChar:  # "Escape"/cancel the game
            self.displayMgr_.cancel()
        elif self.displayMgr_.KEY_RIGHT == inputChar:
            self.gameData_.right()
        elif self.displayMgr_.KEY_LEFT == inputChar:
            self.gameData_.left()
        elif self.displayMgr_.KEY_ROTATE_LEFT == inputChar:
            self.gameData_.rotateLeft()
        elif self.displayMgr_.KEY_DOWN == inputChar:
            self.gameData_.down()
        elif self.displayMgr_.KEY_FALL == inputChar:
            self.gameData_.fall()

    # Change the game'speed
    def _updateSpeed(self, currentDuration, level, incLevel = 1):
        if level >= consts.MAX_LEVEL_ACCELERATION :
            return currentDuration
        
        # duration = currentDuration * acc ^ incLevel
        duration = currentDuration
        acc = (1.0 - consts.ACCELERATION_STEP)
        for _ in range(incLevel):
            duration*=acc
        return duration

#
# Entry point
#

if "__main__" == __name__:
    ver = sys.version_info
    if ver.major < consts.PYTHON_MIN_MAJOR or (ver.major == consts.PYTHON_MIN_MAJOR and ver.minor < consts.PYTHON_MIN_MINOR):
        print(f"Error - Expected minimum version for Python {str(consts.PYTHON_MIN_MAJOR)}.{str(consts.PYTHON_MIN_MINOR)}")
        exit(1) 

    import time
    from board import board, tetrisParameters

    params = tetrisParameters()

    # Test Pygame presence
    try:
        from pygameTetris import pygameTetris
        params.pygameAvailable_ = True
    except ModuleNotFoundError:
        # PYGame isn't installed
        params.pygameAvailable_ = False

    # At least can we use nCurses ?
    try:
        from cursesTetris import cursesTetris
        params.cursesAvailable_ = True
    except ModuleNotFoundError:
        params.cursesAvailable_ = False
    
    #
    # the game ...
    #
    myTetris = tetris(params) 
    if myTetris.parseCmdLine():
        # Just show scores ?
        if myTetris.params_.showScores_ :
            myGame = tetrisGame()
            bestScores = scores(myTetris.params_.user_)
            myGame.showScores(myTetris.params_.user_, None, bestScores.add(None))
        else:
            if myTetris.isReady():    
                myTetris.start()
                myTetris.end()
#EOF 