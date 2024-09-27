import time

class Node:
    def __init__(self, state=None, parent=None, path_cost=0):
        # Initialize default board if no state is provided
        self.state = state if state is not None else [
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [-1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1]
        ]
        self.parent = parent
        self.action = None
        self.path_cost = path_cost  # g(n)

    def __lt__(self, other):
        # For priority comparison in a min-heap
        return self.path_cost < other.path_cost

goal_state = [
    [-1, -1, 0, 0, 0, -1, -1],
    [-1, -1, 0, 0, 0, -1, -1],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [-1, -1, 0, 0, 0, -1, -1],
    [-1, -1, 0, 0, 0, -1, -1]
]

def goal_test(state):
    # Checks if the current state is the goal state
    return state == goal_state

# Global variable for tracking expanded nodes
total_expanded_nodes = 0

def get_successors(node):
    # Generate all possible moves from the current node
    global total_expanded_nodes
    successors = []

    # Direction vectors for moving marbles
    dx2, dy2 = [0, 0, 2, -2], [-2, 2, 0, 0]
    dx1, dy1 = [0, 0, 1, -1], [-1, 1, 0, 0]

    # Explore every cell on the board
    for i in range(7):
        for j in range(7):
            if node.state[i][j] == 1:  # Marble found
                # Try to jump in all four directions
                for direction in range(4):
                    c2i, c2j = i + dy2[direction], j + dx2[direction]
                    c1i, c1j = i + dy1[direction], j + dx1[direction]

                    # Check if the move is within bounds and valid
                    if 0 <= c2i < 7 and 0 <= c2j < 7 and node.state[c1i][c1j] == 1 and node.state[c2i][c2j] == 0:
                        new_state = [row.copy() for row in node.state]  # Deep copy of the current state
                        new_state[c2i][c2j] = 1  # Move the marble
                        new_state[c1i][c1j] = 0  # Remove jumped marble
                        new_state[i][j] = 0      # Remove original marble

                        # Create new node for the successor
                        successor = Node(new_state, node, node.path_cost + 1)
                        successor.action = [[i, j], [c2i, c2j]]  # Store action (move)
                        successors.append(successor)
                        total_expanded_nodes += 1

    return successors

def display_board(state):
    # Display the current board state in matrix form
    for row in state:
        print(row)

def best_first_search():
    start_node = Node()
    frontier = [start_node]  # List used as stack
    explored_states = []

    while frontier:
        current_node = frontier.pop()  # Remove last element from the frontier (LIFO)

        display_board(current_node.state)
        print(f"Path cost: {current_node.path_cost}\n")

        if current_node.state in explored_states:
            continue

        if goal_test(current_node.state):
            print("Search completed.")
            print(f"Total nodes explored: {len(explored_states)}")
            return current_node

        # Get successors and add unexplored ones to the frontier
        for child in get_successors(current_node):
            if child.state not in explored_states:
                frontier.append(child)

        explored_states.append(current_node.state)  # Mark the current state as explored

    return None  # Return None if no solution is found

def get_all_actions(goal_node):
    # Retrieve the sequence of moves leading to the goal
    actions = []
    while goal_node.parent:
        actions.append(goal_node.action)
        goal_node = goal_node.parent
    actions.reverse()  # Actions are collected from goal to start, so reverse them
    return actions

# Start the search
print("Search initiated...")
start_time = time.time()
goal_node = best_first_search()
end_time = time.time()
elapsed_time = end_time - start_time

if goal_node:
    print("Sequence of Moves: ")
    moves = get_all_actions(goal_node)
    for move in moves:
        print(move)

    print("\nFinal board state:")
    display_board(goal_node.state)

    print(f"Total nodes expanded: {total_expanded_nodes}")
    print(f"Time taken: {elapsed_time} seconds")
else:
    print("No solution could be found.")
