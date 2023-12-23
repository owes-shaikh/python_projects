 # library that is used to select random word from the list of words
import random

# asking the name of the user
# greetings to the user
name = input('Enter your name : ')
print(f"Good luck! {name}")

words = ['rainbow', 'computer', 'science', 'programming',     # the list of the words to choose from
         'python', 'mathematics', 'player', 'condition',
         'reverse', 'water', 'board', 'geeks']

# using random function with choice method to get a
# random word from the word list
word = random.choice(words)
print('Guess the word')

guesses = ''

turn = 12  # here the number of turns can be any number

# counts the number of times the user failed and here initialing the value as zero
# as the user is yet to play
while turn > 0:
    failed = 0


# all characters from the input
# word taking one at a time.
    for char in word:
        if char in guesses:  # comparing the character with the character in guesses
            print(char, end=" ")
        else:
            print("_")
            failed += 1   # for every failure the failed will increment by 1

    if failed == 0:
        print()
        print("You Win")
        # will print the user has guessed the word correct
        # after failing to guess the number
        print("you required ", (12 - turn), " tries to guess")

        print(f"The word is: {word} ")
        break

    print()
    guess = input("Guess a character")  # asking for a character from the user

    guesses += guess  # every input character will be stored into guesses

    # check if the input character is in word,
    # if the guess does not match the word then wrong will be given
    if guess not in word:

        turn -= 1      # when guessed wrong the no.of turns will reduce by 1
        print(f"""Wrong You have {turn} more guesses  """)

        if turn == 0:    # when the there are no turns left then
            print(" YOu LOse")
