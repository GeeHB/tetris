#include <iostream>
using namespace std;

#include <stdio.h>

#include "../piece.h"
#include "../templates.h"
#include "../tetrisGame.h"

int main()
{
#ifdef _DEBUG
    cout << "Super il va y avoir des sorties !!!" << endl  << endl;;
#endif // _DEBUG

    // Ma piece ...
	piece mp;

	// Ajout des rotations ...
	mp.addPiece(I_0);
	mp.addPiece(I_1);

	mp.print(0);
	mp.print(1);

	// Mon espace de jeu
	tetrisGame myBoard;
	tetrisParameters params;

	params.dirtyLines_ = 7;
	myBoard.setParameters(params);

	if (myBoard.checkEnvironment()) {
		myBoard.start();

		myBoard.down();
		myBoard.left();
		myBoard.down();
		myBoard.left();
		myBoard.down();

		myBoard.fall();
	}

	myBoard.print();

    return 0;
}

// EOF
