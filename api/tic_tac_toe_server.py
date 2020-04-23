#!/usr/bin/env python3
import time
import random

from flask import Flask

app = Flask(__name__)

random.seed()

@app.route('/game', methods=['GET', 'POST'])
def getData(tile=None):
    return {'move': getMove(tile), 'game_result': checkWinner(), 'taunt': getTaunt()}


def getMove(tile):
    """Returns what move the AI will make

    Args: 
        tile -- players move

    Returns:
        AI move tile number 
        1 2 3
        4 5 6
        7 8 9
    """
    # TODO
    move = 4

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


def getTaunt():
    taunts = ["You can't beat me!", "Beat me if you can!"]
    return random.choice(taunts)

