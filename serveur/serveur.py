
import math
import random

import graphe


import sqlite3
from  flask import Flask, jsonify, request

from flask_cors import CORS
app = Flask(import_name=__name__)
CORS(app)




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
    self.peintre = valeur[1]
    self.nom     = valeur[2]
    self.annee   = valeur[3]
    self.hauteur = valeur[4]
    self.largeur = valeur[5]
    self.tags    = valeur[6]
    self.url     = prefixe + cle + ".jpg" 
    self.dejavu  = 0


class Musee : 

  def __init__(self,prefixe,nomFichier):
    self.tableaux = {}
    self.prefixe  = prefixe
    
    self.relationsEntrePeintres = {'Manet':{'Monet':1,'Morisot':1, 'Bazille':0.5}, 'Monet':{'Sisley':1,'Caillebotte':0.75}}

    data = {}
    # Creation du graphe et ajout des concepts
    # ========================================

    self.graphe = graphe.Graphe() 

    self.graphe.root = graphe.Noeud("root",None,self.graphe)

    with open("concepts.csv","r") as f : 
      for ligne in f :
        mots = ligne.split(',')
        fils = mots[0]
        pere = mots[1]
        noeudPere = self.graphe.ajouterNoeud(pere,None)
        noeudFils = self.graphe.ajouterNoeud(fils,None)
        self.graphe.ajouterArc(noeudFils, noeudPere,1.0)

    # Lecture du fichier qui contient la description des tableaux
    # ===========================================================
    with open(nomFichier,"r") as f : 
      data = json.load(f)


    self.peintres = data["peintres"]
    tableaux = data["tableaux"]
    self.tableaux = {}
    for cle in tableaux :
      self.tableaux[cle] = Tableau(prefixe,cle,tableaux[cle])
      l = tableaux[cle][6] # la liste des tags

      # Dans le graphe chaque tableau est identifiee par : cle
      # cle permet d acceder aux proprietes du tableau dans le dictionnaire self.tableaux
      noeudObjet = self.graphe.ajouterObjet(cle,l[:])
      for concept in l : 
        noeudConcept = self.graphe.ajouterNoeud(concept, None)
        self.graphe.ajouterArc(noeudObjet, noeudConcept, 1.0)

      # # Pour test
      # for noeud in self.graphe.noeuds : 
      #   print("Nom : ", self.graphe.noeuds[noeud].nom)
      #   print("Parents : ", [x.nom for x in self.graphe.noeuds[noeud].parents])

    self.graphe.calculNiveau()
    

  def peintsPar(self, peintre):
    l = list(self.tableaux.values())
    res = [x for x in l if x.peintre == peintre]
    return res



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
    self.scene = {}     # contient tous les acteurs
    self.assets = {}
    
  def actors(self):
    return list(self.scene.keys())
    
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
         
def porte(nom, l,h,e):
  return {
            "type" : "porte" ,
            "data" : {"name" : nom, "width":l, "height":h, "depth":e}
           
         }
 
