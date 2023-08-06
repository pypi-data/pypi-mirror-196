import time

def receipt():
    print("********** Welcome to Your First Project **********")
    time.sleep(2)
    print("Iam Glad you are here , in this project we will go through your first Project. \nwe gonna make a Receipt Layout using only 2 built in Functions (print,input)")
    time.sleep(2)
    print("*********** let`s start CODING ***********")
    time.sleep(2)
    print("So first we need to put our project into smaller steps .\n in this project we have 2 parts . \n--1st part will be the inputs we need from the user, \n--2nd Part will be printing the layout")
    time.sleep(2)
    print("*"*80)
    print("***************let's start with our input function***************")
    time.sleep(2)
    print("*"*80)
    print("\tThe ** input() ** function in Python is a built-in function that allows you to interact with the user and get input from them via the keyboard.")
    print("""Example : name = str(input("What is Your Name? "))\n******{name} >>> the Variable name , {str} >>> for the data type we need to get in this case (String) \n******{input("....")} >>> the message will appear for the user to know what is this input for..""")
    time.sleep(5)
    print("IMPORTANT >> the input variables i used is (name, item_name, item_price, item_quantity, tax_rate, subtotal, tax_amount, total)")
    time.sleep(5)
    print("*"*80)
    print("Let's Start acting like a user and insert your inputs")
    name = str(input("What is Your Name? ")).title()
    item_name = input("What is the name of the item you purchased? ")
    item_price = float(input("What was the price of the item? "))
    item_quantity = int(input("How many of the item did you purchase? "))
    tax_rate = float(input("What is the tax rate for your location (e.g., 0.05 for 5%)? "))
    # Calculate the total cost of the purchase
    subtotal = item_price * item_quantity
    tax_amount = subtotal * tax_rate
    total = subtotal + tax_amount
    {time.sleep(2)}
    print(f"Let's go now for the ** print() ** function ")
    {time.sleep(2)}
    print("You should know that ** print() ** have many optional arguments")
    {time.sleep(2)}
    print("But in our case we don't need any arguments :D")
    {time.sleep(2)}
    print("all we need is printing out the Receipt including the inputs Variables we got from the user")
    time.sleep(2)
    print("""Example >> print(f"item : {item_name})""")
    time.sleep(5)

    # Print the receipt
    print(f"--------{name} Receipt --------")
    print(f"Item: \t\t{item_name}")
    print(f"Quantity: \t{item_quantity}")
    print(f"Price per item: ${item_price:.2f}")
    print(f"Subtotal: \t${subtotal:.2f}")
    print(f"Tax ({tax_rate:.0%}): \t${tax_amount:.2f}")
    print(f"Total: \t\t${total:.2f}")
    print("---------------------------------")
    print(f"Thanks For Visiting us today {name} <3")
    print("---------------------------------")

def receipt_download():
    pro = """name = str(input("What is Your Name? ")).title()
item_name = input("What is the name of the item you purchased? ")
item_price = float(input("What was the price of the item? "))
item_quantity = int(input("How many of the item did you purchase? "))
tax_rate = float(input("What is the tax rate for your location (e.g., 0.05 for 5%)? "))
# Calculate the total cost of the purchase
subtotal = item_price * item_quantity
tax_amount = subtotal * tax_rate
total = subtotal + tax_amount
 # Print the receipt
print(f"--------{name} Receipt --------")
print(f"Item: \t\t{item_name}")
print(f"Quantity: \t{item_quantity}")
print(f"Price per item: ${item_price:.2f}")
print(f"Subtotal: \t${subtotal:.2f}")
print(f"Tax ({tax_rate:.0%}): \t${tax_amount:.2f}")
print(f"Total: \t\t${total:.2f}")
print("---------------------------------")
print(f"Thanks For Visiting us today {name} <3")
print("---------------------------------")
    """
    with open ("Receipt.txt","w") as f :
        f.write(pro)

def receipt_quiz():
    print("Welcome to the Receipt Quiz!")
    print("Answer the following questions to test your knowledge of receipts.")
    print("--------------------------------------------------------------")

    # Define a list of quiz questions and answers
    questions = [
        ("What is the name of the function we used to get user data ?", "input"),
        ("What is the name of the function we used to show user data", "print"),
        ("Write code to get user age HINT {use int()}", "age = int(input('What is your age'))"),
        ("How many of the item were purchased?", "item_quantity"),
        ("What is the tax rate for the location?", "tax_rate"),
        ("What is the formula for calculating the subtotal?", "item_price * item_quantity"),
        ("What is the formula for calculating the tax amount?", "subtotal * tax_rate"),
        ("What is the formula for calculating the total?", "subtotal + tax_amount")
    ]

    score = 0
    num_questions = len(questions)

    # Ask each question and check the user's answer
    for i, (question, answer) in enumerate(questions):
        print(f"\nQuestion {i+1}: {question}")
        user_answer = input("Your Answer: ").lower()
        if user_answer == answer:
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. The correct answer is '{answer}'.")

    # Print the user's final score
    print("\nQuiz complete!")
    print(f"You got {score} out of {num_questions} questions correct.")




def calculator():
    print("********** Welcome to Your Second Project **********")
    time.sleep(2)
    print("In this project, we will create a simple calculator that can perform addition, subtraction, multiplication, and division.")
    time.sleep(2)
    print("*********** Let's start CODING ***********")
    time.sleep(2)
    print("*"*80)
    print("*************** Let's start with our input function ***************")
    time.sleep(2)
    print("*"*80)
    print("\tThe ** input() ** function in Python is a built-in function that allows you to interact with the user and get input from them via the keyboard.")
    time.sleep(2)
    print("We will ask the user to enter two numbers and the operation they want to perform.")
    time.sleep(2)
    print("IMPORTANT >> The input variables I used are (num1, num2, operation)")
    time.sleep(2)
    print("*"*80)
    print("Let's act like a user and insert your inputs")
    time.sleep(2)
    num1 = float(input("Enter the first number: "))
    num2 = float(input("Enter the second number: "))
    operation = input("Enter the operation (+, -, *, /): ")
    {time.sleep(2)}
    print(f"Now let's use the ** print() ** function to display the result of our calculation.")
    {time.sleep(2)}
    print("We will use a conditional statement (if/elif/else) to perform the operation the user requested.")
    time.sleep(2)
    if operation == '+':
        result = num1 + num2
        print(f"{num1} + {num2} = {result:.2f}")
    elif operation == '-':
        result = num1 - num2
        print(f"{num1} - {num2} = {result:.2f}")
    elif operation == '*':
        result = num1 * num2
        print(f"{num1} * {num2} = {result:.2f}")
    elif operation == '/':
        result = num1 / num2
        print(f"{num1} / {num2} = {result:.2f}")
    else:
        print("Invalid operation. Please try again.")
        
def calculator_download():
    pro = """num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))
operation = input("Enter the operation (+, -, *, /): ")

if operation == '+':
    result = num1 + num2
    print(f"{num1} + {num2} = {result:.2f}")
elif operation == '-':
    result = num1 - num2
    print(f"{num1} - {num2} = {result:.2f}")
elif operation == '*':
    result = num1 * num2
    print(f"{num1} * {num2} = {result:.2f}")
elif operation == '/':
    result = num1 / num2
    print(f"{num1} / {num2} = {result:.2f}")
else:
    print("Invalid operation. Please try again.")"""
    
    with open ("calculator.txt","w") as f :
        f.write(pro)
        
        
        