import secrets
import hashlib
import getpass

# Function to generate a salted hash for a given password
# Inputs: 
#   salt: as a hex string
#   password: as a string
# Returns:
#   the salt concatenated with salted hash as a hex string
def get_hash_str(salt, password):
    m = hashlib.sha256()                                # Initialize a SHA-256 hash object
    saltedinput = salt + password                       # Concatenate the salt and password
    m.update(saltedinput.encode('utf-8'))               # Update the hash object with the encoded input
    hhex = m.hexdigest()                                # Get the hash as a hexadecimal string
    return salt + hhex                                  # Return the salt concatenated with the hash


# Function to add a user record to the password file
# Arguments: 
#   username: The unique identifier for the user
#   password: The plain text password for the user
#   name: The full name of the user
#   role: The role assigned to the user
# The function will chose a random salt and hash the password and store the data in the file
def add_record(username,password,name,role):
    salthex = secrets.token_hex(24)                       # Generate a random 24-byte salt
    h = get_hash_str(salthex, password)                   # Generate the salted hash using the password and salt
    record = username + ':' + h + ':' + name + ':' + role + '\n'    
    with open('passwd.txt','a') as f:                     # Open 'passwd.txt' 
        f.write(record)                                   # Write the record to the file


# Function to read a user record from the passwd.txt file based on username
# Arguments:
    # username: The identifier for the user
# Returns:
#   A list containing the user's data (username, hashed password, name, role) if found, or None otherwise
def read_record(username):
    try:
        with open('passwd.txt') as f:
            for line in f.readlines():              # Read each line from the file
                line = line.strip()                 # Remove any leading or trailing whitespace  
                u = line.split(':')[0]              # Extract the username from the line
                if u == username:                   # Check if the username matches the requested one
                    return line.split(':')          # Return the record as a list
    except FileNotFoundError:
        return None
    return None

# Test cases for adding and retrieving user records
records = [['johnDoe','mysecret','John Doe','Premium Client'],
            ['sashak','password1','Sasha Kim','Client'], 
            ['emeryb','password2','Emery Blake','Client'], 
            ['noorA','password3','Noor Abbassi','Premium Client'], 
            ['zuriA','password4','Zuri Adebayo','Premium Client'], 
            ['mikchaen','passwd5','Mikael Chen','Financial Advisor'], 
            ['jordanR','password6','Jordan Riley','Financial Advisor'], 
            ['ellisN','password7','Ellis Nakamura','Financial Planner'], 
            ['harperD','password8','Harper Diaz','Financial Planner'], 
            ['adairp','password9','Adair Patel','Teller'], 
            ['alexHayes','password9','Alex Hayes','Teller']
          ]

# Adding test records to 'passwd.txt'
for r in records:
    print("Adding")
    print("  id:",r[0])
    print("  password:",r[1])
    print("  name:",r[2])
    print("  role:",r[3])
    add_record(r[0],r[1],r[2],r[3])

# Reading and displaying user records for specified usernames
for x in ['johnDoe', 'sashak', 'noorA', 'zuriA', 'mikchaen', 'jordanR', 'ellisN', 'harperD', 'adairp','alexHayes', 'emeryc']:
    print("Reading record for",x)
    r = read_record(x)
    if r is None:
        print("  Not found")
    else:
        print("  id:",r[0])
        print("  password:",r[1])
        print("  name:",r[2])
        print("  role:",r[3])
