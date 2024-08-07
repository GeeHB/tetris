#### Version 0.10.1
* 22 july 2024
* Corrections
    - Correction of pyRight warnings
    - Retrait de la compatibilité avec casioPlot

#### Version 0.9.1
* 25 sept. 2023
* Added
    * consoleTetris.py - abstract class for console clients
    * display.py - Instantiate the valid display mgr
    * casioplotTetris.py - display on a casio calculator
        * casioplotVTetris.py - display vertically
    * -m / --mode to specify GUI mode (auto, console, pygame, casioplot, casioplotv)
    * piece in preview can have different size (smaller in casioplotv mode)
* Corrections
    - Simplify color management (shadow, erase, back block color, ...)

#### Version 0.8.xxx
* 04 aug. 2023
* Added
    * use fast strings
    * Animation when line(s) completed
    * use argparse as command line parser
    * PYGame : Initial window size depends on desktop size !!!
    * getters and setters
* Fixes
    * PyGame Window flickering on ChromeOS
    * BUG : No window resizing on ChromeOS (and avoid scaling !!!)

#### Version 0.7.1
* 22 sept. 2021
+ use of module sharedTools.common for cmdLineParser and colorizer versions

#### v0.6.2
* 06/01/2021
+ minor bug fixes
+ add "-top" command line option to show high (top) scores

#### v0.5.3
* 01/10/2020
+ Linux
    + console mode => OK
+ End of sources translation - I hope so :)
+ Scores handling
+ Press "Enter" to start & quit game
+ Bug fixes
    - Error while displaying and computing Level
    - Escaping the game while playing
    - Game finished : wait for key pressed (Esc ou Quit) to close the window
    - Regression : score and # lines errors
    - Regression : keyboard handling bugs with curses

known issues:
- PYGAME : no window resizing on Linux (tested on Fedora 32)

#### v0.5.2
* 21/09/2020
* Fonctionnal
+ beginning of translation process
+ Add command line options
    - remove "basic" text-based ui
+ resize the pygame::window
+ Minor bug fixes:
    + new acceleration algo (slower at level 1 & faster at level 10)
    - game board no longer sticked to the window's bottom
+ Handle pygame::event.QUIT
+ code review for simplification(s)

#### v0.4.10
* Date : 15/08/2020
* Fixed : Bug PYGame à l'initialisation sous MacOS

#### v0.4.8
* Date : 05/05/2020
* Fixed : PYGame initialization error(s)
