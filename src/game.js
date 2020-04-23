import React, { useState, useEffect } from 'react';

function Game() {

  const [taunt, setTaunt] = useState("");
  const [next_move, setMove] = useState(0);
  const [game_result, setResult] = useState(0);

  useEffect(() => {
    fetch('/game').then(res => res.json()).then(data => {
        setTaunt(data.taunt);
        setMove(data.move);
        setResult(data.game_result);
     })
  }, []);

  return (
    <div className="game">
      <div className="game-info">
        <div>{"AI Taunt: " + taunt}</div>
        <div>{"Next Move: " + next_move}</div>
        <div>{"Game Result: " + game_result}</div>
      </div>
    </div>
  );
}

export default Game;
