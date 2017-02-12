import csv

# Strucure to hold CSV data
data = {"header": None, "rows": []}

# Read CSV file
with open('Loans.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        if data["header"] is None:
            data["header"] = row
            print("Loaded header row: " + repr(data["header"]))
        else:
            data["rows"].append(row)

print("Data read:")
print(repr(data))

