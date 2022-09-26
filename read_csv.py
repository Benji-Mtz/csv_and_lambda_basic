import csv
csv.register_dialect('pipe', delimiter='|', quoting=csv.QUOTE_NONE)
path_file = './archive/PRE_20220913.txt'

# with open('./archive/data.csv', newline='') as File:  
#     reader = csv.reader(File)
#     for row in reader:
#         print(row)

''' 
with open('./archive/data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    count = 0
    for row in reader:
        count += 1
        print(row['date'], row['price'])
        if count == 10:
            break
'''
table = []
batch = []
item_keys = {}

def read_csv_from_txt(file):    
    with open(file) as csvfile:
        ''' Leyendo un csv desde un txt '''
        reader = csv.DictReader(csvfile, dialect='pipe')
        count = 0
        items_count = 0
        for row in reader:
            if items_count == 0:
                for i in row:
                    item_keys[i[1:-1]]=''
                items_count += 0
            # print(row['date'], row['price'])
            # print(list(row.keys())[0][1:-1])
            # print(row['"Fecha"'][1:-1], row['"Emisora"'][1:-1])
            batch.append(row)
            count += 1
            if count == 3:
                break
            

def read_batch(rows, item_keys_table):    
    # techrules-drop
    value_clean = ''
    for i in range(len(rows)):
        item_keys_aux = {}  
        for item in item_keys_table:
            if '"' in rows[i][f'"{item}"']:
                value_clean = rows[i][f'"{item}"'][1:-1]
                # print(rows[i][f'"{item}"'][1:-1])
            if '"' not in rows[i][f'"{item}"']:
                value_clean = rows[i][f'"{item}"']
                # print(rows[i][f'"{item}"'])
            # print(value_clean, type(value_clean))
            item_keys_aux[item] = value_clean
        table.append(item_keys_aux)

   
        
    

read_csv_from_txt(path_file)
# print(batch)
# print(item_keys)
read_batch(batch, item_keys)
print(table)