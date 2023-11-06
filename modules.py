from scipy.special import softmax
import numpy as np
import random
import copy

class Activity:
    def __init__(self, expectedEnrollment, preferredFacilitator, otherFacilitator):
        self.expectedEnrollment = expectedEnrollment
        self.preferredFacilitator = preferredFacilitator
        self.otherFacilitator = otherFacilitator

#reference for defining an activity used for scoring purposes only
# sla100A = Activity(50, ("Glen","Lock","Banks","Zeldin"), ("Numen","Richards"))
# sla100B = Activity(50, ("Glen","Lock","Banks","Zeldin"), ("Numen","Richards"))
# sla191A = Activity(50, ("Glen","Lock","Banks","Zeldin"), ("Numen","Richards"))
# sla191B = Activity(50, ("Glen","Lock","Banks","Zeldin"), ("Numen","Richards"))
# sla201 = Activity(50, ("Glen","Banks","Zeldin","Shaw"), ("Numen","Richards","Singer"))
# sla291 = Activity(50, ("Lock","Banks","Zeldin","Singer"), ("Numen","Richards","Singer"))
# sla303 = Activity(60, ("Glen","Zeldin","Banks"), ("Numen","Singer","Shaw")) 
# sla304 = Activity(25, ("Glen","Banks","Tyler"), ("Numen","Singer","Shaw","Richards","Uther","Zeldin"))
# sla394 = Activity(20, ("Tyler","Singer"), ("Richards","Zeldin"))
# sla449 = Activity(60, ("Tyler","Singer","Shaw"), ("Zeldin","Uther"))
# sla451 = Activity(100, ("Tyler","Singer","Shaw"), ("Zeldin","Uther"))

