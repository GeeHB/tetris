#!/bin/python3

# coding=UTF-8
#
#   File     :   tetris.py
#
#   Auteur      :   JHB
#
#   Description :   The "tetris" game 
#
#   Remarque    :   Need Python 3.xx or higher
#
#   Version     :   0.5.2
#
#   Date        :   2020/09/21
#

import platform, sys
from cmdLineParser import cmdLineParser
from colorizer import colorizer, backColor, textColor, textAttribute    # for text coloration in console mode
from tetrisGame import tetrisGame
from board import PLAYFIELD_HEIGHT, tetrisParameters

# Public consts
#

PYTHON_MIN_MAJOR = 3
PYTHON_MIN_MINOR = 7

MAX_LEVEL_ACCELERATION = 12     # No more acceleration when this level is reached
ACCELERATION_STEP = 0.18        # Growing speed % per level
INITIAL_SPEED = 1200            # Level 1 speed (larger is slower)
MOVES_UPDATE_LEVEL = 250        # Change level criterium (# of pieces going down one step)

SCORES_FILE = 'scores.high'     # Scores' file

# Command line options
#

CMD_OPTION_CHAR = "-"

CMD_OPTION_START_LEVEL = "level"
CMD_OPTION_SHADOW = "shadow"
CMD_OPTION_DIRTY_LINES = "lines"
CMD_OPTION_USER = "me"

