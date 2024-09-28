import time
import heapq

class Node:
    def __init__(self, state=None, parent=None, action=None, g=0, h=0):
        self.state = state if state else [[-1, -1, 1, 1, 1, -1, -1], 
                                          [-1, -1, 1, 1, 1, -1, -1], 
                                          [1, 1, 1, 1, 1, 1, 1],
                                          [1, 1, 1, 0, 1, 1, 1], 
                                          [1, 1, 1, 1, 1, 1, 1], 
                                          [-1, -1, 1, 1, 1, -1, -1],
                                          [-1, -1, 1, 1, 1, -1, -1]]
        self.parent = parent
        self.action = action
        self.g = g  
        self.h = h  
        self.f = g + h  

    def __lt__(self, other):
        return self.f < other.f  

goal_state = [[-1, -1, 0, 0, 0, -1, -1], 
              [-1, -1, 0, 0, 0, -1, -1], 
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0], 
              [0, 0, 0, 0, 0, 0, 0], 
              [-1, -1, 0, 0, 0, -1, -1],
              [-1, -1, 0, 0, 0, -1, -1]]

def is_goal(state):
    return state == goal_state

def heuristic_one(state):
    return sum(row.count(1) for row in state)  

def heuristic_two(state):
    return sum(1 for i in range(7) for j in range(7) if state[i][j] == 1 and goal_state[i][j] == 0)

def find_successors(node):
    successors = []
    direction_moves = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    middle_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for x in range(7):
        for y in range(7):
            if node.state[x][y] == 1:
                for d in range(4):
                    new_x, new_y = x + direction_moves[d][0], y + direction_moves[d][1]
                    mid_x, mid_y = x + middle_moves[d][0], y + middle_moves[d][1]

                    if 0 <= new_x < 7 and 0 <= new_y < 7 and node.state[mid_x][mid_y] == 1 and node.state[new_x][new_y] == 0:
                        new_state = [row[:] for row in node.state]
                        new_state[x][y] = 0
                        new_state[mid_x][mid_y] = 0
                        new_state[new_x][new_y] = 1
                        child_node = Node(new_state, node, action=[(x, y), (new_x, new_y)],
                                          g=node.g + 1, h=heuristic_one(new_state))
                        successors.append(child_node)
    return successors

def a_star_search(heuristic):
    initial_node = Node()
    frontier = []
    explored = set()

    initial_node.h = heuristic(initial_node.state)
    heapq.heappush(frontier, initial_node)

    while frontier:
        current_node = heapq.heappop(frontier)

        if is_goal(current_node.state):
            print("Search completed")
            return current_node

        explored.add(str(current_node.state))

        for child in find_successors(current_node):
            if str(child.state) not in explored:
                child.h = heuristic(child.state)
                heapq.heappush(frontier, child)

    return None

def extract_actions(node):
    actions = []
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    return actions[::-1]

print("A* search started with heuristic one")
start_time = time.time()
result_node = a_star_search(heuristic_one)
end_time = time.time()
elapsed_time = end_time - start_time

if result_node:
    
    print("Moves:")
    moves = extract_actions(result_node)
    for move in moves:
        print(move)
    print("Total cost:", result_node.f)
    print("Elapsed time:", elapsed_time)
else:
    print("No solution found.")

print("\nA* search started with heuristic two")
start_time = time.time()
result_node = a_star_search(heuristic_two)
end_time = time.time()
elapsed_time = end_time - start_time

if result_node:
    
    print("Moves:")
    moves = extract_actions(result_node)
    for move in moves:
        print(move)
    
    print("Total cost:", result_node.f)
    print("Elapsed time:", elapsed_time)
    
else:
    print("No solution found.")
