
import math
import random


import sqlite3
from  flask import Flask, jsonify, request

from flask_cors import CORS
app = Flask(import_name=__name__)
CORS(app)



graphe = {}


scene = set()

def couleur(r,v,b):
    return {"r":r,"v":v,"b":b}


# =============================================================================================    
# La base de données Musée
# =============================================================================================

import json

class Tableau : 

  def __init__(self,prefixe,cle,valeur):
    self.cle     = cle
    self.peintre = valeur[0]
    self.nom     = valeur[1]
    self.annee   = valeur[2]
    self.hauteur = valeur[3]
    self.largeur = valeur[4]
    self.url     = prefixe + cle + ".jpg" 


class Musee : 

  def __init__(self,nomFichier):
    self.tableaux = {}

    data = {}
    with open(nomFichier,"r") as f : 
      data = json.load(f)

    print(data)


# =============================================================================================    
# Représentation 3d
# =============================================================================================


class Acteur : 
  def __init__(self, nom, leType):
    self.json = {"op":"CREATE",
        "id":nom,
        "type":leType,
        "components":[]
        }
        
  def add(self,comp):
    self.json["components"].append(comp)
    return self
    
  def addS(self,l):
    self.json["components"] = self.json["components"] + l
    return self
    
  def toJSON(self):
    return self.json


class Scene : 
  def __init__(self):
    self.scene = {}
    self.assets = {}
    
  def actor(self,nom,leType):
    a = Acteur(nom, leType)
    self.scene[nom] = a
    return a
    
  def getActor(self, nom):
    return self.scene[nom]

    
  def jsonify(self):
    acteurs = list(self.scene.values())
    l = [x.toJSON() for x in acteurs]
    return l    
    
# Les incarnations
# ================

def poster(nom,l,h,url):
  return {
           "type" : "poster",
           "data" : {"name":nom, "largeur":l, "hauteur":h, "tableau":url}
         }
         
def sphere(nom,d,m):
  return {
           "type" : "sphere",
           "data" : {"name":nom, "diameter":d, "material":m}
         }
         
def box(nom,l,h,e,m):
  return {
           "type" : "box",
           "data" : {"name":nom, "width":l, "height":h, "depth":e, "material":m}
         }
         
def wall(nom,l,h,e,m):
  return {
           "type" : "wall",
           "data" : {"name":nom, "width":l, "height":h, "depth":e,"material":m}
         }
         
         
# Le graphe de scène
# ==================
         
def position(x,y,z):
  return {
           "type" : "position",
           "data" : {"x":x, "y":y, "z":z}
         }
         
def rotation(x,y,z):
  return {
           "type" : "rotation",
           "data" : {"x":x, "y":y, "z":z}
         }
         
def anchoredTo(parent):
  return {
           "type":"anchoredTo",
           "data": {"parent":parent}
         }

   
   
# ===========================================================================      


@app.route('/')
def index():

    print("ROUTE : /tous")
    resultat = list(graphe.keys())

    print(resultat)
    return  jsonify(resultat)
    #return render_template('index.html', posts=posts)
    
@app.route('/assets')
def assets():
    materiaux = {}
    
    materiaux["rouge"] = {"color":[1,0,0]}
    materiaux["vert"]  = {"color":[0,1,0]} 
    materiaux["bleu"]  = {"color":[0,0,1]} 
    materiaux["blanc"] = {"color":[1,1,1], "texture":"./assets/textures/murs/dante.jpg","uScale":1,"vScale":1} ; 
    materiaux["murBriques"] = {"color":[1,1,1], "texture":"./assets/textures/murs/briques.jpg","uScale":2,"vScale":1} ;
    materiaux["murBleu"] = {"color":[1,1,1], "texture":"./assets/textures/murs/bleuCanard.jpg","uScale":2,"vScale":1} ; 
    materiaux["parquet"] = {"color":[1,1,1], "texture":"./assets/textures/sol/parquet.jpg","uScale":2,"vScale":2} ;    
    
    return jsonify(materiaux)

@app.route('/init')
def init():
    scene = Scene()
    scene.actor("sphere01","actor").add(sphere("sphere01",0.2,"vert")).add(position(2,0,2))
    scene.actor("box01","actor").add(box("box01",1,3,2,"blanc")).add(position(5,2,2))
    scene.actor("wall01","actor").add(wall("wall01",10,3,0.1,"murBriques")).add(position(10,0,10))
    scene.actor("wall02","actor").add(wall("wall02",10,3,0.1,"murBleu")).add(position(10,0,10)).add(rotation(0,3.14/2,0))   
    scene.actor("poster01","actor").add(poster("poster01",1,1,"./assets/240.jpg")).add(position(3,1.5,-0.2))
    scene.actor("poster02","actor").add(poster("poster02",1,1,"./assets/240.jpg")).add(position(3,1.5,-0.2)).add(anchoredTo("wall01"))
    
    scene.actor("murNord","actor").add(wall("murNord",10,3,0.1,"murBleu")).add(position(0,0,-20))
    scene.actor("murSud","actor").add(wall("murSud",10,3,0.1,"blanc")).add(position(0,0,-24)).add(rotation(0,3.14,0))
    scene.actor("tableau01","actor").add(poster("tableau01",0.8,1,"./assets/expo/monet_la-promenade.jpg")).add(position(3,1.8,-0.2)).add(anchoredTo("murNord"))   
    scene.actor("tableau03","actor").add(poster("tableau03",0.65,0.5,"./assets/expo/monet_les-coquelicots.jpg")).add(position(0,1.8,-0.2)).add(anchoredTo("murNord")) 
    scene.actor("tableau02","actor").add(poster("tableau02",1.91,1.305,"./assets/expo/manet_olympia.jpg")).add(position(3,1.8,-0.2)).add(anchoredTo("murSud"))  
    scene.actor("tableau04","actor").add(poster("tableau04",1.91,1.305,"./assets/expo/manet_le-dejeuner-sur-l-herbe.jpg")).add(position(-3,1.8,-0.2)).add(anchoredTo("murSud"))  
    l = scene.jsonify()
   
    return jsonify(l)



    
@app.route('/click/')
def onClick():
    global scene
    x = request.args.get('X', default=0,type=float)
    y = request.args.get('Y', default=0,type=float)
    z = request.args.get('Z', default=0,type=float)
    nomObjet = request.args.get('Nom')
    print(">> X = ",x)
    if nomObjet != None : 
        print(">>== ", nomObjet)
        try:
            E1 = set(list((graphe[nomObjet]).keys())) - scene
            print("E1 = ", E1)
            listeSuivants = list(E1)
            scene = scene.union(E1)
        except KeyError : listeSuivants = []

        print(">>>> ", listeSuivants)
        x1 = x + (0.5 - random.random())*5
        y1 = y
        z1 = z + (0.5 - random.random())*5
        #l = [creerPoster(nom,(2,2),(x1,2,z1),"./assets/expo/"+nom+".jpg") for nom in listeSuivants]
        #l = [creerPoster(nom,(2,2),(20*random.random(), 2, 20*random.random()),"./assets/expo/"+nom+".jpg") for nom in listeSuivants]
        l = [creerPoster(nom,(2,2),(x+2*random.random(), 2, z-0.5-random.random()),"./assets/expo/"+nom+".jpg",nomObjet) for nom in listeSuivants]
        print(list(l))
        return jsonify(list(l))
    else : 
        return jsonify([])






if __name__ == "__main__" : 
    app.run(debug=True)
