import random
import copy
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
#2D list where each inner list has the form [fitness, activity, room, capacity, time, facilitator]
population = []
for i in range(1000): 
    schedule = []
    fitness = 0
    for i in activities:
        currentActivity = [0] #assigns base fitness of 0
        currentActivity.append(i)
        room = random.choice(rooms)
        currentActivity.append(room[0])
        currentActivity.append(room[1])
        currentActivity.append(random.choice(times))
        currentActivity.append(random.choice(facilitators))
        schedule.append(currentActivity)
        
    fitness = modules.fitness(schedule)
    schedule.insert(0, fitness)
    population.append(schedule)

i=0
gen100 = []
#Generate the first 100 generations
while i < 100:
    print (f"Gen {i+1} Best Candidate")
    population.sort(key= lambda x: x[0], reverse=True)
    print(population[0])
    print()
    if i == 99:
        gen100 = copy.deepcopy(population)
        i+=1
        break
    # modules.naturalSelection(population)
    population = modules.naturalSelection(population)
    i += 1

improvement = 1
#Keep generating new generations until the improvement after gen 100 is < 1%
while improvement > .01:
    population = modules.naturalSelection(population)
    print (f"Gen {i+1} Best Candidate")
    population.sort(key= lambda x: x[0], reverse=True)
    print(population[0])
    improvement = (population[0][0] - gen100[0][0]) / abs(gen100[0][0])
    print()

f = open("output.txt", "w")
f.write(f"Final Schedule Fitness Score: {str(population[0][0])} \n")
f.write("Fitness - Activity - Room - Time - Facilitator\n")
f.write("----------------------------------------------\n")
for i in range(11):
    f.write(f"{str(population[0][i+1][0])} - {str(population[0][i+1][1])} - {str(population[0][i+1][2])} - {str(population[0][i+1][4])} - {str(population[0][i+1][5])}\n")
f.close()