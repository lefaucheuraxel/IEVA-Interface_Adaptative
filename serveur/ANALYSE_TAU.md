# Analyse du paramètre τ (tau) dans la redistribution d'intérêt

## Formules mathématiques

Lorsqu'un visiteur interagit avec un objet `o`, la redistribution de l'intérêt suit ces règles :

- **C** = Σ(w∈Ks) τ·I(w) : quantité totale d'intérêt à redistribuer
- **R** = C / |V+(o)| : quantité d'intérêt ajoutée à chaque tag de l'objet
- **ΔI(w)** = R - τ·I(w) si w ∈ V+(o) (tags liés à l'objet)
- **ΔI(w)** = -τ·I(w) sinon (autres tags)

Où :
- `Ks` = ensemble de tous les tags
- `V+(o)` = ensemble des tags (parents) liés à l'objet o
- `τ ∈ [0,1]` = paramètre de redistribution

## Influence du paramètre τ

### τ proche de 0 (ex: τ = 0.01)
**Redistribution faible et progressive**

- **Avantages** :
  - Changements très graduels dans les préférences
  - Historique des interactions préservé plus longtemps
  - Stabilité du système de recommandation
  - Moins sensible aux clics accidentels

- **Inconvénients** :
  - Adaptation lente aux nouveaux intérêts du visiteur
  - Nécessite beaucoup d'interactions pour observer un changement
  - Peut ne pas refléter un changement soudain de préférence

- **Cas d'usage** :
  - Visiteurs qui explorent méthodiquement
  - Musées avec beaucoup d'œuvres similaires
  - Quand on veut éviter les recommandations trop volatiles

### τ = 0.1 (valeur par défaut recommandée)
**Équilibre entre réactivité et stabilité**

- **Caractéristiques** :
  - 10% de l'intérêt total est redistribué à chaque interaction
  - Adaptation modérée aux nouvelles préférences
  - Bon compromis pour la plupart des cas d'usage

- **Comportement** :
  - Les tags de l'objet cliqué gagnent : R - 0.1·I(w)
  - Les autres tags perdent : -0.1·I(w)
  - Après ~10 interactions, les préférences sont significativement modifiées

### τ proche de 0.5
**Redistribution forte et réactive**

- **Avantages** :
  - Adaptation rapide aux nouveaux intérêts
  - Système très réactif aux dernières interactions
  - Recommandations qui changent rapidement

- **Inconvénients** :
  - Peut "oublier" rapidement les préférences antérieures
  - Sensible aux clics accidentels
  - Recommandations potentiellement instables

- **Cas d'usage** :
  - Visiteurs qui changent souvent d'intérêt
  - Sessions courtes où il faut s'adapter vite
  - Exploration exploratoire plutôt que méthodique

### τ proche de 1 (ex: τ = 0.9)
**Redistribution très agressive (déconseillé)**

- **Comportement** :
  - Presque tout l'intérêt est redistribué à chaque clic
  - Les préférences passées sont quasi effacées
  - Seules les dernières interactions comptent

- **Problèmes** :
  - Perte totale de l'historique
  - Recommandations très volatiles
  - Peut créer des boucles (recommander toujours la même chose)

## Conservation de l'intérêt total

Le système garantit que **la quantité totale d'intérêt reste constante** :

```
Σ(avant) I(w) = Σ(après) I(w)
```

Preuve :
- Intérêt retiré des autres tags : τ · Σ(w∉V+(o)) I(w)
- Intérêt retiré des tags de o : τ · Σ(w∈V+(o)) I(w)
- Total retiré : C = τ · Σ(w∈Ks) I(w)
- Total ajouté aux tags de o : |V+(o)| · R = |V+(o)| · (C / |V+(o)|) = C

## Recommandations pratiques

| Type de visite | τ recommandé | Justification |
|----------------|--------------|---------------|
| Visite guidée méthodique | 0.05 - 0.1 | Préserver l'historique |
| Visite libre standard | 0.1 - 0.2 | Équilibre réactivité/stabilité |
| Exploration rapide | 0.2 - 0.3 | Adaptation rapide |
| Session courte | 0.3 - 0.4 | Maximiser la réactivité |

## Expérimentation

Pour tester différentes valeurs de τ, modifier dans `serveur.py` ligne 419 :

```python
musee.graphe.asynchrone(obj, tau=0.1)  # Changer la valeur ici
```

Ou ajouter un paramètre dans l'URL :
```python
tau = request.args.get('Tau', default=0.1, type=float)
musee.graphe.asynchrone(obj, tau=tau)
```

## Visualisation de l'effet de τ

Exemple avec 3 tags (A, B, C) ayant chacun I=1.0, et interaction avec objet ayant tag A :

| τ | C | R | ΔI(A) | ΔI(B) | ΔI(C) | I(A) après | I(B) après | I(C) après |
|---|---|---|-------|-------|-------|------------|------------|------------|
| 0.1 | 0.3 | 0.3 | +0.2 | -0.1 | -0.1 | 1.2 | 0.9 | 0.9 |
| 0.3 | 0.9 | 0.9 | +0.6 | -0.3 | -0.3 | 1.6 | 0.7 | 0.7 |
| 0.5 | 1.5 | 1.5 | +1.0 | -0.5 | -0.5 | 2.0 | 0.5 | 0.5 |

On observe que plus τ est grand, plus la différenciation entre les tags est forte.
