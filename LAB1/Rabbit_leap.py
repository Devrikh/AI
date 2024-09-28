from collections import deque

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

def get_successors(node):
    successors = []
    empty_index = node.state.index('.')  # Find the index of the empty stone
    
    # Possible moves for the rabbits
    possible_moves = [-1, -2, 1, 2]  
    
    for move in possible_moves:
        im = empty_index + move
        
        # Check if the new position is within bounds
        if 0 <= im < 7:
            new_state = list(node.state)
            # print(im)
            # print(new_state)
            # Move Forward (Move by 1 step)
            if move == 1 and new_state[im] == 'W':  # East-bound rabbit moving right
              temp = new_state[im]
              new_state[im] = new_state[empty_index]
              new_state[empty_index] = temp
              successor = Node(new_state, node) 
              successors.append(successor) 

            elif move == -1 and new_state[im] == 'E':  # West-bound rabbit moving left
              temp = new_state[im]
              new_state[im] = new_state[empty_index]
              new_state[empty_index] = temp
              successor = Node(new_state, node)
              successors.append(successor) 
            
            # Leap Over (Move by 2 steps)
            elif move == 2 and new_state[im] == 'W':
            #   between_index = empty_index + 1  # The index between the current and target positions
            #     # East-bound rabbit jumps over a West-bound rabbit
              temp = new_state[im]
              new_state[im] = new_state[empty_index]
              new_state[empty_index] = temp
              successor = Node(new_state, node) 
              successors.append(successor) 

            elif move == -2 and new_state[im] == 'E':
              temp = new_state[im]  
              new_state[im] = new_state[empty_index]
              new_state[empty_index] = temp
              successor = Node(new_state, node) 
              successors.append(successor) 
    return successors


def bfs(start_state, goal_state):
    start_node = Node(start_state)
    goal_node = Node(goal_state)
    queue = deque([start_node])
    visited = set()
    nodes_explored = 0
    
    while queue:
        node = queue.popleft()
        if tuple(node.state) in visited:  
            continue 
        visited.add(tuple(node.state))      
        nodes_explored = nodes_explored + 1     
        if node.state == list(goal_node.state):   
            path = []                               
            while node:                              
                path.append(node.state)
                node = node.parent
            print('Total nodes explored with BFS:', nodes_explored)
            return path[::-1]
        
        for successor in get_successors(node):
                queue.append(successor)
    
    print('Total nodes explored with BFS:', nodes_explored)
    return None

def dfs(start_state, goal_state):
    start_node = Node(start_state)
    goal_node = Node(goal_state)
    stack = [start_node]
    visited = set()
    nodes_explored = 0
    
    while stack:
        node = stack.pop()
        if tuple(node.state) in visited:
            continue
        visited.add(tuple(node.state))
        nodes_explored += 1
        
        if node.state == list(goal_node.state):   
            path = []                            
            
            while node:                              
                path.append(node.state)
                node = node.parent
            print('Total nodes explored with DFS:', nodes_explored)
            return path[::-1]
        
        for successor in get_successors(node):
            stack.append(successor)
    
    print('Total nodes explored with DFS:', nodes_explored)
    return None


def print_state(state):
    print(' '.join(state))
    print()

start_state = ('E', 'E', 'E', '.', 'W', 'W', 'W')
goal_state = ('W', 'W', 'W', '.', 'E', 'E', 'E')

solution_bfs = bfs(start_state, goal_state)
solution_dfs=  dfs(start_state, goal_state)

if solution_bfs:
    print("Solution found with BFS: \n")
    for state in solution_bfs:
        print_state(state)
else:
    print("No solution found with BFS.")

if solution_dfs:
    print("Solution found with DFS: \n")
    for state in solution_dfs:
        print_state(state)
else:
    print("No solution found with DFS.")
