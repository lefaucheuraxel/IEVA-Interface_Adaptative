# Guide de test de l'adaptation du musée virtuel

## Vue d'ensemble

Ce guide explique comment démontrer que le système s'adapte aux centres d'intérêt du visiteur.

## Fichiers créés

### 1. `test_adaptation.py`
Script Python pour simuler des visiteurs et mesurer l'adaptation.

**Fonctionnalités :**
- Simulation de clics sur des tableaux
- Mesure du taux de pertinence des recommandations
- Génération de graphiques de visualisation
- Rapport textuel des résultats

### 2. `METHODOLOGIE_TEST.md`
Documentation détaillée de la méthodologie de test.

### 3. Route API `/stats`
Nouvelle route dans le serveur pour obtenir des statistiques en temps réel.

## Méthodes de test

### Méthode 1 : Test automatisé (Recommandé)

#### Étape 1 : Identifier les tableaux disponibles

```bash
cd /home/axel/Documents/IEVA_Interface_adaptative/IEVA-Interface_Adaptative/serveur
python test_adaptation.py
```

Le script affichera les 20 premiers tableaux avec leurs tags.

#### Étape 2 : Personnaliser les scénarios

Modifier `test_adaptation.py` (fonction `main()`) :

```python
# Exemple : Amateur de portraits
scenarios['Amateur de portraits'] = test.scenario_visiteur(
    nom_scenario="Amateur de portraits",
    tableaux_a_cliquer=['monet_01', 'manet_03', 'renoir_05'],  # Vos tableaux
    tags_preferes=['portrait', 'impressionnisme'],  # Vos tags
    nb_iterations=10
)

# Exemple : Amateur de paysages
scenarios['Amateur de paysages'] = test.scenario_visiteur(
    nom_scenario="Amateur de paysages",
    tableaux_a_cliquer=['monet_10', 'sisley_02', 'pissarro_07'],
    tags_preferes=['paysage', 'nature'],
    nb_iterations=10
)
```

#### Étape 3 : Lancer le test complet

```python
# Décommenter dans main() :
test.visualiser_resultats(scenarios)
test.generer_rapport(scenarios)
```

#### Résultats générés :
- `adaptation_musee_resultats.png` : Graphiques de visualisation
- `rapport_adaptation.txt` : Rapport textuel

### Méthode 2 : Test manuel via l'interface web

#### Étape 1 : Lancer le serveur

```bash
cd /home/axel/Documents/IEVA_Interface_adaptative/IEVA-Interface_Adaptative/serveur
python serveur.py
```

#### Étape 2 : Consulter les statistiques initiales

Ouvrir dans un navigateur :
```
http://127.0.0.1:5000/stats
```

Vous verrez :
- Tags les plus intéressants (tous à 1.0 initialement)
- Top 10 des tableaux recommandés (aléatoire initialement)
- Statistiques globales

#### Étape 3 : Utiliser l'interface 3D

1. Ouvrir le client web
2. Cliquer sur 5-10 tableaux ayant des tags similaires (ex: tous des portraits)
3. Changer de salle

#### Étape 4 : Vérifier l'adaptation

Recharger `http://127.0.0.1:5000/stats`

**Observations attendues :**
- Les tags des tableaux cliqués ont un intérêt > 1.0
- Les tableaux recommandés ont ces tags
- L'écart-type augmente (différenciation)

### Méthode 3 : Test via logs console

#### Observer les logs du serveur

Chaque clic affiche :
```
============================================================
INTERACTION avec le tableau: monet_01
Tags associés: ['portrait', 'impressionnisme']
============================================================

--- Propagation BOTTOM-UP ---
Intérêts propagés vers les concepts parents

--- Propagation TOP-DOWN ---
Intérêts redistribués vers les objets similaires

--- Redistribution asynchrone ---
...
```

Chaque tic-tac (10s) affiche :
```
============================================================
TIC-TAC à t=120.00s (sigma=0.05)
============================================================
Status: Nivellement effectué
Intérêt moyen: 1.2500
...
```

## Interprétation des résultats

### Indicateurs de succès

#### 1. Taux de pertinence
- **Initial** : ~10-20% (système neutre)
- **Après 5 clics** : ~50-60%
- **Après 10 clics** : >70%

#### 2. Intérêt des tags
- **Tags préférés** : 1.0 → 2.5-3.0
- **Autres tags** : 1.0 → 0.7-0.9

#### 3. Recommandations
- **Avant** : Tableaux variés, sans lien
- **Après** : Tableaux partageant les tags préférés

### Exemple de résultat attendu

**Scénario : Amateur de portraits impressionnistes**

| Métrique | Initial | Après 10 clics | Gain |
|----------|---------|----------------|------|
| Taux de pertinence | 15% | 85% | +70 points |
| Intérêt "portrait" | 1.0 | 2.8 | +1.8 |
| Intérêt "impressionnisme" | 1.0 | 2.5 | +1.5 |
| Intérêt "paysage" | 1.0 | 0.8 | -0.2 |

**Interprétation :**
- ✅ Le système a appris les préférences
- ✅ Les recommandations sont personnalisées
- ✅ L'adaptation est significative

## Paramètres ajustables

### Dans `graphe.py`

```python
# Propagation top-down (ligne 375)
facteur_redistribution = 0.1  # Plus élevé = adaptation plus rapide

# Méthode asynchrone (serveur.py ligne 464)
musee.graphe.asynchrone(obj, tau=0.1)  # Plus élevé = oubli plus rapide

# Méthode synchrone (serveur.py ligne 277)
musee.graphe.synchrone(sigma=0.05)  # Plus élevé = nivellement plus rapide
```

### Impact des paramètres

| Paramètre | Valeur basse | Valeur haute |
|-----------|--------------|--------------|
| `facteur_redistribution` | Adaptation lente | Adaptation rapide |
| `tau` | Mémoire longue | Mémoire courte |
| `sigma` | Spécialisation | Diversité |

## Troubleshooting

### Problème : Pas d'adaptation visible
- Vérifier que les tableaux cliqués ont des tags communs
- Augmenter `facteur_redistribution` à 0.2-0.3
- Réduire `sigma` à 0.01-0.02

### Problème : Adaptation trop rapide
- Réduire `facteur_redistribution` à 0.05
- Augmenter `sigma` à 0.1

### Problème : Recommandations trop homogènes
- Augmenter `sigma` pour plus de diversité
- Réduire `tau` pour garder plus d'historique

## Conclusion

Ces méthodes permettent de **prouver objectivement** que le musée virtuel s'adapte aux préférences du visiteur. Les graphiques et métriques fournissent une **démonstration quantitative** de l'adaptation.

**Recommandation :** Utiliser la méthode automatisée pour des résultats reproductibles et documentés.
