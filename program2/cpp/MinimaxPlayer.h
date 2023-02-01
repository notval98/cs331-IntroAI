/*
 * MinimaxPlayer.h
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
 */

#ifndef MINIMAXPLAYER_H
#define MINIMAXPLAYER_H

#include "OthelloBoard.h"
#include "Player.h"
#include <vector>

/**
 * This class represents an AI player that uses the Minimax algorithm to play the game
 * intelligently.
 */
class MinimaxPlayer : public Player {
public:

	/**
	 * @param symb This is the symbol for the minimax player's pieces
	 */
	MinimaxPlayer(char symb);

	/**
	 * Destructor
	 */
	virtual ~MinimaxPlayer();

	/**
	 * @param b The board object for the current state of the board
	 * @param col Holds the return value for the column of the move
	 * @param row Holds the return value for the row of the move
	 */
    void get_move(OthelloBoard* b, int& col, int& row);

	/*
	a struct containing a board, and the col and row of the latest move
	*/
	struct treeNode{
		int col;
		int row;
		OthelloBoard b;
	}; 

    /**
     * @return A copy of the MinimaxPlayer object
     * This is a virtual copy constructor
     */
    MinimaxPlayer* clone();

private:
	/*
	takes the current board and returns a vector of nodes containing
	all successors that can be reached in one move	
	*/
	std::vector<treeNode> successor(OthelloBoard b, char symb);

	//maximizing function
	int maxValue(OthelloBoard b);

	//minimizing function
	int minValue(OthelloBoard b);

	/*
	checks the board and returns the quality of the board
	quality is from the pov of the maximizing player
	the first player to move is the maximizing player
	*/
	int utility(OthelloBoard b);

	/*
	determines if a board is in an end state
	end state is if neither player can make a move
	*/
	bool gameOver(OthelloBoard b);

};


#endif
