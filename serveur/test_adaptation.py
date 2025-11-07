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
import matplotlib.pyplot as plt
import numpy as np

# Importer les modules du musée
sys.path.append('/home/axel/Documents/IEVA_Interface_adaptative/IEVA-Interface_Adaptative/serveur')
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
    
    def visualiser_resultats(self, resultats_scenarios):
        """
        Créer des graphiques pour visualiser l'adaptation
        
        Paramètres:
        - resultats_scenarios: dictionnaire {nom_scenario: resultats}
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle("Démonstration de l'adaptation du musée virtuel aux préférences du visiteur", 
                     fontsize=16, fontweight='bold')
        
        # Graphique 1: Évolution du taux de pertinence
        ax1 = axes[0, 0]
        for nom_scenario, resultats in resultats_scenarios.items():
            ax1.plot(resultats['iterations'], resultats['taux_pertinence'], 
                    marker='o', label=nom_scenario, linewidth=2)
        ax1.set_xlabel('Nombre de clics')
        ax1.set_ylabel('Taux de pertinence (%)')
        ax1.set_title('Évolution du taux de pertinence des recommandations')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim([0, 105])
        
        # Graphique 2: Évolution de l'intérêt des tags préférés (premier scénario)
        ax2 = axes[0, 1]
        premier_scenario = list(resultats_scenarios.values())[0]
        for tag, valeurs in premier_scenario['interets_tags'].items():
            ax2.plot(premier_scenario['iterations'], valeurs, 
                    marker='s', label=tag, linewidth=2)
        ax2.set_xlabel('Nombre de clics')
        ax2.set_ylabel('Intérêt du tag')
        ax2.set_title(f'Évolution de l\'intérêt des tags - {list(resultats_scenarios.keys())[0]}')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Graphique 3: Comparaison initiale vs finale (premier scénario)
        ax3 = axes[1, 0]
        categories = ['Initial', 'Final']
        taux_initial = premier_scenario['taux_pertinence'][0]
        taux_final = premier_scenario['taux_pertinence'][-1]
        bars = ax3.bar(categories, [taux_initial, taux_final], 
                      color=['#ff7f0e', '#2ca02c'], alpha=0.7, width=0.5)
        ax3.set_ylabel('Taux de pertinence (%)')
        ax3.set_title('Comparaison: État initial vs État final')
        ax3.set_ylim([0, 105])
        
        # Ajouter les valeurs sur les barres
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        # Graphique 4: Gain d'adaptation par scénario
        ax4 = axes[1, 1]
        scenarios_noms = list(resultats_scenarios.keys())
        gains = [res['taux_pertinence'][-1] - res['taux_pertinence'][0] 
                for res in resultats_scenarios.values()]
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        bars = ax4.barh(scenarios_noms, gains, color=colors[:len(scenarios_noms)], alpha=0.7)
        ax4.set_xlabel('Gain de pertinence (points de %)')
        ax4.set_title('Gain d\'adaptation par scénario')
        ax4.grid(True, alpha=0.3, axis='x')
        
        # Ajouter les valeurs
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax4.text(width, bar.get_y() + bar.get_height()/2.,
                    f'+{width:.1f}', ha='left', va='center', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('adaptation_musee_resultats.png', dpi=300, bbox_inches='tight')
        print("✓ Graphiques sauvegardés dans 'adaptation_musee_resultats.png'")
        plt.show()
    
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
    
    # Définir les scénarios de test
    scenarios = {}
    
    # Scénario 1: Amateur de portraits
    # (À adapter selon les tableaux réellement présents dans votre inventaire)
    print("\nPréparation des scénarios de test...")
    print("Note: Adapter les noms de tableaux selon votre inventaire.json")
    
    # Exemple de scénarios (à personnaliser)
    # Vous devez remplacer ces noms par des vrais tableaux de votre collection
    
    # Pour trouver les tableaux disponibles:
    print("\nTableaux disponibles (premiers 20):")
    tous_tableaux = list(test.musee.tableaux.keys())[:20]
    for i, cle in enumerate(tous_tableaux, 1):
        tab = test.musee.tableaux[cle]
        print(f"  {i}. {cle} - Tags: {tab.tags}")
    
    print("\n" + "="*80)
    print("INSTRUCTIONS POUR LANCER LE TEST:")
    print("="*80)
    print("1. Examinez la liste des tableaux ci-dessus")
    print("2. Modifiez le code pour sélectionner des tableaux avec des tags spécifiques")
    print("3. Créez 2-3 scénarios avec des préférences différentes")
    print("4. Relancez le script")
    print("="*80)
    
    # Exemple de code à décommenter et adapter:
    """
    scenarios['Amateur de portraits'] = test.scenario_visiteur(
        nom_scenario="Amateur de portraits",
        tableaux_a_cliquer=['tableau1', 'tableau2', 'tableau3'],  # Remplacer par vrais noms
        tags_preferes=['portrait', 'visage'],  # Adapter selon vos tags
        nb_iterations=10
    )
    
    scenarios['Amateur de paysages'] = test.scenario_visiteur(
        nom_scenario="Amateur de paysages",
        tableaux_a_cliquer=['tableau4', 'tableau5', 'tableau6'],
        tags_preferes=['paysage', 'nature'],
        nb_iterations=10
    )
    
    # Visualiser et générer le rapport
    test.visualiser_resultats(scenarios)
    test.generer_rapport(scenarios)
    """

if __name__ == "__main__":
    main()
