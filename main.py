from creature import Creature, Genome, Brain
import time
import numpy as np

# testCreature = Creature()


#creating the world
gridXrange = 10 
gridYrange = 10
world = [[0]*(gridXrange + 2) for i in range(gridYrange + 2)]
world[0] = [1 for i in world[0]]
world[-1] = [1 for i in world[-1]]
for i in world:
    i[0] = 1
    i[-1] = 1

#Creating the creatures
numberOfCreatures = 9
idx = np.random.choice(gridXrange*gridYrange, size=numberOfCreatures, replace=0)
pop = []
for i in idx:
    x,y = np.unravel_index(i,(gridXrange,gridYrange))
    pos = (x,y)
    pop.append(Creature(position=pos))

# print("Inition positions:")
# for c in pop:
#     print(c.position)
# print(" ")

deconflict = []   


for st in range(35):
    print(f"step {st}")
    # print("position at start of loop")
    for c in pop:
        # print(c.position)
        # mark out the position of creatures in the world map
        world[c.position[1]+1][c.position[0]+1] = c.id
        # Populate creature's sensors
        c.updateInputs(world=world)
        # Declare creature's intentions
        c.declareIntent()
        # Check if intentions are out of bounds, roll back if yes.
        if c.checkOutOfBound(xlim=gridXrange, ylim=gridYrange):
            c.tempPosition = c.position
        # populate creature intentions in a look up table
        deconflict.append(c.tempPosition)
    # print(deconflict)

    # roll back intention for all creature that clashes.
    while len(deconflict) != len(set(deconflict)):
        
        # print(len(deconflict))
        # print(len(set(deconflict)))    

        # reassing intention for clashing creatures
        for c in pop:
            if deconflict.count(c.tempPosition) > 1:
                c.tempPosition = c.position
        
        #clear deconflict list
        deconflict.clear()       
        
        #rebuild deconflict list
        for c in pop:
            deconflict.append(c.tempPosition)
    # print(" ")
    # print("final position")
    # execute move for all creatures
    for c in pop:
        # clear old position on map
        world[c.position[1]+1][c.position[0]+1] = 0
        # creature takes on new position
        c.position = c.tempPosition
        # Update world map
        world[c.position[1]+1][c.position[0]+1] = c.id
        # intention is cleared 
        c.tempPosition = None
        # print(c.position)



    # Visualise the world map
    for l in world:
        print(l)
    # print("end of step")
    print(" ")
    print(" ")
    time.sleep(0.5)   





