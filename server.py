import json
from flask import Flask, render_template, request, redirect, url_for, session, flash
from os import listdir, remove
from os.path import isfile, join
from flask_login import LoginManager, UserMixin, login_user, login_required
from backend.classes.classes import *
from backend.classes.charClasses import *
from backend.classes.itemClasses import *
import backend.func as func
import backend.serverfunc as sfunc

#Start server:
#flask --app server run --debug

app = Flask(__name__, static_url_path="", static_folder="static", template_folder="html")

app.secret_key = "i/2r:='d8$V{[:gHm5x?#YBB-D-6)N"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with open("users.json","r") as f:
        users = json.loads(f.read())
    for user in users:
        if user_id == user["id"]:
            correct_user = User(user["name"], user["password"], user["id"])
            
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
                    verified_user = User(user["name"], user["password"], user["id"])
                    break
        
        if verified_user:
            login_user(verified_user)
            return redirect(url_for("index"))
    
    
    return render_template("login.html")

@app.route("/index", methods=["GET", "POST"])
def index():
    PCs = [] 
    for PC in listdir("PCs"):
        PCs.append(PC.split(".")[0])

    if request.method == "POST":

        if request.form["sheet-name"]:
            return redirect(url_for(f'sheet',jsonNam = request.form["sheet-name"]))
        elif request.form["redirect-to"] == "load-sheet":
            return redirect(url_for(f'sheet',jsonNam = request.form["sheets"]))
        return redirect(url_for(f'{request.form["redirect-to"]}'))
    
    return render_template("index.html", PCs = PCs)

@app.route(f'/sheet/<jsonNam>', methods=["GET", "POST"])
def sheet(jsonNam):
    sfunc.makeNewJson(jsonNam)
    with open(f'PCs/{jsonNam}.json', 'r') as f:
        pc = PC(existingPC=json.loads(f.read()))

    form = request.form

    if request.method == "POST":

        sfunc.saveDetails(form,pc,jsonNam)

        if form["button"] == "edit-mode":
            return redirect(url_for(f'sheet_edit',jsonNam = jsonNam))

    return render_template("parts/sheet.html",pc=pc)

@app.route(f'/sheet/<jsonNam>/edit_mode', methods=["GET", "POST"])
def sheet_edit(jsonNam):
    with open(f'PCs/{jsonNam}.json', 'r') as f:
        pc = PC(existingPC=json.loads(f.read()))
    
    form = request.form

    if request.method == "POST":

        sfunc.savePC(form, pc, jsonNam)

        if "finish" in form["button"].split(","):
            return redirect(url_for(f'sheet',jsonNam = jsonNam))
        
    return render_template("parts/sheet_edit_mode.html",pc=pc)


@app.route("/map", methods=["GET", "POST"])   
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
def mapMarkers():
    with open(f'static/map/mapStuff/markers.json', "r") as f:
        map = json.loads(f.read())
    return map

@app.route("/geoJSON", methods=["GET"])
def geoJSON():
    with open(f'static/map/mapStuff/geojson.json', "r") as f:
        geojson = json.loads(f.read())
    return geojson

@app.route("/areaItems", methods=["GET"])
def areaItems():
    with open(f'static/map/mapStuff/areas.json', "r") as f:
        areas = json.loads(f.read())
    relavantArea = Area("", 0,existingArea = areas[request.args.get("area")])
    return relavantArea.searchArea(focus = request.args.get("focus"))