# Méthodologie de test de l'adaptation du musée virtuel

## Objectif

Démontrer que les procédures mises en œuvre permettent l'adaptation du musée virtuel aux centres d'intérêt d'un visiteur.

## Principe de la méthode

### 1. Simulation de visiteurs avec profils distincts

Créer plusieurs profils de visiteurs ayant des préférences différentes :
- **Visiteur A** : Amateur de portraits
- **Visiteur B** : Amateur de paysages
- **Visiteur C** : Amateur d'art abstrait

### 2. Mesures quantitatives

#### Métrique principale : Taux de pertinence
```
Taux de pertinence = (Nombre de tableaux recommandés correspondant aux préférences / Nombre total de recommandations) × 100
```

#### Métriques secondaires :
- **Évolution de l'intérêt des tags** : Mesurer l'augmentation des tags préférés vs autres tags
- **Diversité** : S'assurer que le système ne recommande pas toujours les mêmes œuvres
- **Vitesse d'adaptation** : Nombre de clics nécessaires pour atteindre 80% de pertinence

### 3. Protocole expérimental

Pour chaque profil de visiteur :

1. **État initial** : Tous les intérêts = 1.0 (système neutre)
2. **Simulation de clics** : 10-15 clics sur des œuvres correspondant aux préférences
3. **Mesure à chaque étape** :
   - Capturer les 10 tableaux les plus recommandés
   - Calculer le taux de pertinence
   - Enregistrer l'intérêt des tags préférés
4. **Comparaison** : État initial vs état final

### 4. Critères de succès

Le système est considéré comme adaptatif si :
- ✅ Le taux de pertinence augmente significativement (>30 points)
- ✅ Les tags préférés voient leur intérêt augmenter
- ✅ Les recommandations évoluent au fil des interactions
- ✅ Différents profils obtiennent des recommandations différentes

## Implémentation

### Script de test : `test_adaptation.py`

Le script fourni permet de :
1. Simuler des scénarios de visite
2. Mesurer automatiquement les métriques
3. Générer des graphiques de visualisation
4. Produire un rapport textuel

### Utilisation

```bash
cd /home/axel/Documents/IEVA_Interface_adaptative/IEVA-Interface_Adaptative/serveur
python test_adaptation.py
```

### Personnalisation

Modifier le script pour :
1. Identifier les tableaux disponibles dans votre collection
2. Définir les scénarios selon vos tags
3. Ajuster les paramètres (tau, sigma, nb_iterations)

## Résultats attendus

### Graphique 1 : Évolution du taux de pertinence
- Courbe ascendante montrant l'amélioration progressive
- Différentes courbes pour différents profils

### Graphique 2 : Évolution de l'intérêt des tags
- Tags préférés : courbe ascendante
- Autres tags : courbe descendante ou stable

### Graphique 3 : Comparaison initial/final
- Barres montrant l'augmentation du taux de pertinence

### Graphique 4 : Gain par scénario
- Comparaison des gains entre profils

## Interprétation des résultats

### Cas de succès
- **Taux initial** : ~10-20% (système neutre, recommandations aléatoires)
- **Taux final** : >70% (système adapté, recommandations pertinentes)
- **Gain** : +50-60 points

### Explication du mécanisme

1. **Clic sur un tableau** → Intérêt +1.0
2. **Propagation bottom-up** → Les tags du tableau gagnent de l'intérêt
3. **Propagation top-down** → Les tableaux similaires gagnent de l'intérêt
4. **Redistribution asynchrone** → Nivellement entre tags
5. **Nivellement synchrone** → Oubli progressif (évite la sur-spécialisation)

### Validation de l'adaptation

Le système s'adapte si :
- Les recommandations changent après les interactions
- Les tableaux recommandés correspondent aux préférences
- Le système généralise (recommande des œuvres similaires, pas identiques)

## Limites et améliorations possibles

### Limites actuelles
- Nécessite plusieurs clics pour s'adapter
- Peut sur-spécialiser si sigma trop faible
- Oublie progressivement avec le temps (sigma)

### Améliorations possibles
1. **Apprentissage plus rapide** : Augmenter le facteur de redistribution top-down
2. **Mémoire à long terme** : Sauvegarder les préférences entre sessions
3. **Détection de changement** : Adapter tau/sigma selon le comportement
4. **Diversité forcée** : Garantir un minimum de variété

## Conclusion

Cette méthodologie permet de **mesurer objectivement** l'adaptation du système aux préférences du visiteur. Les graphiques et métriques fournissent une **preuve quantitative** que le musée virtuel personnalise l'expérience de visite.
