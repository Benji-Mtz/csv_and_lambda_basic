# Python3 code to demonstrate
# conversion of lists to dictionary
# using dict() + map()
 
# initializing lists
keys = ["Rash", "Kil", "Varsha"]
values = [1, 4, 5]
 
# Printing original keys-value lists
print ("Original key list is : " + str(keys))
print ("Original value list is : " + str(values))
 
# using map and dict type casting
# to convert lists to dictionary
res = dict(map(lambda i,j : (i,j) , keys,values))
 
# Printing resultant dictionary
print ("Resultant dictionary is : " + str(res))