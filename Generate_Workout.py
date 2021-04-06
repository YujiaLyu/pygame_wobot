from wobot.workouts import *
from wobot.displays import *
import pygame
import pygame_gui as pgg
import os
import datetime
import sys
import ast
import pathlib

from Define_Workout import info_panel




pygame.mixer.init(44100, -16, 1, 512)
pygame.init()

# initialize basic game index
x_bg = 1080
y_bg = 720

# initialize game clock
clock = pygame.time.Clock()


# initialize game condition
generate_on = False
seed_on = False




############# Pygame Page Design #####################
window_surface = pygame.display.set_mode((x_bg,y_bg)) 

workout_gen = pygame.Surface((x_bg,y_bg))
workout_gen.fill((255,255,255))

manager4 = pgg.UIManager((x_bg,y_bg))

# parameters: muscles=None, equipment=ALL_EQUIPMENT, exclude_exercises=None, etypes=None, seed=None

# initialize positions
x_4 = 150
y_4 = 150
w_4 = 150
h_4 = 50

# create buttons based on workout definition and button to next



nextButton = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((440,650),(200,50)),
                                                    text = "Next",
                                                    manager = manager4,
                                                    object_id = "next")

title_button = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect(((x_bg-500)//2,50),(500,50)),
                                                    text = "More Workout Customization",
                                                    manager = manager4,
                                                    object_id = "title")


# text entry in panel
equipment = pgg.elements.ui_text_entry_line.UITextEntryLine(relative_rect = pygame.Rect(((1080-200)//2,y_4+120+150),(200,20)),
                                                           manager = manager4,
                                                           object_id = "equipment",
                                                           visible = 0)
#equipment.set_allowed_characters(['band', 'kettlebell', 'dumbbell'])

alteration  = pgg.elements.ui_text_entry_line.UITextEntryLine(relative_rect = pygame.Rect(((1080-200)//2,y_4+120+180),(200,20)),
                                                           manager = manager4,
                                                           object_id = "alt",
                                                           visible = 0)
#alteration.set_allowed_characters([True, False, 0,1, "Yes", "No"])

entry_list = [equipment, alteration]
entry_text = ["equipment", "alt"]

# customize button in panel
add_button = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect(((1080-50)//2+100,y_4+350),(50,30)),
                                                    text = "Add",
                                                    manager = manager4,
                                                    object_id = "add",
                                                    visible = 0)

cancel_button = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect(((1080-50)//2-100,y_4+350),(50,30)),
                                                    text = "Cancel",
                                                    manager = manager4,
                                                    object_id = "cancel",
                                                    visible = 0)

func_list = [add_button, cancel_button]



def generate_workout(generate_on, workout_define, muscle_result):
    global seed_on

    total_workout = dict()
    button_click1 = 0
    button_click2 = 0
    button_click3 = 0
    button_click4 = 0
    button_click5 = 0
    button_click0 = 0

    # more workout specifications (dropset and exox do not have alt)
    workout_spec = {"muscle":None, "equipment": ALL_EQUIPMENT, "etypes": None, "alt":False}

    workout_key = list(workout_define.keys())
    workout_num = len(workout_key)

    for i in range(len(workout_key)):
        pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_4+(w_4+10)*i,y_4),(w_4,h_4)),
                                                    text = workout_key[i],
                                                    manager = manager4,
                                                    object_id = workout_key[i].lower())


    # selection menu in panel
    muscle_menu = list(muscle_result.keys())
    muscle = pgg.elements.ui_selection_list.UISelectionList(relative_rect  = pygame.Rect(((1080-200)//2,y_4+120),(200,85)),
                                                        item_list  = muscle_menu,  
                                                        manager = manager4,
                                                        allow_multi_select = True,
                                                        object_id = "muscle",
                                                        visible = 0)
    etypes = pgg.elements.ui_selection_list.UISelectionList(relative_rect = pygame.Rect(((1080-200)//2,y_4+120+95),(200,45)),
                                                        item_list  = ["Strength", "Cardio"], 
                                                        manager = manager4,        
                                                        object_id = "etypes",
                                                        visible = 0)

    selection_list = [muscle,etypes]

    # workout output
    output_font = pygame.font.SysFont("Calibri", 20)
    output_ins = output_font.render("We will have", False, (0,0,0))
    output_y = 0

    while generate_on:
        time_delta = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                generate_on = False

            if event.type == pygame.USEREVENT:
                if event.user_type == pgg.UI_BUTTON_PRESSED:
                    if event.ui_object_id == "next":
                        generate_on = False
                        seed_on = True
                        
                    elif event.ui_object_id == "add":
                        total_workout[list(total_workout.keys())[-1]] = workout_spec
                        #total_workout = dict([(k,v)for k,v in total_workout.items()if len(v) > 0])
                        workout_spec = {"muscle":None, "equipment": ALL_EQUIPMENT, "etypes": None, "alt":False}
                        info_panel(workout_gen, entry_list, func_list, entry_text, selection_list)
                        output_text = output_font.render(str(list(total_workout.keys())[-1]), False, (0,0,0))
                        workout_gen.blit(output_text,((800,375+output_y)))
                        output_y += 25
                    
                    elif event.ui_object_id == "cancel":
                        info_panel(workout_gen, entry_list, func_list, entry_text, selection_list)

                        added_workout = list(total_workout.keys())
                        if workout_key[0].lower() in added_workout[-1]:
                            button_click0 -=1
                        elif workout_key[1].lower() in added_workout[-1]:
                            button_click1 -=1
                        elif workout_key[2].lower() in added_workout[-1]:
                            button_click2 -=1
                        elif workout_key[3].lower() in added_workout[-1]:
                            button_click3 -=1
                        elif workout_key[4].lower() in added_workout[-1]:
                            button_click4 -=1
                        elif workout_key[5].lower() in added_workout[-1]:
                            button_click5 -=1
                        elif workout_key[6].lower() in added_workout[-1]:
                            button_click6 -=1
                        
                        total_workout.popitem()
                        

                        

                    # don't know how many workout user defined previously.
                    # If there is better presentation, please let me know.
                    
                    if workout_num != 0: 
                        if event.ui_object_id == workout_key[0].lower():
                            button_click0 +=1
                            info_panel(workout_gen, entry_list, func_list, entry_text, selection_list,action = "show")
                            total_workout.update({workout_key[0]+str(button_click0):{}})
                            
                        if workout_num >=2 :
                            if event.ui_object_id == workout_key[1].lower():
                                button_click1 +=1
                                info_panel(workout_gen, entry_list, func_list, entry_text, selection_list,action = "show")
                                total_workout.update({workout_key[1]+str(button_click1):{}})
                                
                            if workout_num >=3:
                                if event.ui_object_id == workout_key[2].lower():
                                    button_click2 +=1
                                    info_panel(workout_gen, entry_list, func_list, entry_text, selection_list,action = "show")
                                    total_workout.update({workout_key[2]+str(button_click2):{}})
                                    
                                if workout_num >=4:
                                    button_click3 +=1
                                    if event.ui_object_id == workout_key[3].lower():
                                        info_panel(workout_gen, entry_list, func_list, entry_text, selection_list,action = "show")
                                        total_workout.update({workout_key[3]+str(button_click3):{}})
                                        
                                    if workout_num >=5:
                                        button_click4 +=1
                                        if event.ui_object_id == workout_key[4].lower():
                                            info_panel(workout_gen, entry_list, func_list, entry_text, selection_list,action = "show")
                                            total_workout.update({workout_key[4]+str(button_click4):{}})
                                            
                                        if workout_num >=6:
                                            button_click5 +=1
                                            if event.ui_object_id == workout_key[5].lower():
                                                info_panel(workout_gen, entry_list, func_list, entry_text, selection_list,action = "show")
                                                total_workout.update({workout_key[5]+str(button_click5):{}})
                                                
                                
                    
                elif event.user_type == pgg.UI_TEXT_ENTRY_CHANGED:
                    if event.ui_object_id == "equipment":
                        if any(item for item in ["all","y","yes","1"] if item == event.text.lower()):
                            workout_spec["equipment"] = ALL_EQUIPMENT
                        elif any(item for item in ["none","n","no","0"] if item == event.text.lower()):
                            workout_spec["equipment"] = (None,)
                        else:
                            if "," in event.text:
                                workout_spec["equipment"] = tuple(event.text.split(",")) 
                            else:
                                workout_spec["equipment"] = (event.text,) 
                    if event.ui_object_id == "alt":
                        if any(item for item in ["true","y","yes","1"] if item == event.text.lower()):
                            workout_spec["alt"] = True
                        else:
                            workout_spec["alt"] = False
                        

                elif event.user_type == pgg.UI_SELECTION_LIST_NEW_SELECTION:
                    if event.ui_object_id == "muscle":
                        workout_spec["muscle"] = muscle.get_multi_selection()
                    elif event.ui_object_id == "etypes":
                        workout_spec["etypes"] = (etypes.get_single_selection().lower(),)
                elif event.user_type == pgg.UI_SELECTION_LIST_DROPPED_SELECTION:
                    if event.ui_object_id == "muscle":
                        workout_spec["muscle"] = muscle.get_multi_selection()
                    elif event.ui_object_id == "etypes":
                        workout_spec["etypes"] = (etypes.get_single_selection().lower(),)


            manager4.process_events(event)

        manager4.update(time_delta)


        # paint text
        workout_gen.blit(output_ins,(800,350))

        # paint surface
        window_surface.blit(workout_gen,(0,0))
        manager4.draw_ui(workout_gen)

        pygame.display.update()

    return seed_on, total_workout
#endregion
