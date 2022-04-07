#fjzfhnkjzefkjcnqs
#skdjnkcjsnd
#hdsbckbsdkjbf
#cqhbjsbck

##test

#git init
#git remote add origin https://github.com/SimonBossard/Mongo_DB.git
#git add partie1.py
#git commit -a -m "test"

#git push origin mgaster


from pymongo import MongoClient

db_uri = "mongodb+srv://etudiant:ur2@clusterm1.0rm7t.mongodb.net/"
client = MongoClient(db_uri, tls=True, tlsAllowInvalidCertificates=True)
db = client["publications"]
print(db.list_collection_names())



