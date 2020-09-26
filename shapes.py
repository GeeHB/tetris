# coding=UTF-8
#
#   File     :   shapes.py
#
#                   Definition of the 7 tetraminos
#
#                   The num. value is the colour ID. Colours'IDS are based on nCurses index

#                   A piece is given with all its postions after rotation in trignometric direction
#                   Each "rotation", to be precise, is a combination of a rotation and a translation
#                   
#                   Based on Nintendo for pieces and rotation. 
#
#   Authors     :   JHB
#
#   Description :   tetraminos definitions
#
#   Version     :   0.5.2
#
#   Date        :   2020/09/21
#

# Different pieces and their rotations
#

# Green
S = [['.2..',
      '.22.',
      '..2.',
      '...'],
      ['....',
      '.22.',
      '22..',
      '...']]

# Red
Z = [['..1.',
      '.11.',
      '.1..',
      '....'],
      ['....',
       '11..',
       '.11.',
       '....']]

# Cyan
I = [['..6.',
      '..6.',
      '..6.',
      '..6.'],
      ['....',
      '....',
      '6666',
      '....']
      ]

# Yellow
O = [[ '....',
      '.33.',
      '.33.',
      '....']]

# Grey (for curse) or orange
L = [['77..',
      '.7..',
      '.7..',
      '....'],
      ['....',
      '777.',
      '7...',
      '....'],
      ['.7..',
      '.7..',
      '.77.',
      '....'],
      ['..7.',
      '777.',
      '....',
      '....']]

# Blue
J = [['.4..',
      '.4..',
      '44..',
      '....'],
      ['....',
      '444.',
      '..4.',
      '....'],
      ['.44.',
      '.4..',
      '.4..',
      '....'],
      ['4...',
       '444.',
      '....',
      '....']
      ]

# Violet
T = [['.5..',
      '55..',
      '.5..',
      '....'],
      ['....',
       '555.',
       '.5..',
      '....'],
      ['.5..',
       '.55.',
       '.5..',
      '....'],
      ['.5..',
       '555.',
       '....',
       '....']]

# List of all the pieces
shapes_ = [S, Z, I, O, J, L, T]

# EOF