import csv
import random

def read_csv_file(csv_file_path):
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        return [row[0] for row in csvreader]
    
def read_text_file(text_file_path):
    with open(text_file_path, 'r') as textfile:
        text_reader = textfile.read().split('\n')
    return text_reader

def get_initial_probabilities(words):
    return {word: 1.0 / len(words) for word in words} # Start with uniform probs

def update_probabilities(words, probabilities, guess, correct, misplaced, absent):
    new_probabilities = {}
    for word in words:
        if is_possible(word, guess, correct, misplaced, absent):
            new_probabilities[word] = probabilities[word] * calculate_match_probability(word, guess, correct, misplaced, absent)
    
    total_prob = sum(new_probabilities.values())
    return {word: prob / total_prob for word, prob in new_probabilities.items()}  # Normalize probabilities


definitively_absent_letters = set() # Global set for absent letters

def update_definitively_absent_letters(guess, correct, misplaced, absent):
    # Update definitively absent letters based on new information
    for idx, char in enumerate(guess):
        if idx in absent:
            # Update logic to handle repeated characters
            if guess.count(char) == len([i for i in absent if guess[i] == char]):
                definitively_absent_letters.add(char)

def is_possible(word, guess, correct, misplaced, absent):
    update_definitively_absent_letters(guess, correct, misplaced, absent)
    
    if any(char in word for char in definitively_absent_letters):
        return False

    from collections import defaultdict

    # Initialize valid positions for each letter in the guess
    valid_positions = defaultdict(set)
    invalid_positions = defaultdict(set)
    required_counts = defaultdict(int)  # Tracks minimum required counts of letters

    # Process correct positions
    for idx, char in enumerate(guess):
        if idx in correct:
            if word[idx] != char:
                return False
            valid_positions[char].add(idx)
            required_counts[char] += 1

    # Process misplaced positions
    for idx, char in enumerate(guess):
        if idx in misplaced:
            if char not in word or word[idx] == char:
                return False
            if idx not in valid_positions[char]:  # Cannot be in the current index
                invalid_positions[char].add(idx)
            required_counts[char] += 1

    # Process absent positions
    # This needs to be fixed, it's overfiltering
    for idx, char in enumerate(guess):
        if idx in absent:
            if char in word and guess.count(char) == word.count(char):
                return False  

    # Ensuring the count of each letter meets the minimum required based on the feedback
    for char, count in required_counts.items():
        if word.count(char) < count:
            return False

    # Validating against valid and invalid positions
    for idx, char in enumerate(word):
        if char in invalid_positions and idx in invalid_positions[char]:
            return False
        #if char in valid_positions and idx not in valid_positions[char] and valid_positions[char]:
            #return False

    return True

# Fix this
def calculate_match_probability(word, guess, correct, misplaced, absent):
    probability = 1.0
    for idx, char in enumerate(guess):
        if idx in correct:
            probability *= 1.2
        elif idx in misplaced:
            probability *= 0.8
        elif idx in absent and char not in word: # maybe change absent to the definitively absent list
            probability *= 1.1
    return probability

def parse_feedback(guess):
    correct_positions = {}
    misplaced_letters = {}
    absent_letters = set()
    print("Provide feedback for each position:")
    for i, char in enumerate(guess):
        feedback = input(f"Feedback for {char} at position {i} (enter 'correct', 'misplaced', or 'absent'): ")
        if feedback == 'correct':
            correct_positions[i] = char
        elif feedback == 'misplaced':
            misplaced_letters[i] = char
        elif feedback == 'absent':
            absent_letters.add(i)
    return correct_positions, misplaced_letters, absent_letters

def main():
    # Still need to remove the used words from valid guesses
    
    all_words = read_csv_file('valid_answers.csv')
    probabilities = get_initial_probabilities(all_words)
    first_guess = True  # Flag to indicate if it's the first guess

    while True:
        if not probabilities:  # Check if the probabilities dictionary is empty
            print("No valid words left. Please check the feedback provided.")
            break

        if first_guess:
            guess = random.choice(list(probabilities.keys()))  # Start with a random word
            first_guess = False  # Reset flag after first guess
        else:
            guess = max(probabilities, key=probabilities.get)  # Choose the word with the highest probability

        print("Try this word:", guess)
        user_input = input("Was the word correct? (yes/no): ")
        if user_input.lower() == 'yes':
            print("Awesome! Wordle solved!")
            break
        correct, misplaced, absent = parse_feedback(guess)
        probabilities = update_probabilities(list(probabilities.keys()), probabilities, guess, correct, misplaced, absent)
        print("Remaining possible words:", len(probabilities))

if __name__ == "__main__":
    main()
