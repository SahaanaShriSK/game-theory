import pygame
import random
import math
import tkinter as tk
from tkinter import simpledialog

# Constants
FIELD_LENGTH = 1200
FIELD_WIDTH = 800
GOAL_SIZE = 200
PLAYER_RADIUS = 20
BALL_RADIUS = 15
FPS = 60

# Colors
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((FIELD_LENGTH, FIELD_WIDTH))
pygame.display.set_caption("AI Soccer Game")

# Clock
clock = pygame.time.Clock()


class Player:
    def __init__(self, name, position, color, is_human=False):
        self.name = name
        self.position = list(position)
        self.color = color  # Color for the player
        self.speed = 3
        self.is_human = is_human
        self.target_position = position  # AI players use this to scatter randomly

    def move(self, direction):
        if direction == "UP":
            self.position[1] -= self.speed
        elif direction == "DOWN":
            self.position[1] += self.speed
        elif direction == "LEFT":
            self.position[0] -= self.speed
        elif direction == "RIGHT":
            self.position[0] += self.speed

        # Keep player within bounds
        self.position[0] = max(PLAYER_RADIUS, min(FIELD_LENGTH - PLAYER_RADIUS, self.position[0]))
        self.position[1] = max(PLAYER_RADIUS, min(FIELD_WIDTH - PLAYER_RADIUS, self.position[1]))

    def ai_move(self, ball_position, scatter=False):
        """Move towards ball or scatter randomly."""
        if scatter:
            if math.dist(self.position, self.target_position) < 5:  # Reached target
                self.target_position = (random.randint(100, FIELD_LENGTH - 100), random.randint(100, FIELD_WIDTH - 100))
            else:
                angle = math.atan2(self.target_position[1] - self.position[1], self.target_position[0] - self.position[0])
                self.position[0] += self.speed * math.cos(angle) * 0.8  # AI is slower than the human player
                self.position[1] += self.speed * math.sin(angle) * 0.8  # AI is slower than the human player
        else:
            angle = math.atan2(ball_position[1] - self.position[1], ball_position[0] - self.position[0])
            self.position[0] += self.speed * math.cos(angle) * 0.8  # AI is slower than the human player
            self.position[1] += self.speed * math.sin(angle) * 0.8  # AI is slower than the human player

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), PLAYER_RADIUS)


class Ball:
    def __init__(self, position):
        self.position = list(position)
        self.velocity = [0, 0]
        self.image = pygame.image.load(r"C:\Users\Nethra R\OneDrive\Pictures\soccer_ball.png")
        # Path to your soccer ball PNG image
        self.image = pygame.transform.scale(self.image, (30, 30))  # Resize the ball image

    def kick(self, direction):
        """Add a moderate velocity to the ball based on the kick direction."""
        kick_speed = 4  
        if direction == "UP":
            self.velocity[1] -= kick_speed
        elif direction == "DOWN":
            self.velocity[1] += kick_speed
        elif direction == "LEFT":
            self.velocity[0] -= kick_speed
        elif direction == "RIGHT":
            self.velocity[0] += kick_speed

    def apply_physics(self):
        """Update ball position based on velocity and apply strong friction."""
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        # Apply stronger friction to slow the ball
        self.velocity[0] *= 0.9
        self.velocity[1] *= 0.9

        # Keep the ball within bounds
        self.position[0] = max(BALL_RADIUS, min(FIELD_LENGTH - BALL_RADIUS, self.position[0]))
        self.position[1] = max(BALL_RADIUS, min(FIELD_WIDTH - BALL_RADIUS, self.position[1]))

    def draw(self):
        # Draw the soccer ball image at the ball's position
        screen.blit(self.image, (self.position[0] - self.image.get_width() // 2, self.position[1] - self.image.get_height() // 2))


def draw_field():
    screen.fill(GREEN)
    pygame.draw.rect(screen, WHITE, (0, FIELD_WIDTH // 2 - GOAL_SIZE // 2, 10, GOAL_SIZE))  # Left goal
    pygame.draw.rect(screen, WHITE, (FIELD_LENGTH - 10, FIELD_WIDTH // 2 - GOAL_SIZE // 2, 10, GOAL_SIZE))  # Right goal
    pygame.draw.line(screen, WHITE, (FIELD_LENGTH // 2, 0), (FIELD_LENGTH // 2, FIELD_WIDTH), 2)  # Midline


def draw_scoreboard(team_a_score, team_b_score):
    font = pygame.font.Font(None, 50)
    score_text = font.render(f"Team A: {team_a_score} - Team B: {team_b_score}", True, WHITE)
    screen.blit(score_text, (FIELD_LENGTH // 2 - score_text.get_width() // 2, 10))


def show_popup(winner, team_a_score, team_b_score):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    tk.messagebox.showinfo(
        "Game Over",
        f"{winner} Wins!\n\nFinal Score:\nTeam A: {team_a_score}\nTeam B: {team_b_score}",
    )


def main():
    # Ask user for points to win
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    points_to_win = int(simpledialog.askstring("Points to Win", "Enter the points required to win:"))

    # Replace with your player and AI colors
    human_player = Player("Human", (200, FIELD_WIDTH // 2), RED, is_human=True)
    ai_players = [Player(f"AI {i}", (random.randint(800, 1100), random.randint(100, 700)), BLUE) for i in range(3)]
    ball = Ball([FIELD_LENGTH // 2, FIELD_WIDTH // 2])

    team_a_score, team_b_score = 0, 0

    running = True
    scatter_timer = 0  # Timer for scattering AI players
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            human_player.move("UP")
        if keys[pygame.K_DOWN]:
            human_player.move("DOWN")
        if keys[pygame.K_LEFT]:
            human_player.move("LEFT")
        if keys[pygame.K_RIGHT]:
            human_player.move("RIGHT")
        if keys[pygame.K_SPACE]:
            ball.kick("UP" if keys[pygame.K_UP] else "DOWN" if keys[pygame.K_DOWN] else "LEFT" if keys[pygame.K_LEFT] else "RIGHT")

        # AI behavior
        scatter_timer += 1
        for ai in ai_players:
            if scatter_timer % (FPS * 2) == 0:  # Scatter every 2 seconds
                ai.ai_move(ball.position, scatter=True)
            else:
                ai.ai_move(ball.position)

        # Update ball
        ball.apply_physics()

        # Check for goals
        if ball.position[0] - BALL_RADIUS <= 10 and FIELD_WIDTH // 2 - GOAL_SIZE // 2 <= ball.position[1] <= FIELD_WIDTH // 2 + GOAL_SIZE // 2:
            team_b_score += 1
            ball.position = [FIELD_LENGTH // 2, FIELD_WIDTH // 2]
            ball.velocity = [0, 0]
        elif ball.position[0] + BALL_RADIUS >= FIELD_LENGTH - 10 and FIELD_WIDTH // 2 - GOAL_SIZE // 2 <= ball.position[1] <= FIELD_WIDTH // 2 + GOAL_SIZE // 2:
            team_a_score += 1
            ball.position = [FIELD_LENGTH // 2, FIELD_WIDTH // 2]
            ball.velocity = [0, 0]

        # Check win condition
        if team_a_score >= points_to_win:
            show_popup("Team A", team_a_score, team_b_score)
            break
        elif team_b_score >= points_to_win:
            show_popup("Team B", team_a_score, team_b_score)
            break

        # Draw everything
        draw_field()
        draw_scoreboard(team_a_score, team_b_score)
        human_player.draw()
        for ai in ai_players:
            ai.draw()
        ball.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
