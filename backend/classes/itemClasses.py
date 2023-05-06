class ItemTemplates:
    template = {
        "base":{
            "name":"",
            "type":"",
            "value":0,
            "size":0,
            "desc":"",
            "amount":1,
            "notes":""
        },
        "consumable":{
            "type":"",
            "effect":"",
            "formula":"",
            "uses":0,
            "used":0,
            "other":[]
        },
        "armor":{
            "apMax":0,
            "apValue":0,
            "material":"",
            "weak":[],
            "strong":[]
        },
        "weapon":{
            "dmg-formula":[],
            "prereqs":[],
            "material":"",
        },
        "weapon-dmg-formula":{
            "prereq":"",
            "desc":"",
            "dmg-type":"",
            "faces":0,
            "amount":0,
            "flat":0
        },
        "staff":{
            "accumulators":[],
            "level":"",
            "staff-type":"",
            "legal":True,
            "material":"",
        },
        "rod":{
            "color":""
        },
        "accumulator":{
            "slots":0,
            "rods":[]
        },
        "trade-good":{
            "sale-value":0,
            "material":"",
        },
        "ingredient":{
            "name":"",
            "value":0
        },
        "crafting-part":{
            "type":"",
            "for":"",
            "material":"",
            "other":[]
        },
        "kit":{
            "for":""
        },
        "bag":{
            "slots":0
        }
    }

class Item:
    def __init__(self, type:str = "", existingItem:dict = None) -> None:
        self.item = self.merge(ItemTemplates.template["base"],ItemTemplates.template[type],type) if existingItem == None else existingItem["item"]

    def merge(throwAwayObject,dict1, dict2,type):
        dict1["type"] = type
        return dict1 | dict2


