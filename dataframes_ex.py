
#Selecting different imports

import pandas as pd
from pprint import pprint
import openpyxl
import csv

# Open the given workbook and store it in an excel object
excel = openpyxl.load_workbook("mental_health.xlsx")

# Select the active sheet
sheet = excel.active

# Create a writer object for the CSV file
col = csv.writer(open("mental_health.csv", "w", newline=""))

# Write the data into the CSV file row by row
for row in sheet.iter_rows():
    col.writerow([cell.value for cell in row])

# Read the CSV file "tt.csv" and convert it to a dataframe
data = pd.DataFrame(pd.read_csv("mental_health.csv"))

# Print the dataframe
print(data)

# Print the whole dataframe
print(data.to_markdown())

#query by country in a modular way
country = str(input('What country would you like to query:\t').strip()).capitalize()

results = ''
while True:
    if country in data['Entity'].values:

        # print results after querying by country
        results = data[data['Entity']== f'{country}']
        print(results.to_markdown())
        break
    else:
        print(f'The country you have entered is not in the list! Please check your spelling! You have entered {country}')
        country = str(input('What country would you like to query:\t').capitalize().strip())


