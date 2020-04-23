#!/usr/bin/env python3
import time
import random

from flask import Flask, request

app = Flask(__name__)

random.seed()

# Initialize an empty game board
board = [None] * 9
remainingTiles = list(range(9))


@app.route('/game', methods=['POST'])
def getData():
    aiMove = None
    new_game = False
    
    req_data = request.get_json()

    if (req_data.get('reset') is True):
        newGame()   
        new_game = True

    elif (req_data.get('player_move') is not None):
        aiMove = getMove(req_data.get('player_move'))

    return {'move': aiMove, 'game_result': checkWinner(), 'taunt': getTaunt(new_game)}

def getMove(player_move):
    """Returns what move the AI will make

    Args: 
        player_move -- players move

    Returns:
        AI move tile number 
        0 1 2
        3 4 5 
        6 7 8 
    """
    move = None
    # Set player's move in board 
    if (player_move is not None):
        board[player_move] = 'X'
        # Verify the tile is still in the list
        if (player_move in remainingTiles):
            remainingTiles.remove(player_move)

        # Make sure the player didn't win (can't happen, but just to be safe)
        #checkWinner()


        # Check to see if a move will win the game
        """
        winMove = checkForWinMove()
        if (winMove):
            move = winMove
        elif (
        """

        # Select a random remaining tile
        if (remainingTiles):
            move = random.choice(remainingTiles)
            remainingTiles.remove(move)
        else:
            move = None

    return move


def checkWinner():
    """Checks for a winner to the game and returns the result
    
    Returns: 
        Player wins: 'player'
        AI wins: 'ai' 
        Draw: 'draw'
        Game not over yet: None

    """
    # TODO
    return None


def newGame():
    """Resets the game board"""
    board = [None] * 9
    remainingTiles = list(range(9))


def getTaunt(new_game):
    taunts = ["You can't beat me!", "Beat me if you can!"]

    if (not new_game):
        taunts += ["You call that a move?!", "Nice try!"]

    return random.choice(taunts)


