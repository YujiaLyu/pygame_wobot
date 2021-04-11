from wobot.workouts import *
from wobot.displays import *


lower_body = ('Quadriceps', 'Hamstrings', 'Glutes', 'Calves', "LowerBack", "Abductors", "Adductors")
upper_body = ("Chest", "MiddleBack", "Lats", "Traps", 'Shoulders')
arms = ('Biceps', 'Triceps', "Forearms")


def monday_tabata_timed_emom(SEED =  None):
    global lower_body, upper_body, arms
    exclude = []
    # start with tabata
    tabata = Tabata(on_time=20, off_time=10, round_rest=10, rounds=4, n_exercises=3)
    tabata_workout = tabata.init(muscles=lower_body, seed=SEED)
    exclude.extend(list(set([ex.__class__ for ex in tabata_workout])))

    # arms involved
    timed_workout = TimedWorkout(on_time=45, off_time=15, round_rest=15, rounds=3, n_exercises=4)
    norm_workout = timed_workout.init(muscles=upper_body + arms, exclude_exercises=exclude, seed=SEED)
    exclude.extend(list(set([ex.__class__ for ex in norm_workout])))

    # end with cardio EMOM
    emom = EXOX()
    emom_workout = emom.init(etypes=('cardio',), equipment=(None,), exclude_exercises=exclude, seed=SEED)

    workout = tabata_workout + norm_workout + emom_workout

    final_list = []
    for item in workout:
        final_list.append(repr(item))

    return final_list
    

def monday_tabata_abtimed(SEED = None):
    global lower_body, upper_body, arms
    ab_burn = TimedWorkout(on_time=30, off_time=0, round_rest=15, rounds=1, n_exercises=6)
    tabata = Tabata(on_time=20, off_time=10, round_rest=10, rounds=4, n_exercises=4)

    exclude = []
    # leg tabata
    leg_tabata = tabata.init(muscles=lower_body, etypes=('strength',), alt=True, seed=SEED)
    exclude.extend(list(set([ex.__class__ for ex in leg_tabata])))
    abs1 = ab_burn.init(muscles=("Abdominals",), equipment=(None,), etypes=('strength',), seed=SEED)
    exclude.extend(list(set([ex.__class__ for ex in abs1])))

    # arm tabata
    arm_tabata = tabata.init(muscles=arms, etypes=('strength',), exclude_exercises=exclude, alt=True, seed=SEED)
    exclude.extend(list(set([ex.__class__ for ex in arm_tabata])))
    abs2 = ab_burn.init(muscles=("Abdominals",), equipment=(None,), seed=SEED ** 2)
    exclude.extend(list(set([ex.__class__ for ex in abs2])))

    # upper body
    upper_body = tabata.init(muscles=upper_body, etypes=('strength',), exclude_exercises=exclude, seed=SEED)
    exclude.extend(list(set([ex.__class__ for ex in upper_body])))
    abs3 = ab_burn.init(muscles=("Abdominals",), equipment=(None,), exclude_exercises=exclude, seed=SEED ** 3)
    exclude.extend(list(set([ex.__class__ for ex in abs3])))
    # cardio tabata
    cardio = tabata.init(etypes=('cardio',), exclude_exercises=exclude, seed=SEED)
    abs4 = ab_burn.init(muscles=("Abdominals",), equipment=(None,), etypes=('strength',), exclude_exercises=exclude, seed=SEED ** 4)

    workout = leg_tabata + abs1 + arm_tabata + abs2 + upper_body + abs3 + cardio + abs4 

    final_list = []
    for item in workout:
        final_list.append(repr(item))

    return final_list


def monday_dropset_emom(SEED = None):
    drop_set = DropSet(on_time=30, off_time=0, round_rest=10, n_exercises=4)
    emom = EXOX(difficulty=0.75, rounds=3)
    exclude = []

    drop_legs = drop_set.init(muscles=lower_body, etypes=('strength'), equipment=(None,), seed=SEED)
    exclude.extend(list(set([ex.__class__ for ex in drop_legs])))

    emom_legs = emom.init(exclude_exercises=exclude, muscles=lower_body, seed=SEED)
    exclude.extend(list(set([ex.__class__ for ex in emom_legs])))

    # upper body
    drop_upper_body = drop_set.init(muscles=upper_body, exclude_exercises=exclude, etypes=("strength",), seed=SEED)
    exclude.extend(list(set([ex.__class__ for ex in drop_upper_body])))
    emom_upper_body = emom.init(exclude_exercises=exclude, muscles=upper_body, seed=SEED)
    exclude.extend(list(set([ex.__class__ for ex in emom_upper_body])))
    # abs
    drop_abs = drop_set.init(muscles=('Abdominals',), exclude_exercises=exclude, equipment=(None,), seed=SEED)
    exclude.extend(list(set([ex.__class__ for ex in drop_abs])))
    emom_abs = emom.init(exclude_exercises=exclude, muscles=('Abdominals',), seed=SEED)

    workout = drop_legs + emom_legs + [Rest(20)] + drop_upper_body + emom_upper_body + [Rest(20)] + drop_abs + emom_abs

    final_list = []
    for item in workout:
        final_list.append(repr(item))

    return final_list


#def wednesday_timed_emom(SEED):


def thursday_thirty(SEED = None):
    total_random = TotalRandom(n_exercises=35)

    workout = total_random.init(equipment=(None,), seed=SEED)
    
    final_list = []
    for item in workout:
        final_list.append(repr(item))

    return final_list



def get_workout(workout,seed, display_on):
    if workout == "Tabata+Timed+Emom":
        final_list = monday_tabata_timed_emom(seed)
    elif workout == "Tabata+Timed(ab)":
        final_list = monday_tabata_abtimed(seed)
    elif workout == "Dropset+Emom":
        final_list = monday_dropset_emom(seed)
    elif workout == "Thursday Thirty":
        final_list = thursday_thirty(seed)

    display_on = True
    return display_on, final_list

