
import json

def process(nomCSV):

    res = {"peintres":[], "tableaux":{}}
    with open(nomCSV,"r") as f : 
        for ligne in f :
            listeMots = ligne.split(';')

            id = listeMots[0]
            nom = listeMots[1]
            peintre = listeMots[2]
            annee = listeMots[3]
            hauteur = int(listeMots[4])
            largeur = int(listeMots[5][0:-1])
            
            res["tableaux"][id] = [id,peintre,nom,annee,hauteur,largeur,[]]
    
    peintres = set()  
    for attr in list(res["tableaux"].values()) : 
        peintres.add(attr[1])
    res["peintres"] = list(peintres)
    return res
            
            

            
        
res = process('expo.csv')

with open("inventaire.json","w") as f : 
  json.dump(res,f,ensure_ascii=False)


