import sqlite3
import random

# ouverture/initialisation de la base de donnee 
conn = sqlite3.connect('logement.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

# A completer...
c.execute('SELECT * FROM Factures WHERE typeFacture = \'ELEC\';')
# insertion d'une donnee
#c.execute("INSERT INTO Logements(Adresse,NumTel,Adresse_IP) VALUES ('6 RUE ','0626875077', '22.22.22.22')")


# insertion de plusieurs donnees 
valuesMesures = []
for i in range(3):
	valuesMesures.append((1,random.randint(1,100)))
c.executemany('INSERT INTO Mesures (id_capteur,valeur) VALUES (?,?)', valuesMesures)

valuesFactures = []
for i in range(3):
	valuesFactures.append(("ELEC","%d/11/2024"%(random.randint(1,30)),random.randint(400,1500),random.randint(100,300),1))
c.executemany('INSERT INTO Factures (typeFacture,DateFacture,montant,valeur_conso,id_logements) VALUES (?,?,?,?,?)', valuesFactures)



# fermeture
conn.commit()
conn.close()