#This is where all of the methods dealing with the database are. Essentially this class provides a nice convenient wrapper for the database and streamlines the other methods access to the database.
from rerun.rerunbackend.models import User, Filter, Item, FilterResults
from rerun.rerunbackend.utils.errorUtils import Error  

#These are the user database management methods which allow a users data to be added and removed from the database. 
#Every single database entry is uniquely defined by the users email. There can only be one user per email.

#This method is used to add a new user to the database system
def addUser(userName, userEmail, userID, filters):
    user = User.objects.filter(userEmail=userEmail)
    #Checks to see if there are any other users with this email in the database already
    if(len(user)==0):#if not then add a new user
        user = User(userName=userName,userEmail=userEmail,userID=userID)
        user.save()
        for key in filters.keys():
            user.filter_set.create(filterName=key, filterKeywords=filters[key])
    else: #otherwise throw error
        Error.userAlreadyExists(userEmail)


#This method is used to change the users name in a database entry 
def setUserName(newUserName, userEmail):
    user = User.objects.filter(userEmail=userEmail)
    if(len(user)==0):
        Error.userNotFound(userEmail) #This is the error handler class 
    else if(len(user)==1):
        user[0].userName=newUserName
    else:#If there is more than one user with the same email int DB
        Error.aliasingError(userEmail)#Error for multiple entries with the same email

#This method is used to change a users email.
def setUserEmail(newUserEmail, userEmail):
    user = User.objects.filter(userEmail=userEmail)
    if(len(user)==0):#Checks if there is no user with this email
        Error.userNotFound(userEmail)
    else if(len(user)==1):#If there is then it changes the email
        user[0].userEmail=newUserEmail
    else:#If there is more than one entry with the same email 
        Error.aliasingError(userEmail)#light on fire and run around

#This method can change the usersID which atm is used to store phone meid or number
def setUserID(newUserID, userEmail):
    user = User.objects.filter(userEmail=userEmail)
    if(len(user)==0):#If there is no user throw user not found error
        Error.userNotFound(userEmail)
    else if(len(user)==1):
        user[0].userID=newUserID #Set new id
    else:#if there is more than one user with the same email throw aliasing error
        Error.aliasingError(userEmail)

#This method is used to remove people from the database
def removeUser(userEmail):
    user = User.objects.filter(userEmail=userEmail)
    if(len(user)==0):
        Error.userNotFound(userEmail)
    else if(len(user)==1):
        user.
        user.delete()
    else:
        Error.aliasingError(userEmail)

##################End of User Database Management methods#######################

##################Begin Filter Management Utilities#############################

def overwriteFilters(filters, userEmail):
    user = User.objects.filter(userEmail=userEmail)
    if(len(user)==0):
        Error.userNotFound(userEmail) #This is the error handler class 
    else if(len(user)==1):
        user[0].filter_set.all().delete()#Clear existing filters and wipe
        for key in filters.keys():
            user.filter_set.create(filterName=key, filterKeywords=filters[key])
    else:#If there is more than one user with the same email int DB
        Error.aliasingError(userEmail)#Error for multiple entries with the same email    

def removeFilter(filterName, userEmail):
    user = User.objects.filter(userEmail=userEmail)
    if(len(user)==0):
        Error.userNotFound(userEmail) #This is the error handler class 
    else if(len(user)==1):
        user[0].filter_set.filter(filterName=filterName).delete()
    else:#If there is more than one user with the same email int DB
        Error.aliasingError(userEmail)#Error for multiple entries with the same email   

def addFilter(filterName, filterKeywords, userEmail):
    user = User.objects.filter(userEmail=userEmail)
    if(len(user)==0):
        Error.userNotFound(userEmail) #This is the error handler class 
    else if(len(user)==1):
        currFilter=user[0].filter_set.filter(filterName=filterName)
        if(len(currFilter)==0):
            user[0].filter_set.create(filterName=filterName, filterKeywords=filterKeywords)
        else:
            Error.filterNameAlreadyExists()
    else:#If there is more than one user with the same email int DB
        Error.aliasingError(userEmail)#Error for multiple entries with the same email 

###############TODO for Filters############################
def overwriteFilterKeywords(filterName, filterKeywords):

def insertFilterKeyword(filterName, filterKeyword, userEmail):

def removeFilterKeyword(filterName, filterKeyword, userEmail):

def getUserFilters(userEmail):

###########################End of Filters Management Utilites#################################

###########################Item Utilities#####################################################
# NEED to give thought to how items are referenced in the code, how do I call a particular item etc.
def insertNewItem(ItemData,ItemID):

def removeItem(ItemID):

def returnLastNItems(N):

def getItem(ItemID):

##########################End Item Utilites####################################################

##########################Filter Results Utilities#############################################

def transformUserResults(originalFilterKeywords, newFilterKeywords):

def generateTransformationMatrix(originalFilterKeywords, newFilterKeywords):

def getResults(userEmail, itemID):

def setResult(itemID):

def removeResult(itemID):

##########################End of Filter Results Utilities######################################
