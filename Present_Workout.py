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
display_on = False
is_running = False



################## display workout  ####################
window_surface = pygame.display.set_mode((x_bg,y_bg))

workout_dis = pygame.Surface((x_bg,y_bg))
workout_dis.fill((235,236,238))

manager6 = pgg.UIManager((x_bg,y_bg),"workout_review.json")

# needed function
def convert_time(num_seconds):
    '''
    function to return time in 00:00 format
    '''
    min = "00"
    second = ""
    if num_seconds > 60:
        min = str(num_seconds // 60)
        if num_seconds % 60 < 10:
            second = "0" + str(num_seconds % 60)
        else:
            second = str(num_seconds % 60)
    else:
        if num_seconds == 60:
            min = "01"
            second = "00"
        elif num_seconds % 60 <10:
            second = "0" + str(num_seconds % 60)
        else:
            second = str(num_seconds % 60)
    
    return min+":"+second



# buttons
nextButton = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect(((x_bg-250)//2,650),(250,50)),
                                                    text = "Workout Looks Good",
                                                    manager = manager6,
                                                    object_id = "next")


title_button = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect(((x_bg-500)//2,50),(500,50)),
                                                    text = "Workout for Today",
                                                    manager = manager6,
                                                    object_id = "title")
title_button.disable()


def display_workout(display_on, final_list, total_time):
    global is_running
    
    # workout display list
    pgg.elements.ui_selection_list.UISelectionList(relative_rect=pygame.Rect(((x_bg-500)//2,150),(500,450)),
                                                               item_list = final_list,
                                                               manager = manager6,
                                                               object_id = "review_list")


    pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((800,520),(150,30)),
                                                    text = "Total Duration",
                                                    manager = manager6,
                                                    object_id = "total_time").disable()

    pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((800,550),(150,50)),
                                                    text = convert_time(total_time),
                                                    manager = manager6,
                                                    object_id = "time").disable()



    while display_on:
        time_delta = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                display_on = False
                

            if event.type == pygame.USEREVENT:
                if event.user_type == pgg.UI_BUTTON_PRESSED:
                    if event.ui_object_id == "next":
                        display_on = False
                        is_running = True
                    

            manager6.process_events(event)

        manager6.update(time_delta)

        # paint surface
        window_surface.blit(workout_dis,(0,0))
        manager6.draw_ui(workout_dis)

        pygame.display.update()
    
    return is_running

#endregion
