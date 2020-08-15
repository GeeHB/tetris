#!/bin/python3

# coding=UTF-8
#
#   Fichier     :   tetris.py
#
#   Auteur      :   JHB
#
#   Description :   Jeu "tetris" 
#
#   Remarque    :   Nécessite Python 3.xx
#
#   Version     :   0.4.9
#
#   Date        :   15 aout 2020
#

import platform, sys
from tetrisGame import tetrisGame

# Quelques constantes
#

# Version minimale de Python
PYTHON_MIN_MAJOR = 3
PYTHON_MIN_MINOR = 7

MAX_LEVEL_ACCELERATION = 10     # Passé ce niveau il n'y a plus d'accelération
ACCELERATION_STEP = 24          # Ratio (1 / x) d'accélération du jeu
DEBUG_MESSAGE_DURATION = 1      # Durée d'afficage des messages en secondes
INITIAL_SPEED = 700             # Vitesse initiale (pour le niveau 1)
MOVES_UPDATE_LEVEL = 250        # Changement de niveau après x déplacements

SCORES_FILE = 'scores.high'     # Fichier des scores

# Classe tetris
#   Gestion des parties et des scores
#
class tetris(object):
    # Données membres
    #
    gameData_ = None        # Données du jeu
    gameHandler_ = None     # Gestionnaire / afficheur du jeu

    params_ = None

    # Moteur d'affichage

    # Construction
    def __init__(self, params):
        # Initalisation des données membres
        self.params_ = params

        if False == params.gui_:
            self.gameHandler_ = cursesTetris()
        else:
            #self.gameHandler_ = cursesTetris()
            self.gameHandler_ = pygameTetris()

    # La partie peut-elle commencer ?
    def isReady(self):
        # Validation du moteur d'affichage
        error = self.gameHandler_.checkEnvironment()
        if len(error) > 0:
            print("Impossible de lancer la partie. Message : ", error)
            return False

        # Gestionnaire de jeu
        self.gameData_ = board(self.gameHandler_)
        self.gameHandler_.setBoard(self.gameData_)

        # Oui
        return True

    # Démarrage du jeu
    def start(self):
        # Préparation de l'espace de jeu
        self.gameData_.setParameters(self.params_)
        
        # Gestion des parties
        while True == self._mainMenu():
            self._newGame()

        # Le jeu est terminé !

    # Fin du jeu
    def end(self):
        if None != self.gameHandler_:
            self.gameHandler_.end()

    # Lancement d'une partie
    def _newGame(self):

         # "Vitesse" initiale
        seqCount = 0
        seqDuration = self._updateSpeed(INITIAL_SPEED * 1000000, self.params_.startLevel_, 0)
        ts, now = 0, 0
        uWait = 5 / 1000.0   # en ms.

        # On part !
        self.gameData_.setParameters(self.params_)
        self.gameHandler_.start()

        # Gestion du jeu
        while self.gameHandler_.isRunning():
            diff = 0
            ts = now

            # Pendant l'intervalle de descente, on peut bouger la pièce
            while self.gameHandler_.isRunning() and diff < seqDuration :
                self._handleGameKeys()
                time.sleep(uWait) # usleep(5000)
                now = time.monotonic_ns() # Fonctionne aussi sous macOS à partir de Python 3.7
                diff = now - ts

            # Descente automatique ...
            self.gameData_.down()

            # Gestion de l'accelération
            seqCount += 1
            if 0 == (seqCount % MOVES_UPDATE_LEVEL):
                # Un niveau de plus
                level = self.gameData_.incLevel()
                self.gameHandler_.levelChanged(level)

                # Accelération
                seqDuration = self._updateSpeed(seqDuration, 1, level)

        # La partie est terminée !

        # On affiche les meilleurs scores
        self._hallOfFame(self.gameData_.score())

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

        # Ajout des lignes
        lines = []
        i = 1
        for top in tops:
            sLine = str(i) + ("  - " if i < 10 else " - " ) + str(top)
            lines.append(sLine)

            # Mon score ?
            if top == currentScore:
                scoreIndex = i - 1

            # Score suivant  
            i+=1

        # Le score n'est pas dans les meilleurs => je l'affiche
        if scoreIndex == -1 :
            line = "Votre score : " + str(currentScore)
            lines += line
            scoreIndex=len(lines) - 1   # On met en surbrillance cette ligne
        else:
            # Modification du tableau => enregistrement
            self._saveScores(tops)

        # Affichage ...
        self.gameHandler_.drawText(lines, "Meilleurs scores", scoreIndex)

        # ... jusqu'à ce que l'utilisateur appuie sur une touche
        inputChar = self.gameHandler_.KEY_NOEVENT
        while self.gameHandler_.KEY_NOEVENT == inputChar:
            inputChar = self.gameHandler_.checkKeyboard()

        # On efface
        self.gameHandler_.clearText()
    
    # Analyse du clavier pendant la phase de jeu
    def _handleGameKeys(self):
        inputChar = self.gameHandler_.checkKeyboard()
        if self.gameHandler_.KEY_STOP == inputChar:
            # Fin de partie
            self.gameHandler_.end()
        elif self.gameHandler_.KEY_RIGHT == inputChar:
            self.gameData_.right()
        elif self.gameHandler_.KEY_LEFT == inputChar:
            self.gameData_.left()
        elif self.gameHandler_.KEY_ROTATE_LEFT == inputChar:
            self.gameData_.rotateLeft()
        elif self.gameHandler_.KEY_DOWN == inputChar:
            self.gameData_.down()
        elif self.gameHandler_.KEY_FALL == inputChar:
            self.gameData_.fall()

    # Mise à jour de la vitesse (ie. délai max. d'attente entre 2 descentes auto.)
    def _updateSpeed(self, currentDuration, level, incLevel = 1):
        if level < MAX_LEVEL_ACCELERATION:
            newDuration = currentDuration
            for _ in range(incLevel):
                newDuration -= (newDuration / (1 + ACCELERATION_STEP))
            return newDuration
        else:
            # Passé le seuil on n'accelère plus
            return currentDuration

    # Menu principal du jeu
    #   retourne True si la partie doit commencer et False pour indiquer la fin du jeu
    def _mainMenu(self):
        self.gameHandler_.drawText(["\"Entrée\" - Démarrer la partie", "\"o\" - Mode ombré", "\"n\" - Mode normal", "\"0\",\"1\",...,\"9\" - Nombre de ligne de handicap  ", "\"q\" - Quitter le jeu"], "Menu")
        
        startGame = True
        quitMenu = False
        
        # Lecture du clavier
        while False == quitMenu:
            inputChar = self.gameHandler_.checkKeyboard()
            #if '' != inputChar : print(inputChar)
            if self.gameHandler_.KEY_NOEVENT != inputChar:
                # Sortie du jeu ?
                if self.gameHandler_.KEY_QUIT == inputChar:
                    quitMenu = True
                    startGame = False
                # Nouvelle partie ?
                #elif self.gameHandler_.KEY_START == inputChar or inputChar == chr(10):
                elif self.gameHandler_.KEY_START == inputChar:
                    quitMenu = True
                    startGame = True
                # Ombre
                elif self.gameHandler_.KEY_SHADOW_MODE == inputChar:
                    self.params_.shadow_ = True
                # Pas d'ombre
                elif self.gameHandler_.KEY_NORMAL_MODE == inputChar:
                    self.params_.shadow_ = False
                # Nombre de ligne de handicap ?
                else:
                    if inputChar < 255 :
                        # C'est un "simple" caractère
                        num = ord(chr(inputChar)) - ord('0')
                        if num >= 0 and num <= 9:
                            self.params_.dirtyLines_ = num

        # On réaffiche l'écran
        self.gameHandler_.clearText()
        return startGame

#
# Boucle principale du jeu
#

# Vérification de la version minimale de python
ver = sys.version_info
if ver.major < PYTHON_MIN_MAJOR or (ver.major == PYTHON_MIN_MAJOR and ver.minor < PYTHON_MIN_MINOR):
    out = str(PYTHON_MIN_MAJOR) + "." + str(PYTHON_MIN_MINOR)
    print("Python doit être au minimum en version", out)
    exit(1) 

# nCurses n'existe pas sous Windows !
if platform.system() == "Windows":
    print("L'application ne fonctionne pas dans l'environnement Windows")
    exit(1)

# Maintenant que les causes d'erreur(s) sont écartées ...
import time
from cursesTetris import cursesTetris
from board import board, tetrisParameters

params = tetrisParameters()

# Pygame est-il disponible ?
try:
    from pygameTetris import pygameTetris
    params.gui_ = True  # Interface graphique disponible
except ModuleNotFoundError:
    # PYGame n'est pas installé
    params.gui_ = False

#
# le jeu ...
#
myTetris = tetris(params) 
if myTetris.isReady():    
    # Démarrage du jeu
    myTetris.start()

    # Fin & libérations
    myTetris.end()
#EOF 