def title(nom, titre):
  return {
           "type" : "titre",
           "data" : {"name":nom, "titre":titre}
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


# ===========================================
# Traitement des requêtes provenant du client
# ===========================================

# fonction onSalle  : traitement des requêtes qui correspondent à un changement de salle
# fonction onClick  : traitement des requêtes qui correspondent à un clic souris du client
# fonction onTicTac : traitement des requêtes qui correspondent à un top d'horloge du client

musee = Musee("./assets/expo/","inventaire.json")    
dejavuSalle = []
dejavuPeintre = []


    
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
    
    
    print(">>> ASSETS OK") 
    
    return jsonify(materiaux)

@app.route('/tictac')
def onTicTac():
  t = request.args.get("Time",default=0,type=float)
  #print("tictac ",t)
  musee.graphe.synchrone()
  return jsonify([])


@app.route('/init')
def init():
    scene = Scene()
    
    dx = 10
    dz = 10

    # ================
    # Création du toit
    # ================     
    scene.actor("toit","actor").add(box("toit",50,0.1,50,"blanc")).add(position(25,3,25))

    # =================    
    # Création des murs
    # =================
    for i in range(0,5) : 
      for j in range(0,5):
        x = i*dx
        z = j*dz 
        suffixe = str(i)+"-"+str(j)
        nomSalle = "salle-" + suffixe
        scene.actor(nomSalle,"actor").add(sphere(nomSalle,0.2,"vert")).add(position(x,0,z))
        nomMurH = "H-"+suffixe
        scene.actor(nomMurH,"actor").add(wall(nomMurH,8,3,0.1,"murBleu")).add(position(i*dx+dx/2,0,j*dz+dz/2))
        nomMurV = "V-"+suffixe
        scene.actor(nomMurV,"actor").add(wall(nomMurV,8,3,0.1,"murBleu")).add(position(i*dx+dx/2,0,j*dz+dz/2)).add(rotation(0,math.pi/2,0))


    print(scene.actors())
    return jsonify(scene.jsonify())
    



    
@app.route('/salle/')
def onSalle():
  print("CHANGEMENTDE SALLE")
  i = request.args.get("I",default=0,type=int)
  j = request.args.get("J",default=0,type=int)
  print("CHANGEMENTDE SALLE : i=",i," - j=",j)
  
  peintres = musee.peintres # liste des peintres
  tableaux = musee.tableaux.values() # les tableaux, liste d'instance de la classe Tableau'

  sceneSalle = Scene()


  # ===============================================================================================================

  # res contient les tableaux (instances de la classe Tableau) à placer dans le musée
  res = []

  # 1. Trouver les tableaux avec le plus fort intérêt (ceux qui ont été cliqués)
  objetsInteret = musee.graphe.calculerObjetsLesPlusInteressants()
  
  # 2. Identifier les parents (tags/concepts) les plus intéressants
  # basés sur les tableaux qui ont le plus d'intérêt
  parents_scores = {}
  
  print("=== Analyse des tableaux les plus intéressants ===")
  for obj in objetsInteret[:5]:  # Prendre les 5 tableaux les plus intéressants
    if obj.interet > 1.0:  # Seulement ceux qui ont été cliqués (intérêt > valeur initiale)
      print(f"Tableau intéressant: {obj.nom}, intérêt: {obj.interet}")
      for parent in obj.consulterParents():
        print(f"  - Parent: {parent.nom}, intérêt: {parent.consulterInteret()}")
        if parent.nom not in parents_scores:
          parents_scores[parent.nom] = 0
        parents_scores[parent.nom] += parent.consulterInteret()
  
  print(f"\n=== Scores des concepts/tags ===")
  for concept, score in sorted(parents_scores.items(), key=lambda x: x[1], reverse=True):
    print(f"{concept}: {score}")
  
  # 3. Calculer un score pour chaque tableau restant basé sur ses parents
  tableaux_scores = []
  for tab in musee.tableaux.values():
    if tab.dejavu == 0:  # Seulement les tableaux non encore placés
      obj = musee.graphe.obtenirNoeudConnaissantNom(tab.cle)
      if obj:
        score = 0
        parents_detail = {}
        for parent in obj.consulterParents():
          if parent.nom in parents_scores:
            score += parents_scores[parent.nom]
            parents_detail[parent.nom] = parents_scores[parent.nom]
        tableaux_scores.append((tab, score, obj.interet, parents_detail))
  
  # 4. Trier les tableaux par score (basé sur les parents) puis par intérêt propre
  tableaux_scores.sort(key=lambda x: (x[1], x[2]), reverse=True)
  
  print(f"\n=== Tableaux recommandés ===")
  for tab, score_parents, interet_propre, parents_detail in tableaux_scores[:10]:
    print(f"{tab.cle}:")
    for parent_nom, parent_score in sorted(parents_detail.items(), key=lambda x: x[1], reverse=True):
      print(f"  {parent_nom}: {parent_score}")
  
  # 5. Sélectionner les tableaux à placer
  res = [tab for tab, _, _, _ in tableaux_scores]

  print(f"\nPaintings left : {len(res)}")

  # ================================================================================================================
  
  # for painting placement
  possible_angles = [0, math.pi/2, 0, math.pi/2 + math.pi, math.pi, math.pi/2 + math.pi, math.pi, math.pi/2]
  a = 3
  b = 4.9
  possible_positions = [(a, b), (b, a), (-a, b), (-b, a), (-a, -b), (-b, -a), (a, -b), (b, -a)]

  nmb_tab_par_sal = 8

  salle = (i,j)
  if(not salle in dejavuSalle):
    currentSalle = sceneSalle.actor("salle-" + str(i)+"-"+str(j),"actor")
    for k in range(0,nmb_tab_par_sal):
      
        sceneSalle.actor("tableau-" + str(i)+"-"+str(j)+"-"+str(k),"actor").add(poster(res[k].cle,res[k].largeur/100,res[k].hauteur/100,res[k].url))
        sceneSalle.getActor("tableau-" + str(i)+"-"+str(j)+"-"+str(k)).add(anchoredTo("salle-" + str(i)+"-"+str(j)))

        print("placed : ",res[k].cle)

        if 0 <= k < 8:
          difPosX, difPosY = possible_positions[k]
          angle = possible_angles[k]

        sceneSalle.getActor("tableau-" + str(i)+"-"+str(j)+"-"+str(k)).add(position(10*i + difPosX, 1.5, 10*j +difPosY))
        sceneSalle.getActor("tableau-" + str(i)+"-"+str(j)+"-"+str(k)).add(rotation(0, angle,0))
        res[k].dejavu = 1
        
    currentSalle.add(position(10*i,0,10*j))
    dejavuSalle.append(salle)


  return jsonify(sceneSalle.jsonify())
    
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

        for obj in musee.graphe.consulterObjets():
          if(obj.nom == nomObjet):
            print("ADDING INTEREST TO ",obj.nom, " tags : ", obj.consulterParents())

            musee.graphe.asynchrone(obj)

            # Augmenter l'intérêt du tableau cliqué
            obj.ajouterInteret(1.0)
            print("Tableau ",obj.nom," intérêt:",obj.consulterInteret())

            for p in obj.consulterParents():
              p.ajouterInteret(1.0)
              print(p.nom,":",p.consulterInteret())

        return jsonify([])
    else : 
        return jsonify([])

if __name__ == "__main__" : 
    app.run(debug=True)
