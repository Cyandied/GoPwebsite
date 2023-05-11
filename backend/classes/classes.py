import uuid
import backend.func as func
import random

class Area:
    def __init__(self, name:str, size:int,existingArea = None) -> None:
        self.name = name if existingArea == None else existingArea["name"]
        self.size = size if existingArea == None else existingArea["size"]
        self.ingredients = func.genrate_items(size) if existingArea == None else existingArea["ingredients"]

    def searchArea(self,minFind = 4, maxFind = 8,focus = None):
        ingredients = self.ingredients["item_list"]
        result = []
        if focus:
            randWeight = []
            baseWeight = (1-0.70)/(len(ingredients)-1)
            for item in ingredients:
                if item["value"] != focus:
                    randWeight.append(baseWeight)
                    continue
                randWeight.append(0.30)
            for i in range(random.randint(minFind,maxFind)):
                result.append(random.choices(ingredients, randWeight)[0])
        
        else:
            for i in range(random.randint(minFind,maxFind)):
                result.append(random.choices(ingredients)[0])
        return result

class User():
    def __init__(self, name, password,role="player",games = [], id = None) -> None:
        self.name = name
        self.password = password
        self.role = role
        self.games = games
        self.id = id or str(uuid.uuid4())
    def to_json(self):        
        return {"name": self.name}

    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.id)





