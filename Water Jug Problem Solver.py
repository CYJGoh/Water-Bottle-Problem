from abc import ABCMeta, abstractmethod
import queue as Q
import time

#Queue data structure
class Queue:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def add(self, item):
        self.items.insert(0, item)
    def get(self):
        return self.items.pop()
    def size(self):
        return len(self.items)

#Stack data structure
class Stack:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def push(self, item):
        self.items.append(item)
    def pop(self):
         return self.items.pop()
    def peek(self):
         return self.items[len(self.items)-1]
    def size(self):
         return len(self.items)

#Solver class
class Solver(metaclass=ABCMeta):
    @abstractmethod
    def get(self):
        raise notImplementedError()
    @abstractmethod
    def add(self):
        raise NotImplementedError()

#Breadth-first search
class Solver1(Solver):
    def __init__(self):
        self.queue = Queue()
    def get(self):
        return self.queue.get()
    def add(self, state):
        self.queue.add(state)
    def size(self):
        return self.queue.size()

#Depth-first search
class Solver2(Solver):
    def __init__(self):
        self.stack = Stack()
    def get(self):
        return self.stack.pop()
    def add(self,state):
        self.stack.push(state)

#Greedy Best-First search
class Solver3(Solver):
    def __init__(self, goal):
        self.pq = Q.PriorityQueue()
        self.g = goal
    def get(self):
        if not self.pq.empty():
             (val,state)=self.pq.get()
             return state
        else:
             return None
    def add(self, state):
        value=self.heuristic(state)
        self.pq.put((value,state))
    def heuristic(self, state):
        #current state (n)
        b1, b2, b3 = state[0], state[1], state[2]
        
        #goal
        g1, g2, g3 = self.g[0], self.g[1], self.g[2]
        
        heuristic1 = abs(b1-g1) + abs(b2-g2) + abs(b3-g3)
        
        return heuristic1

