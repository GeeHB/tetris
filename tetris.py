#!/usr/bin/python3
#
# coding=UTF-8
#
#   File     :   tetris.py
#
#   Author     :   JHB
#
#   Description :   The "tetris" game 
#
#   Comment    :   Need Python 3.xx or higher
#
import time, sys, math
import consts, display
from sharedTools import colorizer as color
from tetrisGame import tetrisGame
from board import board, tetrisParameters
from scores import scores

# Public consts
#

# tetris object
#   Handles game and scores 
#
class tetris(object):
    # Members
    #
    gameData_       = None        # Game's datas
    displayMgr_     = None        # Display manager

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
        try:
            from cmdParser import cmdParser
            myParser = cmdParser()
            if myParser.parse():
                # Valid
                self.params_ = myParser.parameters()
                return True
        except ModuleNotFoundError:
            return False
                
    # Can we start the game ?
    #
    #   return tuple(ok?, error message)
    #
    def isReady(self):

        # Display mode
        #
        displayMgr = display.display()
        self.displayMgr_ = displayMgr.create(self.params_.mode_)
        
        # No display ?
        if self.displayMgr_ is None:
            return False, f"Error - no display handler found for '{self.mode_}'. Ending the game"

        # Check display manager
        if False == self.params_.showScores_:
            done, error = self.displayMgr_.checkEnvironment()
            if not done and len(error) > 0:
                # End nCurses
                self.displayMgr_.clear()
                return False, error

        self.gameData_ = board(self.displayMgr_)
        self.displayMgr_.setBoard(self.gameData_)

        # yes !
        return True, ""

    # Starting the game
    #
    def start(self):
        self.gameData_.setParameters(self.params_)
        self._newGame()

    # Game ending
    #
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
        
        if not self.displayMgr_.resizable:
            time.sleep(1)
            self.displayMgr_.reDraw()
            self.displayMgr_.updateDisplay()

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
                if rLevel >= self.gameData_.level:
                    self.displayMgr_.levelChanged(self.gameData_.incLevel())
                    seqDuration = self._updateSpeed(seqDuration, self.gameData_.level, 1)
        
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
            myScore = self.gameData_.score
            if False != myScore:
                self.displayMgr_.showScores(self.params_.user_, myScore, bestScores.add(myScore))
    
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

    params = tetrisParameters()
    
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
            ret, message = myTetris.isReady()
            if ret:    
                myTetris.start()
                myTetris.end()
            else:
                print(message)
#EOF 