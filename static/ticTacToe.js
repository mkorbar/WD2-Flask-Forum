
const PLAYER_1 = 'X';
const PLAYER_2 = 'O';

var currentPlayer = PLAYER_1;

var board = [
            ['','',''],
            ['','',''],
            ['','',''],
            ];


function makeMove(x, y) {
  if(board[x-1][y-1] !== '') {
    alert('Invalid move!!!!')
    return;
  }
  board[x-1][y-1] = currentPlayer;

  displayBoard();
  if (isGameFinished()){
      alert('game finished');
      resetBoard();
  } else {
  switchPlayer();
  }
}


function switchPlayer() {
  if(currentPlayer == PLAYER_1) {
    currentPlayer = PLAYER_2;
  }else{
    currentPlayer = PLAYER_1;
  }
}

function displayBoard() {
  document.getElementById('box1-1').innerHTML = board[0][0];
  document.getElementById('box1-2').innerHTML = board[0][1];
  document.getElementById('box1-3').innerHTML = board[0][2];

  document.getElementById('box2-1').innerHTML = board[1][0];
  document.getElementById('box2-2').innerHTML = board[1][1];
  document.getElementById('box2-3').innerHTML = board[1][2];

  document.getElementById('box3-1').innerHTML = board[2][0];
  document.getElementById('box3-2').innerHTML = board[2][1];
  document.getElementById('box3-3').innerHTML = board[2][2];
}

function isGameFinished() {
  // po vrsticah
  if (
  board[0][0] !== '' &&  board[0][0] == board[0][1] && board[0][0] == board[0][2] ||
  board[1][0] !== '' &&  board[1][0] == board[1][1] && board[1][0] == board[1][2] ||
  board[2][0] !== '' &&  board[2][0] == board[2][1] && board[2][0] == board[2][2]
  ) {
  console.log('zmaga po vrsticah');
  return true
  }
  // po stolpcih
  if (
  board[0][0] !== '' &&  board[0][0] == board[1][0] && board[0][0] == board[2][0] ||
  board[0][1] !== '' &&  board[0][1] == board[1][1] && board[0][1] == board[2][1] ||
  board[0][2] !== '' &&  board[0][2] == board[1][2] && board[0][2] == board[2][2]
  ) {
  console.log('zmaga po stolpcih');
  return true
  }
  // po diagonalah
  if (
  board[0][0] !== '' &&  board[0][0] == board[1][1] && board[0][0] == board[2][2] ||
  board[0][2] !== '' &&  board[0][2] == board[1][1] && board[0][2] == board[2][0]
  ) {
  console.log('zmaga po diagonali');
  return true;
  }
  return false;
}

function resetBoard(){
  board = [
            ['','',''],
            ['','',''],
            ['','',''],
            ];
  currentPlayer = PLAYER_1;
  displayBoard();
};

// logika za zmago
// resetiraj igro
