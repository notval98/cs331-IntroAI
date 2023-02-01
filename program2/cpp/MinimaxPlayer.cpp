/*
 * MinimaxPlayer.cpp
 *
 *  Created on: Apr 17, 2015
 *      Author: wong
 */
#include <iostream>
#include <assert.h>
#include <algorithm>
#include "MinimaxPlayer.h"

using std::vector;

MinimaxPlayer::MinimaxPlayer(char symb) :
		Player(symb) {

}

MinimaxPlayer::~MinimaxPlayer() {

}

std::vector<MinimaxPlayer::treeNode> MinimaxPlayer::successor(OthelloBoard b, char symb)
{
	std::vector<MinimaxPlayer::treeNode> validMoves;

	for(int row = 0; row < b.get_num_rows(); row++)
	{
		for(int col = 0; col < b.get_num_cols(); col++)
		{
			if(b.is_legal_move(col, row, symb) && b.is_cell_empty(col, row))
			{
				OthelloBoard temp = b;
				temp.play_move(col, row, symb);
				treeNode toAdd = {col, row, temp};
				validMoves.push_back(toAdd);
			}
		}
	}
	return validMoves;
}

int MinimaxPlayer::maxValue(OthelloBoard b)
{
	std::vector<treeNode> children;
	if(gameOver(b))
	{
		return utility(b);
	}

	//initialize to neg infinity
	int v = -9999;

	//p1 is maximizing
	char symb = b.get_p1_symbol();
	children = successor(b, symb);

	for(int i = 0; i < children.size(); i++)
	{
		v = std::max(v, minValue(children[i].b));
	}

	return v;
}

int MinimaxPlayer::minValue(OthelloBoard b)
{
	std::vector<treeNode> children;
	if(gameOver(b))
	{
		return utility(b);
	}

	//initialize to pos infinity
	int v = 9999;

	//p2 is minimizing
	char symb = b.get_p2_symbol();
	children = successor(b,symb);

	for(int i = 0; i < children.size(); i++)
	{
		v = std::min(v, maxValue(children[i].b));
	}

	return v;
}

void MinimaxPlayer::get_move(OthelloBoard* b, int& col, int& row) 
{
    // To be filled in by you
	treeNode bestBoard = {-1, -1, *b};
	int minBest = 9999;
	int maxBest = -9999;

	//get first level of successors
	std::vector<treeNode> children = successor(*b, get_symbol());

	for(int i = 0; i < children.size(); i++)
	{
		if(b->get_p1_symbol() == get_symbol())
		{
			int v = minValue(children[i].b);
			if(v > maxBest)
			{
				maxBest = v;
				bestBoard = children[i];
			}
		}
		else
		{
		
			int v = maxValue(children[i].b);
			if( v < minBest)
			{
				minBest = v;
				bestBoard = children[i];
			}
		}
	}
	//play the col and row from best board
	col = bestBoard.col;
	row = bestBoard.row;
}

bool MinimaxPlayer::gameOver(OthelloBoard b)
{
	if(!b.has_legal_moves_remaining(b.get_p2_symbol()) && !b.has_legal_moves_remaining(b.get_p1_symbol()))
	{
		return true;
	}
	else
	{
		return false;
	}
}

int MinimaxPlayer::utility(OthelloBoard b) 
{
	int p1Score = b.count_score(b.get_p1_symbol());
	int p2Score = b.count_score(b.get_p2_symbol());

	return p1Score - p2Score;
}

MinimaxPlayer* MinimaxPlayer::clone() {
	MinimaxPlayer* result = new MinimaxPlayer(symbol);
	return result;
}
