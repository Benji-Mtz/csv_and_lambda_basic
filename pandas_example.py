import pandas as pd

df = pd.read_csv("./archive/data.csv")

# print(df)
print(df.columns)
print(df.shape)

'''iLOC'''
# Print row 10
print(df.iloc[9])
# Print from row 0 to 10
print(df.iloc[:10])
# Coordenada (0,1)
print(df.iloc[0,1])
# Print first 5 columns from the rows 0,1 y 2
print(df.iloc[[0,1,2],0:5])

'''LOC'''
print("LOC")
# Obtain the value of the colum price on the first row
print(df.loc[0,'price'])
# Obtain the firsts rows from 0 to 3 (included 3) with the columns from the price to bathrooms
print(df.loc[:3,'price':'bathrooms'])

# Only numerical data
print(df.describe())
# All data
print(df.describe(include='all'))
# Delete a column
print(df.drop(columns=['view']))

# Save dataframe with changes
df2 = df.drop(columns=['view'])
df2.to_csv('./archive/precios_casas.csv', index=False)
