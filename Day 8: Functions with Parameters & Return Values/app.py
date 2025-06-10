# Day 8 – Functions with Parameters & Return Values

# 🔹 Example 1: Function with one parameter
def greet(name):
    print(f"Hello, {name}!")

greet("Tag")  # Output: Hello, Tag!


# 🔹 Example 2: Function with two parameters and return value
def full_name(first, last):
    return f"{first} {last}"

name = full_name("Syed", "Zaidi")
print("Full Name:", name)  # Output: Full Name: Syed Zaidi


# 🔹 Practice Task 1: Square of a number
def square(num):
    return num * num

print("Square of 5:", square(5))  # Output: 25


# 🔹 Practice Task 2: Check if a number is even
def is_even(number):
    return number % 2 == 0

print("Is 4 even?", is_even(4))  # Output: True
print("Is 7 even?", is_even(7))  # Output: False


# 🔹 Practice Task 3: Personalized message
def welcome_message(name, course):
    return f"Welcome {name} to the {course} course!"

print(welcome_message("Tag", "Python"))  
# Output: Welcome Tag to the Python course!


# 🔹 Mini Project: BMI Calculator
def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return round(bmi, 2)

# User input
w = float(input("Enter your weight in kg: "))
h = float(input("Enter your height in meters: "))

result = calculate_bmi(w, h)
print("Your BMI is:", result)
