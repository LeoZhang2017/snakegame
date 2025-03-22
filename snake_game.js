const GRID_SIZE = 25;
const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 600;
const GRID_WIDTH = Math.floor(CANVAS_WIDTH / GRID_SIZE);
const GRID_HEIGHT = Math.floor(CANVAS_HEIGHT / GRID_SIZE);

// Colors
const COLORS = {
    MINT: '#b7e4c7',
    WHITE: '#ffffff',
    COIN_5: '#ffffcc',
    COIN_10: '#ffdfba',
    COIN_15: '#ffb6c1'
};

class Snake {
    constructor() {
        this.reset();
    }

    reset() {
        this.positions = [{
            x: Math.floor(GRID_WIDTH / 2),
            y: Math.floor(GRID_HEIGHT / 2)
        }];
        this.direction = { x: 1, y: 0 };
        this.length = 1;
        this.coinsEaten = 0;
        this.sizeMultiplier = 1;
    }

    update() {
        const head = this.positions[0];
        const newHead = {
            x: (head.x + this.direction.x + GRID_WIDTH) % GRID_WIDTH,
            y: (head.y + this.direction.y + GRID_HEIGHT) % GRID_HEIGHT
        };

        // Check collision with self
        for (let i = 3; i < this.positions.length; i++) {
            if (this.positions[i].x === newHead.x && this.positions[i].y === newHead.y) {
                return false;
            }
        }

        this.positions.unshift(newHead);
        if (this.positions.length > this.length) {
            this.positions.pop();
        }
        return true;
    }

    draw(ctx) {
        this.positions.forEach((pos, i) => {
            const x = pos.x * GRID_SIZE + GRID_SIZE / 2;
            const y = pos.y * GRID_SIZE + GRID_SIZE / 2;
            const baseRadius = (GRID_SIZE / 2 - 2) * this.sizeMultiplier;

            // Draw body
            ctx.beginPath();
            ctx.fillStyle = COLORS.MINT;
            ctx.arc(x, y, baseRadius, 0, Math.PI * 2);
            ctx.fill();

            // Draw shine
            ctx.beginPath();
            ctx.fillStyle = COLORS.WHITE;
            ctx.arc(x - baseRadius/3, y - baseRadius/3, baseRadius/3, 0, Math.PI * 2);
            ctx.fill();

            // Draw eyes on head
            if (i === 0) {
                // Left eye
                ctx.beginPath();
                ctx.fillStyle = COLORS.WHITE;
                ctx.arc(x - baseRadius/2, y - baseRadius/4, baseRadius/4, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.fillStyle = '#000';
                ctx.arc(x - baseRadius/2, y - baseRadius/4, baseRadius/8, 0, Math.PI * 2);
                ctx.fill();

                // Right eye
                ctx.beginPath();
                ctx.fillStyle = COLORS.WHITE;
                ctx.arc(x + baseRadius/2, y - baseRadius/4, baseRadius/4, 0, Math.PI * 2);
                ctx.fill();
                ctx.beginPath();
                ctx.fillStyle = '#000';
                ctx.arc(x + baseRadius/2, y - baseRadius/4, baseRadius/8, 0, Math.PI * 2);
                ctx.fill();
            }
        });
    }
}

class Coin {
    constructor() {
        this.randomize();
    }

    randomize() {
        this.position = {
            x: Math.floor(Math.random() * GRID_WIDTH),
            y: Math.floor(Math.random() * GRID_HEIGHT)
        };
        this.value = [5, 10, 15][Math.floor(Math.random() * 3)];
        this.color = {
            5: COLORS.COIN_5,
            10: COLORS.COIN_10,
            15: COLORS.COIN_15
        }[this.value];
    }

    draw(ctx) {
        const x = this.position.x * GRID_SIZE + GRID_SIZE / 2;
        const y = this.position.y * GRID_SIZE + GRID_SIZE / 2;
        const radius = GRID_SIZE / 2 - 2;

        // Draw coin
        ctx.beginPath();
        ctx.fillStyle = this.color;
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fill();

        // Draw shine
        ctx.beginPath();
        ctx.fillStyle = COLORS.WHITE;
        ctx.arc(x - radius/3, y - radius/3, radius/3, 0, Math.PI * 2);
        ctx.fill();

        // Draw value
        ctx.fillStyle = '#666';
        ctx.font = '16px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(this.value.toString(), x, y);
    }
}

class Game {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.snake = new Snake();
        this.coins = Array(6).fill(null).map(() => new Coin());
        this.score = 0;
        this.gameWon = false;
        this.setupControls();
    }

    setupControls() {
        document.addEventListener('keydown', (e) => {
            if (this.gameWon) {
                if (e.code === 'Space') {
                    this.resetGame();
                }
                return;
            }

            switch(e.code) {
                case 'ArrowUp':
                    if (this.snake.direction.y !== 1) {
                        this.snake.direction = { x: 0, y: -1 };
                    }
                    break;
                case 'ArrowDown':
                    if (this.snake.direction.y !== -1) {
                        this.snake.direction = { x: 0, y: 1 };
                    }
                    break;
                case 'ArrowLeft':
                    if (this.snake.direction.x !== 1) {
                        this.snake.direction = { x: -1, y: 0 };
                    }
                    break;
                case 'ArrowRight':
                    if (this.snake.direction.x !== -1) {
                        this.snake.direction = { x: 1, y: 0 };
                    }
                    break;
            }
        });
    }

    resetGame() {
        this.snake.reset();
        this.coins.forEach(coin => coin.randomize());
        this.score = 0;
        this.gameWon = false;
        document.getElementById('gameOver').style.display = 'none';
        this.updateScoreBoard();
    }

    updateScoreBoard() {
        document.getElementById('score').textContent = `Score: ${this.score}`;
        document.getElementById('coins').textContent = `Coins: ${this.snake.coinsEaten}`;
    }

    checkCollisions() {
        const head = this.snake.positions[0];
        this.coins.forEach(coin => {
            if (coin.position.x === head.x && coin.position.y === head.y) {
                this.snake.length += 1;
                this.snake.coinsEaten += 1;
                this.score += coin.value;

                if (this.score >= 500) {
                    this.gameWon = true;
                    document.getElementById('gameOver').style.display = 'block';
                    document.getElementById('finalScore').textContent = `Final Score: ${this.score}`;
                }

                if (this.snake.coinsEaten % 3 === 0) {
                    this.snake.sizeMultiplier += 0.5;
                }

                coin.randomize();
                this.updateScoreBoard();
            }
        });
    }

    update() {
        if (this.gameWon) return;

        if (!this.snake.update()) {
            this.resetGame();
            return;
        }

        this.checkCollisions();
    }

    draw() {
        this.ctx.fillStyle = '#ffffff';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.coins.forEach(coin => coin.draw(this.ctx));
        this.snake.draw(this.ctx);
    }

    gameLoop() {
        this.update();
        this.draw();
        setTimeout(() => requestAnimationFrame(() => this.gameLoop()), 1000 / 4); // 4 FPS for slow speed
    }
}

// The game will now start when startGame() is called after payment
// window.onload = () => {
//     const game = new Game();
//     game.gameLoop();
// }; 