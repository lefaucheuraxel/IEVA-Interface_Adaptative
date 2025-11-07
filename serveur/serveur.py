
import math
import random
import numpy as np

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
  sigma = request.args.get("Sigma",default=0.05,type=float)
  
  print(f"\n{'='*60}")
  print(f"TIC-TAC à t={t:.2f}s (sigma={sigma})")
  print(f"{'='*60}")
  
  # Appeler la méthode synchrone pour niveller progressivement les intérêts
  # sigma contrôle la vitesse de nivellement (0.05 = 5% par tick)
  resultat = musee.graphe.synchrone(sigma=sigma)
  
  # Afficher un résumé dans la console
  if resultat:
    print(f"Status: {resultat.get('message', 'N/A')}")
    if resultat.get('status') == 'success':
      print(f"Intérêt moyen: {resultat.get('I_avg', 0)}")
      print(f"Intérêt collecté: {resultat.get('interet_collecte', 0)}")
      print(f"Tags au-dessus de la moyenne: {resultat.get('nb_tags_au_dessus', 0)}")
      print(f"Tags en-dessous de la moyenne: {resultat.get('nb_tags_en_dessous', 0)}")
      
      # Afficher quelques tags modifiés
      if resultat.get('tags_diminues'):
        print("\nTags qui ont perdu de l'intérêt:")
        for tag in resultat['tags_diminues'][:3]:
          print(f"  - {tag['nom']}: {tag['avant']} → {tag['apres']} ({tag['variation']:+.4f})")
      
      if resultat.get('tags_augmentes'):
        print("\nTags qui ont gagné de l'intérêt:")
        for tag in resultat['tags_augmentes'][:3]:
          print(f"  - {tag['nom']}: {tag['avant']} → {tag['apres']} ({tag['variation']:+.4f})")
  
  print(f"{'='*60}\n")
  
  # Retourner les statistiques au client
  return jsonify(resultat if resultat else {})


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

  # 1. Calculer un score pour chaque tableau non encore placé
  # Le score est la somme des intérêts de tous ses parents (tags/concepts)
  tableaux_scores = []
  
  for tab in musee.tableaux.values():
    if tab.dejavu == 0:  # Seulement les tableaux non encore placés
      obj = musee.graphe.obtenirNoeudConnaissantNom(tab.cle)
      if obj:
        # Calculer le score basé sur l'intérêt cumulé de tous les parents
        score_parents = 0
        parents_detail = {}
        
        for parent in obj.consulterParents():
          interet_parent = parent.consulterInteret()
          score_parents += interet_parent
          parents_detail[parent.nom] = interet_parent
        
        # Le score final combine l'intérêt des parents et l'intérêt propre du tableau
        score_total = score_parents + obj.consulterInteret()
        tableaux_scores.append((tab, score_total, score_parents, obj.consulterInteret(), parents_detail))
  
  # 2. Trier les tableaux par score total (parents + propre)
  tableaux_scores.sort(key=lambda x: x[1], reverse=True)
  
  print(f"\n=== Tableaux recommandés pour la salle ({i},{j}) ===")
  for idx, (tab, score_total, score_parents, interet_propre, parents_detail) in enumerate(tableaux_scores[:10]):
    print(f"{idx+1}. {tab.cle} - Score total: {score_total:.2f} (parents: {score_parents:.2f}, propre: {interet_propre:.2f})")
    if parents_detail:
      top_parents = sorted(parents_detail.items(), key=lambda x: x[1], reverse=True)[:3]
      print(f"   Top parents: {', '.join([f'{p}({s:.2f})' for p, s in top_parents])}")
  
  # 3. Sélectionner les tableaux à placer
  res = [tab for tab, _, _, _, _ in tableaux_scores]

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
    
@app.route('/stats')
def getStats():
  """
  Retourne des statistiques sur l'état actuel du système d'intérêt
  Utile pour mesurer l'adaptation aux préférences du visiteur
  """
  # Récupérer les tags et leurs intérêts
  tags = musee.graphe.consulterTags()
  tags_stats = []
  for tag in tags:
    tags_stats.append({
      "nom": tag.nom,
      "interet": round(tag.consulterInteret(), 4),
      "nb_enfants": len(tag.enfants)
    })
  
  # Trier par intérêt décroissant
  tags_stats.sort(key=lambda x: x['interet'], reverse=True)
  
  # Récupérer les tableaux les plus recommandés
  objets_recommandes = musee.graphe.calculerObjetsLesPlusInteressants(10)
  recommandations = []
  for obj in objets_recommandes:
    tableau = musee.tableaux.get(obj.nom)
    if tableau:
      recommandations.append({
        "cle": obj.nom,
        "nom": tableau.nom,
        "peintre": tableau.peintre,
        "tags": tableau.tags,
        "score": round(musee.graphe.calculerInteretObjet(obj), 4)
      })
  
  # Calculer des statistiques globales
  tous_interets = [tag.consulterInteret() for tag in tags]
  interet_moyen = sum(tous_interets) / len(tous_interets) if tous_interets else 0
  interet_max = max(tous_interets) if tous_interets else 0
  interet_min = min(tous_interets) if tous_interets else 0
  
  stats = {
    "tags_top10": tags_stats[:10],
    "recommandations_top10": recommandations,
    "statistiques_globales": {
      "nb_tags_total": len(tags),
      "interet_moyen": round(interet_moyen, 4),
      "interet_max": round(interet_max, 4),
      "interet_min": round(interet_min, 4),
      "ecart_type": round(np.std(tous_interets), 4) if tous_interets else 0
    }
  }
  
  return jsonify(stats)

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
            print("\n" + "="*60)
            print(f"INTERACTION avec le tableau: {obj.nom}")
            print(f"Tags associés: {[p.nom for p in obj.consulterParents()]}")
            print("="*60)

            # 1. Augmenter l'intérêt propre du tableau cliqué
            obj.interet += 1.0
            print(f"\nIntérêt propre du tableau {obj.nom}: {obj.consulterInteret()}")
            
            # 2. Propagation BOTTOM-UP : de l'objet vers les concepts abstraits
            print("\n--- Propagation BOTTOM-UP ---")
            musee.graphe.calculUpInteret()
            print("Intérêts propagés vers les concepts parents")
            
            # 3. Propagation TOP-DOWN : des concepts abstraits vers les objets similaires
            print("\n--- Propagation TOP-DOWN ---")
            musee.graphe.calculDownInteret(objet_source=obj)
            print("Intérêts redistribués vers les objets similaires")
            
            # 4. Méthode asynchrone pour niveler entre les tags
            print("\n--- Redistribution asynchrone ---")
            musee.graphe.asynchrone(obj, tau=0.1)
            
            print("="*60 + "\n")

        return jsonify([])
    else : 
        return jsonify([])

if __name__ == "__main__" : 
    app.run(debug=True)
