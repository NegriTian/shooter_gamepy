from pygame import *

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_back = 'galaxy.jpg'
img_hero = 'rocket.png'

win_width = 700
win_height = 500
display.set_caption('Cyberpunk 3088')
window = display.set_mode((win_height, win_width))
background = transforv.scale(image.load(img_back), (win_width, win_height))

finish = False
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            rin = False

    if not finish:
        win_height.blit(background, (0,0))
        display.update()
    time.delay(50)