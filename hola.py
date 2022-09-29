my_list = None

# print('a' in my_list)  # 👉️ False

if my_list is None:
    my_list = [] # 👈️ set to empty list if None

print('a' in my_list)  # 👉️ False

ba = [1,2,3,3]

for i in range(len(ba)):
    print(ba[i])
    