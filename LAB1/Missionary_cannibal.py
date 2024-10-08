from collections import deque

def is_valid(state):
    missionaries, cannibals, boat = state
    if missionaries < 0 or cannibals < 0 or missionaries > 3 or cannibals > 3:
        return False
    if missionaries > 0 and missionaries < cannibals:
        return False
    if 3 - missionaries > 0 and 3 - missionaries < 3 - cannibals:
        return False
    return True

def get_successors(state):
    successors = []
    missionaries, cannibals, boat = state
    moves = [(2, 0), (0, 2), (1, 1), (1, 0), (0, 1)]

    if boat == 1:
        for move in moves:
            new_state = (missionaries - move[0], cannibals - move[1], 0)
            if is_valid(new_state):
                successors.append(new_state)
    else:
        for move in moves:
            new_state = (missionaries + move[0], cannibals + move[1], 1)
            if is_valid(new_state):
                successors.append(new_state)
    return successors

def bfs(start_state, goal_state):
    queue = deque([(start_state, [])])
    visited = set()
    nodes_explored=0

    while queue:
        (state, path) = queue.popleft()
        if state in visited:
            continue
        visited.add(state)
        nodes_explored += 1
        path = path + [state]
        if state == goal_state:
            print('Total nodes explored with BFS:', nodes_explored)
            return path
        for successor in get_successors(state):
            queue.append((successor, path))

    print('Total nodes explored with BFS:', nodes_explored)
    return None

def dfs(start_state, goal_state):
    stack = [(start_state, [])] 
    visited = set()
    nodes_explored=0
    
    while stack:
        (state, path) = stack.pop() 
        if state in visited:
            continue
        visited.add(state)
        nodes_explored += 1
        path = path + [state]
        
        if state == goal_state:
            print('Total nodes explored with DFS:', nodes_explored)
            return path
        
        for successor in get_successors(state):
            stack.append((successor, path))  
            

    print('Total nodes explored with DFS:', nodes_explored)
    return None





def display_solution(solution):
    print("Initial State: \n")
    print_state(solution[0])
    print("Solution Steps:\n")
    for step in solution[1:]:
        print_state(step)
        print("\n")

def print_state(state):
    missionaries, cannibals, boat = state
    left_bank = f"M:{missionaries} C:{cannibals}"
    right_bank = f"M:{3 - missionaries} C:{3 - cannibals}"
    
    if boat == 1:
        print(f"[ {left_bank} | \__Boat__/--------------------- | {right_bank} ]")
    else:
        print(f"[ {left_bank} | ---------------------\__Boat__/ | {right_bank} ]")

start_state = (3, 3, 1)
goal_state = (0, 0, 0)

solution_bfs = bfs(start_state, goal_state)
solution_dfs=  dfs(start_state, goal_state)


if solution_bfs:
    print("Solution found with BFS:")
    display_solution(solution_bfs)
else:
    print("No solution found with BFS.")

if solution_dfs:
    print("Solution found with DFS:")
    display_solution(solution_dfs)
else:
    print("No solution found with DFS.")
