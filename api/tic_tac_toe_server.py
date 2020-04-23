#!/usr/bin/env python3
import time
import random

from flask import Flask, request

app = Flask(__name__)

random.seed()


"""
TODO
- convert game into a class for organization and to handle multiple games
- Add user UUIDs to be passed between client and server
    - Allows for multiple games to be played at once



"""

# Initialize an empty game board
board = [None] * 9
remainingTiles = list(range(9))
winner = None

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

    return {'move': aiMove, 'game_result': winner, 'taunt': getTaunt(new_game)}

@app.route('/reset', methods=['POST'])
def resetGame():
    aiMove = None

    newGame()   

    return {'move': aiMove, 'game_result': None, 'taunt': getTaunt(new_game=True)}

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
    global board
    move = None

    # Check to see if the player has won. Shouldn't happen, but just in case    
    checkWinner()
    if (not winner):
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
                board[move] = 'O'
                remainingTiles.remove(move)
            else:
                move = None

        # Check to see if a player has won now that the AI has moved
        checkWinner()

    return move


def checkWinner():
    """Checks for a winner to the game
    
    sets global winner value: 
        Player wins: 'X'
        AI wins: 'O' 
        Draw: 'Draw'
        Game not over yet: None
    """
    global winner

    winningLines = [
        [0,1,2], 
        [3,4,5],
        [6,7,8],
        [0,3,6],
        [1,4,7],
        [2,5,8],
        [0,4,8],
        [2,4,6]
    ]

    for a,b,c in winningLines:
        if (board[a] and board[a] == board[b] and board[b] == board[c]):
            winner = board[a]

    if (not remainingTiles and winner is None):
        winner = 'Draw'


def newGame():
    """Resets the game board"""
    global winner
    global board
    global remainingTiles
    winner = None
    board = [None] * 9
    remainingTiles = list(range(9))


def getTaunt(new_game):
    """Gets a taunt to send to the player based on the state of the game"""
    pre_game_taunts = [
        "Do you dare to challenge the champion?", 
        "You can't beat me!", 
        "Beat me if you can!"
    ]

    mid_game_taunts = [
        "You call that a move?!", 
        "That's not going to work!", 
        "I see your X and raise you an O"
    ]

    ai_wins_taunts = [
        "Better luck next time!", 
        "No one beats the champ!",
        "Nice try!"
    ]

    draw_taunts = [
        "You are a true rival",
        "Till we play again",
        "A tip of my hat to you player"
    ]

    player_wins_taunts = [
        "That shouldn't have been able to happen..."
    ]

    if (new_game):
        taunts = pre_game_taunts
    elif (winner == 'O'):
        taunts =  ai_wins_taunts
    elif (winner == 'Draw'):
        taunts = draw_taunts
    elif (winner == 'X'):
        taunts = player_wins_taunts
    else:
        taunts = mid_game_taunts

    return random.choice(taunts)


