import json

def readjson(rute):
    try:
        with open(rute, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error reading JSON: File '{rute}' not found.")
        exit()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file '{rute}': {e}")
        exit()

def writejson(rute, data):
    """
    Overwrite JSON file content
    """
    try:
        with open(rute, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error writing JSON to file '{rute}': {e}")
        exit()

def main():

    usd = readjson("jsonFiles/usd.json")
    eur = readjson("jsonFiles/eur.json")
    mlc = readjson("jsonFiles/mlc.json")

    all_data = []

    cadinx = 0
    cadv = 62.0

    for idx in range(len(usd)):

        all_data.append({
            "date": usd[idx]["_id"],
            "usd": usd[idx]["median"],
            "eur": eur[idx]["median"],
            "mlc": mlc[idx]["median"],
        })

    writejson("jsonFiles/new.json", all_data)

if __name__ == "__main__":
    main()
