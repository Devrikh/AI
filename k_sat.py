import random

class KSatProblem:
    def __init__(self, k, m, n):
        if k > n:
            raise ValueError("k cannot be greater than n")
        self.k = k
        self.m = m
        self.n = n
        self.clauses = self.generate_k_sat()

    def generate_k_sat(self):
        clauses = []
        for _ in range(self.m):
            clause = []
            used_vars = set()
            while len(clause) < self.k:
                var = random.randint(1, self.n)
                if var not in used_vars:
                    used_vars.add(var)
                    sign = random.choice([True, False])
                    clause.append((var, sign))
            clauses.append(clause)
        return clauses

    def is_satisfied(self, assignment):
        for clause in self.clauses:
            if not any((assignment.get(var, False) if sign else not assignment.get(var, True)) for var, sign in clause):
                return False
        return True

    def backtracking(self):
        def backtrack(assignment):
            if len(assignment) == self.n:
                return assignment if self.is_satisfied(assignment) else None

            var = len(assignment) + 1
            for value in [True, False]:
                assignment[var] = value
                result = backtrack(assignment)
                if result is not None:
                    return result
                del assignment[var]
            return None

        return backtrack({})

    def hill_climbing(self, max_steps=1000):
        current_assignment = {i: random.choice([True, False]) for i in range(1, self.n + 1)}
        
        for _ in range(max_steps):
            if self.is_satisfied(current_assignment):
                return current_assignment
            
            neighbors = []
            for var in current_assignment:
                neighbor = current_assignment.copy()
                neighbor[var] = not neighbor[var]
                neighbors.append(neighbor)

            current_assignment = max(neighbors, key=self.evaluate)

        return None

    def evaluate(self, assignment):
        satisfied_count = 0
        for clause in self.clauses:
            satisfied = False
            for var, sign in clause:
                if sign:  # if the sign is True, check the variable itself
                    if assignment.get(var, False):
                        satisfied = True
                        break
                else:  # if the sign is False, check the negation of the variable
                    if not assignment.get(var, True):  # Treat missing variables as False
                        satisfied = True
                        break
            if satisfied:
                satisfied_count += 1
        return satisfied_count

    def beam_search(self, beam_width=3, max_steps=1000):
        current_assignments = [{i: random.choice([True, False]) for i in range(1, self.n + 1)} for _ in range(beam_width)]

        for _ in range(max_steps):
            next_assignments = []
            for assignment in current_assignments:
                if self.is_satisfied(assignment):
                    return assignment
                
                neighbors = []
                for var in assignment:
                    neighbor = assignment.copy()
                    neighbor[var] = not neighbor[var]
                    neighbors.append(neighbor)

                next_assignments.extend(neighbors)

            current_assignments = sorted(next_assignments, key=self.evaluate, reverse=True)[:beam_width]

        return None

    def print_formula(self):
        clauses_strings = []
        for clause in self.clauses:
            formatted_clause = ' ∨ '.join([f"x{var}" if sign else f"¬x{var}" for var, sign in clause])
            clauses_strings.append(f"({formatted_clause})")
        
        print(" ∧ ".join(clauses_strings))

if __name__ == "__main__":
    k = int(input("Enter the value for k (clause length): "))
    m = int(input("Enter the value for m (number of clauses): "))
    n = int(input("Enter the value for n (number of variables): "))

    ksat = KSatProblem(k, m, n)
    print("Generated k-SAT formula:")
    ksat.print_formula()

    print("Solving using Backtracking...")
    solution = ksat.backtracking()
    print("Backtracking Solution:", solution)

    print("Solving using Hill Climbing...")
    solution = ksat.hill_climbing()
    print("Hill Climbing Solution:", solution)

    print("Solving using Beam Search...")
    solution = ksat.beam_search()
    print("Beam Search Solution:", solution)
