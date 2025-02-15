import secrets
import hashlib
import getpass

# code from problem 1

# The RBAC config
role_to_permissions = {}
role_to_permissions['Client'] = [1,2,4]
role_to_permissions['Premium Client'] = [1,2,3,5]
role_to_permissions['Financial Advisor'] = [1,2,3,7]
role_to_permissions['Financial Planner'] = [1,2,3,6,7]
role_to_permissions['Teller'] = [1,2]


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


# Function to login by verifying correctness of password
# Prompts the user for username and password, validates credentials, and checks against stored records
# Returns:
#   A tuple (username, name, role) if login is successful, or None if login fails
def login():
    username = input("Username: ")
    password = getpass.getpass()                  # Securely prompt for password
    record = read_record(username)
    if record is None:
        return None
    else:
        salthex = record[1][0:48]                 # Extracts the salt from the stored hash
        h = get_hash_str(salthex,password)        # Computes the salted hash for the entered password
        if h == record[1]:                        # Compares computed hash with stored hash
            return (username,record[2],record[3]) # Return user details if credentials match
        else:
            return None

# Main function to manage the application flow
# Displays operations, handles login, and provides access based on user roles
def main():
    while True:
        print("justInvest System")
        print("---------------------------------------")
        print("Operations available on the system:")
        print("1.View account balance")
        print("2.View investment portfolio")
        print("3.Modify investment portfolio")
        print("4.View Financial Advisor contact info")
        print("5.View Financial Planner contact info")
        print("6.View money market instruments")
        print("7.View private consumer instruments")
        print("\n\n")
        
        # Performs login
        result = login()
        if result is None:
            print("\nACCESS DENIED!\n\n")
        else:
            (user, name, role) = result
            print("\nACCESS GRANTED!")
            print("Login id:",user)
            print("User name:",name)
            print("Role:",role)
            print("Authorized operations:",role_to_permissions[role])
            if role == 'Teller':
                print("Authorized from 9:00am to 5:00pm only")
            print("\n\n")


if __name__ == "__main__":
    main()
