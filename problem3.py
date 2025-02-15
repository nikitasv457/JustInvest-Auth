import secrets
import hashlib
import getpass

# code from problem 2

# Function to generate a salted hash for a given password
# Inputs: 
#   salt: as a hex string
#   password: as a string
# Returns:
#   the salt concatenated with salted hash as a hex string
def get_hash_str(salt, password):
    m = hashlib.sha256()
    saltedinput = salt + password
    m.update(saltedinput.encode('utf-8'))
    hhex = m.hexdigest()
    return salt + hhex


# Function to add a user record to the password file
# Arguments: 
#   username: The unique identifier for the user
#   password: The plain text password for the user
#   name: The full name of the user
#   role: The role assigned to the user
# The function will chose a random salt and hash the password and store the data in the file
def add_record(username,password,name,role):
    salthex = secrets.token_hex(24)
    h = get_hash_str(salthex, password)
    record = username + ':' + h + ':' + name + ':' + role + '\n'
    with open('passwd.txt','a') as f:
        f.write(record)

# Function to read a user record from the passwd.txt file based on username
# Arguments:
    # username: The identifier for the user
# Returns:
#   A list containing the user's data (username, hashed password, name, role) if found, or None otherwise
def read_record(username):
    try:
        with open('passwd.txt') as f:
            for line in f.readlines():
                line = line.strip()
                u = line.split(':')[0]
                if u == username:
                    return line.split(':')
    except FileNotFoundError:
        return None
    return None

# New code for problem 3

# Function to retrieve a list of weak passwords from 'weak.txt'
# Returns:
#   A list of weak passwords or an empty list if 'weak.txt' is not found
def get_weaks():
    try:
        with open('weak.txt') as f:
            return [x.strip() for x in f.readlines()]             # Returns the list of weak passwords
    except FileNotFoundError:
        return []                                                 # Returns an empty list

# Function to validate a password based on criteria
# Inputs:
#   username: The username associated with the password
#   password: The password to validate
#   weaklist: A list of weak passwords
# Returns:
#   True if the password is valid, False otherwise
def validate_password(username, password, weaklist):
    if len(password) < 8:                                        # Checks if password is lesser than 8 characters
        print("Password should have at least 8 characters")
        return False
    if len(password) > 12:                                       # Checks if password is greater than 12 characters
        print("Password should have at most 12 characters")
        return False
    if username == password:                                     # Checks if password matches username
        print("Password cannot be same as username")
        return False
    if password in weaklist:                                     # Checks if password is in the weak list
        print("Password in prohibited list")
        return False
    specials = '!@#$%*&'                                         # Allowed special characters
    upper = False
    lower = False
    digit = False
    special = False
    for x in password:                                           # Checks for each required character type
        if x.isupper():
            upper = True
        if x.islower():
            lower = True
        if x.isdigit():
            digit = True
        if x in specials:
            special = True

    if not upper:
        print("Password must contain at least one upper case character")
        return False
    if not lower:
        print("Password must contain at least one lower case character")
        return False
    if not digit:
        print("Password must contain at least one digit")
        return False
    if not special:
        print("Password must contain at least one of the following:",specials)
        return False
    return True


# Function to prompt and add a new user
def adduser():
    username=input("Username: ")                                    # Prompts for username
    if read_record(username) is not None:                           # Checks if username already exists
        print("Username already exists")
        return
    name=input("Name: ")
    rolemap = {1:'Client', 2:'Premium Client',3:'Financial Planner',4:'Financial Advisor',5:'Teller'}
    for i in rolemap:                                                # Displays role options   
        print('[',i,rolemap[i],']')     
    r = int(input("Role [1-5]: "))                                   # Prompts the user for role selection
    role = rolemap[r]                                                # Gets the role
    weaklist = get_weaks()                                           # Retrieves the list of weak passwords
    while True:
        p = getpass.getpass()                                        # Prompts for password securely (hides it)
        if validate_password(username,p,weaklist):                   # Validates the password against the weak list
            break
    add_record(username,p,name,role)                                 # If validation is successful, the user is added

    print("User added!")

# Tests for password validation:
def unit_test_validate_password():
    the_weak_list = get_weaks()
    tests = [['john','abcd@G1'],['john','abcdhYUI@3877'],['john','poll@St1'],['john','Abcde@fghi12'],
            ['john','abcdefg1'],['john','ABCDEFG1'],['john','ABCD@efg'],['john','Abcd1234#'],
            ['John@1Deere','John@1Deere'], ['jack','Abcd#1234']]
    for t in tests:
        print('Username:',t[0],'Password:',t[1])
        valid = validate_password(t[0],t[1],the_weak_list)
        print('Valid password?',valid)
    print("++++++ Starting with user addition ++++++")


# unit_test_validate_password()

while True:
    print('\n\njustInvest User addition\n')
    adduser()
