import random
import string
import os

# Get the current working directory
current_working_dir = os.getcwd()

# File names
places_file = 'places.csv'
bird_file = 'bird.csv'

# File paths
places_file_path = os.path.join(current_working_dir, places_file)
bird_file_path = os.path.join(current_working_dir, bird_file)

# Read names from the files
with open(places_file_path, 'r') as file1, open(bird_file_path, 'r') as file2:
    names1 = set(name.strip().lower() for name in file1)
    names2 = set(name.strip().lower() for name in file2)
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
def generatePass():
    tpass = generate_password()
    return tpass


