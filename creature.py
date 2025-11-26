import numpy as np 
import os
import math
import time

# def createGenome(genomeLength):
#     genome = []
#     for i in range(genomeLength + 1):
#         gene = os.urandom(4).hex()
#         genome.append(gene)
#     return genome

class Genome:
    def __init__(self, length=10, owner=None):
        self.owner=owner
        self.length=length
        self.genes = []
        for i in range(length):
            g = os.urandom(4).hex()
            self.genes.append(g)
    
    def __str__(self):
        return f"{self.genes}"
    
class Brain:

    def __init__(self, inner=None, genome=[], owner=None):
        self.owner=owner
        self.inner = [0] * inner # number of inner neurons as a list
        self.genome=genome #list of genes

        self.innWeights = [[0,0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0,0]]

        self.outWeights = [[0,0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0,0]]
        
        self.buildBrain()


    def getSourceNode(self, src='', bitcode=''):
        if src == '0':
            return int(bitcode,2)%8
        elif src == '1':
            return int(bitcode,2)%2 + 8

    def getWeight(self, b):
        w = int(b, 2)
        w = w - 0x10000 if w & 0x8000 else w
        w = math.fmod(w,1000)/1000
        return w 

    def getSinkeNode(self, snk='', bitcode=''):
        if snk == '0':
            return int(bitcode,2)%2
        elif snk == '1':
            return int(bitcode,2)%8

    def buildBrain(self):
        for g in self.genome:

            source, weight, sink = 0, 0, 0    
    
            decoded = ''
            
            for h in g:
                x= int(h,16)
                x= bin(x)[2:].zfill(4)
                decoded += x
                
            source = self.getSourceNode(decoded[0],decoded[1:8])
            weight = self.getWeight(decoded[16:])
            sink = self.getSinkeNode(decoded[8],decoded[9:16])

            if decoded[8] == '0':
                self.innWeights[sink][source] = weight
            elif decoded[8] == '1':
                self.outWeights[sink][source] = weight
        
    def think(self, sensor=[0,0,0,0,0,0,0,0]):
        inputLayer = sensor + self.inner

        #calculate inner layer
        inx = np.dot(self.innWeights, inputLayer)

        #replace inner neuron values
        self.inner[0] = inx[0]
        self.inner[1] = inx[1]
        inputLayer = sensor + self.inner

        #calculate output layer
        onx = np.dot(self.outWeights, inputLayer)

        #return the largest output node
        activated = np.argmax(onx)
        # print(onx)
        return activated
    
class Creature:

    id_generator = 1

    def __init__(self, genome=None, position=None, direction=None, parent1=None, parent2=None):

        #Creature takes on latest unique id, then bumps value by 1 for next creature to be created.
        self.id = Creature.id_generator
        self.position = position
        self.direction = direction
        Creature.id_generator +=1

        # Generates random genome for creature if not assigned
        if genome == None:
            self.genome = Genome(length=100, owner=self.id).genes
        else: self.genome = genome

        # Create a brain for creature
        self.brain = Brain(inner=2, genome=self.genome, owner=self.id)
    
    def updateInputs(self, world=None):
        x = self.position[0]+1
        y = self.position[1]+1
        NW = world[y + 1][x - 1]
        NN = world[y + 1][x]
        NE = world[y + 1][x + 1]
        WW = world[y][x - 1]
        EE = world[y][x + 1]
        SW = world[y - 1][x - 1]
        SS = world[y - 1][x]
        SE = world[y - 1][x + 1]
        s = [NW, NN, NE, WW, EE, SW, SS, SE]
        self.inputs = s

    # Set move intentions

    def moveEast(self):
        # print(f"Creature {self.id} original coord is {self.position}")
        newX = self.position[0] + 1
        newCoord = (newX, self.position[1])
        return newCoord
        

    def moveWest(self):
        # print(f"Creature {self.id} original coord is {self.position}")
        newX = self.position[0] - 1
        newCoord = (newX, self.position[1])
        return newCoord 
    

    def moveSouth(self):
        # print(f"Creature {self.id} original coord is {self.position}")
        newY = self.position[1] - 1
        newCoord = (self.position[0], newY)
        return newCoord 
        

    def moveNorth(self):
        # print(f"Creature {self.id} original coord is {self.position}")
        newY = self.position[1] + 1
        newCoord = (self.position[0], newY)
        return newCoord
        

    def moveNE(self):
        # print(f"Creature {self.id} original coord is {self.position}")
        newX = self.position[0] + 1
        newY = self.position[1] + 1
        newCoord = (newX, newY)
        return newCoord 
        

    def moveSE(self):
        # print(f"Creature {self.id} original coord is {self.position}")
        newX = self.position[0] + 1
        newY = self.position[1] - 1
        newCoord = (newX, newY)
        return newCoord
        

    def moveSW(self):
        # print(f"Creature {self.id} original coord is {self.position}")
        newX = self.position[0] - 1
        newY = self.position[1] - 1
        newCoord = (newX, newY)
        return newCoord
        

    def moveNW(self):
        #print(f"Creature {self.id} original coord is {self.position}")
        newX = self.position[0] - 1
        newY = self.position[1] + 1
        newCoord = (newX, newY)
        return newCoord
        

    # Creature declares move intentions
    def declareIntent(self):
        s = self.inputs
        decision = self.brain.think(sensor=s)
        
        moveKey = {0: self.moveNW,
                   1: self.moveNorth,
                   2: self.moveNE,
                   3: self.moveWest,
                   4: self.moveEast,
                   5: self.moveSW,
                   6: self.moveSouth,
                   7: self.moveSE}
        
        # Declare intention
        self.tempPosition = moveKey[decision]()

        #return the inteded coordinate for deconflicting
        return self.tempPosition


    def checkOutOfBound(self, xlim=None, ylim=None):
        xlower = self.tempPosition[0] < 0
        xupper = self.tempPosition[0] > xlim-1
        ylower = self.tempPosition[1] < 0
        yupper = self.tempPosition[1] > ylim-1
        return xlower or xupper or ylower or yupper




# Testing

# testCreature = Creature()

# for i in range(1,10):
#     testCreature.step()
#     time.sleep(1)













