class Templates:
    spell = {
        "test":""
    }
    
    def returnTemplate(actionType:str):
        base = {
            "name":"",
            "type":actionType,
            "desc":"",
            "notes":""
        }
        print(actionType)
        return base | getattr(Templates,actionType.replace("-",""))
    
class Action:
    def __init__(self, actionType:str, exsistingAction = None) -> None:
        self.action = Templates.returnTemplate(actionType) if exsistingAction == None else exsistingAction