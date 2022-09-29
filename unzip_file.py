from zipfile import ZipFile

path_file = './archive/PRE_20220913.zip'
 
# opening the zip file in READ mode
with ZipFile(path_file, 'r') as zip:
    # printing all the contents of the zip file
    zip.printdir()
  
    # extracting all the files
    print('Extracting all the files now...')
    zip.extractall()
    print('Done!')