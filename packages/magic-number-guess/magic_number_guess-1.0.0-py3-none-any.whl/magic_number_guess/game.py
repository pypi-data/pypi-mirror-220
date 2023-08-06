import random
import sys

def number_guessing_game(min_num=1, max_num=100):
    """
    A magical number guessing game that challenges players to guess a secret number.

    Parameters:
        min_num (int): The minimum value for the range of the secret number (default is 1).
        max_num (int): The maximum value for the range of the secret number (default is 100).

    Returns:
        None: This function doesn't return anything. It interacts with the user to play the game.

    Raises:
        ValueError: If `min_num` is greater than `max_num`.

    Usage:
        Call this function to start the number guessing game. The player will be prompted to enter
        their guesses to identify the secret number within the given range. The game provides feedback
        after each attempt, indicating if the guess is too low or too high. The player has only 3 attempts
        to guess the correct number. If they don't guess correctly within the given attempts, they'll receive
        a message indicating that they lost the game.

        Example:
        >>> number_guessing_game(1, 50)
        Welcome to the Number Guessing Game! Guess the secret number between 1 and 50.
        You have only 3 attempts
        Enter your guess: 25
        Too low. Try again!
        Enter your guess: 40
        Too high. Try again!
        Enter your guess: 35
        Congratulations! You guessed the secret number 35 in 3 attempts!

    """
    if min_num > max_num:
        raise ValueError("min_num must be less than or equal to max_num.")

    secret_number = random.randint(min_num, max_num)
    attempts = 1

    print(f"Welcome to the Number Guessing Game! Guess the secret number between {min_num} and {max_num}.\nYou have only 3 attempts")

    while attempts <= 3:
        guess = int(input("Enter your guess: "))

        if guess == secret_number:
            print(f"Congratulations! You guessed the secret number {secret_number} in {attempts} attempts!")
            sys.exit(0)  # Exit the game successfully

        elif guess < secret_number:
            print("Too low. Try again!")
        else:
            print("Too high. Try again!")

        attempts += 1

    if attempts == 4:
        print("Oops! You Lost, Try Again :)")
        sys.exit(1)  # Exit the game with failure
