import time
from string import ascii_lowercase
import random
from itertools import combinations
import random
from string import ascii_lowercase

def create_problem(m, k, n):
    """Creates a uniform random k-SAT problem with m clauses and n variables."""
    variables = list(ascii_lowercase[:n])
    problem = []

    while len(problem) < m:
        clause = []
        for _ in range(k):
            var = random.choice(variables)
            clause.append(var if random.random() < 0.5 else var.upper())

        if clause not in problem:
            problem.append(clause)

    return variables[:n], problem

def generate_assignment(n):
    return {chr(i + 97): random.choice([True, False]) for i in range(n)}

def heuristic1(problem, assignment):
    return sum(any((assignment[var.lower()] if var.islower() else not assignment[var.lower()]) for var in clause) for clause in problem)

def heuristic2(problem, assignment):
    score = 0
    for clause in problem:
        satisfied_literals = sum((assignment[var.lower()] if var.islower() else not assignment[var.lower()]) for var in clause)
        if satisfied_literals > 0:
            score += 1 / satisfied_literals  
    return score

def hill_climbing(problem, assignment, heuristic, max_steps=1000):
    current_score = heuristic(problem, assignment)
    for step in range(max_steps):
        improved = False
        for var in assignment:
            new_assignment = assignment.copy()
            new_assignment[var] = not new_assignment[var]
            new_score = heuristic(problem, new_assignment)
            if new_score > current_score:
                assignment = new_assignment
                current_score = new_score
                improved = True
                break
        if not improved:
            break  
    return assignment, current_score, step + 1

def beam_search(problem, n, heuristic, beam_width, max_steps=1000):
    beam = [generate_assignment(n) for _ in range(beam_width)]
    for step in range(max_steps):
        candidates = []
        for assignment in beam:
            for var in assignment:
                new_assignment = assignment.copy()
                new_assignment[var] = not new_assignment[var]
                score = heuristic(problem, new_assignment)
                candidates.append((new_assignment, score))
        candidates.sort(key=lambda x: x[1], reverse=True)  
        beam = [candidate[0] for candidate in candidates[:beam_width]] 
        if candidates[0][1] == len(problem):
            return beam[0], candidates[0][1], step + 1 
    return beam[0], heuristic(problem, beam[0]), max_steps

def variable_neighborhood_descent(problem, assignment, heuristic, max_steps=1000):
    current_score = heuristic(problem, assignment)
    for step in range(max_steps):
        improved = False
        for k in range(1, 4):
            new_assignment = assignment.copy()
            for _ in range(k):
                var = random.choice(list(new_assignment.keys()))
                new_assignment[var] = not new_assignment[var]
            new_score = heuristic(problem, new_assignment)
            if new_score > current_score:
                assignment = new_assignment
                current_score = new_score
                improved = True
                break
        if not improved:
            break 
    return assignment, current_score, step + 1

def run_experiment(m, n, k=3, num_runs=100):
    results = {
        'HC_H1': [], 'HC_H2': [],
        'BS3_H1': [], 'BS3_H2': [],
        'BS4_H1': [], 'BS4_H2': [],
        'VND_H1': [], 'VND_H2': []
    }

    for run in range(num_runs):
        print(f"Run {run + 1}/{num_runs} for m={m}, n={n}...")
        variables, problem = create_problem(m, k, n)
        initial_assignment = generate_assignment(n)

        for heuristic_name, heuristic_func in [('H1', heuristic1), ('H2', heuristic2)]:
            print(f"  Using heuristic {heuristic_name}...")

           
            start_time = time.time()
            hc_result = hill_climbing(problem, initial_assignment.copy(), heuristic_func)
            elapsed_time = time.time() - start_time
            print(f"    Hill Climbing: Score = {hc_result[1]}, Steps = {hc_result[2]}, Time = {elapsed_time:.4f}s")
            results[f'HC_{heuristic_name}'].append((hc_result, elapsed_time))

           
            start_time = time.time()
            bs3_result = beam_search(problem, n, heuristic_func, 3)
            elapsed_time = time.time() - start_time
            print(f"    Beam Search (width=3): Score = {bs3_result[1]}, Steps = {bs3_result[2]}, Time = {elapsed_time:.4f}s")
            results[f'BS3_{heuristic_name}'].append((bs3_result, elapsed_time))

            
            start_time = time.time()
            bs4_result = beam_search(problem, n, heuristic_func, 4)
            elapsed_time = time.time() - start_time
            print(f"    Beam Search (width=4): Score = {bs4_result[1]}, Steps = {bs4_result[2]}, Time = {elapsed_time:.4f}s")
            results[f'BS4_{heuristic_name}'].append((bs4_result, elapsed_time))

           
            start_time = time.time()
            vnd_result = variable_neighborhood_descent(problem, initial_assignment.copy(), heuristic_func)
            elapsed_time = time.time() - start_time
            print(f"    Variable Neighborhood Descent: Score = {vnd_result[1]}, Steps = {vnd_result[2]}, Time = {elapsed_time:.4f}s")
            results[f'VND_{heuristic_name}'].append((vnd_result, elapsed_time))

    return results

test_cases = [ (20, 30),(5, 5),(10, 15),(3, 3)]
all_results = {
        'HC_H1': [], 'HC_H2': [],
        'BS3_H1': [], 'BS3_H2': [],
        'BS4_H1': [], 'BS4_H2': [],
        'VND_H1': [], 'VND_H2': []
    }

for m, n in test_cases:
        print(f"\nStarting experiment for m={m}, n={n}...")
        experiment_results = run_experiment(m, n)

        for key in all_results:
            all_results[key].extend(experiment_results[key])

        print(f"\nResults for m={m}, n={n}:")
        print(f"{'Method':<20} | {'Penetrance':<10} | {'Avg Time (s)':<10}")
        print("-" * 50)
        for method, data in experiment_results.items():
            penetrance = sum(1 for ((_, score, _), _) in data if score == m) / len(data)
            avg_time = sum(elapsed_time for (_, elapsed_time) in data) / len(data)
            print(f"{method:<20} | {penetrance:.2%} | {avg_time:.4f}")


