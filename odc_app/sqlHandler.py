# Primary Author: James Shelley
# Database models go here



#checks if email/password combination is valid (returns True/False)
def isValidLogin(email, password):
    pass


#checks if role exists (returns True/False)
def emailExists(email):
    pass


#creates a new user if possible and returns True on success, False on failure
#if no second line of address then it will be None
def createUser(role, email, password, firstName, lastName, phoneNumber, birthdate, country, region, addressFirstLine, addressSecondLine):
    pass


#gets role from email
def getRole(email):
    pass


#gets a list containing all the regions in the DB
def getRegions():
    pass
