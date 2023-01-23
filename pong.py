import pygame
pygame.init()


win_width, win_height = 750, 550
FPS = 60
BALL_RADIUS = 8
WINNING_SCORE = 10

SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINDOW = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Wilber's Pong")

paddle_Width, paddle_height = 20, 100 
whiteRGB = (255, 255, 255)
blackRGB = (0, 0, 0)

def startGame():
    runGame = True

    #use the clock to control the fps of the game
    clock = pygame.time.Clock()

    #Create the paddles that will be used for the game
    L_Paddle = Paddle(10, win_height//2 - paddle_height//2, paddle_Width, paddle_height)
    R_Paddle = Paddle(win_width - 10- paddle_Width, win_height//2 - paddle_height//2, paddle_Width, paddle_height)
    ball = Ball(win_width//2, win_height//2 - 8, BALL_RADIUS)

    leftScore, rightScore = 0, 0

    #While loop will run the gam
    while runGame:
        #the clock will for the while loop to run 60 times per second, no matter
        # what machine the game is ran on
        clock.tick(FPS)
        drawWindow(WINDOW, [L_Paddle, R_Paddle], ball, leftScore, rightScore)
    
        #listens for events that may happen on the window such as user exiting out of the window
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                runGame = False
                break

        keys = pygame.key.get_pressed()    
        ball.moveBall()
        collsion(ball, L_Paddle, R_Paddle)
        paddle_movement(keys, L_Paddle, R_Paddle)

        if ball.x < 0:
            rightScore +=1
            ball.resetBall()
        elif ball.x > win_width:
            leftScore +=1
            ball.resetBall()

        won = False
        if leftScore >= WINNING_SCORE:
            won = True
            win_Text = "Left Player Wins!"
        elif rightScore >= WINNING_SCORE:
            won = True
            win_Text = "Right Player Wins!"
        
        if won:
            text = SCORE_FONT.render(win_Text, 1, whiteRGB)
            drawEndScreen(WINDOW, text)
            ball.resetBall()
            L_Paddle.paddleReset()
            R_Paddle.paddleReset()
            leftScore = 0
            rightScore = 0


    pygame.quit()

#allows for moving both paddles in either direction
def paddle_movement(keys, leftPaddle, rightPaddle):
    if keys[pygame.K_w] and (leftPaddle.y - leftPaddle.velocity >= 0):
        leftPaddle.movePaddle(up = True)
    if keys[pygame.K_s] and (leftPaddle.y + leftPaddle.velocity + leftPaddle.height <= win_height):
        leftPaddle.movePaddle(up = False)

    if keys[pygame.K_UP] and (rightPaddle.y - rightPaddle.velocity >= 0):
        rightPaddle.movePaddle(up = True)
    if keys[pygame.K_DOWN] and (rightPaddle.y + rightPaddle.velocity + rightPaddle.height <= win_height):
        rightPaddle.movePaddle(up = False)
    
def drawEndScreen(window, text):
    window.fill(blackRGB)
    WINDOW.blit(text, (win_width//2-text.get_width()//2, win_height//2-text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


#This function will draw onto the pygame display
def drawWindow(window, paddles, ball,L_Score, R_Score):
    window.fill(blackRGB)
    L_Score_Text = SCORE_FONT.render(f"{L_Score}", 1, whiteRGB)
    R_Score_Text = SCORE_FONT.render(f"{R_Score}", 1, whiteRGB)
    window.blit(L_Score_Text, (win_width//4 - L_Score_Text.get_width()//2, 20))
    window.blit(R_Score_Text, (win_width*3//4 - R_Score_Text.get_width()//2, 20))
    for paddle in paddles:
        paddle.drawPaddle(window)

    for i in range(10, win_height, win_height//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(window, whiteRGB, (win_width//2 - 5, i, 10, win_height//20))
    ball.drawBall(window)
        
    pygame.display.update()



def collsion(ball, leftPaddle, rightPaddle):
    # first handle collision with the ceilings 
    if ball.y + ball.radius >= win_height:
        ball.y_vel *=-1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1
    
    #ball is moving to the left of the screen
    #This handles the collision with the paddles
    if ball.x_vel < 0:
        if ball.y >= leftPaddle.y and ball.y <= leftPaddle.y + paddle_height:
            if ball.x - ball.radius <= leftPaddle.x + leftPaddle.width:
                ball.x_vel *= -1

                middle_y = leftPaddle.y + leftPaddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (leftPaddle.height/2)/ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel * -1
    else:#ball is movin to the right of the screen
        if ball.y >= rightPaddle.y and ball.y <= rightPaddle.y + paddle_height:
            if ball.x + ball.radius >= rightPaddle.x:
                ball.x_vel *= -1

                middle_y = rightPaddle.y + rightPaddle.height/2
                difference_in_y = middle_y - ball.y
                reduction_factor = (rightPaddle.height/2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = y_vel * -1

class Ball:
    MAX_VEL = 5
    COLOR = whiteRGB

    def __init__(self, x, y, radius):
        self.x = self.initial_x = x
        self.y = self.initial_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def drawBall(self, window):
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.radius )

    def moveBall(self):
        self.x +=self.x_vel
        self.y +=self.y_vel

    def resetBall(self):
        self.x = self.initial_x
        self.y = self.initial_y
        self.y_vel = 0
        self.x_vel *= -1
        
#Paddle Object
class Paddle:
    COLOR = whiteRGB
    velocity = 4

    def __init__(self, x, y, width, height):
        self.x = self.initial_x = x
        self.y = self.initial_y = y
        self.width = width
        self.height = height

    #draws a paddle on the screen
    def drawPaddle(self, window):
        pygame.draw.rect(window, self.COLOR, (self.x, self.y, self.width, self.height) )

    #Allows for moving a paddle Object up or down
    def movePaddle(self, up = True):
        if up:
            self.y -= self.velocity
        else:
            self.y += self.velocity

    def paddleReset(self):
        self.x = self.initial_x
        self.y = self.initial_y

#starts the game
startGame()