#                                                  0        1      2,0      2,1     3       4
#recieves one child of the current population [fitness, activity, room and capac, time, facilitator]
def fitness(schedule):
    fitnessNum = 0
    for activity in schedule:
        if isinstance(activity,float):
            continue
        match (activity[1]):
            case 'sla100A':
                activityPreferences = Activity(50, ("Glen","Lock","Banks","Zeldin"), ("Numen","Richards"))
            case 'sla100b':
                activityPreferences = Activity(50, ("Glen","Lock","Banks","Zeldin"), ("Numen","Richards"))
            case 'sla191A':
                activityPreferences = Activity(50, ("Glen","Lock","Banks","Zeldin"), ("Numen","Richards"))
            case 'sla191B':
                activityPreferences = Activity(50, ("Glen","Lock","Banks","Zeldin"), ("Numen","Richards"))
            case 'sla201':
                activityPreferences = Activity(50, ("Glen","Banks","Zeldin","Shaw"), ("Numen","Richards","Singer"))
            case 'sla291':
                activityPreferences = Activity(50, ("Lock","Banks","Zeldin","Singer"), ("Numen","Richards","Singer"))
            case 'sla303':
                activityPreferences = Activity(60, ("Glen","Zeldin","Banks"), ("Numen","Singer","Shaw"))
            case 'sla304':
                activityPreferences = Activity(25, ("Glen","Banks","Tyler"), ("Numen","Singer","Shaw","Richards","Uther","Zeldin"))
            case 'sla394':
                activityPreferences = Activity(20, ("Tyler","Singer"), ("Richards","Zeldin"))
            case 'sla449':
                activityPreferences = Activity(60, ("Tyler","Singer","Shaw"), ("Zeldin","Uther"))
            case 'sla451':
                activityPreferences = Activity(100, ("Tyler","Singer","Shaw"), ("Zeldin","Uther"))

        #check if activity is scheduled at same time in same room as another activity
        for i in schedule:
            if i[1] == activity[1]: #if item being checked is our current activity continue to next iteration of loop
                continue
            elif i[4] == activity[4] and i[2][0] == activity[2][0]: #if item being checked has same time and room
                activity[0] -= 0.5
                break
            else:
                continue

        #check room size
        if activityPreferences.expectedEnrollment > activity[2][1]: #room size too small for expected enrollment
            activity[0] -= 0.5
        elif activityPreferences.expectedEnrollment*3 < activity[2][1]: #room size is over 3 times expected enrollment
            activity[0] -= 0.2
        elif activityPreferences.expectedEnrollment*6 < activity[2][1]: #room size is over 6 times expected enrollment
            activity[0] -= 0.4
        else:
            activity[0] += 0.3

        #check facilitator preferences
        if activity[4] in activityPreferences.preferredFacilitator: #activity overseen by preferred faciliatator
            activity[0] += 0.5
        elif activity[4] in activityPreferences.otherFacilitator: #activity overseen by another listed facilitator
            activity[0] += 0.2
        else:                                                     #activity overseen by unlisted facilitator
            activity[0] -= 0.1
    
        #check faciliatator load
        numClasses = 1 #current facilitator initialized with 1 total class
        timeSlots = [(activity[3], activity[2][0])]
        for i in schedule:
            if i[1] == activity[1]:  #if item being checked is our current activity continue to next iteration of loop
                continue
            elif i[4] == activity[4]: #if facilitator being checked is the same one as current activity but for a different activity
                numClasses += 1
                timeSlots.append((i[3], i[2][0]))
                continue
        
        timeSlots.sort()
        if sum(1 for elem in timeSlots if elem[0] == activity[3]) == 1: #if activity facilitator is scheduled for only 1 activity in this time slot
            activity[0] += 0.2
        else:                                 #if activity facilitator is scheduled for more than one activity at the same time
            activity[0] -= 0.2
        if numClasses > 4: #if facilitator is scheduled to oversee more than 4 activities total
            activity[0] -= 0.5 
        if numClasses == 1 or numClasses == 2: #facilitator is scheduled to oversee 1 or 2 activities
            if activity[4] == 'Tyler' and numClasses < 2:
                continue
            else:
                activity[0] -= 0.4
        
        #check if facilitator has consecutive classes
        j = 0
        consecutive = False
        consecutiveClasses = []
        while j < len(timeSlots)-1:
            if abs(timeSlots[j+1][0] - timeSlots[j][0]) == 1:
                consecutive = True
                consecutiveClasses.append(timeSlots[j][1])
                consecutiveClasses.append(timeSlots[j+1][1])
                break
            j+=1
        if consecutive:
            activity[0] += 0.5
            #if one of the consecutive activites is in Roman or Beach but the other isnt -0.4 otherwise its fine
            if ((consecutiveClasses[0] == 'Roman216' or consecutiveClasses[0] == 'Roman201' or consecutiveClasses[0] == 'Beach201' or consecutiveClasses[0] == 'Beach301') and
               (consecutiveClasses[1] == 'Roman216' or consecutiveClasses[1] == 'Roman201' or consecutiveClasses[1] == 'Beach201' or consecutiveClasses[1] == 'Beach301')):
                continue
            else:
                activity[0] -= 0.4

        #Activity-Specific adjustments
        if activity[1] == 'sla191A' or activity[1] == 'sla191B':
            for i in schedule:
                if i[1] == activity[1]: #if same activity as current 
                    continue
                elif i[1] == 'sla191A' or i[1] == 'sla191B': #if i is the other sla191 section
                    if abs(i[3] - activity[3]) > 4: #if the 2 sections are more than 4 hours apart
                        activity[0] += 0.5
                    else:
                        activity[0] -= 0.5

        if activity[1] == 'sla100A' or activity[1] == 'sla100B':
            for i in schedule:
                if i[1] == activity[1]: #if same activity as current 
                    continue
                elif i[1] == 'sla100A' or i[1] == 'sla100B': #if i is the other sla100 section
                    if abs(i[3] - activity[3]) > 4: #if the 2 sections are more than 4 hours apart
                        activity[0] += 0.5
                    else:
                        activity[0] -= 0.5
                elif i[1] == 'sla191A' or i[1] == 'sla191B':
                    if abs(i[3] - activity[3]) == 1: #if the sla100 and sla191 sections are consecutive
                        activity[0] += 0.5
                        #if one of the consecutive activites is in Roman or Beach but the other isnt -0.4 otherwise its fine
                        if ((i[0] == 'Roman216' or i[0] == 'Roman201' or i[0] == 'Beach201' or i[0] == 'Beach301') and
                            (activity[1] == 'Roman216' or activity[1] == 'Roman201' or activity[1] == 'Beach201' or activity[1] == 'Beach301')):
                            continue
                        else:
                            activity[0] -= 0.4
                    elif abs(i[3] - activity[3]) == 2: #if the sla100 and sla191 sections are separated by 1 hour e.g:10Am and 12Pm
                        activity[0] += 0.25
                    elif abs(i[3] - activity[3]) == 0: #if the sla100 and sla 191 sections are taught in the same time slot
                        activity[0] -= 0.25

        activity[0] = round(activity[0], 2) #used to simplify floatingpoints from excessive decimal places
        fitnessNum += activity[0]

    return round(fitnessNum, 2)

