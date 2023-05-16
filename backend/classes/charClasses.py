from backend.classes.itemClasses import *
import uuid

def id():
    return str(uuid.uuid4())

class SkillQuest:
    def __init__(self, skill:str = "",name:str = "", activity:str = "", goal:int = 0, current:int = 0, unit:str = "", completed:bool = False, existingQuest:dict = None) -> None:
        self.quest = {
            "skill":skill,
            "name":name,
            "activity":activity,
            "goal":goal,
            "current":current,
            "unit":unit,
            "completed":completed
        } if existingQuest == None else existingQuest["quest"]
        self.id = ""
    
    def advance(self, advanceBy:int):
        quest = self.quest
        if quest["goal"] <= quest["current"] + advanceBy:
            quest["completed"] = True
            quest["current"] = quest["goal"]
        else:
            quest["current"] += advanceBy

class PC:
    def __init__(self, existingPC:dict = None) -> None:
        self.userID = "" if existingPC == None else existingPC["userID"]
        self.linkedGame = "" if existingPC == None else existingPC["linkedGame"]
        self.simple = {
                "name":"",
                "player-name":"",
                "level":0,
                "class":"",
                "race":"",
                "carry-capacity":0
        } if existingPC == None else existingPC["simple"]
        self.pc = {
            "health":{
                "ap":{
                    "min":0,
                    "value":0,
                    "max":0
                },
                "hp":{
                    "min":0,
                    "value":0,
                    "max":0
                }
            },
            "dt":{
                "value":0,
                "max":0
            },
            "speed":{
                "land":0,
                "swimming":0,
                "flying":0,
                "climbing":0
            },
            "actions":{
                "spells":[],
                "class":[],
                "race":[],
                "other":[]
            },
            "skills":{
                "ath":{
                    "name":"athletic",
                    "attrib":["stronger","more stamina","can wield heavy weapons","can wield large weapons"],
                    "desc":"This character has spent time training their body, making them a powerhouse of strength and stamina. This character can perform great feats of strength, wield huge and heavy weapons.",
                    "activ":"skill has no downtime activity",
                    "bank":"skill has no knowledge bank",
                    "points":0
                },
                "per":{
                    "name":"performer",
                    "attrib":["good artistic skills","flexible","grant bonues by performing"],
                    "desc":"This character has spent time gaining skills in various arts and can offer a great variety of artistic expressions. They can grant bonuses to friends with their art by instilling hope, extra energy, or serenity within them.",
                    "activ":"can learn new arts, new arts in the same category as learnt arts will be mastered faster",
                    "bank":[],
                    "points":0
                },
                "ari":{
                    "name":"aristocrat",
                    "attrib":["upper class social skills","good debatour","political affiliations"],
                    "desc":"This character has spent time rubbing elbows with the upper class and has therefore gained vast political knowledge and excellent debate skills. This character will be at an advantage when interacting with people of the upper class, with extra bonuses if they have knowledge of the relevant political climate. They have a disadvantage when interacting with those of the lower class.",
                    "activ":"can gain affiliations within the political climate they are currently in, if this political climate chare a culture with a known political climate, affilliations will be made faster.",
                    "bank":[],
                    "points":0
                },
                "oft":{
                    "name":"of the people",
                    "attrib":["lower class social skills", "good mediater","cultural acclimator"],
                    "desc":"This character has spent a lot of time in the slums or shady bars and has therefore had a very intimate experience with the culture of the people. Due to the dicey areas, this character has a lot of experience with mediating and avoiding escalation. This character will be at an advantage with interacting with people of the lower class, with extra bonuses if the character is culturally acclimated to the relevant culture. This character is at a disadvantage when interacting with those of the upper class.",
                    "activ":"can acclimate to the culture they are currently in, if the culture shares a political system with a known culture, acclimation will take less time",
                    "bank":[],
                    "points":0
                },
                "eve":{
                    "name":"everyman",
                    "attrib":["middle class social skills","good buissness sense","guild allinaces"],
                    "desc":"This character has spent  a lot of time in marketplaces, with shop owners, or perhaps wandering traders, this has given them a good sense of business and good alliances with various guilds around the world. This character will have advantages when haggling or speaking to those of the middle class and can pull from their guild network for places to stay, free meals, or even reparations.",
                    "activ":"can expand thier guild network",
                    "bank":[],
                    "points":0
                },
                "hun":{
                    "name":"hunter",
                    "attrib":["good tracker","knows and understands animals","can train pets to battle"],
                    "desc":"This character has spent a lot of time on a farm, or perhaps in the forest, and has gained a good sense for animals. They are better at training animals and can therefore have them fight besides them in battle.",
                    "activ":"can train more pets",
                    "bank":[],
                    "points":0
                },
                "wel":{
                    "name":"well read",
                    "attrib":["pattern recognition","bookish knowledge","can wield complex vanilla staffs"],
                    "desc":"This character has spent a lot of time reading or at university lectures and has gained excellent pattern recognition from various puzzles and riddles. This character can wield complex vanilla staffs.",
                    "activ":"can learn a new subject, if the subject is popular in the area they reside, subject will be mastered faster",
                    "bank":[],
                    "points":0
                },
                "han":{
                    "name":"handy",
                    "attrib":["dexterous","crafting knowledge","can wield complex modded staffs"],
                    "desc":"This character has spent time as an apprentice, or self-teaching at various practical tasks, they have become quite dexterous from working with tools and shaping building materials into things. They can wield complex ranged weapons.",
                    "activ":"can learn a new trade, if a related guild is active in area, trade will be mastered faster",
                    "bank":[],
                    "points":0
                },
                "sne":{
                    "name":"sneaky",
                    "attrib":["convincing lair","intimidating","trained thief"],
                    "desc":"This character has been on the wrong side of the law or had to learn out of necessity, they have learned the way of a silver tongue, quick fingers, and a brooding stare.",
                    "activ":"skill has no downtime activity",
                    "bank":"skill has no knowledge bank",
                    "points":0
                },
                "nat":{
                    "name":"naturalist",
                    "attrib":["survivalist","strong willed","plant friend"],
                    "desc":"This character has spent a lot of time on the cusp of death, having to scavenge to live, always being 1 or 2 missed meals from starvation, due to this they know how to take care of themselves and a small group of people in survival situation, knows their way around the plant life and can shrug off diseases and extreme hunger pain.",
                    "activ":"can get to know local flora and fauna to make gathering easier",
                    "bank":[],
                    "points":0
                }
            }
        } if existingPC == None else existingPC["pc"]
        self.sets = {
            "current":[]
        } if existingPC == None else existingPC["sets"]
        self.bag = {
            "consumables":{},
            "weapons":{},
            "armors":{},
            "staffs":{},
            "trade-goods":{},
            "crafting-parts":{},
            "other":{}
        } if existingPC == None else existingPC["bag"]
        self.equipment = {
            "weapon":None,
            "armor":None,
            "bag":None,
            "staff":None,
            "wallet":{},
            "ingredient-stash":{
                "-2":0,
                "-1":0,
                "0":0,
                "+1":0,
                "+2":0,
                "+3":0,
                "+5":0,
                "x2":0,
                "^2":0
            },
            "item-ready":{
                "slots":0,
                "contents":{}
            }
        } if existingPC == None else existingPC["equipment"]

    def addToRdyBag(self,item:Item):
        bag = self.equipment["item-ready"]
        if len(bag["contents"]) != bag["slots"] and item.item["type"] == "consumable":
            return False
        bag["slots"][id()] = item.item
        return True
           
    def canAddToBag(self,item:Item):
        itemType = item.item["type"]+"s"
        bag = self.bag
        if itemType in bag.keys():
            bag[itemType][id()] = item.item
            return itemType
        bag["other"][id()] = item.item
        return "other"

    def addToBag(self,newItem:Item):
        currentFill = 0
        bag = self.equipment["bag"]
        for key, type in self.bag.items():
            for item in type:
                currentFill += int(type[item]["size"])
        if bag:
            max = bag["slots"]
            if max == currentFill:
                return "Sorry, your bag is full", False
            elif max < currentFill+int(newItem.item["size"]):
                return "Sorry, item cannot fit in bag", False
            category = self.canAddToBag(newItem)
            return f'Item added to bag in category: {category}', True
        max = self.simple["carry-capacity"]
        if max == currentFill:
            return "Sorry, you cant carry anymore", False
        elif max < currentFill+int(newItem.item["size"]):
            return "Sorry, the item you are trying to carry is too big", False
        category = self.canAddToBag(newItem)
        return f'Item added to your carried items in category: {category}', True
    
    def equip(self, item:Item, id = None):
        itemType = item.item["type"]
        if itemType not in ["weapon","armor","bag","staff"]:
            return "Sorry, this item cannot be equipped"
        elif not self.equipment[itemType]:
            if id:
                for key, category in self.bag:
                    if category[id]["amount"] > 1:
                        category[id]["amount"] -= 1
                    else: category.pop(id)
            self.equipment[itemType] = item.item
            self.updateEquipment()
            return "Sucessfully equipped"
        elif self.addToBag(Item(None, exsistingItem= self.equipment[itemType]))[1]:
            if id:
                for key, category in self.bag:
                    if category[id]["amount"] > 1:
                        category[id]["amount"] -= 1
                    else: category.pop(id)
            self.equipment[itemType] = item.item
            self.updateEquipment()
            return "Sucessfully equipped, old equipment added to bag"
        return "Sorry, your old equipment cannot fit in your bag"

    def calcSkillMods(self):
        for key, skill in self.pc["skills"].items():
            formula = (skill["points"]-5)*self.simple["level"]/15
            skill["mod"] = int(round(formula))

    def increaseSkillQuest(self, questId:str, increase:int):
        for key, skill in self.pc["skills"].items():
            if type(skill["bank"]) == list:
                for quest in skill["bank"]:
                    if quest["id"] == questId:
                        quest = SkillQuest(existingQuest=quest)
                        quest.advance(increase)
    
    def addQuest(self, quest:object):
        quest = quest.__dict__
        skillFromQuest = quest["quest"]["skill"]
        skillBank = self.pc["skills"][skillFromQuest]["bank"]
        if len(skillBank) != 0:
            quest["id"] = f'{skillFromQuest}{len(skillBank)+1}'
        else:
            quest["id"] = f'{skillFromQuest}1'
        skillBank.append(quest)

    def updateEquipment(self):
        bag = self.equipment["bag"]
        armor = self.equipment["armor"]
        if bag != None:
            self.simple["carry-capacity"] = bag["slots"]
        if armor != None:
            ap = self.pc["health"]["ap"]
            ap["max"] = armor["apMax"]
            ap["value"] = armor["apValue"]

    def modifyHealth(self, mod,targetStr):
        health = self.pc["health"]
        target = health[targetStr] if targetStr != "dt" else self.pc["dt"]
        ap = self.pc["health"]["ap"]
        hp = self.pc["health"]["hp"]
        dt = self.pc["dt"]
        if mod[0] == "+" or mod[0] == "-":
            if mod[1:].isnumeric():
               target["value"] = int(target["value"]) + int(mod)
            if ap["value"] < 0:
                hp["value"] += ap["value"]
                ap["value"] = 0
            if hp["value"] <= 0:
                dt["max"] = hp["max"]
                dt["value"] = hp["max"] + hp["value"]
                hp["value"] = 0
            if self.equipment["armor"]:
                print("modifying ap on armor")
                self.equipment["armor"]["value"] = ap["value"]
            return True
        elif target["value"] != int(mod) and mod[0] != "+" and mod[0] != "-" and mod.isnumeric():
            target["value"] = int(mod)
            if targetStr == "ap" and self.equipment["armor"]:
                print("modifying ap on armor")
                self.equipment["armor"]["value"] = int(mod)
            return False







