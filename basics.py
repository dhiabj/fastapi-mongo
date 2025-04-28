"""
Python Basics Comprehensive Guide
Covers: Syntax, Data Structures, Operations, and Classes
"""

# ====================
# 1. Syntax Basics
# ====================

# Print statement
print("Hello, Python!")  # Basic output

# Variables and data types
name = "Alice"           # String
age = 30                 # Integer
height = 5.8             # Float
is_student = False       # Boolean
is_adult = True          # Boolean

# Variable naming conventions
user_name = "Alice"  # Snake case recommended
BAD_NAME = "Avoid"   # All caps for constants


# Numeric types
integer = 10
float_num = 3.14
complex_num = 1 + 2j


# Type conversion
str_age = str(age)       # Convert to string
int_height = int(height)  # Convert to integer (truncates)

# Indentation matters for code blocks
# Conditional statements
if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teen")
else:
    print("Child")


# For loop
for i in range(3):       # Range generates 0-2
    print(f"Loop iteration {i}")

# For..Else
numbers = [1, 3, 5]
for num in numbers:
    if num % 2 == 0:
        break
else:
    print("No even numbers")

# While loop
count = 0
while count < 2:
    print(f"While loop: {count}")
    count += 1

# Functions


def greet(name):
    """Documentation string"""
    return f"Hello, {name}!"


# Function arguments
print(greet("Alice"))

# Default arguments


def power(base, exponent=2):
    return base ** exponent


# Keyword arguments
print(power(exponent=3, base=2))

# xargs (*args)


def sum_numbers(*nums):
    return sum(nums)


print(sum_numbers(1, 2, 3))  # 6

# ====================
# 2. Data Structures
# ====================

# Lists - Ordered, mutable
fruits = ["apple", "banana", "cherry"]
fruits.append("orange")      # Add item
fruits[1] = "berry"          # Modify item
print(f"List: {fruits}")

# Tuples - Ordered, immutable
colors = ("red", "green", "blue")
print(f"Tuple element: {colors[0]}")  # Access

# Sets - Unordered, unique elements
unique_numbers = {1, 2, 3, 2}         # {1, 2, 3}
unique_numbers.add(4)

# Dictionaries - Key-value pairs
person = {
    "name": "Charlie",
    "age": 25,
    "city": "Paris"
}
print(f"Dictionary value: {person['name']}")

# Strings
message = "Hello Python"
# Escape sequences
escaped = "He said, \"Python is awesome!\"\nNew line"

# String methods
print(message.upper())       # HELLO PYTHON
print(message.find('Py'))    # 6
print(message.replace('Hello', 'Hi'))

# ====================
# 3. Operations
# ====================

# Arithmetic
result = 10 + 3 * 2   # 16 (operator precedence)


# Comparison
is_equal = (5 == 5.0)  # True (value equality)
print(10 > 5)   # True

# Logical operators
logic_check = (True and False) or True

if 18 <= age < 65 and is_adult:
    print("Working age")

# Ternary operator
status = "Adult" if age >= 18 else "Minor"

# String operations
full_name = "John" + " " + "Doe"   # Concatenation
# Formatted strings (f-strings)
formatted = f"{full_name.upper()} is {age} years old"

# Membership tests
exists = "apple" in fruits         # True

# List comprehension
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]

# ====================
# 4. Classes
# ====================


class Animal:
    """Base class example"""

    # Class variable
    kingdom = "Animalia"

    def __init__(self, name):
        # Instance variable
        self.name = name

    def speak(self):
        raise NotImplementedError("Subclass must implement")


class Dog(Animal):
    """Inherited class"""

    def speak(self):
        return "Woof!"

    # Special method for string representation
    def __str__(self):
        return f"Dog named {self.name}"


# Using classes
buddy = Dog("Buddy")
print(buddy.speak())       # Woof!
print(buddy)               # Uses __str__ method

# ====================
# 5. Error Handling
# ====================

try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
finally:
    print("Cleanup code here")

# ====================
# 6. File Operations
# ====================

# Writing to file
with open("demo.txt", "w") as f:
    f.write("Sample text")

# Reading from file
with open("demo.txt", "r") as f:
    content = f.read()

print(f"File content: {content}")
