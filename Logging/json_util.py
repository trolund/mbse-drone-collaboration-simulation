import json


def dumpJson(data):
    # print(data)
    # Serializing json
    json_object = json.dumps(data.__dict__)

    # Writing to sample.json
    with open("file.json", "w") as outfile:
        outfile.write(json_object)
