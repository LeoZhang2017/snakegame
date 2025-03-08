import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 25  # Slightly larger grid for better visuals
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Pastel Colors
PINK_BG = (255, 198, 201)  # Pastel pink background
MINT = (183, 255, 236)     # Mint green for snake
PASTEL_YELLOW = (255, 255, 204)  # Pastel yellow for coins
WHITE = (255, 255, 255)
BG_COLOR = WHITE  # Changed background to white

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Cute Snake Game')

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.length = 1
        self.coins_eaten = 0  # Track number of coins eaten
        self.size_multiplier = 1  # Scale factor for snake size
        
    def get_head_position(self):
        return self.positions[0]

    def update(self):
        current = self.get_head_position()
        x, y = self.direction
        new = ((current[0] + x) % GRID_WIDTH, (current[1] + y) % GRID_HEIGHT)
        
        # Check if snake hits its body
        if new in self.positions[3:]:
            return False
        
        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()
        return True

    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.length = 1
        self.coins_eaten = 0
        self.size_multiplier = 1

    def draw(self, surface):
        for i, position in enumerate(self.positions):
            x = position[0] * GRID_SIZE + GRID_SIZE // 2
            y = position[1] * GRID_SIZE + GRID_SIZE // 2
            
            # Draw main body circle with size based on multiplier
            base_radius = GRID_SIZE // 2 - 2
            radius = base_radius * self.size_multiplier
            pygame.draw.circle(surface, MINT, (x, y), radius)
            
            # Add shine effect scaled with size
            shine_radius = (radius // 3)
            pygame.draw.circle(surface, WHITE, (x - radius//3, y - radius//3), shine_radius)
            
            # Draw eyes on head, scaled with size
            if i == 0:  # This is the head
                eye_scale = self.size_multiplier
                # Left eye
                pygame.draw.circle(surface, WHITE, (x - radius//2, y - radius//4), 
                                 radius//4)
                pygame.draw.circle(surface, (0, 0, 0), (x - radius//2, y - radius//4), 
                                 radius//8)
                # Right eye
                pygame.draw.circle(surface, WHITE, (x + radius//2, y - radius//4), 
                                 radius//4)
                pygame.draw.circle(surface, (0, 0, 0), (x + radius//2, y - radius//4), 
                                 radius//8)

class Coin:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
        self.value = random.choice([5, 10, 15])  # Different coin values
        self.color = {
            5: (255, 255, 204),    # Light yellow
            10: (255, 223, 186),   # Light orange
            15: (255, 182, 193)    # Light pink
        }[self.value]

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1),
                        random.randint(0, GRID_HEIGHT - 1))
        self.value = random.choice([5, 10, 15])
        self.color = {
            5: (255, 255, 204),    # Light yellow
            10: (255, 223, 186),   # Light orange
            15: (255, 182, 193)    # Light pink
        }[self.value]

    def draw(self, surface):
        x = self.position[0] * GRID_SIZE + GRID_SIZE // 2
        y = self.position[1] * GRID_SIZE + GRID_SIZE // 2
        radius = GRID_SIZE // 2 - 2
        
        # Draw main coin circle
        pygame.draw.circle(surface, self.color, (x, y), radius)
        # Add shine effect
        shine_radius = radius // 3
        pygame.draw.circle(surface, WHITE, (x - radius//3, y - radius//3), shine_radius)
        
        # Draw value number
        font = pygame.font.Font(None, 20)
        text = font.render(str(self.value), True, (100, 100, 100))
        text_rect = text.get_rect(center=(x, y))
        surface.blit(text, text_rect)

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    coins = [Coin() for _ in range(6)]
    score = 0
    font = pygame.font.Font(None, 36)
    game_speed = 4
    game_won = False  # Track if game is won

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_won:  # Reset game if won
                    game_won = False
                    snake.reset()
                    coins = [Coin() for _ in range(6)]
                    score = 0
                    continue
                if not game_won:  # Only allow movement if game isn't won
                    if event.key == pygame.K_UP and snake.direction != (0, 1):
                        snake.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and snake.direction != (0, -1):
                        snake.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and snake.direction != (1, 0):
                        snake.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and snake.direction != (-1, 0):
                        snake.direction = (1, 0)

        if game_won:
            # Display win screen
            screen.fill(BG_COLOR)
            win_text = font.render('YOU WIN!', True, (100, 100, 100))
            score_text = font.render(f'Final Score: {score}', True, (100, 100, 100))
            instruction_text = font.render('Press SPACE to play again', True, (100, 100, 100))
            
            win_rect = win_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 50))
            score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
            instruction_rect = instruction_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))
            
            screen.blit(win_text, win_rect)
            screen.blit(score_text, score_rect)
            screen.blit(instruction_text, instruction_rect)
            
            pygame.display.update()
            continue

        if not snake.update():
            snake.reset()
            coins = [Coin() for _ in range(6)]
            score = 0

        # Check if snake ate any coin
        for coin in coins:
            if snake.get_head_position() == coin.position:
                snake.length += 1
                snake.coins_eaten += 1
                score += coin.value
                
                # Check for win condition
                if score >= 500:
                    game_won = True
                    break
                
                # Increase snake size every 3 coins
                if snake.coins_eaten % 3 == 0:
                    snake.size_multiplier += 0.5
                
                coin.randomize_position()
                # Make sure new coin position doesn't overlap with snake or other coins
                while (coin.position in snake.positions or 
                       any(c.position == coin.position for c in coins if c != coin)):
                    coin.randomize_position()

        screen.fill(BG_COLOR)
        snake.draw(screen)
        for coin in coins:
            coin.draw(screen)

        # Display score and coins eaten
        score_text = font.render(f'Score: {score}', True, (100, 100, 100))
        coins_text = font.render(f'Coins: {snake.coins_eaten}', True, (100, 100, 100))
        target_text = font.render(f'Target: 500', True, (100, 100, 100))
        screen.blit(score_text, (10, 10))
        screen.blit(coins_text, (10, 50))
        screen.blit(target_text, (10, 90))

        pygame.display.update()
        clock.tick(game_speed)

if __name__ == '__main__':
    main() 