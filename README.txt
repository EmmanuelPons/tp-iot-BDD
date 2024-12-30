Pour lancer le serveur sans collecter de data de l'ESP il suffit de lancer la commande suivante :
-fastapi dev restFullFastApi.py

Ensuite il faut aller à l'adresse http://127.0.0.1:8000/accueil/
On peut ensuite naviguer sur le site et intéragir avec la base de donnée

Si on veut collecter des data de l'esp il faut utiliser la commande 
-python3 restFullFastApi.py

Ensuite il faut modifer dans le code l'adresse ip à la ligne 471 et mettre l'adresse ip du pc
Puis on peut se connecter sur le site à l'adresse de votre pc par ex si l'adresse est 192.168.1.210
il faut aller à l'adresse http://192.168.1.210:8000/accueil/
ensute il faut aussi adapté le code de l'esp pour qu'il se connecte sur le même WiFi que sur lequelle est connecter le pc
Une fois le code adapté l'esp va envoyé les données sur le capteur avec l'id 1 & 2 les valeur d'humidité et de température. Via un Json

Sur le site il est possible d'ajouter des factures et des capteurs à la BDD il est cependent impossible d'en supprimer. Il est possible d'ajouter des logements et des pièces uniqument via http://127.0.0.1:8000/docs/
Le code HTML, Javascript et CSS on été en grande partie généra grâce à ChatGPT