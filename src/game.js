import React from 'react';
import './game.css';

function Tile(props) {
  // Each tile of the game board that is clickable
  return (
    <button className="tile" onClick={props.onClick}>
      {props.value}
    </button>
  );
}

class Board extends React.Component {
  // Render a tic tac toe board of 3 rows and 3 columns of tiles

  renderTile(i) {
    return (
      <Tile
        value={this.props.tiles[i]}
        onClick={() => this.props.onClick(i)}
      />
    );
  }

  render() {
    return (
      <div>
        <div className="board-row">
          {this.renderTile(0)}
          {this.renderTile(1)}
          {this.renderTile(2)}
        </div>
        <div className="board-row">
          {this.renderTile(3)}
          {this.renderTile(4)}
          {this.renderTile(5)}
        </div>
        <div className="board-row">
          {this.renderTile(6)}
          {this.renderTile(7)}
          {this.renderTile(8)}
        </div>
      </div>
    );
  }
}

async function postData(url = '', data = {}) {
    // Function to send POST data to the server and wait for a response
    // Non blocking
    const response = await fetch(url, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data)
    });

    return response.json();
}

class Game extends React.Component {
  // The main game class that handles the client side 
  // logic, display and interaction

  constructor(props) {
    super(props);

    this.state = {
        tiles: Array(9).fill(null),
        moveNumber: 0,
        taunt: 'Want to play a game?',
        next_move: 0,
        game_result: null
    };

    fetch('/game').then(res => res.json()).then(data => {
        this.state.taunt = data.taunt;
        this.state.next_move = data.move;
        this.state.game_result = data.game_result;
    
    }, []);
  }

  handleTileClick(i) {
     // Function called when user clicks on a game tile
     const newTiles = this.state.tiles.slice();

     // Don't let the player make a move if 
     // 1. The tile is already taken
     // 2. The game is over
     if (newTiles[i] || this.state.game_result) {
        return;
     }
     newTiles[i] = 'X';

     // Tell the server what move was made 
     postData('/game', {'player_move': i}).then((data) => {
         // Set the AI's move
         newTiles[data.move] = 'O';

         // Update local states
         this.setState({
            tiles: newTiles,
            taunt: data.taunt,
            next_move: data.move,
            game_result: data.game_result
         });
     });
  }

  handleResetClick() {
     // Tell the server to reset the game when the new game button is pressed
     postData('/reset', {}).then((data) => {

         // Update local states
         this.setState({
            tiles: Array.from(this.state.tiles, x => null),
            taunt: data.taunt,
            next_move: data.move,
            game_result: data.game_result
         });
     });
  }


  render() {
      const currentTiles = this.state.tiles;

      let game_result_str
      if (this.state.game_result) {
          if (this.state.game_result == 'Draw') {
              game_result_str = "Game ended in a draw. Good luck next time!";
          } else {
              game_result_str = this.state.game_result + " is the winner!!";
          }
      } else {
          game_result_str = "";
      }

      return (
        <div className="Game">
          <div className="Game-title">
            <div>{"Tic Tac Toe"}</div>
            <div className="Game-welcome">
              {"Welcome to the game"}
            </div>
              <Board
                tiles={currentTiles}
                onClick={i => this.handleTileClick(i)}
              />
              <div className="Game-info">
                <div>{"AI: " + this.state.taunt}</div>
              </div>
              <div className="Game-info">
                <div>{game_result_str}</div>
              </div>
              <div className="Game-info">
                <button onClick={() => this.handleResetClick()}>{"New Game"}</button>
              </div>
              <div className="Game-signature">
                <div>{"Created by David Hawbaker"}</div>
              </div>
          </div>
        </div>
      );
  }
}

export default Game;
