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
muscle_on = True
select_on = False


### initialize main input variables
# muscle records 
lower_body = ["Quadriceps", "Hamstrings", "Glutes", "Calves", "LowerBack", "Abductors", "Adductors"]
upper_body = ["Chest", "MiddleBack", "Lats", "Traps", 'Shoulders']
arms = ['Biceps', 'Triceps', "Forearms"]
ab = ["Abdominals", "LowerBack"]




############# Pygame Page Design #####################
window_surface = pygame.display.set_mode((x_bg,y_bg))

muscle_sel = pygame.Surface((x_bg,y_bg))
muscle_sel.fill((255,255,255))

manager = pgg.UIManager((x_bg,y_bg))


# initialize object positions
x = 200
y = 150
w = 300
h = 200


# create selection list
lower_body_sel = pgg.elements.ui_selection_list.UISelectionList(relative_rect=pygame.Rect((x,y),(w,h)),
                                                               item_list = lower_body,
                                                               manager = manager,
                                                               allow_multi_select = True,
                                                               allow_double_clicks = True,
                                                               object_id = "LB")

upper_body_sel = pgg.elements.ui_selection_list.UISelectionList(relative_rect=pygame.Rect((x+400,y),(w,h)),
                                                               item_list = upper_body,
                                                               manager = manager,
                                                               allow_multi_select = True,
                                                               allow_double_clicks = True,
                                                               object_id = "UB")

arm_sel = pgg.elements.ui_selection_list.UISelectionList(relative_rect=pygame.Rect((x,y+250),(w,h)),
                                                               item_list = arms,
                                                               manager = manager,
                                                               allow_multi_select = True,
                                                               allow_double_clicks = True,
                                                               object_id = "ARM")

ab_sel = pgg.elements.ui_selection_list.UISelectionList(relative_rect=pygame.Rect((x+400,y+250),(w,h)),
                                                               item_list = ab,
                                                               manager = manager,
                                                               allow_multi_select = True,
                                                               allow_double_clicks = True,
                                                               object_id = "AB")


## create instruction text
title_button = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect(((x_bg-500)//2,50),(500,50)),
                                                    text = "Remove Muscles You don't Want",
                                                    manager = manager,
                                                    object_id = "title")

label_font = pygame.font.SysFont("Calibri",20)
LB_text = label_font.render("Lower Body", False, (0,0,0))
LB_rect = LB_text.get_rect(center=(x+w//2,y-10))
UB_text = label_font.render("Upper Body", False, (0,0,0))
UB_rect = UB_text.get_rect(center=(x+w//2+400,y-10))
ARM_text = label_font.render("Arms", False, (0,0,0))
ARM_rect = ARM_text.get_rect(center=(x+w//2,y+240))
AB_text = label_font.render("Abs", False, (0,0,0))
AB_rect = AB_text.get_rect(center=(x+w//2+400,y+240))


# create button
nextButton = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((440,650),(200,50)),
                                                    text = "Next",
                                                    manager = manager,
                                                    object_id = "next")


# first game loop (get muscle target)
def get_muscle(muscle_on):
    global select_on

    # muscle selection results
    muscle_result = {"LB":tuple(lower_body), "UB": tuple(upper_body), "ARM": tuple(arms), "AB":tuple(ab)}

    while muscle_on:
        time_delta = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                muscle_on = False
                
            
            if event.type == pygame.USEREVENT:
                if event.user_type == pgg.UI_SELECTION_LIST_NEW_SELECTION:
                    if event.ui_object_id == "LB":
                        muscle_result.update({"LB": tuple([item for item in lower_body if item not in lower_body_sel.get_multi_selection()])})
                    elif event.ui_object_id == "UB":
                        muscle_result.update({"UB": tuple([item for item in upper_body if item not in upper_body_sel.get_multi_selection()])})
                    elif event.ui_object_id == "ARM":
                        muscle_result.update({"ARM": tuple([item for item in arms if item not in arm_sel.get_multi_selection()])})
                    elif event.ui_object_id == "AB":
                        muscle_result.update({"AB": tuple([item for item in ab if item not in ab_sel.get_multi_selection()])})
                elif event.user_type == pgg.UI_SELECTION_LIST_DROPPED_SELECTION:
                    if event.ui_object_id == "LB":
                        muscle_result.update({"LB": tuple([item for item in lower_body if item not in lower_body_sel.get_multi_selection()])})
                    elif event.ui_object_id == "UB":
                        muscle_result.update({"UB": tuple([item for item in upper_body if item not in upper_body_sel.get_multi_selection()])})
                    elif event.ui_object_id == "ARM":
                        muscle_result.update({"ARM": tuple([item for item in arms if item not in arm_sel.get_multi_selection()])})
                    elif event.ui_object_id == "AB":
                        muscle_result.update({"AB": tuple([item for item in ab if item not in ab_sel.get_multi_selection()])})
                elif event.user_type == pgg.UI_BUTTON_PRESSED:
                    if event.ui_object_id == "next":
                        muscle_on = False
                        select_on = True
                        

            manager.process_events(event)

        manager.update(time_delta)


        # paint text
        muscle_sel.blit(LB_text,LB_rect)
        muscle_sel.blit(UB_text,UB_rect)
        muscle_sel.blit(ARM_text,ARM_rect)
        muscle_sel.blit(AB_text,AB_rect)


        # paint surface
        window_surface.blit(muscle_sel,(0,0))
        manager.draw_ui(muscle_sel)

        pygame.display.update()

    return select_on, muscle_result



