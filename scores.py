#!/bin/python3

# coding=UTF-8
#
#   File     :   scores.py
#
#   Authors     :   JHB
#
#   Description :   Handle scoring
#
#   Comment    :   Need Python 3.xx or higher
#

import sharedConsts

# scores object
#   Handles scores 
#
class scores(object):
    
    # Members
    #
    user_               = ""        # Current user name
    scores_             = None      # Score list (for all users)
    
    # Construction
    #
    def __init__(self, name):
        self.user_ = name if name else ""
        self._load()

    # Add (or try to add) the current score to the list
    #   return the list of topScores for the current User (or top 10 for all if no user is specified)
    #
    def add(self, newScore):
        
        # Load the scores
        self._load()
        
        # no scores
        tops = [(-1, None)]

        # Add to the list (must be unique)
        if newScore != None and newScore not in self.scores_:
            parse = True
            index = 0
            while parse:
                score = self.scores_[index]
                if newScore > score[0]:
                    self.scores_.insert(index, (newScore, self.user_))
                    parse = False
                elif newScore == score[0]:
                    self.scores_[index] = (newScore, self.user_)    # update the name
                    parse = False
                else:
                    # Next ...
                    index += 1
                    if index == len(self.scores_):
                        parse = False          # end of the list
            
            # Last pos.
            if index == len(self.scores_):
                self.scores_.append((newScore, self.user_))

        # Hall of fame
        if self.user_:
            # Search for user's previous scores in the global table
            parse = True
            index = 0
            while parse:
                score = self.scores_[index]

                if self.user_ == score[1]:
                    # Add to the top list
                    tops.append(score)

                    if score[0] == newScore:                    
                        tops[0] = (len(tops) - 2, None)      # keep its index

                # Next ...
                index += 1
                if index == len(self.scores_) or len(tops) == sharedConsts.SCORES_MAX_COUNT:
                    parse = False                        
        else:
            # Returns the first elements of the global table
            size = len(self.scores_)
            max =  sharedConsts.SCORES_MAX_COUNT if size > sharedConsts.SCORES_MAX_COUNT else size
            for index in range(max):
                score = self.scores_[index]
                tops.append(score)

                # Current score ?
                if score[0] == newScore:                    
                    tops[0] = (len(tops) - 2, None)      # keep its index
        
        # Update on disk
        self._save()
        
        # returns the top list
        return tops
        
    #
    # "Private" methods
    #
    
    # Load all the scores
    #   returns True if scores has been read, False in all other cases
    #
    def _load(self):
        
        self.scores_ = []

        # Read & parse the file
        try:
            file = open(sharedConsts.SCORES_FILE)
            for line in file :
                if len(line) > 0:
                    # remove EOL
                    if line[len(line) - 1] == "\n":
                        line = line[:len(line) - 1]
                    
                    values = line.split(sharedConsts.SCORES_FILE_SEP)
                    if values[0].isnumeric():
                        self.scores_.append((int(values[0]), values[1] if 2 == len(values) else "" ))
            file.close()

            self.scores_.sort(reverse = True)

        except :
           # File doesn't exist or file io error
           self.scores_ = []

        # done ?
        return len(self.scores_) > 0
 
    # Save the scores
    #
    def _save(self):
        try:
            file = open(sharedConsts.SCORES_FILE, "w")
            userCount = 0
            for index in range(len(self.scores_)) :
                line = str(self.scores_[index][0])
                
                if self.scores_[index][1] == self.user_:
                    userCount += 1
                
                if len(self.scores_[index][1]):    
                    line+=sharedConsts.SCORES_FILE_SEP
                    line+=self.scores_[index][1]
                
                if userCount <= sharedConsts.SCORES_MAX_COUNT:
                    line+="\n"
                    file.write(line)
            file.close()
        except:
            return False
        
        # done
        return True  
# EOF