# pygame_wobot
Need WorkoutGenerator (https://github.com/jdkent/workoutGenerator) to function

**** Simple Start****
** Run Simple_Wobot to start **
- Simple_Start
- Get_Seed
- Predefined_Workout
- Present_Workout
- Running_Workout




**** Full Customization Version ****
**Run main_wobot_loop to use the game.**

Each pygame page are written in their own file:
- Muscle_Select (remove unwanted muscles)
- Select_Workout (select workout types: tabata, dropset, timed workout, exox, total random)
- Define_Workout (get user input on basic parameters: on_time, off_time, round_rest, rounds, n_exercises, interval, difficulty, on_range, off_range,on_prob)
- Generate_Workout (get user input on other parameters: muscles, equipment, etypes, alt)
- Get_Seed (ask user to give a number; can use members' names)
- Calculate_Workout (functions to sample workouts based on specification)
- Present_Workout (review generated workout)
- Running_Workout (page with timer)


Generated workout are automatically stored into .txt file, noted with today's date.


Bugs in workout parameters are fixed. Should be able to generate workout in most cases.



Next Step:
- improve visuals
- makes text input follow natural style; avoid crush result from wrong key
- if workout doesn't look good, go back and get another seed
- check small bugs
