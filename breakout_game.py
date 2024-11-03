import pygame
import random

pygame.init()

#Screen dimensions and colours for the game
SCREEN_HEIGHT = 800
SCREEN_WIDTH = 1000
BLUE = (0, 0, 255)
LIGHT_GREEN = (144, 238, 144) 
BROWN = (139, 69, 19)                     
ORANGE = (255, 165, 0)         
RED = (255, 0, 0)             

# Creates the game screen wich is the width and height
def create_screen():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Breakout Game")
    return screen

# Create a clock object to manage the frame rate
def create_clock():
    return pygame.time.Clock()

# Creates the fonts for the text 
def create_fonts():
    font = pygame.font.Font(None, 36)
    large_font = pygame.font.Font(None, 74)
    return font, large_font

# Defines the properties of the paddle
def create_paddle():
    paddle_width = 100
    paddle_height = 10
    paddle_speed = 7
    paddle = pygame.Rect((SCREEN_WIDTH // 2) - (paddle_width // 2), SCREEN_HEIGHT - 40, paddle_width, paddle_height)
    return paddle, paddle_speed

# Defines properties pf the ball
def create_ball():
    ball_radius = 10
    ball_speed = [4, -4]
    ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, ball_radius * 2, ball_radius * 2)
    return ball, ball_speed

# Creates a grid of bricks
def create_bricks():
    brick_rows = 5
    brick_cols = 8
    brick_width = SCREEN_WIDTH // brick_cols
    brick_height = 20
    bricks = []

    for row in range(brick_rows):
        brick_row = []
        for col in range(brick_cols):
            brick = pygame.Rect(col * brick_width, row * brick_height, brick_width, brick_height)
            brick_row.append(brick)
        bricks.append(brick_row)

    return bricks


def draw_game(screen, paddle, ball, bricks):
    screen.fill(BROWN)  
    pygame.draw.rect(screen, BLUE, paddle) 
    pygame.draw.ellipse(screen, ORANGE, ball)  
    for row in bricks:
        for brick in row:
            pygame.draw.rect(screen, LIGHT_GREEN, brick) 


def display_text(screen, text, font, color, position):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)


def game_logic(ball, ball_speed, paddle, bricks):
  
    ball.move_ip(ball_speed)

   
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_speed[0] = -ball_speed[0]  
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]  

    if ball.colliderect(paddle):
        ball_speed[1] = -ball_speed[1] 

    
    for row in bricks:
        for brick in row:
            if ball.colliderect(brick):
                ball_speed[1] = -ball_speed[1] 
                row.remove(brick) 
                return

def reset_game(ball):
    ball.x = SCREEN_WIDTH // 2
    ball.y = SCREEN_HEIGHT // 2
    return [4, -4]  


def main():
    screen = create_screen()
    clock = create_clock()
    font, large_font = create_fonts()
    paddle, paddle_speed = create_paddle()
    ball, ball_speed = create_ball()
    bricks = create_bricks()

    running = True
    game_active = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not game_active:
                if event.key == pygame.K_RETURN: 
                    game_active = True
                    ball_speed = reset_game(ball)

        if game_active:
            keys = pygame.key.get_pressed()  
            if keys[pygame.K_LEFT] and paddle.left > 0:
                paddle.move_ip(-paddle_speed, 0)  
            if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
                paddle.move_ip(paddle_speed, 0)  

            game_logic(ball, ball_speed, paddle, bricks)  

            if ball.bottom >= SCREEN_HEIGHT:
                game_active = False  

       
        draw_game(screen, paddle, ball, bricks)

        if not game_active:
            screen.fill(BROWN) 
            display_text(screen, "Press ENTER to Start", font, LIGHT_GREEN, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
            if ball.bottom >= SCREEN_HEIGHT:
                display_text(screen, "You lose! Game Over", large_font, RED, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 50))

        pygame.display.flip() 
        clock.tick(60) 

    pygame.quit() 

if __name__ == "__main__":
    main()
