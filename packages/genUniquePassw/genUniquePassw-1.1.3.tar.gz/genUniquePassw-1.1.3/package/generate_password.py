import random
import string

# Read names from two files
with open('places.csv', 'r') as file1, open('bird.csv', 'r') as file2:
    names1 = set(name.strip().lower() for name in file1)
    names2 = set(name.strip().lower() for name in file2)
 #combines the names from both files into a single set called names using the union() method.
    names = names1.union(names2)

# Define function to generate random password
def generate_password():
    while True:
        # Generate random password
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        # Check if password meets requirements
        if any(char.isupper() for char in password) and any(char.islower() for char in password) and any(char.isdigit() for char in password) and password.lower() not in names:
            return password

# Call function to generate password
password = generate_password()
print(password)
