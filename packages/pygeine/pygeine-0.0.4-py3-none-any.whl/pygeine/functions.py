def hello(name):
    """
    Returns a greeting message with the given name.

    Parameters:
        name (str): The name of the person to greet.

    Returns:
        str: A greeting message.
    """
    message = f"Welcome to Py Geine, {name}!"
    print(f"[pygeine] Greeting '{name}': {message}")
    return message


def is_even(number):
    """
    Determines whether a number is even.

    Parameters:
        number (int): The number to check.

    Returns:
        bool: True if the number is even, False otherwise.
    """
    even = number % 2 == 0
    print(f"[pygeine] Checking evenness of {number}: {even}")
    return even


def sum_numbers(numbers):
    """
    Calculates the sum of a list of numbers.

    Parameters:
        numbers (list): A list of numbers.

    Returns:
        int or float: The sum of the numbers.
    """
    total = sum(numbers)
    print(f"[pygeine] Summing {len(numbers)} numbers: {total}")
    return total


def reverse_string(string):
    """
    Reverses a string.

    Parameters:
        string (str): The string to reverse.

    Returns:
        str: The reversed string.
    """
    reverse = string[::-1]
    print(f"[pygeine] Reversing string '{string}': '{reverse}'")
    return reverse


def count_vowels(string):
    """
    Counts the number of vowels in a string.

    Parameters:
        string (str): The string to count vowels in.

    Returns:
        int: The number of vowels in the string.
    """
    vowels = "aeiouAEIOU"
    count = 0
    for char in string:
        if char in vowels:
            count += 1
    print(f"[pygeine] Counting vowels in '{string}': {count}")
    return count


def calculator():
    """
    Calculates the result of a simple arithmetic operation.

    Parameters:
        None

    Returns:
        None
    """
    num1 = input("Enter the first number: ")
    operator = input("Enter an operator (+, -, *, /): ")
    num2 = input("Enter the second number: ")

    try:
        num1 = float(num1)
        num2 = float(num2)
    except ValueError:
        print("[pygeine] Invalid input, please enter numbers only")
        return

    if operator == "+":
        result = num1 + num2
    elif operator == "-":
        result = num1 - num2
    elif operator == "*":
        result = num1 * num2
    elif operator == "/":
        if num2 == 0:
            print("[pygeine] Cannot divide by zero")
            return
        result = num1 / num2
    else:
        print(f"[pygeine] Invalid operator '{operator}', please enter a valid operator")
        return

    print(f"[pygeine] Calculating {num1} {operator} {num2}: {result}")
    return
