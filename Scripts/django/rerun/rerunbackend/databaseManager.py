#This is where all of the methods dealing with the database are. Essentially this class provides a nice convenient wrapper for the database and streamlines the other methods access to the database.
from rerun.rerunbackend.models import User, Filter, Item, FilterResults
import rerun.rerunbackend.errorUtils as Error 

def doesUserExist(userEmail):
    user = User.objects.filter(userEmail=userEmail)
    if(len(user)==0):
        Error.userDoesNotExist(userEmail)
        return False
    elif(len(user)==1):
        return True
    else:
        Error.userAlreadyExists(userEmail)
        return False
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
    if(doesUserExist(userEmail)==True):
        user = User.objects.get(userEmail=userEmail)
        user.userName=newUserName
        user.save()

#This method is used to change a users email.
def setUserEmail(newUserEmail, userEmail):
    if(doesUserExist(userEmail)==True):#If there is then it changes the email
        user = User.objects.get(userEmail=userEmail)
        user.userEmail=newUserEmail
        user.save()

#This method can change the usersID which atm is used to store phone meid or number
def setUserID(newUserID, userEmail):
    if(doesUserExist(userEmail)==True):
        user = User.objects.get(userEmail=userEmail)
        user.userID=newUserID #Set new id
        user.save()

#This method is used to remove people from the database
def removeUser(userEmail):
    if(doesUserExist(userEmail)==True):
        user.objects.get(userEmail=userEmail)
        user.delete()
    
##################End of User Database Management methods#######################

##################Begin Filter Management Utilities#############################

def overwriteFilters(filters, userEmail):
    if(doesUserExist(userEmail)==True):
        user = User.objects.get(userEmail = userEmail)
        user.filter_set.all().delete()#Clear existing filters and wipe
        for key in filters.keys():
            user.filter_set.create(filterName=key, filterKeywords=filters[key])
  
def removeFilter(filterName, userEmail):
    if(doesUserExist(userEmail)==True):
        user = User.objects.get(userEmail=userEmail)
        user.filter_set.filter(filterName=filterName).delete()   

def addFilter(filterName, filterKeywords, userEmail):
    if(doesUserExist(userEmail)==True):
        user = User.objects.get(userEmail=userEmail)
        currFilter=user.filter_set.filter(filterName=filterName)
        if(len(currFilter)==0):
            currFilter = user.filter_set.get(filterName=filterName)
            user.filter_set.create(filterName=filterName, filterKeywords=filterKeywords)
        else:
            Error.filterNameAlreadyExists()

###############TODO for Filters############################
def doesFilterExist(userEmail, filterName):
    if(doesUserExist(userEmail)==True):
        filters=User.objects.get(userEmail=userEmail).filter_set.filter(filterName=filterName)
        if(len(filters)==0):
            Error.filterDoesNotExist(userEmail,filterName)
            return False
        if(len(filters)==1):
            return True
        else:
            Error.filterAliasError(userEmail, filterName)
            return False
        

def overwriteFilterKeywords(userEmail,filterName, filterKeywords):
    if(doesUserExist(userEmail)==True):
        if(doesFilterExist(userEmail,filterName)==True):
            user=User.objects.get(userEmail=userEmail)
            user.filter_set.get(filterName=filterName).filterKeywords=filterKeywords
            user.save()

#def insertFilterKeyword(filterName, filterKeyword, 

#def removeFilterKeyword(filterName, filterKeyword, userEmail):

def getUserFilters(userEmail):
    if(doesUserExist(userEmail)==True):
        user = User.objects.get(userEmail=userEmail)
        print user.filter_set.all()
        return [(str(filters.filterName), str(filters.filterKeywords)) for filters in user.filter_set.all()]
 
###########################End of Filters Management Utilites#################################

###########################Item Utilities#####################################################
# NEED to give thought to how items are referenced in the code, how do I call a particular item etc.
def doesItemExist(ItemID):
    item = Item.objects.filter(id=ItemID)
    if(len(item)==0):
        Error.itemDoesNotExist(ItemID)
        return False
    if(len(item)==1):
        return True
    else:
        Error.itemAliasingError(ItemID)
        return False

def insertNewItem(itemInformation):
    item = Item(itemInformation=itemInformation)
    item.save()
    item.itemInformation=item.itemInformation + ", " + str(item.id)
    item.save()
    
def removeItem(ItemID):
    item= Item.objects.filter(id=ItemID)
    if(len(item)==0):
        Error.noItemFound();
    else:
        item.delete()

def returnLastNItemsData(N):
    if(Item.objects.count()>=N):    
        return [item.itemInformation for item in Item.objects.all()[:N]]
    else:
        N=Item.objects.count()
        return [item.itemInformation for item in Item.objects.all()[:N]]

def getItem(ItemID):
    item= Item.objects.filter(id=ItemID)
    if(len(item)==0):
        Error.noItemFound();
        return "Error"
    else:
        return item.itemInformation

##########################End Item Utilites####################################################

##########################Filter Results Utilities#############################################

#def transformUserResults(originalFilterKeywords, newFilterKeywords):
def doesFilterResultExist(userEmail, itemID):
    if(doesUserExist(userEmail)==True):
        if(doesItemExist(itemID)==True):
            result = User.filterResults_set.filter(itemKey=itemID)
            if(len(result)==0):
                Error.filterResultDoesNotExist(userEmail, itemID)
                return True
            elif(len(result)==1):
                return True
            else:
                Error.filterResultAliasingError(userEmail,itemID)
                return False

def getResults(userEmail, itemID):
    if(doesUserExist(userEmail)==True):
        if(doesFilterResultExist(userEmail,itemID)==True):
            return [itemID + ": "+ str(filterResult) for filterResult in User.filterResults_set.all()]

def setResult(itemID, results):
    if(doesUserExist(userEmail)==True):
        if(doesFilterResultExist(userEmail, itemID)):
           user= User.filterResults_set.get(itemKey=itemID)
           user.results = results
           user.save()

#def removeResult(itemID):

##########################End of Filter Results Utilities######################################
