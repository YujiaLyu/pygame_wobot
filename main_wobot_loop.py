'''
main game loop
'''
import Muscle_Select as MS
import Select_Workout as SW
import Define_Workout as DW
import Generate_Workout as GW
import Get_Seed as GS
import Calculate_Workout as CW
import Present_Workout as PW


from datetime import date
import pathlib



# locate current file address
filepath = pathlib.Path(__file__).parent

# initialize game loop condition
muscle_on = True
select_on = True
define_on = False
generate_on = False
seed_on = False
display_on = False
is_running = False
ended = False


# remove unwanted workout
select_on, muscle_result = MS.get_muscle(muscle_on) 
print(muscle_result)


# select types of workout
define_on, workout_result = SW.select_workout(select_on)
print(workout_result)

# define workout (on_time, off_time, round_rest, rounds, n_exercises, interval, difficulty, on_range, off_range,on_prob)
generate_on, workout_define = DW.define_workout(define_on, workout_result)
print(workout_define)

# further customize workout (muscles, equipment, etypes, alt)
seed_on, total_workout = GW.generate_workout(generate_on, workout_define, muscle_result)
print(total_workout)

# get random seed
display_on, seed_output = GS.obtain_seed(seed_on)
print(seed_output)

# calculate workout
defined_workout = CW.define_all_workout(workout_define)

final_list = CW.get_final_workout(total_workout, defined_workout, muscle_result, seed_output)


# check if last two items are rests
if "rest" in final_list[-2].lower() and "rest" in final_list[-1].lower():
    final_list.pop()
    final_list.pop()
elif "rest" in final_list[-1].lower():
    final_list.pop()

# save workout to file
today = date.today().strftime("%d_%m_%Y")
with open("workout_result_"+today+".txt", 'w') as out_file:
    out_file.write(str(final_list))


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


# import must happen at last
from Running_Workout import running_workout

running_workout(is_running, ended, total_time, final_list, filepath)

