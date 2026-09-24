# This program simulates a simple lottery draw. It randomly generates six unique numbers from 1 to 49, asks the user to enter six numbers, and then compares the user's numbers with the randomly generated numbers to find the matches.

import random

def generate_random_numbers():
    numbers = random.sample(range(1, 50), k=6)
    print(f"Generated numbers: {numbers}")
    return numbers

def compare_numbers(given_numbers, random_numbers):
    guess_table = []
    for num1 in given_numbers:
        for num2 in random_numbers:
            if num1 == num2:
                guess_table.append(num1)
    print(f"Guessed numbers: {guess_table}")

def main():
    random_numbers = generate_random_numbers()
    while True:
        try:
            given_numbers = list(map(int, input("Give me 6 numbers: ").split()))
    
            if len(given_numbers) != 6:
                print("Please enter exactly 6 numbers.")
                continue
    
            break
    
        except ValueError:
            print("Only integers are allowed.")
    compare_numbers(given_numbers, random_numbers)

if __name__ == "__main__":
    main()