#Bottle class
class Bottle:
    def __init__(self, capacity, startState, goalState):
        self.capacity = capacity
        self.startState = startState
        self.goalState = goalState
        
        #SOLVERS HERE
        #self.Solver = Solver1() #Breadth-First Search
        #self.Solver = Solver2() #Depth-First Search
        self.Solver = Solver3(goalState) #Greedy Best-First Search

     
    
    def solve(self):
        global found
        found = False
        self.visited = [] #visited node
        self.Solver.add(self.startState) #add the state to the solver
        state_eval = self.Solver.get()  #visit/solve this state
        cost = 0
        count = 0
        
        print("------------------------------------------")
        print(" Maximum of bottles:", self.capacity, "\n Start State:", self.startState, "\n Goal State:", self.goalState)
        print("------------------------------------------")
        

        while not (found):
            # we only continue if we're not at the goal
            if state_eval != self.goalState:
                print("\n Exploring State", state_eval)
                temp = self.chooseAction(state_eval)
                
                
                #add into self.visited if never visited
                if(state_eval not in self.visited):
                    self.visited.append(state_eval)
                
                for i in temp:
                    if not (i in self.visited):
                        self.Solver.add(i)
                        
                        # add to visited
                        self.visited.append(i)
                        yield i
                        if (i == self.goalState):
                            print("\nReach Goal State:", i)
                            print("Total nodes visited:", count)
                            found = True
                            break
                count += 1
                state_eval = self.Solver.get() #get new state to visit
            else:
                print("Found goal state.")
                found = True
                    
        yield "Task Completed"
        
        
    # Operators    
    def chooseAction(self, state_eval):
        b1 = state_eval[0]
        b2 = state_eval[1]
        b3 = state_eval[2]

        b1Max = self.capacity[0]
        b2Max = self.capacity[1]
        b3Max = self.capacity[2]

        states = []
        
        #empty the bottles
        if(b1 > 0 and found == False):
            #print("empty b1")
            state = (0, b2, b3)
            states.append(state)
            
        if(b2 > 0 and found == False):
            #print("empty b2")
            state = (b1, 0, b3)
            states.append(state)
            
        if(b3 > 0 and found == False):
            #print("empty b3")
            state = (b1, b2, 0)
            states.append(state)

        #fill the bottles
        if(b1 < 10 and found == False):
            #print("filled b1")
            state = (b1Max, b2, b3)
            states.append(state)

        if(b2 < 6 and found == False):
            #print("filled b2")
            state = (b1, b2Max, b3)
            states.append(state)

        if(b2 < 5 and found == False):
            #print("filled b3")
            state = (b1, b2, b3Max)
            states.append(state)

        #transfer between bottles with leftover kept in origianl bottle
        if(b1 + b2 > 0 and b1 + b2 >= b2Max and b1 > 0 and found == False):
            #print("transfered to b2 from b1 with leftover")
            state = (b1 - (b2Max - b2), b2Max, b3)
            states.append(state)

        if(b1 + b3 > 0 and b1 + b3 >= b3Max and b1 > 0 and found == False):
            #print("transfered to b3 from b1 with leftover")
            state = (b1 - (b3Max - b3), b2, b3Max)
            states.append(state)   
            
        if(b1 + b2 > 0 and b1 + b2 >= b1Max and b2 > 0 and found == False):
            #print("transfered to b1 from b2 with leftover")
            state = (b1Max, b2 - (b1Max - b1), b3)
            states.append(state)

        if(b2 + b3 > 0 and b2 + b3 >= b3Max and b2 > 0 and found == False):
            #print("transfered to b3 from b2 with leftover")
            state = (b1, b2 - (b3Max - b3), b3Max)
            states.append(state)

        if(b1 + b3 > 0 and b1 + b3 >= b1Max and b3 > 0 and found == False):
            #print("transfered to b1 from b3 with leftover")
            state = (b1Max, b2, b3 - (b1Max - b1 ))
            states.append(state)

        if(b2 + b3 > 0 and b2 + b3 >= b2Max and b3 > 0 and found == False):
            #print("transfered to b2 from b3 with leftover")
            state = (b1, b2Max, b3 - (b2Max - b2))
            states.append(state)

        #transfer between bottles with leftover fall to ground
        if(b1 + b2 > 0 and b1 + b2 <= b2Max and b1 >= 0 and found == False):
            #print("transfered to b2 from b1 without leftover")
            state = (0, b1 + b2, b3)
            states.append(state)

        if(b1 + b3 > 0 and b1 + b3 <= b3Max and b1 > 0 and found == False):
            #print("transfered to b3 from b1 without leftover")
            state = (0, b2, b1 + b3)
            states.append(state)
            
        if(b1 + b2 > 0 and b1 + b2 <= b1Max and b2 > 0 and found == False):
            #print("transfered to b1 from b2 without leftover")
            state = (b1 + b2, 0, b3)
            states.append(state)

        if(b2 + b3 > 0 and b2 + b3 <= b3Max and b2 > 0 and found == False):
            #print("transfered to b3 from b2 without leftover")
            state = (b1, 0, b2 + b3)
            states.append(state)

        if(b1 + b3 > 0 and b1 + b3 <= b1Max and b3 > 0 and found == False):
            #print("transfered to b1 from b3 without leftover")
            state = (b1 + b3, b2, 0)
            states.append(state)

        if(b2 + b3 > 0 and b2 + b3 <= b2Max and b3 > 0 and found == False):
            #print("transfered to b2 from b3 without leftover")
            state = (b1, b2 + b3, 0)
            states.append(state)

        return states

    def main():
        
        #problem (a) where l = 8, start state is (10,0,0), goal state is (8,0,0)
        startTime = time.time()
        bot1 = Bottle((10,6,5), (10,0,0), (8,0,0))
        b1 = bot1.solve()
        for i in b1:
            print(i)
        print("Time taken for this problem: ", time.time() - startTime, "s")
        
        #problem (b) where l = 4, start state is (2,0,0), goal state is (4,0,0)
        startTime = time.time()
        bot2 = Bottle((10,6,5), (2,0,0), (4,0,0))
        b2 = bot2.solve()
        for i in b2:
            print(i)
        print("Time taken for this problem: ", time.time() - startTime, "s")
        
        #problem (c) where l = 7, start state is (3,0,0), goal state is (7,0,0)
        startTime = time.time()
        bot3 = Bottle((10,6,5), (3,0,0), (7,0,0))
        b3 = bot3.solve()
        for i in b3:
            print(i)
        print("Time taken for this problem: ", time.time() - startTime, "s")

        '''
        problem (d) where maximum of bottles is (11,7,4)
        start state is (10,0,0), goal state is (8,0,0)
        '''
        startTime = time.time()
        bot4 = Bottle((11,7,4), (10,0,0), (8,0,0))
        b4 = bot4.solve()
        for i in b4:
            print(i)
        print("Time taken for this problem: ", time.time() - startTime, "s")
    

#run the program            
Bottle.main()
        

