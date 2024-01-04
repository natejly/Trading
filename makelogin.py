import os
create = False
user = ''
password = ''
key = ''

while not create:
    user = input('Username: ')
    password = input('Password: ')
    key = input('MFA key: ')
    create = input('Create? (y/n): ') == "y"

def addline(str):
    return 'echo ' + str + ' >> login.txt'
os.system('touch login.txt')
os.system(addline(user))
os.system(addline(password))
os.system(addline(key))
print("login file sucessfully created")




