import random
import modules

#all activities MWF - 50 mins
#2 sections (A and B) of some activity
#Program assigns for each activity: Room, Time, Facilitator

#Room names and their capacity
rooms = [("Slater003",45), ("Roman216",30), ("Loft206",75), ("Roman201",50), 
         ("Loft310",108), ("Beach201",60), ("Beach301",75), ("Logos325",450), ("Frank119",60)]
facilitators = ["Lock", "Glen", "Banks", "Richards", "Shaw", "Singer", "Uther", "Tyler", "Numen", "Zeldin"]
activities = ["sla100A", "sla100B", "sla191A", "sla191B", "sla201", 
              "sla291", "sla303", "sla304", "sla394", "sla449", "sla451"]
#10AM, 11AM, 12PM, 1PM, 2PM, 3PM  in 24 hour time
times = [10, 11, 12, 13, 14, 15]

#Create initial population
#2D list where each inner list has the form [fitness, activity, room, time, facilitator]
population = []
for i in range(1000): 
    schedule = []
    fitness = 0
    for i in activities:
        currentActivity = [0] #assigns base fitness of 0
        currentActivity.append(i)
        currentActivity.append(random.choice(rooms))
        currentActivity.append(random.choice(times))
        currentActivity.append(random.choice(facilitators))
        schedule.append(currentActivity)
        
    fitness = modules.fitness(schedule)
    schedule.insert(0, fitness)
    population.append(schedule)

# print("OLD GEN")
# for x in population:    
#     print(x)
#     print()


#Something is wrong with the way new generations are being created and their fitness values, may be due to how children are created and lists
for i in range(100):
    print (f"Gen {i+1} Best Candidate")
    population.sort(key= lambda x: x[0])
    print(population[0])
    print()
    modules.naturalSelection(population)