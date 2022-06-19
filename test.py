import json, datetime

# Main loop
while True:

    # Read
    with open("biking.json", "r") as f:
        data = json.loads(f.read())

    # Print
    for i in data:
        if i["nominal"]:
            print(f'{i["date"]}  {i["miles"]} mi  {i["percent"]}%')
        else:
            print(f'{i["date"]}  {i["miles"]} mi  {i["percent"]}%  OFF COURSE')
    if len(data) > 0:
        print()

    # Input
    data.append({})
    data[-1]["date"] = datetime.datetime.now().strftime("%x")
    data[-1]["miles"] = int(input("Miles: "))
    data[-1]["percent"] = round(data[-1]["miles"]/23.6*100, 1)
    if input("Nominal? ").lower().startswith("n"):
        data[-1]["nominal"] = False
    else:
        data[-1]["nominal"] = True
    print()

    # Write
    with open("biking.json", "w") as f:
        print(json.dumps(data, indent=4), file=f)
