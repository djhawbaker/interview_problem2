#!/usr/bin/env python3
import random

from flask import Flask, request

app = Flask(__name__)

# Setup the seed for the random selection of tiles
random.seed()

"""
TODO
- convert game into a class for organization and to avoid global variables
- Add user UUIDs to be passed between client and server
    - Allows for multiple games to be played at once
"""

# Initialize an empty game board
board = [None] * 9
remainingTiles = list(range(9))
winner = None
availableCorners = [0, 2, 6, 8]
availableSides = [1, 3, 5, 7]

center = 4
corners = [0, 2, 6, 8]
sides = [1, 3, 5, 7]

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


@app.route('/game', methods=['POST'])
def getData():
    """Route to get the player's move and send back the AI's move
    
    Args:
        player_move -- tile the player selected

    Returns:
        move -- The AI's move
        game_result -- None or the winner or Draw
        taunt -- A taunt message from the AI
    """
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
    """Route to reset the game when the button is pressed"""
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
    global availableCorners
    global availableSides
    move = None

    # Check to see if the player has won. Shouldn't happen, but just in case    
    checkWinner()
    if (not winner):
        # Set player's move in board 
        if (player_move is not None):
            board[player_move] = 'X'

            # Update available spaces
            if (player_move in availableCorners):
                availableCorners.remove(player_move)
            elif (player_move in availableSides):
                availableSides.remove(player_move)

            # Verify the tile is still in the list before removing it
            if (player_move in remainingTiles):
                remainingTiles.remove(player_move)

            # If there are any tiles left select the AI's move
            if (remainingTiles):
                
                # Check to see if a move will win the game
                oWinMove = checkForWinMove('O')
                xWinMove = checkForWinMove('X')

                # If O can win, select that 
                if (oWinMove is not None):
                    move = oWinMove

                # If X could win block it
                elif (xWinMove is not None):
                    move = xWinMove

                # If x in corner => o in center 
                elif (player_move in corners):

                    # Pick the center
                    if (board[center] is None):
                        move = pickCenter()

                    # If X is in the center then pick a corner else pick a side
                    elif (board[center] is 'X'):
                        # If the center by X pick a corner
                        if (availableCorners):
                            move = pickCorner()

                        # If all corners are taken pick a side 
                        else:
                            move = pickSide()

                    # If the center is taken pick a side
                    elif (availableSides):
                        move = pickSide()

                    # If all sides are taken pick a corner
                    else:
                        move = pickCorner()
                        
                # If x in center => o in corner
                elif (player_move is center):

                    # Pick a corner
                    if (availableCorners):
                        move = pickCorner()

                    # If all corners taken pick the center
                    elif (board[center] is None):
                        move = pickCenter()

                    # If all sides are taken pick a corner
                    else:
                        move = pickSide()
                    
                # if x on side => o in center
                elif (player_move in sides):

                    # pick the center
                    if (board[center] is None):
                        move = center

                    # If the center is taken Pick a corner
                    elif (availableCorners):
                        move = pickCorner()

                    # If all corners are taken pick a side
                    else:
                        move = pickSide()


                # Update the board with the AI's move
                board[move] = 'O'

                # Update available spaces
                remainingTiles.remove(move)
                if (move in availableCorners):
                    availableCorners.remove(move)
                elif (move in availableSides):
                    availableSides.remove(move)

            else:
                move = None

        # Check to see if a player has won now that the AI has moved
        checkWinner()

    return move


def checkForWinMove(player):
    """AI logic to see if it can win in 1 move

    Args: 
        player -- Which player to check for

    Returns:
        move -- Winning move for input player 
                else None
    """
    move = None

    for a,b,c in winningLines:
        # number of tiles in the row that are the player's
        playerTileCount = 0
        winningMove = None
        otherPlayer = ''

        if (player == 'X'):
            otherPlayer = 'O'
        else:
            otherPlayer = 'X'

        # Loop through the tiles in the line to find a possible win
        for tile in [a, b, c]:
            if (board[tile] is player):
                playerTileCount += 1
            # If a tile is the other player's can't win with this line
            elif (board[tile] is otherPlayer):
                break
            # Tile still available, mark it as a possible winning move
            else:
                winningMove = tile

        # If two of the tiles are the players and the 3rd is empty
        # That's the winning move
        if (playerTileCount is 2 and winningMove is not None):
            move = winningMove
            break

    return move


def pickCenter():
    """Picks the center tile if available"""
    move = None
    
    # Pick the center
    if (board[center] is None):
        move = center

    return move


def pickCorner():
    """Picks a corner tile if available"""
    move = None

    # Pick a corner
    if (availableCorners):
        move = random.choice(availableCorners)

    return move


def pickSide():
    """Picks a side tile if available"""
    move = None
    
    # Pick a side
    if (availableSides):
        move = random.choice(availableSides)

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
    global availableCorners
    global availableSides

    winner = None
    board = [None] * 9
    remainingTiles = list(range(9))
    availableCorners = [0, 2, 6, 8]
    availableSides = [1, 3, 5, 7]


def getTaunt(new_game):
    """Gets a taunt to send to the player based on the state of the game
    
    Args:
        new_game -- bool if it's a new game or not
    """
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

    # Select the taunt based on the game status
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
