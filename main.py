from creature import Creature, Genome, Brain
import time
import numpy as np

def main():
    
    #Set the parameters
    gridXrange = int(input('Enter x limits. \nEnter for default(10) ').strip() or "10")
    gridYrange = int(input('Enter y limits. \nEnter for default(10) ').strip() or "10")
    numberOfCreatures = int(input('How many creatures? \nMaximum 9 \nEnter for default(9) ').strip() or "9")
    numberOfSteps = int(input('How many steps? \nRecommended 20-40 \nEnter for default(30) ').strip() or "30")
    numberOfInnerNeurons = int(input('How many inner neurons? \nEnter for default(2) ').strip() or "2")
    geneLength = int(input('How many genes in genome? \nEnter for default(50) ').strip() or "10")

    #creating the world
    world = [[0]*(gridXrange + 2) for i in range(gridYrange + 2)]
    world[0] = [1 for i in world[0]]
    world[-1] = [1 for i in world[-1]]
    for i in world:
        i[0] = 1
        i[-1] = 1

    #Creating the creatures
    idx = np.random.choice(gridXrange*gridYrange, size=numberOfCreatures, replace=0)
    pop = []
    for i in idx:
        x,y = np.unravel_index(i,(gridXrange,gridYrange))
        pos = (x,y)
        pop.append(Creature(position=pos, geneLength=geneLength, innerNeurons=numberOfInnerNeurons))

    deconflict = []   

    # Run simulation for a number of steps.
    for st in range(numberOfSteps):
        print(f"step {st}")
        for c in pop:

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


        # roll back intention for all creature that clashes.
        # Steps repeat until no clashing intentions.
        while len(deconflict) != len(set(deconflict)):
            
            # reassing intention for clashing creatures
            for c in pop:
                if deconflict.count(c.tempPosition) > 1:
                    c.tempPosition = c.position
            
            #clear deconflict list
            deconflict.clear()       
            
            #rebuild deconflict list
            for c in pop:
                deconflict.append(c.tempPosition)

        # execute intentions for all creatures
        for c in pop:

            # clear old position on map
            world[c.position[1]+1][c.position[0]+1] = 0

            # creature takes on new position
            c.position = c.tempPosition

            # Update world map
            world[c.position[1]+1][c.position[0]+1] = c.id

            # creature's intentions are cleared 
            c.tempPosition = None

        # Visualise the world map for that step
        for l in world:
            print(l)
        print(" ")
        print(" ")
        time.sleep(0.5)   


if __name__ == "__main__":
    main()

