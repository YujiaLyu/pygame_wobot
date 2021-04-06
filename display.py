import pygame
import pygame_gui as pgg
import os
import datetime
import sys
import pathlib


# locate current file address
filepath = pathlib.Path(__file__).parent


# open file and read workout file
workout_file = open(str(filepath)+"\workout_result.txt", "r").read()
final_list = workout_file.strip("[]").split(",")
final_list = [item.strip("' ").split() for item in final_list]
final_list = [(int(item[0]),item[1]," ".join(item[3:])) for item in final_list]
final_list.insert(0,(3,'seconds', 'Get Ready'))
print(final_list)


# get total time length
total_time = 0
for item in final_list:
    if item[1] == "reps":
        total_time += 60
    else:
        total_time += int(item[0])
'''
if isinstance(final_list, list):
    final_list = [item.strip() for item in final_list]
    final_list = [(int(item.split()[0])," ".join(item.split()[3:])) for item in final_list]
'''


# initialize pygame
pygame.mixer.init(44100, -16, 1, 512)
pygame.init()

### paint the basic layers: window, background, UImanager
window_surface = pygame.display.set_mode((1080,720))

display_page = pygame.Surface((1080,720))
display_page.fill((255,255,255))

end_page = pygame.Surface((1080,720))
end_page.fill((255,255,255))

end_img =pygame.transform.scale(pygame.image.load(str(filepath)+"\end_image\end_image1.jpg"),(700,500))
end_img.convert()
end_rect = end_img.get_rect()
end_rect.center = (1080//2, 720//2)

manager = pgg.UIManager((1080,720),"display.json")
manager2 = pgg.UIManager((1080,720),"display.json")

clock = pygame.time.Clock()

# initialize key workout variables
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
    


# initialize time count
pygame.time.set_timer(pygame.USEREVENT, 1000)


# use button to display numbers and workout names
w_current = 500
x_current = (1080-w_current)//2
y_current = 120
w_next = 200
x_next = 800
y_next = 550



current_timelen = 0

pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((900,120),(150,30)),
                                                    text = convert_time(total_time),
                                                    manager = manager,
                                                    object_id = "total_time").disable()

if final_list[0][1] == "reps":
    current_timelen = 60
    pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_current,y_current),(w_current,150)),
                                                text = " ".join(final_list[0][::2]),
                                                manager = manager,
                                                object_id = "current_workout").disable()

    pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_current,y_current+150),(w_current,250)),
                                                text = convert_time(current_timelen),
                                                manager = manager,
                                                object_id = "current_time").disable()
else:
    current_timelen = int(final_list[0][0])
    pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_current,y_current),(w_current,150)),
                                                text = final_list[0][2],
                                                manager = manager,
                                                object_id = "current_workout").disable()

    pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_current,y_current+150),(w_current,250)),
                                                text = convert_time(current_timelen),
                                                manager = manager,
                                                object_id = "current_time").disable()


if len(final_list) > 1:
    pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_next,y_next),(w_next,50)),
                                                text = final_list[1][2],
                                                manager = manager,
                                                object_id = "next_workout").disable()

    pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_next,y_next+50),(w_next,75)),
                                                text = convert_time(int(final_list[1][0])),
                                                manager = manager,
                                                object_id = "next_time").disable()



# initialize health bar
num_total = len(final_list)
num_done = 0

def load_scale(num_total, num_done, surface, x,y,w,h, bc, sc, ic, font, font_size, font_color):
    pygame.draw.rect(surface, (213,213,213), (x+5,y+5,w+80,h))
    pygame.draw.rect(surface, bc, (x,y,w+80,h))
    pygame.draw.rect(surface, sc, (x+5,y+5,w-10,h-10))
    pygame.draw.rect(surface, ic, (x+5,y+5,(num_done/num_total)*(w-10),h-10))

    numText = pygame.font.SysFont(font, font_size)
    numprint = numText.render(str(num_done)+"/"+str(num_total), True, (0,0,0))
    surface.blit(numprint, (x+w+5,y+5))





# initialize sound effect
next_sound = pygame.mixer.Sound("beep.wav")
end_sound = pygame.mixer.Sound("beep_long.wav")


# initialize game loop condition:
is_displaying = True
ended = False

#initiate pausing
pause = False


# start game loop
while is_displaying:
    time_delta = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_displaying = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.USEREVENT:
            if current_timelen > 0:
                current_timelen -=1
                pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_current,y_current+150),(w_current,250)),
                                                text = convert_time(current_timelen),
                                                manager = manager,
                                                object_id = "current_time").disable()
            else:
                num_done +=1
                next_sound.play()
                if len(final_list) > 1:
                    final_list.pop(0)
                    if final_list[0][1] == "reps":
                        current_timelen = 60
                        pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_current,y_current),(w_current,150)),
                                                text = " ".join(final_list[0][::2]),
                                                manager = manager,
                                                object_id = "current_workout").disable()

                        pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_current,y_current+150),(w_current,250)),
                                                text = convert_time(current_timelen),
                                                manager = manager,
                                                object_id = "current_time").disable()
                    else:
                        current_timelen = int(final_list[0][0])
                        pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_current,y_current),(w_current,150)),
                                                text = final_list[0][2],
                                                manager = manager,
                                                object_id = "current_workout").disable()

                        pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_current,y_current+150),(w_current,250)),
                                                text = convert_time(current_timelen),
                                                manager = manager,
                                                object_id = "current_time").disable()

                    if len(final_list) > 1:
                        if final_list[1][1] == "reps":
                            pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_next,y_next),(w_next,50)),
                                                text = " ".join(final_list[1][::2]),
                                                manager = manager,
                                                object_id = "next_workout").disable()

                            pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_next,y_next+50),(w_next,75)),
                                                text = convert_time(60),
                                                manager = manager,
                                                object_id = "next_time").disable()
                        else:
                            pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_next,y_next),(w_next,50)),
                                                text = final_list[1][2],
                                                manager = manager,
                                                object_id = "next_workout").disable()

                            pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_next,y_next+50),(w_next,75)),
                                                text = convert_time(int(final_list[1][0])),
                                                manager = manager,
                                                object_id = "next_time").disable()
                    else:
                        pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_next,y_next),(w_next,50)),
                                                text = "DONE",
                                                manager = manager,
                                                object_id = "next_workout").disable()

                        pgg.elements.ui_button.UIButton(relative_rect=pygame.Rect((x_next,y_next+50),(w_next,75)),
                                                text = "DONE",
                                                manager = manager,
                                                object_id = "next_time").disable()
                else:
                    end_sound.play()
                    is_displaying = False
                    ended = True
        
        elif event.type == pygame.KEYDOWN:
            next_sound.play()
            pause = True

    while pause == True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                next_sound.play()
                pause = False
        
        pygame.time.delay(300)

  
        manager.process_events(event)

    manager.update(time_delta)

    load_scale(num_total, num_done,display_page, 110,50,800,40,(178,180,204),(201,202,219),(167,151,213), "Arial",25,(0,0,0))
    # paint surface
    window_surface.blit(display_page,(0,0))
    
    manager.draw_ui(display_page)
    pygame.display.update()



while ended:
    time_delta = clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_displaying = False
            pygame.quit()
            sys.exit()
    
        manager2.process_events(event)
    
    manager2.update(time_delta)

    window_surface.blit(end_page,(0,0))
    window_surface.blit(end_img, end_rect)
    manager2.draw_ui(end_page)

    pygame.display.update()



pygame.quit()











