# 2048_GameProgLangCompiler


The task is to make a parser-translator (that mean a complete syntax-directed translation scheme) for a game programming language.

It is a 2048-game ”family”: Here, variations on the original 2048 game are to be also provided
for. The variations are:
1. Allowing subtraction, multiplication and division in addition to the plain doubling
operation at tile mergers. Thus, each move, when it is making two same-value tiles
merge, may obliterate them together (making them 0 by subtraction), or reduce them
to 1 by divition, or square them by multiplication. In this variation, the goal also will
be flexible, any number not necessarily a power of 2 will be achievable.
2. Allowing variables in place of tile values to make puzzles: enabling questions like how
many operations it would take at the least, to double the maximum tile value in this
position?
Thus, the elementary operations of the 2048 game are to be provided, and little tweaks to
them to allow all four arithmetic operations and variables are to be added.


README

Libraries needed: pip3 and sly

pip3 install sly


Run the code:

python3 COMPILER.py


The entire code is modularized. COMPILER.py contains the modularized Lexer, Parser and Tree.

GAME.py contains a modularized version of 2048.



The code implements 2048 in an implementation where subtract left on 4,2,2,4 gives 4,4,0,0.

The other implementations can be added, with slight changes in code due to the modularity,
but to keep it as a game which even children can play, one implementation is followed.

The code can do the following ERROR Handling:

1. Tells if deadend is reached and give option to continue(can be modified to get more future moves).
	
	for example, if all tiles are filled and left, right operations arent possible then the 
	parser identifies it and divides it into 2 cases.

	a. UP/DOWN moves are possible. The code tells the user to think of a better approach, that
	   is choose UP/DOWN rather than LEFT/RIGHT.

	b. IF UP/DOWN operations arent possible too, then the code suggests user to use assign statement
	   as it is the only way to get out of the deadlock and keep playing for eternity.

2. Detect missing fullstops for known commands.

3. Detect FLOATS in cases.

4. Detect out of bound assignments for example if ASSIGN 2 TO 5,5 is said then invalid tile is outputted.

5. SLY by default doesnt allow TOKENS to be used as variables, so that is also taken care of.

6. Syntax Error for other cases where the command is incorrect.
