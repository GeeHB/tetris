# coding=UTF-8
#
#   Fichier     :   shapes.py
#
#                   Défintions des 7 tetraminos possibles
#
#                   La valeur numérique correspond à l'indice de la couleur
#
#                   Tous les états (après rotation dans le sens trigo.) sont fournis
#
#                   Chaque rotation est, pour être précis, la combinaison d'un rotation et d'une translation. 
#                   Le référentiel utilisé est celui de Nintendo pour la forme et nCurses pour l'indice des couleurs
#
#   Auteur      :   JHB
#
#   Description :   Définition des tetraminos
#
#   Version     :   0.4.9
#
#   Date        :   15 aout 2020
#

# Les "pièces"
#

# Vert
S = [['.2..',
      '.22.',
      '..2.',
      '...'],
      ['....',
      '.22.',
      '22..',
      '...']]

# Rouge
Z = [['..1.',
      '.11.',
      '.1..',
      '....'],
      ['....',
       '11..',
       '.11.',
       '....']]

# Cyan
# Seulement 2 rotations
I = [['..6.',
      '..6.',
      '..6.',
      '..6.'],
      ['....',
      '....',
      '6666',
      '....']
      ]

# Jaune
# La rotation ne change rien
O = [[ '....',
      '.33.',
      '.33.',
      '....']]

# Gris (pour curse) ou orange
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

# Bleu
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

# Variable globale contenant les 7 tetraminos possibles
shapes = [S, Z, I, O, J, L, T]

# EOF