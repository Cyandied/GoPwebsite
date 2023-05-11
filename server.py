import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from os import listdir, remove
from os.path import isfile, join
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from backend.classes.classes import *
from backend.classes.charClasses import *
from backend.classes.itemClasses import *
import backend.func as func
import backend.serverfunc as sfunc

#Start server:
#flask --app server run --debug

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="html")

app.secret_key = "i/2r:='d8$V{[:gHm5x?#YBB-D-6)N"

sfunc.newUser("test2","test2",False)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    correct_user = ""
    with open("users.json","r") as f:
        users = json.loads(f.read())
    for user in users:
        if user_id == user["id"]:
            correct_user = User(user["name"], user["password"], user["role"], user["games"], user["id"])
            
    return correct_user

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        with open("users.json", "r") as f:
            users = json.loads(f.read())
            verified_user = False
        for user in users:
            if request.form["user"] == user["name"]:
                if request.form["pass"] == user["password"]:
                    verified_user = User(user["name"], user["password"], user["role"], user["games"], user["id"])
                    break
        
        if verified_user:
            login_user(verified_user)
            session["user"] = verified_user.__dict__
            return redirect(url_for("index"))
    
    
    return render_template("login.html")

@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        print(session["user"])
        if request.form["button"] == "index":
            return redirect(url_for("index"))
        if request.form["game-name"]:
            with open("users.json","r") as f:
                users = json.loads(f.read())
            for user in users:
                if user["id"] == session["user"]["id"]:
                    user["games"][request.form["game-name"].replace(" ","-")] = str(uuid.uuid4())
                    session["user"] = user
            with open(f'users.json','w') as f:
                f.write(json.dumps(users))
    return render_template("profile.html", user = session["user"])

@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    PCs = [] 
    for jsonNam in listdir("PCs"):
        with open(f'PCs/{jsonNam}', 'r') as f:
            pc = PC(existingPC=json.loads(f.read()))
        dm = False
        games=[]
        if session["user"]["role"] == "dm":
            dm = True
            dmsGames = session["user"]["games"]
            games = dmsGames.keys()
            if pc.linkedGame:
                if pc.linkedGame["id"] in dmsGames.values():
                    game = list(dmsGames.keys())[list(dmsGames.values()).index(pc.linkedGame["id"])]
                    PCs.append([jsonNam.split(".")[0],game])

        if pc.userID == session["user"]["id"] or session["user"]["id"] == "admin":
            PCs.append([jsonNam.split(".")[0],"own"])

    if request.method == "POST":

        if request.form["sheet-name"]:
            return redirect(url_for(f'sheet',jsonNam = request.form["sheet-name"].replace(" ","-")))
        elif request.form["redirect-to"] == "load-sheet":
            return redirect(url_for(f'sheet',jsonNam = request.form["sheets"]))
        elif request.form["redirect-to"]=="log-out":
            logout_user()
            return redirect(url_for("login"))
        return redirect(url_for(f'{request.form["redirect-to"]}'))
    
    return render_template("index.html", PCs = PCs, dm = dm, games = games)

@app.route(f'/sheet/<jsonNam>', methods=["GET", "POST"])
@login_required
def sheet(jsonNam):
    sfunc.makeNewJson(jsonNam, session["user"]["id"])
    with open(f'PCs/{jsonNam}.json', 'r') as f:
        pc = PC(existingPC=json.loads(f.read()))

    form = request.form

    if request.method == "POST":

        sfunc.saveDetails(form,pc,jsonNam)

        if form["button"] == "edit-mode":
            return redirect(url_for(f'sheet_edit',jsonNam = jsonNam))
        if form["button"] == "index":
            return redirect(url_for("index"))

    return render_template("parts/sheet.html",pc=pc)

@app.route(f'/sheet/<jsonNam>/edit_mode', methods=["GET", "POST"])
@login_required
def sheet_edit(jsonNam):
    with open(f'PCs/{jsonNam}.json', 'r') as f:
        pc = PC(existingPC=json.loads(f.read()))
    
    form = request.form

    if request.method == "POST":

        sfunc.savePC(form, pc, jsonNam)

        if "finish" in form["button"].split(","):
            return redirect(url_for(f'sheet',jsonNam = jsonNam))
        
    return render_template("parts/sheet_edit_mode.html",pc=pc)

currentID = ""

@app.route("/item", methods=["GET", "POST"])
@login_required
def item():
    itemTypes = ["consumable","armor","weapon","staff","trade-good","ingredient","crafting-part","kit","bag"]

    with open(f'itemsActions/items.json', 'r') as f:
        itemList = json.loads(f.read())


    if request.method == "POST":

        global currentID

        if request.form["button"] == "get-template":
            itemList["template"] = sfunc.getTemplate(request.form["itemType"]).item
        
        elif request.form["button"] == "save":
            _currentID = str(uuid.uuid4())
            if request.form["id"]:
                _currentID = request.form["id"]
            itemList[_currentID] = sfunc.saveItem(request, request.form["itemType"])
            itemList["template"] = {}
            currentID = ""

        elif request.form["button"] == "index":
            itemList["template"] = {}
            with open(f'itemsActions/items.json','w') as f:
                f.write(json.dumps(itemList))
            return redirect(url_for("index"))
                
        elif request.form["button"] in itemList:
            currentID = request.form["button"]
            itemList["template"] = itemList[request.form["button"]]

        elif request.form["button"].split("_")[0] in itemList:
            itemList.pop(request.form["button"].split("_")[0])

        with open(f'itemsActions/items.json','w') as f:
            f.write(json.dumps(itemList))

    return render_template("item.html", itemTypes = itemTypes, itemList=itemList, currentID = currentID)

@app.route("/map", methods=["GET", "POST"])
@login_required
def map():

    markerFiles = listdir("static/map/mapStuff/markerTypes")
    markers = []
    for marker in markerFiles:
        name,_ = marker.split(".")
        markers.append(name)


    with open(f'static/map/mapStuff/markers.json', "r") as f:
        map = json.loads(f.read())

    map = sfunc.map(request,map)

    with open(f'static/map/mapStuff/markers.json', "w") as f:
        f.write(json.dumps(map))

    return render_template("map.html", mapInfo = map, markers = markers)

@app.route("/mapMarkers", methods=["GET"])
@login_required
def mapMarkers():

    with open(f'static/map/mapStuff/markers.json', "r") as f:
        map = json.loads(f.read())
    return map

@app.route("/geoJSON", methods=["GET"])
@login_required
def geoJSON():

    with open(f'static/map/mapStuff/geojson.json', "r") as f:
        geojson = json.loads(f.read())
    return geojson

@app.route("/areaItems", methods=["GET"])
@login_required
def areaItems():

    with open(f'static/map/mapStuff/areas.json', "r") as f:
        areas = json.loads(f.read())
    relavantArea = Area("", 0,existingArea = areas[request.args.get("area")])
    return relavantArea.searchArea(focus = request.args.get("focus"))