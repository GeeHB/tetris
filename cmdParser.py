#!/usr/bin/python3
#
# coding=UTF-8
#
#   File     :   cmdParser.py
#
#   Author     :   JHB
#
#   Description :   cmdParser object for command-line analysis 
#
#   Comment    :   Need Python 3.xx or higher
#
import argparse
import consts
from sharedTools import colorizer as color
from board import tetrisParameters

# cmdPaser object
#   Command-line parser 
#
class cmdParser(object):
    # Members
    #
    txtColours_ = color.colorizer(colored = None)
    params_ = tetrisParameters()

    # Access
    #
    def parameters(self):
        return self.params_
    
    # Parse the command line
    #
    #   return True if no error where found
    #
    def parse(self):
        
        parser = argparse.ArgumentParser(epilog = self.version())
 
        # Define parameters
        #
         
        # High scores
        parser.add_argument(consts.ARG_TOP_S, consts.ARG_TOP, action='store_true', help = consts.COMMENT_TOP, required = False)
        
        # Display shadow ?
        parser.add_argument(consts.ARG_SHADOW_S, consts.ARG_SHADOW, action='store_true', help = consts.COMMENT_SHADOW, required = False)

        # Display mode ?
        parser.add_argument(consts.ARG_MODE_S, consts.ARG_MODE, help = consts.COMMENT_MODE, required = False, nargs = 1, default = [consts.MODE_AUTO], type=str, choices=[consts.MODE_AUTO, consts.MODE_CONSOLE, consts.MODE_CASIOPLOT, consts.MODE_CASIOPLOTV, consts.MODE_PYGAME])

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
        
        # Display mode
        self.params_.mode_ = args.mode[0]

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
    
    # Display app version infos
    #
    #   return a string
    #
    def version(self, verbose = True):
        if None == self.txtColours_:
            self.txtColours_ = color.colorizer(True)

        return f"{self.txtColours_.colored(consts.APP_NAME, formatAttr=[color.textAttribute.BOLD], datePrefix=(False == verbose))} by {consts.APP_AUTHOR} - release {consts.APP_CURRENT_VERSION} - {consts.APP_RELEASE_DATE}"

# EOF