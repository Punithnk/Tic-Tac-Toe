const boardElement = document.getElementById("board");
const statusElement = document.getElementById("status");
const resetButton = document.getElementById("resetBtn");

const board = Array(9).fill("");
let currentPlayer = "X";
let gameOver = false;

/**
 * Create 9 clickable cells, attach event listeners, and render initial state.
 */
function initBoard() {
  boardElement.innerHTML = "";
  for (let i = 0; i < 9; i++) {
    const cell = document.createElement("button");
    cell.className = "cell";
    cell.dataset.index = i;
    cell.addEventListener("click", () => handleMove(i));
    boardElement.appendChild(cell);
  }
  updateStatus(`Player ${currentPlayer}'s turn`);
}

/**
 * Handle a player's move when a cell is clicked.
 * @param {number} index - The index of the clicked cell.
 */
function handleMove(index) {
  if (gameOver) {
    updateStatus("Game over. Reset to play again.");
    return;
  }

  if (board[index] !== "") {
    updateStatus("Cell already filled. Choose another.");
    return;
  }

  board[index] = currentPlayer;
  renderBoard();

  if (checkWinner()) {
    highlightWinningCells();
    updateStatus(`Player ${currentPlayer} wins!`);
    gameOver = true;
    return;
  }

  if (board.every((cell) => cell !== "")) {
    updateStatus("It's a draw!");
    gameOver = true;
    return;
  }

  currentPlayer = currentPlayer === "X" ? "O" : "X";
  updateStatus(`Player ${currentPlayer}'s turn`);
}

/**
 * Update each cell's text and styling based on board state.
 */
function renderBoard() {
  const cells = boardElement.querySelectorAll(".cell");
  cells.forEach((cell, index) => {
    cell.textContent = board[index];
    cell.classList.toggle("filled", board[index] !== "");
  });
}

/**
 * Update the status message displayed to the user.
 * @param {string} message
 */
function updateStatus(message) {
  statusElement.textContent = message;
}

/**
 * Determine whether the current board state contains a winning line.
 * @returns {boolean}
 */
function checkWinner() {
  const lines = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
  ];

  return lines.some(([a, b, c]) => {
    const win = board[a] && board[a] === board[b] && board[a] === board[c];
    if (win) {
      boardElement.dataset.winner = JSON.stringify([a, b, c]);
    }
    return win;
  });
}

/**
 * Highlight winning cells when a player wins.
 */
function highlightWinningCells() {
  const cells = boardElement.querySelectorAll(".cell");
  const winnerLine = JSON.parse(boardElement.dataset.winner || "[]");
  winnerLine.forEach((index) => {
    cells[index].classList.add("win");
  });
}

/**
 * Reset all game state to start a fresh round.
 */
function resetGame() {
  for (let i = 0; i < board.length; i++) {
    board[i] = "";
  }
  currentPlayer = "X";
  gameOver = false;
  boardElement.dataset.winner = "";

  const cells = boardElement.querySelectorAll(".cell");
  cells.forEach((cell) => cell.classList.remove("win"));

  renderBoard();
  updateStatus(`Player ${currentPlayer}'s turn`);
}

resetButton.addEventListener("click", resetGame);
initBoard();


