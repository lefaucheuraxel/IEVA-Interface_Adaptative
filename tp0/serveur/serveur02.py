
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
    self.tags    = valeur[5]
    self.url     = prefixe + cle + ".jpg" 


class Musee : 

  def __init__(self,prefixe,nomFichier):
    self.tableaux = {}
    self.prefixe  = prefixe

    data = {}
    with open(nomFichier,"r") as f : 
      data = json.load(f)
    tableaux = data["tableaux"]
    self.tableaux = {}
    for cle in tableaux :
      self.tableaux[cle] = Tableau(prefixe,cle,tableaux[cle])



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

def rejectedByAll(d):
  return {
            "type" : "repulsion",
            "data" : {"range":d}
         }

def friction(k):
  return {
            "type" : "frottement",
            "data" : {"k":k}
         }
         
def attractedBy(acteur):
  return {
           "type" : "attraction",
           "data" : {"attractedBy":acteur}
         }
   
   
# ===========================================================================  

musee = Musee("./assets/expo/","base.json")    


    
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

    for objet in musee.tableaux.values() : 

      url = objet.url
      hauteur = objet.hauteur
      largeur = objet.largeur

      print(url,' -- ',largeur,'-',hauteur,' -- ',objet.tags)

      a = scene.actor(objet.cle,"actor").add(poster(objet.cle,largeur/100,hauteur/100,url))

      x = (0.5-random.random())*20
      z = (0.5-random.random())*20

      a.add(position(x,2,z))


    return jsonify(scene.jsonify())



    
@app.route('/click/')
def onClick():
    global scene
    x = request.args.get('X', default=0,type=float)
    y = request.args.get('Y', default=0,type=float)
    z = request.args.get('Z', default=0,type=float)
    nomObjet = request.args.get('Nom')

    if nomObjet != None : 

        print("Objet sélectionné : ",nomObjet)
        print("Point d'intersection : ",x," - ", y ," - ",z)

        return jsonify([])
    else : 
        return jsonify([])






if __name__ == "__main__" : 
    app.run(debug=True)
