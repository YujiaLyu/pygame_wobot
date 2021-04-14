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
is_running = False
ended = False

'''
# open file and read workout file
workout_file = open(str(filepath)+"\workout_result.txt", "r").read()
final_list = workout_file.strip("[]").split(",")
final_list = [item.strip("' ").split() for item in final_list]
final_list = [(int(item[0]),item[1]," ".join(item[3:])) for item in final_list]
final_list.insert(0,(3,'seconds', 'Get Ready'))
print(final_list)
'''

################## display workout  ####################
window_surface = pygame.display.set_mode((x_bg,y_bg))

display_page = pygame.Surface((x_bg,y_bg))
display_page.fill((235,236,238))

end_page = pygame.Surface((x_bg,y_bg))
end_page.fill((235,236,238))



manager7 = pgg.UIManager((x_bg,y_bg),"display2.json")
manager8 = pgg.UIManager((x_bg,y_bg),"display2.json")

# use button to display numbers and workout names
w_current = 880
x_current = (x_bg-w_current)//2
y_current = 80
w_next = 300
x_next = 680
y_next = 525


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


def load_scale(num_total, num_done, surface, x,y,w,h, bc, sc, ic, font, font_size, font_color):
    pygame.draw.rect(surface, (213,213,213), (x+5,y+5,w+80,h))
    pygame.draw.rect(surface, bc, (x,y,w+80,h))
    pygame.draw.rect(surface, sc, (x+5,y+5,w-10,h-10))
    pygame.draw.rect(surface, ic, (x+5,y+5,(num_done/num_total)*(w-10),h-10))

    numText = pygame.font.SysFont(font, font_size)
    numprint = numText.render(str(num_done)+"/"+str(num_total), True, (0,0,0))
    surface.blit(numprint, (x+w+5,y+5))


# initialize time count
pygame.time.set_timer(pygame.USEREVENT, 1000)




