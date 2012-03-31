from django.db import models

#These are the database models for the rerun backend. All of the data
#to be stored in the backend will be stored using these objects.

#User: This model is used to store the users information
class User(models.Model):
    userName = models.CharField(max_length=200)
    userEmail = models.EmailField(max_length=75)
    userId = models.CharField(max_length=200)
    #UserId stores each users unique id at the moment it is the phones id

#Filter: This models is used to store the filter name, IE each filter will have a name and an associated list of keywords that are specified by the user. This model stores the relationship to a user and the filter name along with the filter keywords in CSV format.
class Filter(models.Model):
    user = models.ForeignKey(User)
    filterName = models.CharField(max_length=200)
    filterKeywords = models.TextField()

#Item: This model is used for every item that is received. IE each reuse post will have its data posted here in CSV format. 
class Item(models.Model):
    itemInformation = models.TextField()
    
#FilterResults: This stores the result of comparing the filter with an item. If the filter matches the item then a 1 is appended to the results binary string if not then a 0 is appended.  
class FilterResults(models.Model):
    user = models.ForeignKey(User)
    itemKey = models.IntegerField()
    results = models.CharField(max_length=200)
