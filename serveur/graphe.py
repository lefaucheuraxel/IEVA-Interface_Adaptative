import random
# salut
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
    parents = self.consulterParents()
    if(len(parents) == 0):
      return
    # Diviser l'intérêt par le nombre de parents pour éviter la sur-pondération
    # des concepts qui ont beaucoup d'enfants
    dInteretParent = dInteret / len(parents)
    for parent in parents:
      parent.ajouterInteret(dInteretParent)

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
      print(self.niveau)
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
  # L'intérêt d'un objet = somme des intérêts de ses parents (tags/concepts) + intérêt propre
  def calculerInteretObjet(self, o):
    # Intérêt propre de l'objet (si cliqué directement)
    interet_propre = o.consulterInteret()
    
    # Somme des intérêts de tous les parents (tags/concepts)
    interet_parents = sum([p.consulterInteret() for p in o.consulterParents()])
    
    # Score total
    interet_total = interet_propre + interet_parents
    
    print("INTERET : ", interet_total," (propre:", interet_propre, "+ parents:", interet_parents, ") | ", o.nom)
    return interet_total

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

  def asynchrone(self, o, tau=0.1):
    """
    Redistribue l'intérêt suite à une interaction avec l'objet o.
    Augmente l'intérêt des tags liés à o (V+(o)) et diminue celui des autres
    pour garder la quantité totale d'intérêt constante.
    
    Paramètres:
    - o: objet (tableau) avec lequel le visiteur a interagi
    - tau: paramètre ∈ [0,1] qui contrôle l'intensité de la redistribution
    
    Formules:
    - C = Σ(w∈Ks) τ*I(w)  : quantité totale d'intérêt à redistribuer
    - R = C / |V+(o)|      : quantité d'intérêt ajoutée à chaque tag de o
    - ΔI(w) = R - τ*I(w)   si w ∈ V+(o) (tags de o)
    - ΔI(w) = -τ*I(w)      sinon (autres tags)
    """
    print(f"\n=== ASYNCHRONE: Redistribution de l'intérêt (tau={tau}) ===")
    
    # Ks : ensemble de tous les tags (niveau 1 du graphe)
    Ks = self.consulterTags()
    
    # V+(o) : ensemble des tags (parents) liés à l'objet o
    V_plus_o = o.consulterParents()
    V_plus_o_noms = set([tag.nom for tag in V_plus_o])
    
    print(f"Objet: {o.nom}")
    print(f"Tags de l'objet: {V_plus_o_noms}")
    print(f"Nombre total de tags: {len(Ks)}")
    
    # Calcul de C : quantité totale d'intérêt à redistribuer
    C = sum([tau * tag.consulterInteret() for tag in Ks])
    
    # Calcul de R : quantité ajoutée à chaque tag de V+(o)
    if len(V_plus_o) > 0:
      R = C / len(V_plus_o)
    else:
      R = 0
      print("ATTENTION: Objet sans tags!")
      return
    
    print(f"C (intérêt total à redistribuer): {C:.4f}")
    print(f"R (intérêt par tag de l'objet): {R:.4f}")
    
    # Application des variations d'intérêt
    print("\nVariations d'intérêt:")
    for tag in Ks:
      interet_avant = tag.consulterInteret()
      
      if tag.nom in V_plus_o_noms:
        # Tag lié à l'objet : ΔI(w) = R - τ*I(w)
        delta_I = R - tau * interet_avant
      else:
        # Autre tag : ΔI(w) = -τ*I(w)
        delta_I = -tau * interet_avant
      
      # Appliquer la variation (sans utiliser ajouterInteret pour éviter la propagation)
      tag.interet += delta_I
      
      # Éviter les valeurs négatives
      if tag.interet < 0:
        tag.interet = 0
      
      if abs(delta_I) > 0.01:  # Afficher seulement les variations significatives
        print(f"  {tag.nom}: {interet_avant:.4f} -> {tag.consulterInteret():.4f} (Δ={delta_I:+.4f})")
    
    print("=== FIN ASYNCHRONE ===\n")

    

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
