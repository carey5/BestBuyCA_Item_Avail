import json

def add_last_drop(item, date, quantity):
    with open('scrapers_data.json', 'r') as outfile:
        data = json.load(outfile)

        data['lastdrops'].append({
            "item": item,
            "date": date,
            "quantity": quantity
        })

        with open('scrapers_data.json', 'w') as outfile:
            json.dump(data, outfile)
