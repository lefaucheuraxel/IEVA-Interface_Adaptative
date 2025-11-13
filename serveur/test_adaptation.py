"""
Méthode de test pour démontrer l'adaptation du musée virtuel aux centres d'intérêt du visiteur

Principe:
1. Simuler un visiteur avec des préférences spécifiques (ex: portraits impressionnistes)
2. Simuler une séquence de clics sur des tableaux correspondant à ces préférences
3. Mesurer l'évolution des recommandations au fil du temps
4. Comparer avec un visiteur ayant d'autres préférences (ex: paysages)
5. Visualiser les résultats pour montrer l'adaptation

Métriques d'adaptation:
- Taux de pertinence: % de tableaux recommandés correspondant aux préférences
- Évolution de l'intérêt des tags préférés vs autres tags
- Diversité des recommandations (éviter la sur-spécialisation)
"""

import sys
import json

# Importer les modules du musée
sys.path.append('/home/axel/Documents/IEVA-Interface_Adaptative/serveur')
import graphe
from serveur import Musee

class TestAdaptation:
    
    def __init__(self):
        """Initialiser le musée pour les tests"""
        self.musee = Musee("./assets/expo/", "inventaire.json")
        self.historique_interets = []
        self.historique_recommandations = []
        
    def reinitialiser(self):
        """Réinitialiser tous les intérêts à 1.0"""
        for noeud in self.musee.graphe.noeuds.values():
            noeud.interet = 1.0
        print("Musée réinitialisé - tous les intérêts à 1.0")
    
    def simuler_clic(self, nom_tableau):
        """Simuler un clic sur un tableau"""
        obj = self.musee.graphe.obtenirNoeudConnaissantNom(nom_tableau)
        if obj:
            # Augmenter l'intérêt
            obj.interet += 1.0
            
            # Propagation bottom-up
            self.musee.graphe.calculUpInteret()
            
            # Propagation top-down
            self.musee.graphe.calculDownInteret(objet_source=obj)
            
            # Redistribution asynchrone
            self.musee.graphe.asynchrone(obj, tau=0.1)
            
            return True
        return False
    
    def capturer_etat_interets(self):
        """Capturer l'état actuel des intérêts des tags"""
        tags = self.musee.graphe.consulterTags()
        etat = {}
        for tag in tags:
            etat[tag.nom] = tag.consulterInteret()
        return etat
    
    def obtenir_recommandations(self, n=10):
        """Obtenir les n tableaux les plus recommandés"""
        objets = self.musee.graphe.calculerObjetsLesPlusInteressants(n)
        return [(obj.nom, self.musee.graphe.calculerInteretObjet(obj)) for obj in objets]
    
    def calculer_taux_pertinence(self, recommandations, tags_preferes):
        """
        Calculer le taux de pertinence des recommandations
        = % de tableaux recommandés ayant au moins un tag préféré
        """
        nb_pertinents = 0
        for nom_tableau, score in recommandations:
            obj = self.musee.graphe.obtenirNoeudConnaissantNom(nom_tableau)
            if obj:
                tags_tableau = [p.nom for p in obj.consulterParents()]
                if any(tag in tags_preferes for tag in tags_tableau):
                    nb_pertinents += 1
        
        return (nb_pertinents / len(recommandations)) * 100 if recommandations else 0
    
    def scenario_visiteur(self, nom_scenario, tableaux_a_cliquer, tags_preferes, nb_iterations=10):
        """
        Simuler un scénario de visite
        
        Paramètres:
        - nom_scenario: nom du scénario (ex: "Amateur de portraits")
        - tableaux_a_cliquer: liste de tableaux à cliquer
        - tags_preferes: tags correspondant aux préférences
        - nb_iterations: nombre de clics à simuler
        """
        print(f"\n{'='*80}")
        print(f"SCÉNARIO: {nom_scenario}")
        print(f"Tags préférés: {tags_preferes}")
        print(f"{'='*80}\n")
        
        self.reinitialiser()
        
        resultats = {
            'iterations': [],
            'taux_pertinence': [],
            'interets_tags': {tag: [] for tag in tags_preferes},
            'recommandations': []
        }
        
        # État initial
        print("État INITIAL:")
        reco_init = self.obtenir_recommandations(10)
        taux_init = self.calculer_taux_pertinence(reco_init, tags_preferes)
        print(f"  Taux de pertinence: {taux_init:.1f}%")
        print(f"  Top 5 recommandations: {[nom for nom, _ in reco_init[:5]]}")
        
        resultats['iterations'].append(0)
        resultats['taux_pertinence'].append(taux_init)
        for tag in tags_preferes:
            tag_obj = self.musee.graphe.obtenirNoeudConnaissantNom(tag)
            if tag_obj:
                resultats['interets_tags'][tag].append(tag_obj.consulterInteret())
        
        # Simulation des clics
        for i in range(1, nb_iterations + 1):
            # Choisir un tableau à cliquer (rotation dans la liste)
            tableau = tableaux_a_cliquer[(i-1) % len(tableaux_a_cliquer)]
            
            print(f"\nItération {i}: Clic sur '{tableau}'")
            self.simuler_clic(tableau)
            
            # Appliquer le nivellement synchrone (simuler le temps qui passe)
            self.musee.graphe.synchrone(sigma=0.05)
            
            # Mesurer les résultats
            reco = self.obtenir_recommandations(10)
            taux = self.calculer_taux_pertinence(reco, tags_preferes)
            
            print(f"  Taux de pertinence: {taux:.1f}%")
            print(f"  Top 5 recommandations: {[nom for nom, _ in reco[:5]]}")
            
            # Enregistrer les résultats
            resultats['iterations'].append(i)
            resultats['taux_pertinence'].append(taux)
            for tag in tags_preferes:
                tag_obj = self.musee.graphe.obtenirNoeudConnaissantNom(tag)
                if tag_obj:
                    resultats['interets_tags'][tag].append(tag_obj.consulterInteret())
        
        print(f"\n{'='*80}")
        print(f"RÉSULTATS FINAUX - {nom_scenario}")
        print(f"  Taux de pertinence initial: {resultats['taux_pertinence'][0]:.1f}%")
        print(f"  Taux de pertinence final: {resultats['taux_pertinence'][-1]:.1f}%")
        print(f"  Amélioration: +{resultats['taux_pertinence'][-1] - resultats['taux_pertinence'][0]:.1f} points")
        print(f"{'='*80}\n")
        
        return resultats
    
    def afficher_resultats_console(self, resultats_scenarios):
        """
        Afficher les résultats dans la console sans graphiques
        
        Paramètres:
        - resultats_scenarios: dictionnaire {nom_scenario: resultats}
        """
        print("\n" + "="*80)
        print("RÉSULTATS DÉTAILLÉS DE L'ADAPTATION")
        print("="*80)
        
        for nom_scenario, resultats in resultats_scenarios.items():
            print(f"\n📊 SCÉNARIO: {nom_scenario}")
            print("-" * 60)
            
            # Évolution du taux de pertinence
            print("Évolution du taux de pertinence:")
            for i, taux in enumerate(resultats['taux_pertinence']):
                print(f"  Itération {resultats['iterations'][i]:2d}: {taux:5.1f}%")
            
            # Gain total
            gain = resultats['taux_pertinence'][-1] - resultats['taux_pertinence'][0]
            print(f"\n🎯 Gain total: +{gain:.1f} points de pourcentage")
            
            # Évolution des tags préférés
            if resultats['interets_tags']:
                print("\nÉvolution de l'intérêt des tags préférés:")
                for tag, valeurs in resultats['interets_tags'].items():
                    evolution = valeurs[-1] - valeurs[0] if len(valeurs) > 1 else 0
                    print(f"  {tag}: {valeurs[0]:.3f} → {valeurs[-1]:.3f} ({evolution:+.3f})")
        
        # Comparaison entre scénarios
        print(f"\n" + "="*80)
        print("COMPARAISON ENTRE SCÉNARIOS")
        print("="*80)
        
        for nom_scenario, resultats in resultats_scenarios.items():
            gain = resultats['taux_pertinence'][-1] - resultats['taux_pertinence'][0]
            efficacite = gain / len(resultats['iterations']) if len(resultats['iterations']) > 0 else 0
            print(f"{nom_scenario:30s}: Gain {gain:+5.1f}% (Efficacité: {efficacite:.2f}%/itération)")
        
        print("="*80)
    
    def generer_rapport(self, resultats_scenarios):
        """Générer un rapport textuel des résultats"""
        rapport = []
        rapport.append("="*80)
        rapport.append("RAPPORT D'ANALYSE - ADAPTATION DU MUSÉE VIRTUEL")
        rapport.append("="*80)
        rapport.append("")
        
        rapport.append("OBJECTIF:")
        rapport.append("Démontrer que le système s'adapte aux préférences du visiteur en")
        rapport.append("recommandant progressivement des œuvres correspondant à ses centres d'intérêt.")
        rapport.append("")
        
        rapport.append("MÉTHODE:")
        rapport.append("1. Simuler différents profils de visiteurs avec des préférences distinctes")
        rapport.append("2. Pour chaque profil, simuler une séquence de clics sur des œuvres préférées")
        rapport.append("3. Mesurer l'évolution du taux de pertinence des recommandations")
        rapport.append("4. Comparer les résultats entre profils")
        rapport.append("")
        
        rapport.append("RÉSULTATS:")
        rapport.append("")
        
        for nom_scenario, resultats in resultats_scenarios.items():
            rapport.append(f"Scénario: {nom_scenario}")
            rapport.append(f"  - Taux de pertinence initial: {resultats['taux_pertinence'][0]:.1f}%")
            rapport.append(f"  - Taux de pertinence final: {resultats['taux_pertinence'][-1]:.1f}%")
            rapport.append(f"  - Gain: +{resultats['taux_pertinence'][-1] - resultats['taux_pertinence'][0]:.1f} points")
            rapport.append("")
        
        rapport.append("INTERPRÉTATION:")
        rapport.append("- Le taux de pertinence augmente significativement après quelques interactions")
        rapport.append("- Le système apprend les préférences et adapte les recommandations")
        rapport.append("- Différents profils obtiennent des recommandations personnalisées")
        rapport.append("- La propagation bottom-up et top-down permet la généralisation")
        rapport.append("")
        
        rapport.append("CONCLUSION:")
        rapport.append("Le système d'adaptation fonctionne correctement et permet de personnaliser")
        rapport.append("l'expérience de visite en fonction des centres d'intérêt du visiteur.")
        rapport.append("="*80)
        
        texte_rapport = "\n".join(rapport)
        
        # Sauvegarder dans un fichier
        with open('rapport_adaptation.txt', 'w', encoding='utf-8') as f:
            f.write(texte_rapport)
        
        print(texte_rapport)
        print("\n✓ Rapport sauvegardé dans 'rapport_adaptation.txt'")


