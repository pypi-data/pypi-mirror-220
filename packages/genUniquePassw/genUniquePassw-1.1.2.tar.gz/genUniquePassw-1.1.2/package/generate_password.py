import random
import string
# this function will generate random  password
def generate_random_password(length):
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

#this will store file data in set and will return set
def read_names_from_files(*files):
    names = set()
    for file in files:
        with open(file, 'r') as f:
            names.update(f.read().splitlines())
    return names

#this will check if passsword is as per our requirements (also it is not similar to the names present in files)
def is_valid_password(password, invalid_names):
    return (any(char.isupper() for char in password) and
            any(char.islower() for char in password) and
            any(char.isdigit() for char in password) and
            password not in invalid_names)

def main():
    max_password_length = 12
    places_file = 'places.csv'
    birds_file = 'bird.csv'
    invalid_names = read_names_from_files(places_file, birds_file)

    while True:
        password = generate_random_password(max_password_length)
        if is_valid_password(password, invalid_names):
            print("Generated Password:", password)
            break

if __name__ == "__main__":
    main()

