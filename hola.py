my_list = None

# print('a' in my_list)  # 👉️ False

if my_list is None:
    my_list = [] # 👈️ set to empty list if None

print('a' in my_list)  # 👉️ False

ba = [1,2,3,3]

for i in range(len(ba)):
    print(ba[i])
    
import json

# Creating a dictionary
Dictionary = {1:'Welcome', 2:'to',
			3:'Geeks', 4:'for',
			5:'Geeks'}

# Converts input dictionary into
# string and stores it in json_string
json_string = json.dumps(Dictionary)
print('Equivalent json string of input dictionary:',
	json_string)
print("	 ")

# Checking type of object
# returned by json.dumps
print(type(json_string))

# json.dumps pasa de dict a JSON string 
# json.loads pasa de JSON string a dict

# Posiciones es VAL
# Movimientos es TRA

msj = "Como ?"

if "est" in msj or "EST" in msj:
    print("si")
else:
	pass
key = "CCL_20220915.zip"
file_name = key[0:-4]
file_zip = f"{file_name}.zip"
print(file_zip)