import json, sys
sys.path.append("..")

async def JSONUpdate(data):
    with open("database.json", "w") as f:
        f.write(json.dumps(data, indent=4))
    f.close()
    return data

async def reader():
    with open("database.json", "r") as f:
        data = json.loads(f.read())
    f.close()
    return data