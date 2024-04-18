import csv
import random

def read_csv_file(csv_file_path):
    with open(csv_file_path, 'r') as csvfile: #open csv 
    
        csvreader = csv.reader(csvfile) #create csv obj
        validWords = [] #list to hold the valid words 
    
        for row in csvreader:   # Iterate over each row
            validWords.append(row[0])    #append to the list 

    return validWords
        #print(validWords) #print for testing 

def read_text_file(text_file_path):
    with open(text_file_path, 'r') as textfile: #open csv 
    
        textReader = textfile.read() #create csv obj
        used = [] #list to hold the valid words 
    
        lines = textReader.split('\n')
    
    # Iterate over each line and print it
        for line in lines:
            used.append(line)

    return used
        #print(used) #print for testing 

def getGuessList(usedWords, allWords):
    
    validGuesses = [] #will store all of the valid guesses 

    print("len of all", len(allWords))
    print("len of used", len(usedWords))

    for word in allWords: #go through each word and check if its in the used words 
        if word not in usedWords:
            validGuesses.append(word)
    
    print("len of valid guesses", len(validGuesses))

    return validGuesses

def makeListSmaller(guesses, correctLetter, letterInWord, lettersNotIn, word):
    correctIdx = []
    #print(guesses)
    
    if correctLetter != 'none':
        for letter in correctLetter:
            for idx, char in enumerate(word):
                if char == letter:
                    correctIdx.append(idx)
    
    badIdx = []
    if lettersNotIn != 'none':
        for bad in lettersNotIn:
            for idx, char in enumerate(word):
                if char == bad:
                    badIdx.append(idx)

    print(correctIdx)
    print(badIdx)


    filteredGuess = []

    for guess in guesses:
        validWord = True
        hasCorrectLetter = False
        if correctLetter != 'none': 
            for idx in correctIdx: #go through the correct indexs
                if guess[idx] != word[idx] and not hasCorrectLetter: #if the guess and the word have the same then add to teh list 
                    validWord = False
                    break
                elif guess[idx] != word[idx]:
                    hasCorrectLetter = True
        
        if lettersNotIn != 'none': 
            for bad in lettersNotIn: #go through the letters that are not in the word 
                for idx, char in enumerate(guess): #go through the current guess 
                    if char == bad: #check if the bad letter is there 
                        validWord = False
        
        if letterInWord != 'none':
            for check in letterInWord:
                if check not in guess:
                    validWord = False
                elif guess.index(check) == word.index(check):
                    validWord = False

        if validWord:
            print("WORD IS VALID: ", guess)
            filteredGuess.append(guess)

    #print(filteredGuess)
    return filteredGuess


def main():
    # Call the function to read the CSV file
    allWords = read_csv_file('valid_answers.csv')
    # Print or process the CSV rows as needed
    #print("CSV\n", allWords)

    # Call the function to read the text file
    usedWords = read_text_file('usedWords.txt')
    # Print or process the text lines as needed
    #print("ANSWERS\n", usedWords)

    #validGuess = getGuessList(usedWords, allWords)
    validGuess = allWords
    randIdx = random.randint(0, len(validGuess) - 1)
    #randIdx = random.randint(0, len(allWords) - 1) #for testing purposes use all words 
    

    #print("try this word: flood")
    user_input = 'no'


    while True:
        thisGuess = validGuess[random.randint(0, len(validGuess) - 1)]
        print("try this word: ", thisGuess)
        user_input = input("Did that word work? enter yes or no: ")
        if user_input == 'yes':
            break
        correctLetters = input("LETTERS IN CORRECT POSITION (none if all were wrong): ")
        letterInWord = input("LETTERS IN WORD, WRONG POSITION (none if all were wrong): ")
        lettersNotIn = input("LETTERS NOT IN WORD (none if all were wrong): ")

        validGuess = makeListSmaller(validGuess, correctLetters, letterInWord, lettersNotIn, thisGuess)
        
        print("The new list of words is: ", validGuess)
        #print("The word that we recommend using is: ", validGuess[random.randint(0, len(validGuess) - 1)])

    print("Awesome! Wordle solved!")

    
    #print(validGuess)



if __name__ == "__main__":
    main()



