class Templates:
    consumable = {
        "subtype":"",
        "effect":"",
        "formula":"",
        "uses":0,
        "used":0,
        "other":[]
    }
    armor = {
        "apMax":0,
        "apValue":0,
        "material":"",
        "weak":[],
        "strong":[]
    }
    weapon = {
        "dmg-formula":"",
        "prereqs":[],
        "material":"",
    }
    staff = {
        "accumulators":[],
        "level":"",
        "staff-type":"",
        "legal":True,
        "material":"",
    }
    tradegood = {
        "sale-value":0,
        "material":"",
    }
    craftingpart = {
        "type":"",
        "for":"",
        "material":"",
        "other":[]
    }
    kit = {
        "for":""
    }
    bag = {
        "slots":0
    }
    
    def returnTemplate(itemType:str):
        base = {
            "name":"",
            "type":itemType,
            "value":0,
            "size":0,
            "desc":"",
            "amount":1,
            "notes":""
        }
        print(itemType)
        return base | getattr(Templates,itemType.replace("-",""))
    
class Item:
    def __init__(self, itemType:str, exsistingItem = None) -> None:
        self.item = Templates.returnTemplate(itemType) if exsistingItem == None else exsistingItem
    
    def addAccumulator(self, slots:str, rods:list):
        if self.item["type"] == "staff":
            self.item["accumulators"].append(self.makeAccumulator(slots, rods))

    def makeAccumulator(slots:int, rods:list):
        accumulator = {}
        accumulator["slots"] = slots
        accumulator["rods"] = rods
        return accumulator
