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
define_on = False
generate_on = False


# needed function
def info_panel(page,text_entry_list, button_list, init_text_list = None, selection_list = None, action = None):
    '''
    all parameters are in the form of list
    '''
    for i in range(len(text_entry_list)):
        text_entry_list[i].hide()
        if init_text_list != None:
            text_entry_list[i].set_text(init_text_list[i])
    
    if selection_list != None:
        for item in selection_list:
            item.hide()
            item.rebuild()
    
    for item in button_list:
        item.hide()
        item.rebuild()
    
    pygame.draw.rect(page,(255,255,255), pygame.Rect(((1080-w_3-200)//2,y_3+100),(w_3+200,h_3+250)))

    if action == "show":
        pygame.draw.rect(page,(160,160,160), pygame.Rect(((1080-w_3-200)//2,y_3+100),(w_3+200,h_3+250)))
        
        for i in range(len(text_entry_list)):
            text_entry_list[i].show()
        
        if selection_list != None:    
            for item in selection_list:
                item.show()
           
        for item in button_list:
            item.show()



def get_entry_list(workout_dict):
    entry_list = []
    init_text_list = []
    key_list = list(workout_dict.keys())
    for i in range(len(key_list)):
        para = pgg.elements.ui_text_entry_line.UITextEntryLine(relative_rect = pygame.Rect(((1080-200)//2,y_3+150+30*i),(200,20)),
                                                            manager = manager3,
                                                            object_id = str(key_list[i]),
                                                            visible = 0)
        #para.set_allowed_characters('numbers')
        init_text = key_list[i] +"(dflt "+str(workout_dict[key_list[i]])+")"
        para.set_text(init_text)
    
        entry_list.append(para)
        init_text_list.append(init_text)
    return entry_list, init_text_list


############# Pygame Page Design #####################
window_surface = pygame.display.set_mode((x_bg,y_bg))

workout_def = pygame.Surface((x_bg,y_bg))
workout_def.fill((255,255,255))

manager3 = pgg.UIManager((x_bg,y_bg))

# initialize positions
x_3 = 150
y_3 = 150
w_3 = 150
h_3 = 50




# button to next
nextButton = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((440,650),(200,50)),
                                                    text = "Next",
                                                    manager = manager3,
                                                    object_id = "next")

# title button
title_button = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect(((x_bg-500)//2,50),(500,50)),
                                                    text = "Define Your Workout",
                                                    manager = manager3,
                                                    object_id = "title")


###### create info entry part ########

# initialize workout parameter
tabata_parameter = {"on_time":25, "off_time":5, "round_rest":15, "rounds":5, "n_exercises":4}
dropset_parameter = {"on_time":25, "off_time":5, "round_rest":15, "n_exercises":5}
timed_workout_parameter= {"on_time":25, "off_time":5, "round_rest":15, "rounds":5, "n_exercises":4}
exox_parameter = {"interval":60, "difficulty":0.75, "rounds":4,"n_exercises":3}
totalrandom_parameter = {"on_range":(20,60), "off_range":(5,20), "on_prob":0.75, "n_exercises":20}


# customize button in panel
add_button = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect(((1080-50)//2+100,y_3+350),(50,30)),
                                                    text = "Add",
                                                    manager = manager3,
                                                    object_id = "add",
                                                    visible = 0)

cancel_button = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect(((1080-50)//2-100,y_3+350),(50,30)),
                                                    text = "Cancel",
                                                    manager = manager3,
                                                    object_id = "cancel",
                                                    visible = 0)
func_list = [add_button, cancel_button]


# game loop function
def define_workout(define_on, workout_result):
    global generate_on

    workout_define = dict()
    workout_para = {}

    # keep track of how many workouts has been defined for each type
    num_tabata = 1
    num_dropset = 1
    num_time_workout = 1
    num_exox = 1
    num_total_random = 1

    # workout output
    output_font = pygame.font.SysFont("Calibri", 20)
    output_ins = output_font.render("We will have:", False, (0,0,0))
    output_y = 0

    # workout button id = ["tabata","dropset","time_workout","exox","total_random"]
    for i in range(len(workout_result)):
        pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_3+(w_3+10)*i,y_3),(w_3,h_3)),
                                                    text = str(workout_result[i]),
                                                    manager = manager3,
                                                    object_id = workout_result[i].replace(" ","_").lower())

    # game loop
    while define_on:
        time_delta = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                define_on = False
            
            if event.type == pygame.USEREVENT:
                if event.user_type == pgg.UI_BUTTON_PRESSED:
                    if event.ui_object_id == "next":
                        define_on = False
                        generate_on = True
                    elif event.ui_object_id == "tabata":
                        workout_para = tabata_parameter
                        entry_list, init_text_list = get_entry_list(workout_para)
                        info_panel(workout_def, entry_list, func_list, init_text_list, action = "show")
                        workout_define.update({"tabata"+str(num_tabata):{}})
                        num_tabata +=1 
                    elif event.ui_object_id == "dropset":
                        workout_para = dropset_parameter
                        entry_list, init_text_list = get_entry_list(workout_para)
                        info_panel(workout_def, entry_list, func_list, init_text_list, action = "show")
                        workout_define.update({"dropset"+str(num_dropset):{}})
                        num_dropset +=1 
                    elif event.ui_object_id == "timed_workout":
                        workout_para = timed_workout_parameter
                        entry_list, init_text_list = get_entry_list(workout_para)
                        info_panel(workout_def, entry_list, func_list, init_text_list, action = "show")
                        workout_define.update({"timed_workout"+str(num_time_workout):{}})
                        num_time_workout +=1
                    elif event.ui_object_id == "exox":
                        workout_para = exox_parameter
                        entry_list, init_text_list = get_entry_list(workout_para)
                        info_panel(workout_def, entry_list, func_list, init_text_list, action = "show")
                        workout_define.update({"exox"+str(num_exox):{}})
                        num_exox +=1
                    elif event.ui_object_id == "total_random":
                        workout_para = totalrandom_parameter
                        entry_list, init_text_list = get_entry_list(workout_para)
                        info_panel(workout_def, entry_list, func_list, init_text_list, action = "show")
                        workout_define.update({"total_random"+str(num_total_random):{}})
                        num_total_random +=1
                    elif event.ui_object_id == "add":
                        workout_define[list(workout_define.keys())[-1]] = workout_para
                        info_panel(workout_def, entry_list, func_list)
                        output_text = output_font.render(str(list(workout_define.keys())[-1]), False, (0,0,0))
                        workout_def.blit(output_text,((800,375+output_y)))
                        output_y +=25
                    elif event.ui_object_id == "cancel":
                        info_panel(workout_def, entry_list, func_list)
                        added_workout = list(workout_define.keys())
                        if "tabata" in added_workout[-1]:
                            num_tabata -=1
                        elif "dropset" in added_workout[-1]:
                            num_dropset -=1
                        elif "timed_workout" in added_workout[-1]:
                            num_time_workout -=1
                        elif "exox" in added_workout[-1]:
                            num_exox -=1
                        elif "total_random" in added_workout[-1]:
                            num_total_random -=1
                        workout_define.popitem()

                elif event.user_type == pgg.UI_TEXT_ENTRY_CHANGED:
                    if event.ui_object_id == "on_time":
                        workout_para["on_time"] = int(event.text)
                    elif event.ui_object_id == "off_time":
                        workout_para["off_time"] = int(event.text)
                    elif event.ui_object_id == "round_rest":
                        workout_para["round_rest"] = int(event.text)
                    elif event.ui_object_id == "rounds":
                        workout_para["rounds"] = int(event.text)
                    elif event.ui_object_id == "n_exercises":
                        workout_para["n_exercises"] = int(event.text)
                    elif event.ui_object_id == "interval":
                        workout_para["interval"] = int(event.text)
                    elif event.ui_object_id == "difficulty":
                        workout_para["difficulty"] = float(event.text)
                    elif event.ui_object_id == "on_range":
                        workout_para["on_range"] = ast.literal_eval(event.text)
                    elif event.ui_object_id == "off_range":
                        workout_para["off_range"] = ast.literal_eval(event.text)
                    elif event.ui_object_id == "on_prob":
                        workout_para["on_prob"] = float(event.text)
                    
            manager3.process_events(event)

        manager3.update(time_delta)


        # paint text
        workout_def.blit(output_ins, (800,350))

        # paint surface
        window_surface.blit(workout_def,(0,0))
        manager3.draw_ui(workout_def)

        pygame.display.update()

    return generate_on, workout_define

#endregion


