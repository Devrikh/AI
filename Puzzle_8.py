import heapq
import random

class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g  # distance to root
        self.h = h  # estimated distance to goal
        self.f = g + h  # evaluation function

    def __lt__(self, other):
        return self.f < other.f

def heuristic(node, goal_state):
    h = sum(abs((val // 3) - (goal_state.index(val) // 3)) + abs((val % 3) - (goal_state.index(val) % 3))
             for val in node.state if val != 0)
    return h

# def get_successors(node):
#     successors = []
#     index = node.state.index(0)
#     row, col = divmod(index, 3)
    
#     # Possible moves: up, down, left, right
#     moves = [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]
    
#     for r, c in moves:
#         if 0 <= r < 3 and 0 <= c < 3:
#             new_index = r * 3 + c
#             new_state = list(node.state)
#             new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
#             h = heuristic(Node(new_state), goal_state)
#             successor = Node(new_state, node, node.g + 1, h)
#             successors.append(successor)
#     return successors

def get_successors(node):
    successors = []
    value = 0
    index = node.state.index(0)
    quotient = index//3
    remainder = index%3
    # Row constrained moves
    if quotient == 0:
        moves = [3]
    if quotient == 1:
        moves = [-3, 3]
    if quotient == 2:
        moves = [-3]
    # Column constrained moves
    if remainder == 0:
        moves += [1]
    if remainder == 1:
        moves += [-1, 1]
    if remainder == 2:
        moves += [-1]

    # moves = [-1, 1, 3, -3]
    for move in moves:
        im = index+move
        if im >= 0 and im < 9:
            new_state = list(node.state)
            new_state[index], new_state[im] = new_state[im], new_state[index]
            h = heuristic(Node(new_state), goal_state)
            successor = Node(new_state, node, node.g + 1, h)
            successors.append(successor)           
    return successors



def search_agent(start_state, goal_state):
    start_node = Node(start_state, None, 0, heuristic(Node(start_state), goal_state))
    frontier = []
    heapq.heappush(frontier, start_node)
    visited = set()
    
    while frontier:
        node = heapq.heappop(frontier)
        
        if tuple(node.state) in visited:
            continue
        
        visited.add(tuple(node.state))
        
        if node.state == goal_state:
            return construct_path(node)
        
        for successor in get_successors(node):
            if tuple(successor.state) not in visited:
                heapq.heappush(frontier, successor)
    
    return None

def construct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path  # Return reversed path

def generate_puzzle_at_depth(start_state, depth):
    current_state = start_state[:]
    for _ in range(depth):
        successors = get_successors(Node(current_state))
        current_state = random.choice(successors).state
    return current_state

# Example usage
start_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
depth_limit = 20
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]  # Define a goal state

# Generate a random goal state at a specific depth
for d in range(depth_limit + 1):
    goal_state = generate_puzzle_at_depth(start_state, d)

print("Start State:")
print(start_state)
print("\nGenerated Goal State:")
print(goal_state)
print("\n")

solution = search_agent(start_state, goal_state)

if solution:
    print("Solution found:")
    for step in solution:
        print(step)
else:
    print("No solution found.")
