import random
import csv

numerals = ['0','1','2','3','4','5','6','7','8','9']
lowerCaps = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
upperChars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

combinedChars = numerals + lowerCaps + upperChars

with open('Names.csv') as names_file:
        
        names_reader = csv.reader(names_file)
        nameList = []
        for row in names_reader:
            nameList.append(row[0])
        
with open('Places.csv') as places_file:
    places_reader = csv.reader(places_file)
    placeList = []

    for row in places_reader:
        placeList.append(row[0])

def custom_choice(combinedChars):
    idx = random.randint(0, len(combinedChars)-1)
    return combinedChars[idx]

def make_random():
    passLength = random.randint(6, 12)
    password = []
    password.append(random.choice(numerals))  # Include one numeric value
    
    for _ in range(passLength - 1):
        password.append(custom_choice(combinedChars))
    
    random.shuffle(password)
    pswd = "".join(password)
    # print (pswd)
    if(passwordChecker(pswd)==False):
         return make_random()
    else:
        return pswd

def passwordChecker(created_pass):
    # created_pass="Gujrat"# remove comment to see iwhat happens when passwrod is same as word incsv
    password_found = (created_pass in placeList)
    if password_found:
        return False
    
    else:
        password_found2 = (created_pass in placeList)
        if password_found2:
            return False
        else:
            return True

    


def generatePass():
    created_pass = make_random()
    return created_pass


# final_pass = generatePass()
# print(len(final_pass))
# print(final_pass)