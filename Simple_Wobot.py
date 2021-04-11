'''
simple game loop
'''

import Simple_Start as SS 
import Get_Seed as GS
import PreDefined_Workout as PDW
import Present_Workout as PW
import pathlib



# locate current file address
filepath = pathlib.Path(__file__).parent



# initialize game loop condition
is_start = True
seed_on = False
display_on = False
is_running = False
ended = False

# select workout
seed_on, selected_workout = SS.start_selection(is_start, seed_on)
print(selected_workout)

# get random seed
display_on, seed_output = GS.obtain_seed(seed_on)
print(seed_output)

# generate workout
display_on, final_list= PDW.get_workout(selected_workout, seed_output, display_on)

# get total time length
total_time = 0
for item in final_list:
    workout = item.split()
    if "reps" in workout:
        total_time += 60
    else:
        total_time += int(workout[0])



# review workout
is_running = PW.display_workout(display_on, final_list, total_time)


# running workout
from Running_Workout import running_workout

running_workout(is_running, ended, total_time, final_list, filepath)