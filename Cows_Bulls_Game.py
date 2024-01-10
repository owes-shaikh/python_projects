# importing the required random library to generate random integer
import random

# returning the list of digits from string containing a number
# List comprehension

def get_digits(num):
    return f"{[int(i) for i in str(num)]}"

# now dropping duplicates if present in the list of digits
# converting list into set
# as set does not contain repeated values

def drop_duplicates(num):             # to use function within a function u also have to
    num_li = get_digits(num)            # inherit the values of the function used
    if len(num_li) == len(set(num_li)):
        return True
    else:
        return False

# now to create a random number btw 1000 and 9999 i.e. a four digit number
# with no repeated values

def generate_number():
    while True:
        num = random.randint(1000,9999)
        if drop_duplicates(num):
            return num

# getting the random number and the guess number
# using zip as it iterates the two lists at the same time
# getting the bulls and cow values
# guessing digit and position correct = bull value
# guessing digit not the correct position  = cow

def numofBullsCows(num,guess):
    bull_cow = [0,0]
    num_list = get_digits(num)
    guess_list = get_digits(guess)

    for i,j in zip(num_list,guess_list):

        if j in num_list:

            if j == i :
                bull_cow[0] += 1

            else:
                bull_cow[1] += 1
    return bull_cow

# Secret Code
num = generate_number()
tries = int(input('Enter number of tries: '))

# Play game until correct guess
# or till no tries left
while tries > 0:
    guess = int(input("Enter your guess: "))

    if not drop_duplicates(guess):
        print("Number should not have repeated digits. Try again.")
        continue
    if guess < 1000 or guess > 9999:
        print("Enter 4 digit number only. Try again.")
        continue

    bull_cow = numofBullsCows(num, guess)
    print(f"{bull_cow[0]} bulls, {bull_cow[1]} cows")
    tries -= 1

    if bull_cow[0] == 4:
        print("You guessed right!")
        break
else:
    print(f"You ran out of tries. Number was {num}")
