from flask import Flask, jsonify, request
app = Flask(__name__)
import jsonschema

marks_schema = {
    "type": "object",
    "patternProperties": {
        "^[a-zA-Z]+$": {"type": "integer", "minimum": 0}
    },
    "additionalProperties": False,
    "minProperties": 1,
    "required" : ["Python", "Golang", "Java"]
}

user_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "marks": marks_schema,
        "total": {"type": "integer", "minimum": 0}
    },
    "required": ["name", "marks"]
}


record = [{
    "name" : "Alice",
    "marks" : {
        "Python" : 7,
        "Golang" : 8,
        "Java" : 6
    },
    "total" : 21
    }]

@app.route('/', methods=['GET'])
def getAll():
    return record

@app.route('/<string:name>', methods=['GET'])
def getByName(name):
    for i in record:
        if i["name"] == name:
            return jsonify(i)
    return jsonify({"error" : "User not found"})

@app.route("/", methods=["POST"])
def postNew():
    dataRec = request.get_json()
    try:
        jsonschema.validate(dataRec, user_schema)
    except jsonschema.ValidationError as e:
        return jsonify({"error" : "Invalid input"})
    
    for i in record:
        if i["name"] == dataRec["name"]:
            return jsonify({"error" : "Name already exists"})  
    editRec = {
        "name" : dataRec["name"],
        "marks" : {
            "Python" : dataRec["marks"]["Python"],
            "Golang" : dataRec["marks"]["Golang"],
            "Java" : dataRec["marks"]["Java"],
        },
        "total" : dataRec["marks"]["Python"] + dataRec["marks"]["Golang"] + dataRec["marks"]["Java"]
    }      
    record.append(editRec)
    return jsonify({"success" : "New user added"})

@app.route("/<string:name>", methods=["PUT"])
def updateUser(name):
    dataRec = request.get_json()
    try:
        jsonschema.validate(dataRec, user_schema)
    except:
        return jsonify({"error" : "Invalid input"})
    
    for i in record:
        if i["name"] == name:
            record.remove(i)
            record.append(dataRec)
            return jsonify({"success" : "User data updated"})
        else:
            return jsonify({"error" : "User not found"})

@app.route("/<string:name>", methods=["DELETE"])
def deleteUser(name):
    for i in record:
        if i["name"] == name:
            record.remove(i)
            return jsonify({"success" : f"User {name} deleted"})
    return jsonify({"error" : "User not found"})

if __name__ == '__main__':
    app.run(debug=True)
