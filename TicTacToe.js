const board = document.getElementById("board");
const cells = document.querySelectorAll(".cell");
let gameBoard = [
[null, null, null],
[null, null, null],
[null, null, null],
];

function updateBoard() {
cells.forEach((cell) => {
    const row = cell.getAttribute("data-row");
    const col = cell.getAttribute("data-col");
    cell.textContent = gameBoard[row][col];
});
}

function checkWin(player) {
const winPatterns = [
    [
    [0, 0],
    [0, 1],
    [0, 2],
    ],
    [
    [1, 0],
    [1, 1],
    [1, 2],
    ],
    [
    [2, 0],
    [2, 1],
    [2, 2],
    ],
    [
    [0, 0],
    [1, 0],
    [2, 0],
    ],
    [
    [0, 1],
    [1, 1],
    [2, 1],
    ],
    [
    [0, 2],
    [1, 2],
    [2, 2],
    ],
    [
    [0, 0],
    [1, 1],
    [2, 2],
    ],
    [
    [0, 2],
    [1, 1],
    [2, 0],
    ],
];

return winPatterns.some((pattern) =>
    pattern.every(([r, c]) => gameBoard[r][c] === player)
);
}

function isDraw() {
return gameBoard.every((row) => row.every((cell) => cell !== null));
}

function resetGame() {
// Reset game board to initial state
gameBoard = [
    [null, null, null],
    [null, null, null],
    [null, null, null],
];
// Clear the UI
const cells = document.querySelectorAll(".cell");
cells.forEach((cell) => (cell.textContent = ""));

}

function playerMove(row, col) {
if (gameBoard[row][col] === null) {
    gameBoard[row][col] = "X";
    updateBoard();
    if (checkWin("X")) {
    alert("Player X wins!");
    resetGame();
    } else if (isDraw()) {
    alert("It's a draw!");
    resetGame();
    } else {
    computerMove();
    }
}
}


function computerMove() {
fetch("http://127.0.0.1:5000/move", {
    method: "POST",
    headers: {
    "Content-Type": "application/json",
    },
    body: JSON.stringify({ board: gameBoard }),
})
    .then((response) => response.json())
    .then((data) => {
    const { row, col } = data;
    gameBoard[row][col] = "O";
    updateBoard();
    if (checkWin("O")) {
        alert("Computer wins!");
        resetGame();
    } else if (isDraw()) {
        alert("It's a draw!");
    }
    });
}

cells.forEach((cell) => {
cell.addEventListener("click", () => {
    const row = cell.getAttribute("data-row");
    const col = cell.getAttribute("data-col");
    playerMove(row, col);
});
});

updateBoard();

let playbt = document.querySelector("#play");
playbt.addEventListener("click",()=>{
    resetGame();
});