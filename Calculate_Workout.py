from wobot.workouts import *
from wobot.displays import *
import pygame
import pygame_gui as pgg
import os
import datetime
import sys
import ast
import pathlib




############## calculate workout #########
# generate workout based on total_workout
# need to modify for exox and total_random (different parameters)

def define_all_workout(workout_define):
    defined_workout = {}
    for key in workout_define:
        if "tabata" in key:
            tabata = Tabata(on_time = workout_define[key]["on_time"], 
                            off_time = workout_define[key]["off_time"], 
                            round_rest = workout_define[key]["round_rest"], 
                            rounds = workout_define[key]["rounds"], 
                            n_exercises = workout_define[key]["n_exercises"])
            defined_workout.update({key:tabata})
        elif "dropset" in key:
            drop_set = DropSet(on_time = workout_define[key]["on_time"], 
                            off_time = workout_define[key]["off_time"], 
                            round_rest = workout_define[key]["round_rest"], 
                            n_exercises = workout_define[key]["n_exercises"])
            defined_workout.update({key:drop_set})
        elif "timed_workout" in key:
            timed_workout = TimedWorkout(on_time = workout_define[key]["on_time"], 
                                        off_time = workout_define[key]["off_time"], 
                                        round_rest = workout_define[key]["round_rest"], 
                                        rounds = workout_define[key]["rounds"],
                                        n_exercises = workout_define[key]["n_exercises"])
            defined_workout.update({key:timed_workout})
        elif "exox" in key:
            exox = EXOX(interval = workout_define[key]["interval"], 
                                        difficulty = workout_define[key]["difficulty"],  
                                        rounds = workout_define[key]["rounds"],
                                        n_exercises = workout_define[key]["n_exercises"])
            defined_workout.update({key:exox})
        elif "total_random" in key:
            total_random = TotalRandom(on_range = workout_define[key]["on_range"], 
                                        off_range = workout_define[key]["off_range"],  
                                        on_prob = workout_define[key]["on_prob"],
                                        n_exercises = workout_define[key]["n_exercises"])
            defined_workout.update({key:total_random})
    
    return defined_workout


def get_final_workout(total_workout, defined_workout, muscle_result, seed_output):
    exclude = []
    final_workout = []
    final_list = []    
    for key in total_workout:
        workout_name = key[:-1]
        muscle = tuple()
        if total_workout[key]['muscle'] != None:
            for item in total_workout[key]['muscle']:
                muscle += muscle_result[item]
        else:
            muscle = None
        equipment = total_workout[key]["equipment"]
        etypes = total_workout[key]["etypes"]
        alt = total_workout[key]["alt"]

        if any(item for item in ["tabata", "timed_workout"] if item in key):
            workout = defined_workout[workout_name].init(muscles = muscle,
                                            equipment = equipment,
                                            etypes = etypes,
                                            alt = alt,
                                            exclude_exercises = exclude,
                                            seed = seed_output)
            exclude.extend(list(set(ex.__class__ for ex in workout)))
            final_workout.extend(workout)
        elif any(item for item in ["dropset","exox", "total_random"] if item in key):
            workout = defined_workout[workout_name].init(muscles = muscle,
                                            equipment = equipment,
                                            etypes = etypes,
                                            exclude_exercises = exclude,
                                            seed = seed_output)
            exclude.extend(list(set(ex.__class__ for ex in workout)))
            final_workout.extend(workout)

    for item in final_workout:
        final_list.append(repr(item))

    return final_list





#endregion