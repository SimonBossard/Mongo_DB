
#git init
#git remote add origin https://github.com/SimonBossard/Mongo_DB.git
#git add partie1.py
#git commit -a -m "test"

#git push origin mgaster


from pickle import FALSE, TRUE
from pymongo import MongoClient

db_uri = "mongodb+srv://etudiant:ur2@clusterm1.0rm7t.mongodb.net/"
client = MongoClient(db_uri, tls=True, tlsAllowInvalidCertificates=True)
db = client["publications"]
print(db.list_collection_names())

coll = db["hal_irisa_2021"]
##etape1
 # en mongo db : recup des 20 plus grands auteurs en récupérant pour chaque auteur la liste de ses publications

 #lien code couleur pour nombres d'article des noeuds
 #lien entre auteurs pour les arêtes (co-publication)

#epaisseur des arêtes en fonction du nombre proportionnel de publications communes

#les 20 auteurs avec le plus de publications
top20 = list(
    db.hal_irisa_2021.aggregate([
                        {"$unwind": "$authors"},
                        {"$group": {"_id": {"name" :"$authors.name", "firstname" :"$authors.firstname" }   ,
                        "nb": {"$sum":1}
                        }},
                        {"$sort": {"nb": -1}},
                         {"$limit": 20}
                      ])
)

#liste des noms
liste_noms = []
for i in range(0,len(top20)) :
    dict = top20[i]
    liste_noms.append(top20[i]["_id"]['name'])

#liste des prenoms
liste_prenoms = []
for i in range(0,len(top20)) :
    dict = top20[i]
    liste_prenoms.append(top20[i]["_id"]['firstname'])



#récupérer liste des publications des 20 plus grands auteurs
liste_titre = []
noms = []
prenoms = []
for x,y in zip(liste_noms, liste_prenoms):
    auteur =list(db.hal_irisa_2021.find({"authors.name" : x,"authors.firstname" : y}))
    for i in auteur:
        liste_titre.append(i['title'])
        prenoms.append(y)
        noms.append(x)




