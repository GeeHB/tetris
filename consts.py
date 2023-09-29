# coding=UTF-8
#
#   File        :   consts.py
#
#   Author     :   JHB
#
#   Description :   shared consts for Tetris Game

#
#   Public consts
#

APP_NAME = "tetris.py"
APP_CURRENT_VERSION = "0.9.1"
APP_RELEASE_DATE = "25 sept. 2023"
APP_AUTHOR_SHORT = "GeeHB"
APP_AUTHOR = f"{APP_AUTHOR_SHORT} (j.henrybarnaudiere@gmail.com)"

# Expected version (minimal)
PYTHON_MIN_MAJOR = 3
PYTHON_MIN_MINOR = 7

# Playfield's dimensions (in box unit)
#
PLAYFIELD_WIDTH = 10
PLAYFIELD_HEIGHT = 20

#
# Scores
#

SCORES_FILE = "scores.high"     # Scores' file
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
COLOUR_ID_ANIMATE      = 12     # animation When line if full

LAST_COLOUR_ID   = COLOUR_ID_ANIMATE

#
# A few basic colours
#
COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)
COLOUR_RED = (255, 0, 0)
COLOUR_GREEN = (0, 255, 0)
COLOUR_YELLOW = (255, 255, 0)
COLOUR_BLUE = (0, 0, 255)
COLOUR_PURPLE = (255, 0, 255)
COLOUR_CYAN = (0, 255, 255)
COLOUR_ORANGE = (255, 128, 0)

COLOUR_LTGREY = ( 192, 192, 192)
COLOUR_GREY = ( 128, 128, 128)
COLOUR_DKGREY = ( 32, 32, 32)

#
# Command line options
#

ARG_STARTLEVEL_S = "-l"
ARG_STARTLEVEL   = "--level"
COMMENT_STARTLEVEL = "Choose starting level"

MIN_LEVEL = 1
MAX_LEVEL = 15
DEF_LEVEL =  MIN_LEVEL

ARG_SHADOW_S    = "-s"
ARG_SHADOW      = "--shadow"
COMMENT_SHADOW  = "Display piece shadow"

ARG_DIRTY_S     = "-d"
ARG_DIRTY       = "--dirty"
COMMENT_DIRTY   = "Start game with dirty lines"

ARG_USER_S      = "-u"
ARG_USER        = "--user"
COMMENT_USER    = "Set user name"

ARG_TOP_S       = "-t"
ARG_TOP         = "--top"
COMMENT_TOP     = "Show top scores"

ARG_CONSOLE_S   = "-c "                # Console mode
ARG_CONSOLE     = "--console"
COMMENT_CONSOLE = "Force displays in console mode (using nCurses if available)"

ARG_MODE_S      = "-m"
ARG_MODE        = "--mode"
COMMENT_MODE    = "Choose display mode"

MODE_AUTO = "auto"              # Search for the best GUI mode (default mode)
MODE_CONSOLE = "console"        # Console mode using nCurses
MODE_CASIOPLOT = "casioplot"    # GUI using casioplot library 
MODE_CASIOPLOTV = "casioplotv"    # GUI using casioplot library vertically
MODE_PYGAME = "pygame"          # Use PYGame library

# EOF