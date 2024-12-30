-- commandes de destruction des tables
DROP TABLE IF EXISTS Mesures;
DROP TABLE IF EXISTS CapteursActionneurs;
DROP TABLE IF EXISTS Pieces;
DROP TABLE IF EXISTS Factures;
DROP TABLE IF EXISTS TypeCapteurs_Actionneurs;
DROP TABLE IF EXISTS Logements;

-- commandes de creation des tables
CREATE TABLE Logements (id_logements INTEGER PRIMARY KEY ,
                        Adresse TEXT NOT NULL,
						Ville TEXT NOT NULL,
                        NumTel INTEGER,
                        Adresse_IP TEXT,
                        Date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
CREATE TABLE Pieces (id_piece INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_logements INTEGER NOT NULL,
                    nom TEXT NOT NULL,
                    coordonee_X INTEGER,
					coordonee_Y INTEGER,
					coordonee_Z INTEGER,
                    Date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (id_logements) REFERENCES Logements (id_logements)
                    );
CREATE TABLE TypeCapteurs_Actionneurs (typeCapteur INTEGER PRIMARY KEY AUTOINCREMENT,
									   Name TEXT,
                                       unite TEXT,
                                       lower_limit INTEGER,
									   upper_limit INTEGER
                                       );								   
CREATE TABLE CapteursActionneurs (id_capteur INTEGER PRIMARY KEY AUTOINCREMENT,
                                   id_piece INTEGER ,
								   typeCapteur INTEGER ,
                                   RefCom INTEGER,
                                   RefPiece INTEGER,
                                   portCom INTEGER,
                                   Date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                   FOREIGN KEY (id_piece) REFERENCES Pieces (id_piece),
								   FOREIGN KEY (typeCapteur) REFERENCES TypeCapteurs_Actionneurs (typeCapteur)
                                   );
CREATE TABLE Mesures (id_mesure INTEGER PRIMARY KEY AUTOINCREMENT,
                      id_capteur INTEGER,
                      valeur INTEGER,
                      Date_insertion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY(id_capteur) REFERENCES CapteursActionneurs(id_capteur)
                      );



-- insertion de données
INSERT INTO Logements (Adresse,NumTel,Adresse_IP,Ville) VALUES ("6 Avenue ","0626875077", "11.11.11.11","Paris");

INSERT INTO Pieces(nom,coordonee_X,coordonee_Y,coordonee_Z,id_logements) VALUES
    ( "Cuisine", 5,3,2 , (SELECT id_logements from Logements WHERE id_logements=1 ) ),
    ( "SDM", 12,0,4 , (SELECT id_logements from Logements WHERE id_logements=1 ) ),
    ( "SAM", 1,9,0 , (SELECT id_logements from Logements WHERE id_logements=1 ) ),
    ( "Chambre", 1,3,2 , (SELECT id_logements from Logements WHERE id_logements=1 ) );

INSERT INTO TypeCapteurs_Actionneurs(Name,unite,lower_limit,upper_limit) VALUES("DHT22","°",-10,100  )	;

	
INSERT INTO CapteursActionneurs(RefCom,RefPiece,portCom,id_piece,typeCapteur) VALUES
    ( 250,10,8080, (SELECT id_piece from Pieces WHERE id_piece=2 ),(SELECT typeCapteur from TypeCapteurs_Actionneurs WHERE typeCapteur=1 )),
	( 12,80,8080, (SELECT id_piece from Pieces WHERE id_piece=2 ),(SELECT typeCapteur from TypeCapteurs_Actionneurs WHERE typeCapteur=1 ));
	
INSERT INTO Mesures(valeur,id_capteur) VALUES
	(30,(SELECT id_capteur from CapteursActionneurs WHERE id_capteur=1 )),
	(33,(SELECT id_capteur from CapteursActionneurs WHERE id_capteur=1 )),
	(5,(SELECT id_capteur from CapteursActionneurs WHERE id_capteur=2 )),
	(3,(SELECT id_capteur from CapteursActionneurs WHERE id_capteur=2 ));
	
INSERT INTO Factures(typeFacture, DateFacture, montant, valeur_conso, id_logements) 
VALUES
    ("ELEC", "2023-12-01", 400, 3500, (SELECT id_logements FROM Logements WHERE id_logements = 1)),
    ("EAU", "2023-06-22", 130, 15000, (SELECT id_logements FROM Logements WHERE id_logements = 1)),
    ("GAZ", "2023-11-06", 630, 2901, (SELECT id_logements FROM Logements WHERE id_logements = 1)),
    ("ELEC", "2024-01-08", 435, 3400, (SELECT id_logements FROM Logements WHERE id_logements = 1));


