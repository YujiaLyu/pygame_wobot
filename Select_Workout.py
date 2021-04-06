'''
Muscle Selection Page
'''
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
select_on = False
define_on = False



############# Pygame Page Design #####################
window_surface = pygame.display.set_mode((x_bg,y_bg))

workout_sel = pygame.Surface((x_bg,y_bg))
workout_sel.fill((255,255,255))

manager2 = pgg.UIManager((x_bg,y_bg))

x_2 = x_bg//2
y_2 = 150
w_2 = 300
h_2 = 200


# create workout type selection list
workout_type = pgg.elements.ui_selection_list.UISelectionList(relative_rect=pygame.Rect((x_2-w_2//2,y_2),(w_2,h_2)),
                                                               item_list = ["Tabata","Dropset","Timed Workout",
                                                                            "EXOX","Total Random"],
                                                               manager = manager2,
                                                               allow_multi_select = True,
                                                               allow_double_clicks = True,
                                                               object_id = "workout_type")


# button to next
nextButton = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((440,650),(200,50)),
                                                    text = "Next",
                                                    manager = manager2,
                                                    object_id = "next")

# title button
title_button = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect(((x_bg-500)//2,50),(500,50)),
                                                    text = "What Type of Workout Do You Want",
                                                    manager = manager2,
                                                    object_id = "title")


# second game loop
def select_workout(select_on):
    global define_on

    # muscle selection results
    workout_result = []

    while select_on:
        time_delta = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                select_on = False
            
            if event.type == pygame.USEREVENT:
                if event.user_type == pgg.UI_BUTTON_PRESSED:
                    if event.ui_object_id == "next":
                        select_on = False
                        define_on = True
                elif event.user_type == pgg.UI_SELECTION_LIST_NEW_SELECTION:
                    if event.ui_object_id == "workout_type":
                        workout_result = workout_type.get_multi_selection()
                elif event.user_type == pgg.UI_SELECTION_LIST_DROPPED_SELECTION:
                    if event.ui_object_id == "workout_type":
                        workout_result = workout_type.get_multi_selection()

                                            
            manager2.process_events(event)

        manager2.update(time_delta)


    # paint surface
        window_surface.blit(workout_sel,(0,0))
        manager2.draw_ui(workout_sel)

        pygame.display.update()

    return define_on, workout_result

#endregion
