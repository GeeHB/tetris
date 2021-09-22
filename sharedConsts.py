# coding=UTF-8
#
#   File        :   sharedConsts.py
#
#   Authors     :   JHB
#
#   Description :   shared consts for Tetris Game

#   Version     :   0.7.1
#
#   Date        :   2021/09/22
# 

#
#   Public consts
#

# Expected version (minimal)
PYTHON_MIN_MAJOR = 3
PYTHON_MIN_MINOR = 7

# Playfield's dimensions
#
PLAYFIELD_WIDTH = 10
PLAYFIELD_HEIGHT = 20

#
# Scores
#

SCORES_FILE = 'scores.high'     # Scores' file
SCORES_FILE_SEP = ","

SCORES_MAX_COUNT    = 10        # Max. scores per user

# Score valorisation (in %)
SCORE_NO_SHADOW     = 10        # +10% if no pieces'shadowing
SCORE_SPEED_GAME    = 2         # 2% * {piece's height} => quick play <=> more points
SCORE_DIRTY_LINES   = 0.1       # 0.1% per starting dirty-line
SCORE_LEVEL_VALUATION = 15      # 15% more for each level

#
# Timer & game's Levels
#
MAX_LEVEL_ACCELERATION = 15     # No more acceleration when this level is reached
ACCELERATION_STEP = 0.19        # Growing speed % per level
INITIAL_SPEED = 1200            # Level 1 speed (larger is slower)
MOVES_UPDATE_LEVEL = 250        # Change level criterium (# of pieces going down one step)

#
# Colours ID
#
COLOUR_ID_BOARD        = 0
# 1 -> 7 : Pieces colours (nCurses ID)
COLOUR_ID_SHADOW       = 8
COLOUR_ID_TEXT         = 9
COLOUR_ID_BORDER       = 10
COLOUR_ID_BKGRND       = 11

LAST_COLOUR_ID   = COLOUR_ID_BKGRND

#
# Command line options
#

CMD_OPTION_CHAR = "-"

CMD_OPTION_START_LEVEL = "level"
CMD_OPTION_SHADOW = "shadow"
CMD_OPTION_DIRTY_LINES = "lines"
CMD_OPTION_USER = "me"
CMD_OPTION_TOP = "top"

CMD_OPTION_CONSOLE = "c"         # Console mode

# EOF