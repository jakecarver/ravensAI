# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
from PIL import ImageChops
import numpy as np


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.
    def Solve(self,problem):
        #img = Image.open(problem.visualFilename)
        #img.show()
        #print(problem.figures['A'])
        print(problem.problemType)

        alphabet = ['A','B','C','D','E','F','G','H','I']

        qFigures = []
        aFigures = []

        count = 1
        while True:
            try:
                aFigures.append(Image.open(problem.figures[str(count)].visualFilename))
                count += 1
            except:
                break
        

        count = 0

        if problem.problemType == '2x2':
            for i in range (0,2):
                qFigures.append([])
                for j in range(0,2):
                    if count == 3:
                        break
                    qFigures[i].append(Node(Image.open(problem.figures[alphabet[count]].visualFilename)))
                    count += 1

            

            
            qFigures[0][0].right = qFigures[0][1]
            qFigures[0][1].left = qFigures[0][0]
            qFigures[0][0].down = qFigures[1][0]
            qFigures[1][0].up = qFigures[0][0]

            
        
        if problem.problemType == '3x3':
            for i in range (3):
                qFigures.append([])
                for j in range(3):
                    if count == 8:
                        break
                    qFigures[i].append(Node(Image.open(problem.figures[alphabet[count]].visualFilename)))
                    count += 1
        qFigures = State(qFigures)
        ans = SolveTwo(aFigures,qFigures)
        return ans
        
            #min = 

        print('done')

        #figureA = problem.figures["A"]
        #pathToFigureA = figureA.visualFilename
        #Read into OpenCV
        #img = Image.open(pathToFigureA)
        #img.show()
        return np.random.randint(1,6)

def SolveTwo(aFigures, qFigures):
    ans = normalDPRSolve(aFigures, qFigures)
    return ans

def SolveThree(problem):
    return
def normalDPRSolve(aFigures, qFigures):
    goal =  qFigures.links[-1].DPRdif
    bestMin = None
    ans = None
    count = 1
    for h in aFigures:
        

        hbbox = h.getbbox()
        if not hbbox: return 0
        hDPR = sum(h.crop(hbbox)
               .point(lambda x: 255 if x else 0)
               .convert("L")
               .point(bool)
               .getdata())  

        
        jbbox = qFigures.nodeList[-1].img.getbbox()
        if not jbbox: return 0
        jDPR = sum(qFigures.nodeList[-1].img.crop(jbbox)
               .point(lambda x: 255 if x else 0)
               .convert("L")
               .point(bool)
               .getdata())  
        min = abs(goal - abs(hDPR-jDPR))
        if bestMin == None:
            bestMin = min
        elif min <= bestMin:
            bestMin = min
            ans = count
        count += 1
    print ('ANS:')
    print (ans)
    if ans is None:
        return np.random.randint(1,6)
    return ans

'''
def rotateSolve(aFigures, qFigures):
    denom = 0
    numer = 0
    for i in qFigures.links:
        denom += 1
        numer += i.DPR
    average = numer/denom
    bestMin = None
    ans = None
    count = 1
    for h in aFigures:
        min = None
        for i in range (0,180):
            h.rotate(1)
            for j in qFigures.nodeList:
                if min == None:
                    min = abs(average - ImageChops.difference(h, j.img)  )
                elif abs(average - ImageChops.difference(h, j.img)) < min:
                    min = abs(average - ImageChops.difference(h, j.img))
        if bestMin == None:
            bestMin = min
        elif bestMin > min:
            bestMin = min
            ans = count
        count += 1
    print ('ANS:')
    print (ans)
    return
'''
class State():
    def __init__(self, nodeList):
        self.nodeMatrix = nodeList
        self.nodeList = []
        for i in range(0, len(self.nodeMatrix)):
            for j in range(0, len(self.nodeMatrix[i])):
                self.nodeList.append(self.nodeMatrix[i][j])
        self.links = []
        row = 0
        thisNode = nodeList[row][0]
        
        while True:
            #if thisNode.down:
            #    self.links.append(Link(thisNode, thisNode.down))
            if thisNode.right:
                self.links.append(Link(thisNode, thisNode.right))
                thisNode = thisNode.right
            elif len(nodeList)>row+1:
                row+=1
                thisNode = nodeList[row][0]
            else:
                break


#Class for a node
class Node():
    def __init__(self, img, up = None, down = None, left = None, right = None):
        
        self.img = img
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        bbox = img.getbbox()
        if not bbox: return 0
        self.DPR =  sum(img.crop(bbox)
               .point(lambda x: 255 if x else 0)
               .convert("L")
               .point(bool)
               .getdata())  


class Link():
    def __init__(self, parentA, parentB):
        self.parentA = parentA
        self.parentB = parentB
        self.DPRdif = abs(parentA.DPR - parentB.DPR)
        


#EASY SOLUTION FOR FIRST
# 1 find dpr for A-B
# 2 find dpr for A - C
# 3 for each answer find dpr B-D and C-D and compare
# Least DPR wins


#ALSO 
#Make heuristics like mirror or rotate
#Run the heuristics and compare the DPR difference



#Class for connections between two nodes 