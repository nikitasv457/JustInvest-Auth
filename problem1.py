import time

# Hardcoded mapping of users to roles for testing

users = {}
users['Sasha Kim'] = 'Client'
users['Emery Blake'] = 'Client'
users['Noor Abbasi'] = 'Premium Client'
users['Zuri Adebayo'] = 'Premium Client'
users['Mikael Chen'] = 'Financial Advisor'
users['Jordan Riley'] = 'Financial Advisor'
users['Ellis Nakamura'] = 'Financial Planner'
users['Harper Diaz'] = 'Financial Planner'
users['Alex Hayes'] = 'Teller'
users['Adair Patel'] = 'Teller'

# Function to get the role from the user
# As the password file is not implemented yet, this will use the hardcoded
# data set from above

def get_role_from_user(username):
    if username in users:
        return users[username]
    return None # invalid username

# The RBAC config
# This is hard coded as per requirements
role_to_permissions = {}
role_to_permissions['Client'] = [1,2,4]
role_to_permissions['Premium Client'] = [1,2,3,5]
role_to_permissions['Financial Advisor'] = [1,2,3,7]
role_to_permissions['Financial Planner'] = [1,2,3,6,7]
role_to_permissions['Teller'] = [1,2]


# Function to check if a specific access type is permitted for a user
# Ensures Teller role adheres to time restrictions (9:00 AM to 5:00 PM)
# Returns True if access is permitted, False otherwise
# The time_of_access should be a time.struct_time object

def access_check(username,access,time_of_access):
    role = get_role_from_user(username)
    if role is None:
        return False                  # Invalid username
    if role == 'Teller':
        if time_of_access.tm_hour < 9 or time_of_access.tm_hour >= 17:          # If role is Teller, they have time time restrictions
            return False
    permissions = role_to_permissions[role]                                     # 
    return access in permissions


# Test cases to check access control functionality
# Simulates different access times and verifies access permissions  
time_list = ['08:59AM','04:00PM','05:01PM']                 # List of test times    
time_struct_list = [time.strptime(t, "%I:%M%p") for t in time_list]         # Converts times to struct_time
index = 0

# Test access for each user and permission

for x in range(1,8):
    print("access_check(Sasha Kim",x,time_list[index],"):", access_check('Sasha Kim',x,time_struct_list[index]))
    index = (index+1) % len(time_list)

for x in range(1,8):
    print("access_check(Noor Abbasi",x,time_list[index],"):", access_check('Noor Abbasi',x,time_struct_list[index]))
    index = (index+1) % len(time_list)

for x in range(1,8):
    print("access_check(Mikael Chen",x,time_list[index],"):", access_check('Mikael Chen',x,time_struct_list[index]))
    index = (index+1) % len(time_list)

for x in range(1,8):
    print("access_check(Harper Diaz",x,time_list[index],"):", access_check('Harper Diaz',x,time_struct_list[index]))
    index = (index+1) % len(time_list)

for x in range(1,8):
    print("access_check(Adair Patel",x,time_list[index],"):", access_check('Adair Patel',x,time_struct_list[index]))
    index = (index+1) % len(time_list)

# Testing for Teller during various times
for t in range(len(time_list)):
    for x in range(1,3):
        print("access_check(Alex Hayes",x,time_list[t],"):", access_check('Alex Hayes',x,time_struct_list[t]))
