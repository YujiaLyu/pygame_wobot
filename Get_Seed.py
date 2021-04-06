from wobot.workouts import *
import pygame
import pygame_gui as pgg
import os
import datetime
import sys
import ast
import pathlib


pygame.mixer.init(44100, -16, 1, 512)
pygame.init()

# initialize basic game index
x_bg = 1080
y_bg = 720

# initialize game clock
clock = pygame.time.Clock()


# initialize game condition
seed_on = False
display_on = False

############# Pygame Page Design #####################
window_surface = pygame.display.set_mode((x_bg,y_bg)) 

get_seed = pygame.Surface((x_bg,y_bg))
get_seed.fill((255,255,255))

manager5 = pgg.UIManager((x_bg,y_bg))

# buttons
nextButton = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((440,650),(200,50)),
                                                    text = "Next",
                                                    manager = manager5,
                                                    object_id = "next")

title_button = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect(((x_bg-500)//2,50),(500,50)),
                                                    text = "Last Step: Give Me a Number",
                                                    manager = manager5,
                                                    object_id = "title")

# seed entry
seed = pgg.elements.ui_text_entry_line.UITextEntryLine(relative_rect = pygame.Rect(((1080-300)//2,300),(300,30)),
                                                           manager = manager5,
                                                           object_id = "seed",
                                                       visible = 1)
#seed.set_allowed_characters('numbers')
seed.set_text("Seed (can use names)")


def obtain_seed(seed_on):
    global display_on

    seed_output = None

    while seed_on:
        time_delta = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                seed_on = False


            if event.type == pygame.USEREVENT:
                if event.user_type == pgg.UI_BUTTON_PRESSED:
                    if event.ui_object_id == "next":
                        seed_on = False
                        display_on = True

                elif event.user_type == pgg.UI_TEXT_ENTRY_CHANGED:
                    if event.ui_object_id == "seed":
                        if event.text.isdigit():
                            seed_output = int(event.text)
                        elif event.text in ["James","Balyssa","Samon","Shris Ti",
                                            "Kiani","Chandra","Chris","Ianto","Marisol",
                                            "Yujia","Ka Leigh"]:
                            seed_output = NAME_HASHES[event.text]



            manager5.process_events(event)

        manager5.update(time_delta)

        # paint surface
        window_surface.blit(get_seed,(0,0))
        manager5.draw_ui(get_seed)

        pygame.display.update()

    return display_on, seed_output
#endregion
