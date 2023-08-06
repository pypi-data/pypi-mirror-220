import random
import csv

numerals = ['0','1','2','3','4','5','6','7','8','9']
lowerCaps = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
upperChars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

combinedChars = numerals + lowerCaps + upperChars


# Reading the file Names.csv and converting it to a list
with open('Names.csv') as names_file:
        names_reader = csv.reader(names_file)
        nameList = []
        for row in names_reader:
            nameList.append(row[0])
            # nameList.append(row)

# print("nameList>>>>>>>>>>>>>>>" + str(nameList))


# Reading the file Places.csv and converting it to a list
with open('Places.csv') as places_file:
    places_reader = csv.reader(places_file)
    placeList = []

    for row in places_reader:
        placeList.append(row[0])
        # placeList.append(row)
    
    # print("printing the password from the places file : " + str(password))

# print("placeList>>>>>>>>>>>>>>>" + str(placeList))


# Custom function to randomaly choose a char
def custom_choice(combinedChars):
    idx = random.randint(0, len(combinedChars)-1)
    return combinedChars[idx]


#function to randomaly generate a password
def make_random():
    passLength = random.randint(6, 12)
    password = []
    password.append(random.choice(numerals))  # Include one numeric value
    
    for _ in range(passLength - 1):
        password.append(custom_choice(combinedChars))
    
    random.shuffle(password)
    return password

def passwordChecker(created_pass):

        # print("Printing the Password : " + str(password))
        # password_found = any(created_pass in row for row in nameList)
        password_found = (created_pass in row for row in nameList)

        if password_found:
            # print("Password already exists in the CSV.")
            make_random()
        # else:
        #     # print("Password is not present in the CSV.")
        #     continue



        # password_found2 = any(created_pass in row for row in placeList)
        password_found2 = (created_pass in row for row in placeList)

        if password_found2:
            # print("Password already exists in the csv")
            make_random
        else:
            # print("Password is not present in the csv")
            return

    
    # return


def generatePass():
    created_pass = make_random()
    pswd = "".join(created_pass)
    passwordChecker(pswd)
    # print("created password is :>>>>>>>>>>>>>>>> " + str(created_pass))
    # print("the type of the created_pass is : >>>>>>>>>>>>>>>>" + str(type(created_pass)))
    return ''.join(created_pass)

password = generatePass()

print(password)
print(len(password))