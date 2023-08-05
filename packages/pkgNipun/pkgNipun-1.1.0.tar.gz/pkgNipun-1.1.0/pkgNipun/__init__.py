import random
import string

def nipuns_password(exclude_letters):
    length = random.randint(6, 12)
    p1 = []
    
    p1.append(random.choice(string.digits))  # random digit generated
    p1.append(random.choice(string.ascii_uppercase))  # random uppercase alphabet
    p1.append(random.choice(string.ascii_lowercase))  # random lowercase alphabet
    
    for i in range(length - 3):
        char = random.choice(string.ascii_letters + string.digits)
        while char in exclude_letters:
            char = random.choice(string.ascii_letters + string.digits)
        p1.append(char)
    
    return ''.join(p1)

# Read excluded letters from "place.csv" and "name.csv"
with open('Place.csv', 'r') as file:
    excluded_place = file.read().strip()

with open('Name.csv', 'r') as file:
    excluded_name = file.read().strip()

# Combine excluded letters from both files
excluded_letters = excluded_place + excluded_name

# Generate password excluding the letters from the files
p1 = nipuns_password(excluded_letters)
print(p1)
