#Tausif Miah        CS-UY 4613 A

import operator
from itertools import filterfalse

class Node:
    def __init__(self,state,value,action,depth):
        self.state = state;
        self.value = value;
        self.action = action;
        self.depth = depth;
        
#manhattan distance
def mhd(state1, state2):
    mhdist = 0;
    for i, g in ((state1.index(j), state2.index(j)) for j in range(1, 9)):
        mhdist += (abs(i%3 - g%3) + abs(i//3 - g//3)); 
    return mhdist;

#add successors to unexplored set
def expand(currNode, unexplored, goalState):
    blank = currNode.state.index(0)
    # UP:
    if blank > 2:
        swap = blank - 3;
        succ = Node([],0,'U',currNode.depth + 1);
        succ.state.extend(currNode.state[0:swap]);
        succ.state.append(0);
        succ.state.extend(currNode.state[swap+1:blank]);
        succ.state.append(currNode.state[swap]);
        succ.state.extend(currNode.state[blank+1:]);
        succ.value = succ.depth + mhd(succ.state,goalState);
        unexplored.append(succ);
    # DOWN:
    if blank < 6:
        swap = blank + 3;
        succ = Node([],0,'D',currNode.depth + 1);
        succ.state.extend(currNode.state[0:blank]);
        succ.state.append(currNode.state[swap]);
        succ.state.extend(currNode.state[blank+1:swap]);
        succ.state.append(0);
        succ.state.extend(currNode.state[swap+1:]);
        succ.value = succ.depth + mhd(succ.state,goalState);
        unexplored.append(succ);
    # LEFT:
    if blank % 3 > 0:
        swap = blank - 1;
        succ = Node([],0,'L',currNode.depth + 1);
        succ.state.extend(currNode.state[0:swap]);
        succ.state.append(0);
        succ.state.append(currNode.state[swap]);
        succ.state.extend(currNode.state[blank+1:]);
        succ.value = succ.depth + mhd(succ.state,goalState);
        unexplored.append(succ);
    # RIGHT
    if blank % 3 < 2:
        swap = blank + 1;
        succ = Node([],0,'R',currNode.depth + 1);
        succ.state.extend(currNode.state[0:blank]);
        succ.state.append(currNode.state[swap]);
        succ.state.append(0);
        succ.state.extend(currNode.state[swap+1:]);
        succ.value = succ.depth + mhd(succ.state,goalState);
        unexplored.append(succ);
    return unexplored;

#Solution Path: going backwards from final node to find actions that lead to solution
def solnPath(finalNode,solution):
    actionArray = [];
    currNode = finalNode;
    for i in range(finalNode.depth):
        actionArray += currNode.action;
        blank = currNode.state.index(0);
        # UP:
        if currNode.action == 'D':
            swap = blank - 3;
            state = [];
            state.extend(currNode.state[0:swap]);
            state.append(0);
            state.extend(currNode.state[swap+1:blank]);
            state.append(currNode.state[swap]);
            state.extend(currNode.state[blank+1:]);
        # DOWN:
        elif currNode.action == 'U':
            swap = blank + 3;
            state = [];
            state.extend(currNode.state[0:blank]);
            state.append(currNode.state[swap]);
            state.extend(currNode.state[blank+1:swap]);
            state.append(0);
            state.extend(currNode.state[swap+1:]);
        # LEFT:
        elif currNode.action == 'R':
            swap = blank - 1;
            state = [];
            state.extend(currNode.state[0:swap]);
            state.append(0);
            state.append(currNode.state[swap]);
            state.extend(currNode.state[blank+1:]);
        # RIGHT
        elif currNode.action == 'L':
            swap = blank + 1;
            state = [];
            state.extend(currNode.state[0:blank]);
            state.append(currNode.state[swap]);
            state.append(0);
            state.extend(currNode.state[swap+1:]);
        for i in range(len(solution)):
            if state == solution[i].state:
                currNode = solution[i];
    return actionArray[::-1];

#file i/o
filename = input("Enter the filename:");
inputFile = open(filename,"r").read().splitlines();
initial = [inputFile[0].split(' ')[0],inputFile[0].split(' ')[1],inputFile[0].split(' ')[2],inputFile[1].split(' ')[0],inputFile[1].split(' ')[1],inputFile[1].split(' ')[2],inputFile[2].split(' ')[0],inputFile[2].split(' ')[1],inputFile[2].split(' ')[2]];
goal = [inputFile[4].split(' ')[0],inputFile[4].split(' ')[1],inputFile[4].split(' ')[2],inputFile[5].split(' ')[0],inputFile[5].split(' ')[1],inputFile[5].split(' ')[2],inputFile[6].split(' ')[0],inputFile[6].split(' ')[1],inputFile[6].split(' ')[2]];
initial = [int(i) for i in initial];
goal = [int(i) for i in goal];
solution = [];
unexplored = [];
currNode = Node(initial,mhd(initial,goal),'',0);

#main loop
while (mhd(currNode.state,goal) != 0):
    unexplored = expand(currNode,unexplored,goal);
    unexplored.sort(reverse = True, key = operator.attrgetter('depth'));
    for i in range(len(unexplored)):
        if unexplored[i].value <= mhd(initial,goal):
            currNode = unexplored[i];
            solution.append(unexplored[i]);
            unexplored.pop(i);
            break;
        elif i >= len(unexplored)-1:
            print('No solution exists');
            #file i/o
            with open('Output.txt','wt') as ASCII_file:
                ASCII_file.write(open(filename,"r").read()+ '\n' + '\n' + 'No solution exists')
            raise SystemExit;
    
#file i/o
if mhd(currNode.state,goal) == 0:
    soln = solnPath(currNode,solution);
    solnString = " ".join(soln);
    with open('Output.txt','wt') as ASCII_file:
        ASCII_file.write(open(filename,"r").read()+ '\n' + '\n' + str(currNode.depth) + '\n' + str(len(solution)+len(unexplored)+1) + '\n' + solnString);

