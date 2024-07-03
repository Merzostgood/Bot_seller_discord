import json, sys
sys.path.append("..")

async def JSONUpdate(data):
    with open("database.json", "w", encoding='utf8') as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
    f.close()
    return data

async def reader():
    with open("database.json", "r", encoding='utf8') as f:
        data = json.loads(f.read())
    f.close()
    return data