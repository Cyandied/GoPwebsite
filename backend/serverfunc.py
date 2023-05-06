import backend.func as func
from os import listdir
import json
from backend.classes.charClasses import *

def map(request,map):
    if request.method == "POST":
        ids = []
        for marker in map:
            ids.append(marker["id"])

        if request.form["delete"]:
            for marker in map:
                if marker["id"] == int(request.form["id"]):
                    map.remove(marker)

        attributes = func.getAttributes(request.form["attribNames"], request.form["attribVals"])

        if request.form["name"] and int(request.form["id"]) not in ids:
            newMarker = {
                "name":request.form["name"],
                "description":request.form["desc"],
                "attributes":{
                    "names":attributes[0],
                    "values":attributes[1]
                },
                "iconType":request.form["icon"],
                "lat":request.form["lat"],
                "lang":request.form["lang"],
                "id":map[-1]["id"] + 1 if len(map)>0 else 1
            }
            map.append(newMarker)
        if int(request.form["id"]) in ids:
            for marker in map:
                if marker["id"] == int(request.form["id"]):
                    marker["name"]=request.form["name"]
                    marker["description"]=request.form["desc"]
                    marker["iconType"]=request.form["icon"]
                    marker["lat"]=request.form["lat"]
                    marker["lang"]=request.form["lang"]
                    marker["attributes"] = {
                    "names":attributes[0],
                    "values":attributes[1]
                    }
    return map

def makeNewJson(jsonNam):
    PCs = [] 
    for pc in listdir("PCs"):
        PCs.append(pc.split(".")[0])
    if jsonNam not in PCs:
        pc = PC().__dict__
        with open(f'PCs/{jsonNam}.json', "x") as f:
            f.write(json.dumps(pc))
    return

def savePC(form:dict,pc:PC,jsonNam:str):

    for simpleEntry in pc.PC["simple"]:
        pc.PC["simple"][simpleEntry] = int(form[simpleEntry]) if simpleEntry in ["level","carry-capacity"] else form[simpleEntry]
    
    for terrain in pc.PC["speed"]:
        pc.PC["speed"][terrain] = int(form[terrain])
    
    for key, healthEntry in pc.PC["health"].items():
        pc.modifyHealth(form["dt-value"], "dt")
        pc.PC["dt"]["max"] = int(form["dt-max"])
        healthEntry["max"] = int(form[f'{key}-max'])
        if pc.modifyHealth(form[f'{key}-value'],key):
            break

    for key, skill in pc.PC["skills"].items():
        skill["points"] = int(form[f'{key}-points']) if int(form[f'{key}-points']) < 15 else 15

    pc.calcSkillMods()







    button = form["button"].split(",")

    if "add-quest-progress" in button:
        pc.increaseSkillQuest(button[1],1)
    
    if "add" in button:
        pc.addQuest(SkillQuest(form["quest-skill"],form["quest-name"],form["quest-activity"],int(form["quest-goal"]),0,form["quest-unit"]))

    with open(f'PCs/{jsonNam}.json','w') as f:
        f.write(json.dumps(pc.__dict__))

def saveDetails(form:dict,pc:PC,jsonNam:str):
    for key, healthEntry in pc.PC["health"].items():
        pc.modifyHealth(form["dt-value"], "dt")
        pc.PC["dt"]["max"] = int(form["dt-max"])
        healthEntry["max"] = int(form[f'{key}-max'])
        if pc.modifyHealth(form[f'{key}-value'],key):
            break

    button = form["button"].split(",")

    if "add-quest-progress" in button:
        pc.increaseSkillQuest(button[1],1)

    with open(f'PCs/{jsonNam}.json','w') as f:
        f.write(json.dumps(pc.__dict__))



