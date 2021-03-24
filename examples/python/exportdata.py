import json

data = [];
data.append({
    'ID': '000000',
    'Name': 'Screwdriver',
    'Range_lower': '0',
    'Range_upper': '100'
})

with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)
