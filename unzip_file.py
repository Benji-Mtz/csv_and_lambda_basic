from zipfile import ZipFile

path_file = './archive/TRA_20220915.zip'
 
# # opening the zip file in READ mode
# with ZipFile(path_file, 'r') as zip:
#     # printing all the contents of the zip file
#     path = zip.printdir()
#     print(f'path - { path }')
#     # extracting all the files
#     print('Extracting all the files now...')
#     zip.extractall()
#     print('Done!')

import zipfile

with zipfile.ZipFile(path_file, mode="r") as archive:
    archive.printdir()