def running_workout(is_running, ended, total_time, final_list, filepath):
    global current_timelen
    #initiate local variables
    pause = False
    current_timelen = 0
    done_time = -3

    # convert final_list
    final_list = [item.split() for item in final_list]
    final_list = [(int(item[0]),item[1]," ".join(item[3:])) for item in final_list]
    final_list.insert(0,(3,'seconds', 'Get Ready'))

    # initialize sound effect
    next_sound = pygame.mixer.Sound("beep.wav")
    end_sound = pygame.mixer.Sound("beep_long.wav")
    
    # intialize total time buttons
    time_lapse = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((100,y_next),(200,50)),
                                                    text = "Time Lapse",
                                                    manager = manager7,
                                                    object_id = "total_time")
    total_timelen = pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((100,y_next+50),(200,75)),
                                                    text = convert_time(done_time)+"/"+convert_time(total_time),
                                                    manager = manager7,
                                                    object_id = "total_time")
    

    # initialize end image
    end_img =pygame.transform.scale(pygame.image.load(str(filepath)+"\end_image\end_image1.jpg"),(700,500))
    end_img.convert()
    end_rect = end_img.get_rect()
    end_rect.center = (x_bg//2, y_bg//2)

    #current_display(x_current, y_current, w_current, final_list, current_timelen)

    
    # initialize displaying labels
    current_timelen = int(final_list[0][0])
    current_workout = pgg.elements.ui_label.UILabel(relative_rect=pygame.Rect((x_current,y_current),(w_current,150)),
                                                    text = final_list[0][2],
                                                    manager = manager7,
                                                    object_id = "current_workout")
    
    current_time = pgg.elements.ui_label.UILabel(relative_rect=pygame.Rect((x_current,y_current+150),(w_current,250)),
                                                    text = convert_time(current_timelen),
                                                    manager = manager7,
                                                    object_id = "current_time")
    rest = pgg.elements.ui_label.UILabel(relative_rect=pygame.Rect((x_current,y_current),(w_current,150)),
                                                    text = final_list[0][2],
                                                    manager = manager7,
                                                    object_id = "rest",
                                                    visible = 0)
    rest_time = pgg.elements.ui_label.UILabel(relative_rect=pygame.Rect((x_current,y_current+150),(w_current,250)),
                                                    text = convert_time(current_timelen),
                                                    manager = manager7,
                                                    object_id = "rest_time",
                                                    visible = 0)
                                    
    next_workout = pgg.elements.ui_label.UILabel(relative_rect=pygame.Rect((x_next,y_next),(w_next,50)),
                                                    text = final_list[1][2],
                                                    manager = manager7,
                                                    object_id = "next_workout",
                                                    visible = 0)

    next_time = pgg.elements.ui_label.UILabel(relative_rect=pygame.Rect((x_next,y_next+50),(w_next,75)),
                                                    text = convert_time(int(final_list[1][0])),
                                                    manager = manager7,
                                                    object_id = "next_time",
                                                    visible = 0)

    if final_list[0][1] == "reps":
        current_timelen = 30
        current_workout.set_text(" ".join(final_list[0][::2]))
        current_time.set_text(convert_time(current_timelen))

    elif final_list[0][2].lower() == "rest":
        current_timelen = int(final_list[0][0])
        rest.show()
        rest_time.show()

    


    if len(final_list) > 1:
        next_workout.show()
        next_time.show()


    # main running loop
    while is_running:
        time_delta = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame.USEREVENT:
                if current_timelen > 0:
                    done_time += 1
                    current_timelen -=1
                    if final_list[0][2].lower() == "rest":
                        rest_time.set_text(convert_time(current_timelen))
                        
                    else:
                        current_time.set_text(convert_time(current_timelen))

                    total_timelen.set_text(convert_time(done_time)+"/"+convert_time(total_time))    
                    
                else:
                    next_sound.play()
                    if len(final_list) > 1:
                        final_list.pop(0)
                        #current_display(x_current, y_current, w_current, final_list, current_timelen)
                        
                        if final_list[0][1] == "reps":
                            current_timelen = 60
                            current_workout.set_text(" ".join(final_list[0][::2]))
                            current_time.set_text(convert_time(current_timelen))

                        elif final_list[0][2].lower() == "rest":
                            current_timelen = int(final_list[0][0])
                            current_workout.hide()
                            current_time.hide()
                            rest.set_text(final_list[0][2])
                            rest.show()

                            rest_time.set_text(convert_time(current_timelen))
                            rest_time.show()
                    
                        else:
                            rest.hide()
                            rest_time.hide()
                            current_timelen = int(final_list[0][0])
                            current_workout.set_text(final_list[0][2])
                            current_workout.show()
                            current_time.set_text(convert_time(current_timelen))
                            current_time.show()
                        

                        if len(final_list) > 1:
                            if final_list[1][1] == "reps":
                                next_workout.set_text(" ".join(final_list[1][::2]))
                                next_workout.show()
                                next_time.set_text(convert_time(60))
                                next_time.show()
                        
                            else:
                                next_workout.set_text(final_list[1][2])
                                next_workout.show()
                                next_time.set_text(convert_time(int(final_list[1][0])))
                                next_time.show()
                                
                        else:
                            next_workout.set_text("DONE")
                            next_workout.show()
                            next_time.set_text("DONE")
                            next_time.show()
                            
                    else:
                        end_sound.play()
                        is_running = False
                        ended = True
            
            elif event.type == pygame.KEYDOWN:
                next_sound.play()
                pause = True

        while pause == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                if event.type == pygame.KEYDOWN:
                    next_sound.play()
                    pause = False
            
            pygame.time.delay(300)

    
            manager7.process_events(event)

        manager7.update(time_delta)

        # paint surface
        window_surface.blit(display_page,(0,0))
        
        manager7.draw_ui(display_page)
        pygame.display.update()


    while ended:
        time_delta = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ended = False
                pygame.quit()
        
            manager8.process_events(event)
        
        manager8.update(time_delta)

        window_surface.blit(end_page,(0,0))
        window_surface.blit(end_img, end_rect)
        manager8.draw_ui(end_page)

        pygame.display.update()