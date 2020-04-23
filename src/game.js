import React, { useState, useEffect } from 'react';
import './game.css';

function Tile(props) {
  return (
    <button className="tile" onClick={props.onClick}>
      {props.value}
    </button>
  );
}

class Board extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        tiles: Array(9).fill(null)
    }


  }

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

function Game() {

  const [taunt, setTaunt] = useState("");
  const [next_move, setMove] = useState(0);
  const [game_result, setResult] = useState(0);

  const tiles = Array(9).fill(null);

  useEffect(() => {
    fetch('/game').then(res => res.json()).then(data => {
        setTaunt(data.taunt);
        setMove(data.move);
        setResult(data.game_result);
     })
  }, []);

  return (
    <div className="Game">
      <div className="Game-title">
        <div>{"Tic Tac Toe"}</div>
        <div className="Game-welcome">
          {"Welcome to the game. Want to play?"}
        </div>
          <Board
            tiles={tiles}
          />
          <div className="Game-info">
            <div>{"AI: " + taunt}</div>
            <div>{"Next Move: " + next_move}</div>
            <div>{"Game Result: " + game_result}</div>
          </div>
      </div>
    </div>
  );
}

export default Game;
