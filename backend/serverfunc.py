import backend.func as func
from os import listdir
import json
from backend.classes.charClasses import *
from backend.classes.itemClasses import *
from backend.classes.classes import *
from backend.classes.actionClasses import *

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

def getItemTemplate(itemType):
    item = Item(itemType)
    return item

def getActionTemplate(actionType):
    action = Action(actionType)
    return action

def saveItem(request, itemType):
    item = Item(itemType)
    form = request.form
    for entry in item.item:
        if entry not in ["amount","notes"]:
            item.item[entry] = form[entry]
    return item.item

def saveAction(request, actionType):
    action = Action(actionType)
    form = request.form
    for entry in action.action:
        if entry not in ["notes"]:
            action.action[entry] = form[entry]
    return action.action

def makeNewJson(jsonNam, id):
    PCs = [] 
    for pc in listdir("PCs"):
        PCs.append(pc.split(".")[0])
    if jsonNam not in PCs:
        pc = PC().__dict__
        pc["userID"] = id
        with open(f'PCs/{jsonNam}.json', "x") as f:
            f.write(json.dumps(pc))
    return

def savePC(form:dict,pc:PC,jsonNam:str):
    message = ""
    with open(f'itemsActions/items.json', 'r') as f:
        items = json.loads(f.read())
    with open(f'itemsActions/actions.json', 'r') as f:
        actions = json.loads(f.read())

    for simpleEntry in pc.simple:
        pc.simple[simpleEntry] = int(form[simpleEntry]) if simpleEntry in ["level","carry-capacity"] else form[simpleEntry]
    
    for terrain in pc.pc["speed"]:
        pc.pc["speed"][terrain] = int(form[terrain])
    
    for key, healthEntry in pc.pc["health"].items():
        pc.modifyHealth(form["dt-value"], "dt")
        pc.pc["dt"]["max"] = int(form["dt-max"])
        healthEntry["max"] = int(form[f'{key}-max'])
        if pc.modifyHealth(form[f'{key}-value'],key):
            break

    for key, skill in pc.pc["skills"].items():
        skill["points"] = int(form[f'{key}-points']) if int(form[f'{key}-points']) < 15 else 15

    pc.calcSkillMods()

    button = form["button"].split(",")

    if "new-set" in button:
        if form["new-set-name"]:
            pc.sets[form["new-set-name"].replace(" ","-")] = pc.sets["current"]
    
    elif "overwrite" in button:
        if form["set"] != "current":
            pc.sets[form["set"]] = pc.sets["current"]
    
    elif "load" in button:
        if form["set"] != "current":
            pc.sets["current"] = pc.sets[form["set"]]
    
    elif "delete-set" in button:
        if form["set"] != "current":
            pc.sets.pop(form["set"])

    elif "add-quest-progress" in button:
        pc.increaseSkillQuest(button[1],1)
    
    elif "add-item" in button:
        message = pc.addToBag(Item(None, exsistingItem=items[button[1]]))[0]
    
    elif "equip-item" in button:
        message = pc.equip(Item(None, exsistingItem=items[button[1]]))
    
    elif "add" in button:
        pc.addQuest(SkillQuest(form["quest-skill"],form["quest-name"],form["quest-activity"],int(form["quest-goal"]),0,form["quest-unit"]))
    
    elif "linkGame" in button:
        with open("users.json","r") as f:
            users = json.loads(f.read())
        for user in users:
            if user["games"]:
                for game in user["games"]:
                    if user["games"][game] == form["linkGame"]:
                        pc.linkedGame = {"name":game,
                                         "id":form["linkGame"]}
    elif "unlinkGame" in button:
        pc.linkedGame = ""

    with open(f'PCs/{jsonNam}.json','w') as f:
        f.write(json.dumps(pc.__dict__))
    
    return message

def saveDetails(form:dict,pc:PC,jsonNam:str):

    button = form["button"].split(",")

    if "add-quest-progress" in button:
        pc.increaseSkillQuest(button[1],1)

    if "linkGame" in button:
        with open("users.json","r") as f:
            users = json.loads(f.read())
        for user in users:
            if user["games"]:
                for game in user["games"]:
                    if user["games"][game] == form["linkGame"]:
                        pc.linkedGame = {"name":game,
                                         "id":form["linkGame"]}
    if "unlinkGame" in button:
        pc.linkedGame = ""

    with open(f'PCs/{jsonNam}.json','w') as f:
        f.write(json.dumps(pc.__dict__))

def newUser(name:str,password:str,make:bool):
    if make:
        with open("users.json","r") as f:
            users = json.loads(f.read())
        users.append(User(name,password).__dict__)
        with open("users.json",'w') as f:
            f.write(json.dumps(users))

