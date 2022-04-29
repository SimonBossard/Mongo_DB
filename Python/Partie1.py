
#git init
#git remote add origin https://github.com/SimonBossard/Mongo_DB.git
#git add partie1.py
#git commit -a -m "test"

#git push origin mgaster



from pickle import FALSE, TRUE
from pymongo import MongoClient
import pandas as pd 
import networkx as nx 

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
top20
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

#on regroupe nom et prénoms
prenom_nom = []
for i in range(0, len(noms)):
    prenom_nom.append(prenoms[i] +"_"+  noms[i])




#on mets toutes les informations necassaires dans un dataframe
data = {'prenom_nom':prenom_nom, 
        'titre':liste_titre } 
  
df = pd.DataFrame(data) 


grouped_df = df.groupby('titre').size()


liste_commun = []
for i in range(0, len(df)-1):
    for j in range(i+1,len(df)) :
        if (df['titre'][i] == df['titre'][j]) :
            liste = []
            liste.append(df['prenom_nom'][i])
            liste.append(df['prenom_nom'][j])
            liste_commun.append(liste)




#compter nombre de liens
data_lien = {'lien':liste_commun}
data_lien = pd.DataFrame(data_lien) 
data_lien.sum()

nb_liens = []
lien_vu = []
for i in range(0,len(data_lien)-1):
    cpt =0
    if data_lien["lien"][i] not in lien_vu :
        cpt += 1
        lien_vu.append(data_lien["lien"][i])
        for j in range(i+1,len(data_lien)):
            if (data_lien["lien"][i] == data_lien["lien"][j]):
                cpt += 1
    if cpt != 0 :   
        nb_liens.append(cpt)
    


print(nb_liens)




#Partie graph




from matplotlib.pyplot import *
figure(figsize=(10,5))
G = nx.Graph()
H = nx.Graph()
H.add_nodes_from(prenom_nom)
G.add_edges_from(liste_commun )
I = nx.compose(H,G)


#couleur pour le nombre d'article



#on recupere nombre publications :
nombre_publi = []
for i in range(0,len(top20)) :
    nombre_publi.append(top20[i]['nb'])

#on donne une couleur  correspondant à chaue nombre de publication
node_color = []
for i in range(0,len(nombre_publi)) :
    if nombre_publi[i]>20 :
        node_color.append('red')
    elif 16>nombre_publi[i]>12 :
        node_color.append("orange")
    elif 13>nombre_publi[i]>10 :
        node_color.append("yellow")
    else :
        node_color.append("green")

nx.draw(I,with_labels= True, width=nb_liens, node_color = node_color,font_size = 7)



import matplotlib.pyplot as plt
figure(figsize=(25,10))
pos = nx.spring_layout(I,k=0.25,iterations=5,scale = 0.2)
nx.draw(I,pos ,with_labels= True, width=nb_liens, node_color = node_color,font_size = 29,node_size = 550)

plt.savefig("graph.png")

