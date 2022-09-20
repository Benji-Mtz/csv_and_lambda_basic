import csv
 
# with open('./archive/data.csv', newline='') as File:  
#     reader = csv.reader(File)
#     for row in reader:
#         print(row)

with open('./archive/data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    count = 0
    for row in reader:
        count += 1
        print(row['date'], row['price'])
        if count == 10:
            break