import nltk
import string
from heapq import heappop, heappush

nltk.download('punkt')
nltk.download('punkt_tab')

def tokenize_text(text):
    sentences = nltk.sent_tokenize(text)
    return sentences

def normalize_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def levenshtein_distance(s1, s2):
    len_s1, len_s2 = len(s1), len(s2)
    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

    for i in range(len_s1 + 1):
        for j in range(len_s2 + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[len_s1][len_s2]

def a_star_search(doc1_sentences, doc2_sentences):
    def heuristic(i, j):
        remaining_doc1 = sum(len(sentence) for sentence in doc1_sentences[i:])
        remaining_doc2 = sum(len(sentence) for sentence in doc2_sentences[j:])
        return min(remaining_doc1, remaining_doc2)

    # Initial state: first sentence in both documents, zero cost
    start_state = (0, 0, 0)  # (index in doc1, index in doc2, accumulated cost)
    frontier = [(0, start_state)]  # Priority queue: (estimated total cost, state)
    visited = set()
    alignments = []

    while frontier:
        estimated_cost, (i, j, cost) = heappop(frontier)

        # Goal state: all sentences aligned
        if i == len(doc1_sentences) and j == len(doc2_sentences):
            return alignments

        if (i, j) in visited:
            continue
        visited.add((i, j))

        # Transition: align, skip doc1 sentence, skip doc2 sentence
        if i < len(doc1_sentences) and j < len(doc2_sentences):
            new_cost = cost + levenshtein_distance(doc1_sentences[i], doc2_sentences[j])
            heappush(frontier, (new_cost + heuristic(i + 1, j + 1), (i + 1, j + 1, new_cost)))
            alignments.append((doc1_sentences[i], doc2_sentences[j]))

        if i < len(doc1_sentences):
            heappush(frontier, (cost + heuristic(i + 1, j), (i + 1, j, cost)))
            alignments.append((doc1_sentences[i], ""))  # Skip sentence in doc2

        if j < len(doc2_sentences):
            heappush(frontier, (cost + heuristic(i, j + 1), (i, j + 1, cost)))
            alignments.append(("", doc2_sentences[j]))  # Skip sentence in doc1

    return alignments

def detect_plagiarism(aligned_sentences, threshold=5):
    plagiarized_pairs = []
    for (s1, s2) in aligned_sentences:
        if s1 and s2 and levenshtein_distance(s1, s2) < threshold:
            plagiarized_pairs.append((s1, s2))
    return plagiarized_pairs

def run_test_cases():
    test_cases = {
        "Test Case 1: Identical Documents": (
            "This is a test. Testing is important.", 
            "This is a test. Testing is important."
        ),
        "Test Case 2: Slightly Modified Document": (
            "This is a test. Testing is important.",
            "This is a trial. Testing is crucial."
        ),
        "Test Case 3: Completely Different Documents": (
            "This is a test. Testing is important.",
            "The weather is nice. I love sunny days."
        ),
        "Test Case 4: Partial Overlap": (
            "This is a test. Testing is important.",
            "Testing is important. This is another example."
        ),
    }

    for test_name, (doc1, doc2) in test_cases.items():
        print(f"\n{test_name}")
        print("-" * len(test_name))
        sentences1 = tokenize_text(doc1)
        sentences2 = tokenize_text(doc2)
        normalized1 = [normalize_text(sentence) for sentence in sentences1]
        normalized2 = [normalize_text(sentence) for sentence in sentences2]
        aligned_sentences = a_star_search(normalized1, normalized2)
        plagiarized_pairs = detect_plagiarism(aligned_sentences, threshold=5)
        print("\nAligned Sentences:")
        for s1, s2 in aligned_sentences:
            print(f"Doc1: {s1} | Doc2: {s2}")
        print("\nPotential Plagiarism:")
        for s1, s2 in plagiarized_pairs:
            print(f"Doc1: {s1} | Doc2: {s2}")


run_test_cases()
