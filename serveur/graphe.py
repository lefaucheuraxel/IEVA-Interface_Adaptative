import random

class Noeud : 

  def __init__(self, nom, data, graphe):
    self.nom     = nom
    self.gr      = graphe
    self.niveau  = 1
    self.interet = 1.0
    self.parents = []
    self.enfants = []

  def charger(self, concepts, inventaire):
    pass
     
  def ajouterParent(self, noeud):
    self.parents.append(noeud)
    
  def ajouterEnfant(self, noeud):
    self.enfants.append(noeud)
    
  def consulterParents(self):
    return self.parents
    
  def consulterEnfants(self):
    return self.enfants
    
  def modifierInteret(self,interet):
    self.interet = interet
    
  def ajouterInteret(self, dInteret):
    if(self.nom =="root"):
      return
    self.interet += dInteret
    if(len(self.consulterParents()) == 0):
      return
    for t in self.consulterParents():
      t.ajouterInteret(dInteret/self.niveau)

  def consulterInteret(self):
    return self.interet
    
  def arc(self, noeud1, noeud2):
    return self.gr.arcs.get((noeud1.nom, noeud2.nom), None)
    
  def calculNiveau(self):
    if self.enfants == [] :
      return 0
    else:
      l = [noeud.calculNiveau() for noeud in self.enfants]
      self.niveau = 1 + max(l)
     # print(self.niveau)
      return self.niveau
      

      

class Objet(Noeud):
  def __init__(self, nom, tags, gr):
    Noeud.__init__(self,nom, tags, gr)
    self.tags     = tags
    self.niveau   = 0

  def calculInteret(self):
    if self.parents != [] : 
      self.interet = sum([p.consulterInteret() for p in self.consulterParent()])    

# ========================================================

class Graphe :

  def __init__(self):
    self.noeuds  = {}
    self.arcs    = {}
    self.root    = None
    self.niveaux = []

  def calculerObjetsLesPlusInteressants(self,n=999):
    resultat = sorted(self.niveaux[0], key=self.calculerInteretObjet, reverse=True)

    if(n>len(resultat)):
      return resultat
    else:
      return resultat[:n]
 
  # Méthode qui calcule l'intérêt d'un objet o
  # A modifier selon la méthode utilisée

  def calculerInteretObjet(self, o):
    interet = 0

    interet = random.random()

    return interet

  # Obtenir une référence sur un noeud connaissant son nom
  # ------------------------------------------------------
  def obtenirNoeudConnaissantNom(self,nom):
    return self.noeuds.get(nom, None)

  # Obtenir une liste des références sur les objets dans la taxonomie (niveau 0)
  # ----------------------------------------------------------------------------
  def consulterObjets(self):
    return self.niveaux[0]

  # Obtenir une liste des références sur les tags dans la taxonomie (niveau 1)
  # --------------------------------------------------------------------------
  def consulterTags(self):
    return self.niveaux[1]

  def consulterNiveau(self,i):
    return self.niveaux[i]
    
  # Obtenir un dictionnaire dont les clés sont les noms des noeuds d'un niveau i et les 
  # valeurs associées les degrés d'intérêt pour ces noeuds
  # -----------------------------------------------------------------------------------
  def montrerDoiNiveau(self,i):
    return dict((n.nom,n.doi) for n in self.niveaux[i])

  # Ajoût au graphe d'un noeud appelé nom caractérisé par les données data
  # ---------------------------------------------------------------------- 
  def ajouterNoeud(self, nom, data):
    if not nom in self.noeuds : 
      noeud = Noeud(nom, data, self)
      self.noeuds[noeud.nom] = noeud
      return noeud
    else:
      return self.noeuds[nom]

  # Ajoût au graphe d'un noeud terminal appelé nom caractérisé par les données data
  # -------------------------------------------------------------------------------  
  def ajouterObjet(self, nom, data):
    if not nom in self.noeuds : 
      noeud = Objet(nom, data, self)
      self.noeuds[noeud.nom] = noeud
      return noeud
    else:
      return self.noeuds[nom]

  # Ajoût d'un arc (arête orientée) entre les noeuds référencés par noeud1 et noeud2
  # Cet arc est valué par w
  # --------------------------------------------------------------------------------
  def ajouterArc(self, noeud1, noeud2, w):
    self.arcs[(noeud1.nom, noeud2.nom)] = w 	  
    noeud1.ajouterParent(noeud2)
    noeud2.ajouterEnfant(noeud1)
  
  # Structuration en niveaux du graphe
  # ----------------------------------  
  def calculNiveau(self):
    n = self.root.calculNiveau() + 1
    

    self.niveaux = [[] for i in range(n+1)]
    for noeud in self.noeuds.values() : 
      #print(">>>> ", noeud.nom, " > ", noeud.niveau)
      self.niveaux[noeud.niveau].append(noeud)

  def interetObjets(self):
    pass

  def asynchrone(self,o):
    print("ASYNCHRONE")

    

  def synchrone(self):
    print("SYNCHRONE")

      
  def calculInteretMax(self):
    l = [noeud.interet for noeud in self.noeuds.values()]
    return max(l)
    
  def normalisationInteret(self):
    l = [noeud.interet for noeud in self.noeuds.values()]
    interetMax = max(l)
    for noeud in self.noeuds.values():
      noeud.interet = noeud.interet / doiMax
      
  def calculUpInteret(self):
    pass
        
  def calculDownInteret(self):
    pass
