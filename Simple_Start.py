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
is_start = False


def selection_panel(page, selection_list, action = None):
    '''
    parameters are in the form of list
    '''
    for item in selection_list:
        item.hide()
        #item.rebuild()
    

    if action == "show":
        for item in selection_list:
            item.show()



################## display workout  ####################
window_surface = pygame.display.set_mode((x_bg,y_bg))

button_start = pygame.Surface((x_bg,y_bg))
button_start.fill((235,236,238))

manager = pgg.UIManager((x_bg,y_bg),"start_page.json")


x = 125
y = 150
w = 200
h = 100


# initiate buttons (Fullbody Monday, Weighty Wednesday, Thursday Thirty, )
button_list = ["Fullbody Monday", "Weighty Wednesday", "Thursday Thirty", "Happy Saturday"]

for i in range(len(button_list)):
    pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x+i*(w+10),y),(w,h)),
                                                    text = button_list[i],
                                                    manager = manager,
                                                    object_id = button_list[i].replace(" ",""))


# title button
title_button = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect(((x_bg-500)//2,50),(500,50)),
                                                    text = "Select a Workout",
                                                    manager = manager,
                                                    object_id = "title")
title_button.disable()



# internal workout selection list
monday = ["Tabata+Timed+Emom","Tabata+Timed(ab)", "Dropset+Emom"]
wednesday = ["Timed+Emom"]
saturday = []
internal_selection = [monday, wednesday,saturday]

selection_list = []
for item in internal_selection:
    select = pgg.elements.ui_selection_list.UISelectionList(relative_rect=pygame.Rect(((x_bg-w-100)//2,y+150),(w+100,h+150)),
                                                    item_list = item,
                                                    manager = manager,
                                                    allow_double_clicks= True,
                                                    object_id = "selection",
                                                    visible = 0)
    selection_list.append(select)



# game loop function
def start_selection(is_start, seed_on):

    # initialize return
    selected_workout = ""

    # game loop
    while is_start:
        time_delta = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_start = False
            
            if event.type == pygame.USEREVENT:
                if event.user_type == pgg.UI_BUTTON_PRESSED:
                    if event.ui_object_id == "FullbodyMonday":
                        selection_panel(button_start, [selection_list[1]])
                        selection_panel(button_start, [selection_list[2]])
                        selection_panel(button_start, [selection_list[0]],action = "show")
                    elif event.ui_object_id == "WeightyWednesday":
                        selection_panel(button_start, [selection_list[0]])
                        selection_panel(button_start, [selection_list[2]])
                        selection_panel(button_start, [selection_list[1]],action = "show")
                    elif event.ui_object_id == "ThursdayThirty":
                        selected_workout = "Thursday Thirty"
                        is_start = False
                        seed_on = True
                    elif event.ui_object_id == "HappySaturday":
                        selection_panel(button_start, [selection_list[0]])
                        selection_panel(button_start, [selection_list[1]])
                        selection_panel(button_start, [selection_list[2]],action = "show")

                elif event.user_type == pgg.UI_SELECTION_LIST_NEW_SELECTION:
                    if event.ui_object_id == "selection":
                        selected_workout = event.text

                    is_start = False
                    seed_on = True        
                    
                
            manager.process_events(event)

        manager.update(time_delta)



        # paint surface
        window_surface.blit(button_start,(0,0))
        manager.draw_ui(button_start)

        pygame.display.update()

    return seed_on, selected_workout