CMD_OPTION_CONSOLE = "c"         # Console mode

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
        parameters = cmdLineParser(CMD_OPTION_CHAR)

        if 0 == parameters.size():
            # No parameters use default and start game !
            return True
        else:
            # Console display mode ?
            self.params_.useGUI_ = (parameters.findAndRemoveOption(CMD_OPTION_CONSOLE) == parameters.NO_INDEX)

            # Start level
            index =  parameters.findAndRemoveOption(CMD_OPTION_START_LEVEL)
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
            index =  parameters.findAndRemoveOption(CMD_OPTION_DIRTY_LINES)
            if not parameters.NO_INDEX == index:
                # num. value expected
                try :
                    rets = parameters.parameterOrValue(index + 1)
                    if rets[1] == False : 
                        self.params_.dirtyLines_ = int(rets[0])
                        if self.params_.dirtyLines_ < 0 or self.params_.dirtyLines_ >= PLAYFIELD_HEIGHT:
                            self._usage()
                            exit(1)
                except IndexError:
                    # no value ...
                    self._usage()
                    return False

             # username (for score)
            index =  parameters.findAndRemoveOption(CMD_OPTION_USER)
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
            
            # Display pieces'shadow ?
            self.params_.shadow_ = not (parameters.findAndRemoveOption(CMD_OPTION_SHADOW) == parameters.NO_INDEX)

        # There should be no options left
        if parameters.options() > 0:
            self._usage()
            return False

        # Ok
        return True
        
    # Can we start the game ?
    def isReady(self):

        # Display mode
        #
        if self.params_.useGUI_:
            if self.params_.pygameAvailable_:
                self.displayMgr_ = pygameTetris()
            else:
                # GUI wanted but no pygame => try curses
                print("Error - pygame not installed try with curses")
                params.useGUI_ = False

        if False == params.useGUI_:
            if self.params_.cursesAvailable_:
                self.displayMgr_ = cursesTetris()
            else:
                print("Error - curses not installed")
                
        # No display ?
        if not self.displayMgr_:
            print("Error - no display handler. Ending game")
            return False

        # Check display manager
        error = self.displayMgr_.checkEnvironment()
        if len(error) > 0:
            print("Display init. error. Message : ", error)
            return False

        self.gameData_ = board(self.displayMgr_)
        self.displayMgr_.setBoard(self.gameData_)

        # yes !
        return True

    # Starting the game
    def start(self):
        self.gameData_.setParameters(self.params_)
        self._newGame()

    # Game ending
    def end(self):
        if self.displayMgr_:
            self.displayMgr_.end()

    # Lancement d'une partie
    def _newGame(self):

         # "Vitesse" initiale
        seqCount = 0
        seqDuration = self._updateSpeed(INITIAL_SPEED * 1000000, self.params_.startLevel_, self.params_.startLevel_ - 1)
        ts, now = 0, 0
        uWait = 5 / 1000.0   # en ms.

        # On part !
        self.gameData_.setParameters(self.params_)
        self.displayMgr_.start()
        
        # Quit the game ?
        if self.displayMgr_.waitForEvent().type == tetrisGame.EVT_QUIT:
            exit(1) 

        # Gestion du jeu
        while self.displayMgr_.isRunning():
            diff = 0
            ts = now

            # Pendant l'intervalle de descente, on peut bouger la pièce
            while self.displayMgr_.isRunning() and diff < seqDuration :
                self._handleGameKeys()
                time.sleep(uWait) # usleep(5000)
                now = time.monotonic_ns() # Fonctionne aussi sous macOS à partir de Python 3.7
                diff = now - ts

            # Descente automatique ...
            self.gameData_.down()

            # Gestion de l'accelération
            seqCount += 1
            if 0 == (seqCount % MOVES_UPDATE_LEVEL):
                self.displayMgr_.levelChanged(self.gameData_.incLevel())

                # Accelération
                seqDuration = self._updateSpeed(seqDuration, self.displayMgr_.level(), 1)

        # the game is over

        # On affiche les meilleurs scores
        #self._hallOfFame(self.gameData_.score())

    # Méthodes privées
    #

    # Lecture des meilleurs scores
    def _loadScores(self):
        scores = [] # Par défaut il n'y a pas de scores

        # Le fichier doit exister
        try:
            file = open(SCORES_FILE)
            for line in file :
                if len(line) > 0:
                    value = int(line)
                    if not value in scores: # Pas déja présent ?
                        scores.append(value)
            file.close()

        except FileNotFoundError:
           # Le fichier n'existe pas !
           pass

        # Retourne le tableau ordonné des scores
        return scores

    # Ajout d'un score
    def _newScore(self, currentScore):
        tops = self._loadScores()
        append = False
        
        # Le score est-il dans le tableau ?
        cScores = len(tops)
        if cScores >= 10 : 
            tops.sort(reverse = True)
            if tops[9] < currentScore:
                # On l'ajoute si la valeur n'est pas déja présente
                append = True
        else:
            # Ajout dans tous les cas
            append = True

        if True == append and not currentScore in tops :
            tops.append(currentScore)
            tops.sort(reverse = True)

        # On retourne le tableau ordonné
        return tops 

    # Sauvegarde du tableau des scores
    def _saveScores(self, scores):
        try:
            file = open(SCORES_FILE, "w")
            max = 10 if len(scores)>10 else len(scores)
            for i in range(max) :
                # Une ligne de plus à écrire
                line = str(scores[i])+"\n"
                file.write(line)
            file.close()
        except:
            pass
    
    # Affichage des scores
    def _hallOfFame(self, currentScore):
        tops = self._newScore(currentScore)
        scoreIndex = -1
        
    
    # Analyse du clavier pendant la phase de jeu
    def _handleGameKeys(self):
        inputChar = self.displayMgr_.checkKeyboard()
        if self.displayMgr_.KEY_STOP == inputChar:
            # Fin de partie
            self.displayMgr_.end()
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

    # Mise à jour de la vitesse (ie. délai max. d'attente entre 2 descentes auto.)
    def _updateSpeed(self, currentDuration, level, incLevel = 1):
        if level >= MAX_LEVEL_ACCELERATION :
            return currentDuration
        
        # duration = currentDuration * acc ^ incLevel
        duration = currentDuration
        acc = (1.0 - ACCELERATION_STEP)
        for _ in range(incLevel):
            duration*=acc
        return duration

    # Show usage
    #
    def _usage(self):
        print(self.txtColours_.colored("\tetris.py", formatAttr=[textAttribute.GRAS]))
        print("\t", self.txtColours_.colored(CMD_OPTION_CHAR + CMD_OPTION_START_LEVEL + " {numLevel} ", formatAttr=[textAttribute.FONCE]), ": Start the game at {numLevel}")
        print("\t", self.txtColours_.colored(CMD_OPTION_CHAR + CMD_OPTION_SHADOW, formatAttr=[textAttribute.FONCE]), ": Display shadow ot the piece at the bottom of the playfiled")
        print("\t", self.txtColours_.colored(CMD_OPTION_CHAR + CMD_OPTION_DIRTY_LINES + " {numLines} ", formatAttr=[textAttribute.FONCE]), ": Start the game with {numLine} 'dirty' lines at the bottom of the playfield")
        print("\t", self.txtColours_.colored(CMD_OPTION_CHAR + CMD_OPTION_USER + " {username} ", formatAttr=[textAttribute.FONCE]), ": Set the name of the current player")
        print("\t", self.txtColours_.colored(CMD_OPTION_CHAR + CMD_OPTION_CONSOLE, formatAttr=[textAttribute.FONCE]), ": Console display mode (if nCurses is available)")

#
# Boucle principale du jeu
#

if __name__ == '__main__':
    # Vérification de la version minimale de python
    ver = sys.version_info
    if ver.major < PYTHON_MIN_MAJOR or (ver.major == PYTHON_MIN_MAJOR and ver.minor < PYTHON_MIN_MINOR):
        out = str(PYTHON_MIN_MAJOR) + "." + str(PYTHON_MIN_MINOR)
        print("Python doit être au minimum en version", out)
        exit(1) 

    # Maintenant que les causes d'erreur(s) sont écartées ...
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
    if False == params.pygameAvailable_:
        try:
            from cursesTetris import cursesTetris
            params.cursesAvailable_ = True
        except ModuleNotFoundError:
            params.cursesAvailable_ = False
    
    #
    # the game ...
    #
    myTetris = tetris(params) 
    if myTetris.parseCmdLine() and myTetris.isReady():    

        # Démarrage du jeu
        myTetris.start()

        # Fin & libérations
        myTetris.end()
#EOF 