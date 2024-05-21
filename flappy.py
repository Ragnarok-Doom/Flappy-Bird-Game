import random  # For Generating Random Numbers
import sys  # To exit the program
import pygame
from pygame.locals import *

# Global variables for the game
FPS = 32
SCREENWIDTH = 500
SCREENHEIGHT = 700
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/back.jpg'
PIPE = 'gallery/sprites/pipe.png'


def welcomeScreen():
    '''
    Shows Welcome image on the screen
    '''

    # PLAYER POSITION
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height()) / 2)

    # MESSAGE POSITION
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.13)

    # BASE POSITION
    basex = 0

    while True:
        for event in pygame.event.get():

            # If user clicked on cross - close the game
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            # If the user presses space or up key - start the game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0

    playerx = int(SCREENWIDTH / 5)
    playery = int(SCREENHEIGHT / 2)

    basex = 0

    # Create 2 pipes on blitting of the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']}
    ]

    # list of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']}
    ]

    # PIPE Velocity
    pipeVelx = -4
    playerVely = -9
    playerMaxVely = 10
    playerMinVely = -8
    playerAccy = 1

    playerFlapAccv = -8
    playerFlapped = False  # it true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVely = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)  # this function returns if player crashed
        if crashTest:
            return

        # Check for Scores
        playerMidPos = playerx + GAME_SPRITES['player'].get_width() / 2

        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if playerVely < playerMaxVely and not playerFlapped:
            playerVely += playerAccy

        if playerFlapped:
            playerFlapped = False

        player_height = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVely, GROUNDY - playery - player_height)

        # move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelx
            lowerPipe['x'] += pipeVelx

        # Add a new pipe when the first pipe is about to go to the left part of the screen
        if 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # if the pipe is out of the screen - remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # Lets Blit our sprites now
        SCREEN.blit(GAME_SPRITES['background'], (0, 0))

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width) / 2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery > GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipex = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipex, 'y': -y1},  # upper pipe
        {'x': pipex, 'y': y2}  # lower pipe
    ]
    return pipe


if __name__ == '__main__':
    pygame.init()  # It initializes all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')

    # 0 to 9 images
    number_images = [
        pygame.image.load(f'gallery/sprites/{i}.png').convert_alpha() for i in range(10)
    ]

    # Resize the number images
    scaled_number_images = []
    for img in number_images:
        scaled_img = pygame.transform.scale(img, (img.get_width() // 20, img.get_height() // 20))
        scaled_number_images.append(scaled_img)

    GAME_SPRITES['numbers'] = scaled_number_images

    # MESSAGE Image
    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/welcome.png').convert_alpha()

    # BASE Image
    GAME_SPRITES['base'] = pygame.transform.scale(
        pygame.image.load('gallery/sprites/base.png').convert_alpha(), (500, 200)
    )

    # PIPE Image
    original_pipe_image = pygame.image.load(PIPE).convert_alpha()
    pipe_width = original_pipe_image.get_width() // 5
    pipe_height = original_pipe_image.get_height() // 5
    scaled_pipe_image = pygame.transform.scale(original_pipe_image, (pipe_width, pipe_height))

    GAME_SPRITES['pipe'] = (scaled_pipe_image, pygame.transform.rotate(scaled_pipe_image, 180))

    # BACKGROUND Image
    GAME_SPRITES['background'] = pygame.transform.scale(
        pygame.image.load(BACKGROUND).convert(), (SCREENWIDTH, SCREENHEIGHT)
    )

    # PLAYER Image
    original_player_image = pygame.image.load(PLAYER).convert_alpha()
    player_width = original_player_image.get_width() // 25  # Adjust the divisor to scale down further if needed
    player_height = original_player_image.get_height() // 25
    GAME_SPRITES['player'] = pygame.transform.scale(original_player_image, (player_width, player_height))

    # GAME Sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.mp3')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.mp3')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.mp3')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.mp3')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.mp3')

    while True:
        welcomeScreen()  # Shows welcome message to the user until he presses a button
        mainGame()  # This is the main game function
