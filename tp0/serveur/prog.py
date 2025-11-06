

import json

data = {}
with open("base.json","r") as f : 
  data = json.load(f)
 
print(data)
tableaux = data["tableaux"]
for cle in tableaux : 
  print(tableaux[cle])
        