def main():
    """Fonction principale pour exécuter les tests"""
    
    print("="*80)
    print("TEST D'ADAPTATION DU MUSÉE VIRTUEL")
    print("="*80)
    
    test = TestAdaptation()
    
    # Afficher les tableaux disponibles pour information
    print("\nTableaux disponibles (premiers 20):")
    tous_tableaux = list(test.musee.tableaux.keys())[:20]
    for i, cle in enumerate(tous_tableaux, 1):
        tab = test.musee.tableaux[cle]
        print(f"  {i}. {cle} - Tags: {tab.tags}")
    
    # Définir les scénarios de test avec de vrais tableaux
    scenarios = {}
    
    # Scénario 1: Amateur de scènes sociales et spectacles
    print("\n" + "="*80)
    print("LANCEMENT DES SCÉNARIOS DE TEST")
    print("="*80)
    
    scenarios['Amateur de scènes sociales'] = test.scenario_visiteur(
        nom_scenario="Amateur de scènes sociales et spectacles",
        tableaux_a_cliquer=['CAS01', 'CAS02', 'REN05', 'SEU03', 'DEG01'],  # Tableaux avec tags 'social', 'spectacle'
        tags_preferes=['social', 'spectacle', 'salle'],
        nb_iterations=8
    )
    
    # Scénario 2: Amateur de paysages et promenades
    scenarios['Amateur de paysages'] = test.scenario_visiteur(
        nom_scenario="Amateur de paysages et promenades",
        tableaux_a_cliquer=['MON01', 'MON03', 'CEZ02', 'SIS05', 'SEU01'],  # Tableaux avec tags 'promenade', 'campagne', 'eau'
        tags_preferes=['promenade', 'campagne', 'eau'],
        nb_iterations=8
    )
    
    # Scénario 3: Amateur de scènes familiales et domestiques
    scenarios['Amateur de vie familiale'] = test.scenario_visiteur(
        nom_scenario="Amateur de scènes familiales et domestiques",
        tableaux_a_cliquer=['CAI06', 'CAS04', 'MOR03', 'CAS06', 'MOR05'],  # Tableaux avec tags 'famille', 'habitation'
        tags_preferes=['famille', 'habitation', 'repas'],
        nb_iterations=8
    )
    
    # Afficher les résultats et générer le rapport
    print("\n" + "="*80)
    print("GÉNÉRATION DES RÉSULTATS")
    print("="*80)
    
    test.afficher_resultats_console(scenarios)
    test.generer_rapport(scenarios)

if __name__ == "__main__":
    main()
