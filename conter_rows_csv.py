import csv

with open('./archive/test.csv') as File:  
    reader = csv.reader(File)
    
    # row_count = sum(1 for i in reader) 
    
    # print("reader len",row_count)
    
    for row in reader:
        print(row)