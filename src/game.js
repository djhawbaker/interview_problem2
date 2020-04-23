import React from 'react';
import './game.css';

function Tile(props) {
  return (
    <button className="tile" onClick={props.onClick}>
      {props.value}
    </button>
  );
}

class Board extends React.Component {

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

  constructor(props) {
    super(props);

    this.state = {
        tiles: Array(9).fill(null),
        moveNumber: 0,
        taunt: '',
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
     const newTiles = this.state.tiles.slice();

     if (newTiles[i]) {
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
     // Tell the server to reset the game 
     postData('/game', {'reset': true}).then((data) => {

         // Update local states
         this.setState({
            tiles: Array(9).fill(null),
            taunt: data.taunt,
            next_move: data.move,
            game_result: data.game_result
         });
     });
  }


  render() {
      const currentTiles = this.state.tiles;


      return (
        <div className="Game">
          <div className="Game-title">
            <div>{"Tic Tac Toe"}</div>
            <div className="Game-welcome">
              {"Welcome to the game. Want to play?"}
            </div>
              <Board
                tiles={currentTiles}
                onClick={i => this.handleTileClick(i)}
              />
              <div className="Game-info">
                <button onClick={() => this.handleResetClick()}>{"New Game"}</button>
                <div>{"AI: " + this.state.taunt}</div>
                <div>{"Next Move: " + this.state.next_move}</div>
                <div>{"Game Result: " + this.state.game_result}</div>
              </div>
          </div>
        </div>
      );
  }
}

export default Game;
