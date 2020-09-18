# coding=UTF-8
#
#   File     :   cmdLineParser.py
#
#   Author      :   JHB
#
#   Description :   Définition des objets :
#                     - cmdLineParser : Gestion de la ligne de commandes
#
#   Remarque    :  
#
#   Version     :   0.1.25-2
#
#   Date        :   3 mars 2020
#

import sys

#
#   cmdLineParser  - Gestion de la ligne de commandes
#
class cmdLineParser:
    # Données membres
    #
    optionChar_ = ""        # Caractère précédent les options
    assignChar_ = " "       # Caractère d'assignation / affectation

    options_    = 0         # Nombre d'options(restantes) dans la ligne de commandes

    NO_INDEX    = -1
    
    # Construction
    def __init__(self, optionChar = "-"):
        self.optionChar_ = optionChar
        
        # Analyse des paramètres de la ligne de commande
        self._parse()

    # Nombre total d'éléments
    def size(self):
        # On retire le nom du "programme"
        return (len(sys.argv) - 1)

    # Nombre d'options / paramètres
    def options(self):
        return self.options_

    # Accès
    #

    # Accès à un paramètre (ou valeur) par son index
    def at(self, index):
        if index > self.size() or index < 0:
            raise IndexError()

        # Valeur à l'index
        return sys.argv[index]

    # Accès à une valeur
    #   retourne le tuple {l'option / ou la valeur selon son index, option ? }
    def parameterOrValue(self, index):
        if index >= self.size() or index < 0:
            raise IndexError()

        # Valeur à l'index
        value = sys.argv[index + 1]

        # Une option ?
        if not value[0] == self.optionChar_:
            # non, une valeur ...
            # est ce une chaine de caractères quotée ?
            lenV = len(value)
            if value[0] == '/"' and value[lenV - 1] == '/"':
                value = value[1:lenV - 1]

        return (value, value[0] == self.optionChar_)

    
    # Recherche d'une option par son nom
    #   retourne son index ou NO_INDEX (-1) si l'option n'existe pas
    def findOption(self, name, remove):
        # Pas de nom => pas d'index valable
        if not 0 == len(name):
            index = 0
            searchedName = self.optionChar_ + name
            for parameter in sys.argv:
                if parameter == searchedName:
                    # Trouvé
                    if True == remove:
                        self.options_-=1
                    return (index - 1)
                
                # paramètre suivant
                index+=1

        # Pas trouvé
        return self.NO_INDEX

    # Recherche et retrait si existante d'une option
    # l'option peut avoir plusieurs noms
    #   retourne son index ou NO_INDEX (-1) si l'option n'existe pas
    def old_findAndRemoveOption(self, name, altName = None):
        # On recherche le premier nom
        index = self.findOption(name, True)
        if index == self.NO_INDEX:
            # On recherche la valeur alternative (si elle est fournie)
            return self.NO_INDEX if None == altName else self.findOption(altName, True)
        return index

    # Nombre variable de paramètres ayant la même signification ...
    def findAndRemoveOption(self, *args):          
        for name in args:
            # Les paramètres par ordre ....
            index = self.findOption(name, True)
            
            # Trouvé ?
            if not self.NO_INDEX == index:
                return index
        
        # Non trouvé
        return self.NO_INDEX

    #
    # Méthodes privées
    # 

    # Première analyse de la ligne de commande
    def _parse(self):
        self.options_ = 0

        for parameter in sys.argv:
            if parameter[0] == self.optionChar_:
                # Une option de +
                self.options_+=1
# EOF