#!/bin/python3

# coding=UTF-8
#
#   File     :   tetris.py
#
#   Authors     :   JHB
#
#   Description :   The "tetris" game 
#
#   Remarque    :   Need Python 3.xx or higher
#
#   Version     :   0.6.1
#
#   Date        :   2020/10/21
#

import platform, sys, math

import sharedConsts
from cmdLineParser import cmdLineParser
from colorizer import colorizer, backColor, textColor, textAttribute
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
    txtColours_     = colorizer(True)

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
        parameters = cmdLineParser(sharedConsts.CMD_OPTION_CHAR)

        if 0 == parameters.size():
            # No parameters use default and start game !
            return True
        else:
            # Display high-scores
            self.params_.showScores_ = not (parameters.findAndRemoveOption(sharedConsts.CMD_OPTION_TOP) == parameters.NO_INDEX)

            if self.params_.showScores_:
                self.params_.useGUI_ = False
            else:
                # Console display mode ?
                self.params_.useGUI_ = (parameters.findAndRemoveOption(sharedConsts.CMD_OPTION_CONSOLE) == parameters.NO_INDEX)
                
                # Start level
                index =  parameters.findAndRemoveOption(sharedConsts.CMD_OPTION_START_LEVEL)
                if not parameters.NO_INDEX == index:
                    # Num. value expected
                    try :
                        rets = parameters.parameterOrValue(index + 1)
                        if rets[1] == False : 
                            self.params_.startLevel_ = int(rets[0])
                            if self.params_.startLevel_ <= 0 or self.params_.startLevel_ > 15:
                                self._usage()
                                return False
                    except IndexError:
                        # no value ...
                        self._usage()
                        return False
                    
                # # of dirty lines
                index =  parameters.findAndRemoveOption(sharedConsts.CMD_OPTION_DIRTY_LINES)
                if not parameters.NO_INDEX == index:
                    # num. value expected
                    try :
                        rets = parameters.parameterOrValue(index + 1)
                        if rets[1] == False : 
                            self.params_.dirtyLines_ = int(rets[0])
                            if self.params_.dirtyLines_ < 0 or self.params_.dirtyLines_ >= sharedConsts.PLAYFIELD_HEIGHT:
                                self._usage()
                                exit(1)
                    except IndexError:
                        # no value ...
                        self._usage()
                        return False
                
                # Display pieces'shadow ?
                self.params_.shadow_ = not (parameters.findAndRemoveOption(sharedConsts.CMD_OPTION_SHADOW) == parameters.NO_INDEX)

             # username (for score)
            index =  parameters.findAndRemoveOption(sharedConsts.CMD_OPTION_USER)
            if not parameters.NO_INDEX == index:
                # username expected
                try :
                    rets = parameters.parameterOrValue(index + 1)
                    if rets[1] == False : 
                        self.params_.user_ = rets[0]
                except IndexError:
                    # no value ...
                    self._usage()
                    return False

        # There should be no options left
        if parameters.options() > 0:
            self._usage()
            return False

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
                print("Display init. error. Message : ", error)
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
        seqDuration = self._updateSpeed(sharedConsts.INITIAL_SPEED * 1000000, self.params_.startLevel_, self.params_.startLevel_ - 1)
        ts, now = 0, 0
        uWait = 5 / 1000.0   # en ms.

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
            if 0 == (seqCount % sharedConsts.MOVES_UPDATE_LEVEL):
                # Real level (based on pieces movements)
                rLevel = math.floor(seqCount / sharedConsts.MOVES_UPDATE_LEVEL) + 1
                
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

    #
    # Private methods
    #   
    
    # Hadle keyboard inputs
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
        if level >= sharedConsts.MAX_LEVEL_ACCELERATION :
            return currentDuration
        
        # duration = currentDuration * acc ^ incLevel
        duration = currentDuration
        acc = (1.0 - sharedConsts.ACCELERATION_STEP)
        for _ in range(incLevel):
            duration*=acc
        return duration

    # Show usage
    #
    def _usage(self):
        print(self.txtColours_.colored("\tetris.py", formatAttr=[textAttribute.BOLD]))
        print("\t", self.txtColours_.colored(sharedConsts.CMD_OPTION_CHAR + sharedConsts.CMD_OPTION_START_LEVEL + " {numLevel} ", formatAttr=[textAttribute.DARK]), ": Start the game at {numLevel}")
        print("\t", self.txtColours_.colored(sharedConsts.CMD_OPTION_CHAR + sharedConsts.CMD_OPTION_SHADOW, formatAttr=[textAttribute.DARK]), ": Display shadow ot the piece at the bottom of the playfiled")
        print("\t", self.txtColours_.colored(sharedConsts.CMD_OPTION_CHAR + sharedConsts.CMD_OPTION_DIRTY_LINES + " {numLines} ", formatAttr=[textAttribute.DARK]), ": Start the game with {numLine} 'dirty' lines at the bottom of the playfield")
        print("\t", self.txtColours_.colored(sharedConsts.CMD_OPTION_CHAR + sharedConsts.CMD_OPTION_USER + " {username} ", formatAttr=[textAttribute.DARK]), ": Set the name of the current player")
        print("\t", self.txtColours_.colored(sharedConsts.CMD_OPTION_CHAR + sharedConsts.CMD_OPTION_CONSOLE, formatAttr=[textAttribute.DARK]), ": Console display mode (if nCurses is available)")
        print("\t", self.txtColours_.colored(sharedConsts.CMD_OPTION_CHAR + sharedConsts.CMD_OPTION_TOP, formatAttr=[textAttribute.DARK]), ": show high-scores")

#
# Entry point
#

if __name__ == '__main__':
    ver = sys.version_info
    if ver.major < sharedConsts.PYTHON_MIN_MAJOR or (ver.major == sharedConsts.PYTHON_MIN_MAJOR and ver.minor < sharedConsts.PYTHON_MIN_MINOR):
        out = str(sharedConsts.PYTHON_MIN_MAJOR) + "." + str(sharedConsts.PYTHON_MIN_MINOR)
        print("Error - Expected minimum version for Python ", out)
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