def naturalSelection(population):
    #Perform softmax normalization to convert all fitness scores into a probability distribution
    matingPool = []
    fitnessValues=[]
    for schedule in population:
        fitnessValues.append(schedule[0])
    # print(fitnessValues)
    normalized = softmax(fitnessValues)
    # print(normalized)

    #Select 500 schedules to reproduce
    while len(matingPool) != 500:
        randomNum = random.random()
        for elem in normalized:
            if elem >= randomNum:
                matingPool.append(population[np.where(normalized == elem)[0][0]])
                break
    
    newPopulation = reproduce(matingPool)
    for schedule in newPopulation:
        scheduleFitness = 0
        scheduleFitness = fitness(schedule)
        schedule.insert(0, scheduleFitness)
    # for i in range(500):
    #     population[i] = newPopulation[i]
    return newPopulation

def reproduce(matingPool): #Generates 2 children from 2 parents and adds them to the next generation
    newGeneration = []
    for i in range(500):
        schedule1 = random.choice(matingPool)
        schedule2 = random.choice(matingPool)

        newSchedules = crossover(schedule1, schedule2)
        mutate(newSchedules[0], 0.01)
        mutate(newSchedules[1], 0.01)
        newGeneration.append(newSchedules[0])
        newGeneration.append(newSchedules[1])
    return newGeneration

def crossover(schedule1, schedule2):    #Crossover of form [m,d,m,d,m,d,m,d,m,...] for child 1 and [d,m,d,m,d,m,d,m,d,m,...] for child 2
    # newSchedule1 = [] 
    # newSchedule2 = []
    newSchedule1 = [None] * (len(schedule1))
    newSchedule2 = [None] * (len(schedule1))
    

    for i in range(11):
        schedule1[i+1][0] = 0
        schedule2[i+1][0] = 0

    newSchedule1[0::2] = schedule1[0::2]
    newSchedule1[1::2] = schedule2[1::2]
    newSchedule2[0::2] = schedule2[0::2]
    newSchedule2[1::2] = schedule1[1::2]

    # for i in range(11): #11 classes
    #     if i % 2 == 0:
    #         schedule1[i+1][0] = 0
    #         schedule2[i+1][0] = 0
    #         newSchedule1.append(copy.deepcopy(schedule1[i+1]))
    #         newSchedule2.append(copy.deepcopy(schedule2[i+1]))
    #         # newSchedule1.append(schedule1[i+1])
    #         # newSchedule2.append(schedule2[i+1])
    #     else:
    #         schedule1[i+1][0] = 0
    #         schedule2[i+1][0] = 0
    #         # activity1 = schedule2[i+1].copy()
    #         # activity2 = schedule1[i+1].copy()
    #         # newSchedule1.append(activity1)
    #         # newSchedule2.append(activity2)
    #         newSchedule1.append(copy.deepcopy(schedule2[i+1]))
    #         newSchedule2.append(copy.deepcopy(schedule1[i+1]))
    #         # newSchedule1.append(schedule2[i+1])
    #         # newSchedule2.append(schedule1[i+1])
    
    return [newSchedule1,newSchedule2]
    # schedule1[:] = copy.deepcopy(newSchedule1)
    # schedule2[:] = copy.deepcopy(newSchedule2)


def mutate(schedule, mutationRate):
    rooms = [("Slater003",45), ("Roman216",30), ("Loft206",75), ("Roman201",50), 
         ("Loft310",108), ("Beach201",60), ("Beach301",75), ("Logos325",450), ("Frank119",60)]
    facilitators = ["Lock", "Glen", "Banks", "Richards", "Shaw", "Singer", "Uther", "Tyler", "Numen", "Zeldin"]
    #10AM, 11AM, 12PM, 1PM, 2PM, 3PM  in 24 hour time
    times = [10, 11, 12, 13, 14, 15]

    for activity in schedule:
        if isinstance(activity,float):
            continue
        if (random.random() < mutationRate):
            mutatedRoom = random.choice(rooms)
            mutatedTime = random.choice(times)
            mutatedFacilitator = random.choice(facilitators)

            activity[2] = mutatedRoom
            activity[3] = mutatedTime
            activity[4] = mutatedFacilitator