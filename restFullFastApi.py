from fastapi import FastAPI, Request, HTTPException
import requests
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel,Field
import sqlite3
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from datetime import datetime

templates = Jinja2Templates(directory="templates")

API_KEY = "9ec328ae612f1fb0e362a02951134dfc"
BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

class Mesure(BaseModel):
    valeur: int
    id_capteur: int

class Facture(BaseModel):
    typeFacture: str
    DateFacture: str = Field(..., pattern=r"\d{4}-\d{2}-\d{2}")  
    montant: int
    valeur_conso: int
    id_logements: int

class CapteurActionneur(BaseModel):
    RefCom: int
    RefPiece: int
    portCom: int
    id_piece: int
    typeCapteur: int

def get_db_connection():
    conn = sqlite3.connect('logement.db')
    conn.row_factory = sqlite3.Row
    return conn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")




def get_adresses():

    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("SELECT id_logements ,Adresse, Ville FROM logements;")  
    result = c.fetchall()  
    conn.close()
    
    return [{"id_log": row[0], "adresse": row[1], "ville": row[2]} for row in result]


def get_pieces(id_log):

    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("SELECT id_piece, nom FROM Pieces WHERE id_logements = ?",(id_log,))  
    result = c.fetchall()  
    conn.close()
    
    return [{"id_piece": row[0], "nom": row[1],"id_log" : id_log } for row in result]

def get_capteur(id_piece):

    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute("SELECT id_capteur,id_piece, typeCapteur FROM CapteursActionneurs WHERE id_piece = ?",(id_piece,))  
    capteurs = c.fetchall()  
    
    result = []

    result.append({
            "id_piece": id_piece,
        })
   
    for capteur in capteurs:
        id_capteur, id_piece, typeCapteur = capteur

        
        c.execute("SELECT name,unite FROM TypeCapteurs_Actionneurs WHERE typeCapteur = ?", (typeCapteur,))
        type_capteur = c.fetchone()
        type_capteur_nom = type_capteur[0] if type_capteur else "Type inconnu"
        Unite = type_capteur[1]
        
        c.execute("""SELECT valeur FROM Mesures WHERE id_capteur = ? ORDER BY Date_insertion DESC LIMIT 1""", (id_capteur,))
        last_value = c.fetchone()
        last_value = last_value[0] if last_value else "Pas de valeurs associé"

        
        result.append({
            "id_capteur": id_capteur,
            "id_piece": id_piece,
            "typeCapteur": type_capteur_nom,
            "last_value": last_value,
            "unite": Unite
        })
    

    conn.close()
    return result

def get_mesure(id_capteur):

    conn = get_db_connection()
    c = conn.cursor()

   
    c.execute("SELECT typeCapteur FROM CapteursActionneurs WHERE id_capteur = ?",(id_capteur,))
    typeCapteur = c.fetchone()
    typeCapteur = typeCapteur[0]

    print(f"typeCapteur: {typeCapteur}")

    
    c.execute("SELECT name, unite FROM TypeCapteurs_Actionneurs WHERE typeCapteur = ?", (typeCapteur,))
    type_capteur = c.fetchone()

    
    type_capteur_nom = type_capteur[0] if type_capteur else "Type inconnu"
    Unite = type_capteur[1] if type_capteur else "Unité inconnue"

    
    c.execute("SELECT valeur, Date_insertion FROM Mesures WHERE id_capteur = ?",(id_capteur,))  
    result = c.fetchall()  

    conn.close()
    
    return [{"valeur": row[0], "Date_insertion": row[1], "id_log": id_capteur, "Unite": Unite, "Type": type_capteur_nom } for row in result]


@app.post("/ADDlogements/")
async def ajouter_logement(Adresse : str,Ville : str ,NumTel : int, Adresse_IP: str):

    #connection à la BDD
    conn = get_db_connection()
    c = conn.cursor()

    #ajout du logement à la BDD
    c.execute('INSERT INTO Logements(Adresse,NumTel,Adresse_IP,Ville) VALUES(?,?,?,?)',(Adresse, NumTel, Adresse_IP,Ville))
    conn.commit()
    conn.close()


@app.post("/ADDPieces/")
async def ajouter_Pieces(Nom : str, c_X : int,c_Y : int,c_Z : int, Id_log: int):

    #connection à la BDD
    conn = get_db_connection()
    c = conn.cursor()

    #ajout du logement à la BDD
    c.execute('INSERT INTO Pieces(nom,coordonee_X,coordonee_Y,coordonee_Z,id_logements) VALUES(?,?,?,?,?)',(Nom, c_X, c_Y,c_Z,Id_log))
    conn.commit()
    conn.close()

@app.post("/ADDTypeCapteurs/")
async def ajouter_types(Nom : str, unite : str ,lower_limit : int,upper_limit : int):

    #connection à la BDD
    conn = get_db_connection()
    c = conn.cursor()

    #ajout du logement à la BDD
    c.execute('INSERT INTO TypeCapteurs_Actionneurs(Name,unite,lower_limit,upper_limit) VALUES(?,?,?,?)',(Nom, unite, lower_limit,upper_limit))
    conn.commit()
    conn.close()

@app.post("/ADDCapteursActionneurs/")
async def ajouter_types(RefCom : int,RefPiece : int,portCom :int,id_piece :int, typeCapteur :int ):

    #connection à la BDD
    conn = get_db_connection()
    c = conn.cursor()

    #ajout du logement à la BDD
    c.execute('INSERT INTO CapteursActionneurs(RefCom,RefPiece,portCom,id_piece,typeCapteur) VALUES(?,?,?,?,?)',(RefCom, RefPiece, portCom,id_piece,typeCapteur))
    conn.commit()
    conn.close()

@app.post("/ADDCapteursActionneursJson/")
async def ajouter_types(capteur_actionneur: CapteurActionneur):

    # Connexion à la BDD
    conn = get_db_connection()
    c = conn.cursor()
    
    c.execute(
        '''
        INSERT INTO CapteursActionneurs
        (RefCom, RefPiece, portCom, id_piece, typeCapteur)
        VALUES (?, ?, ?, ?, ?)
        ''',
        (
            capteur_actionneur.RefCom,
            capteur_actionneur.RefPiece,
            capteur_actionneur.portCom,
            capteur_actionneur.id_piece,
            capteur_actionneur.typeCapteur
        )
    )

    conn.commit()
    conn.close()

    return {"message": "Capteur ajouté avec succès"}

@app.post("/ADDMesures/")
async def ajouter_types(valeur : int,id_capteur : int):

    #connection à la BDD
    conn = get_db_connection()
    c = conn.cursor()

    #ajout du logement à la BDD
    c.execute('INSERT INTO Mesures(valeur,id_capteur) VALUES(?,?)',(valeur, id_capteur))
    conn.commit()
    conn.close()

@app.post("/ADDMesuresJson/")
async def ajouter_mesures(mesure: Mesure):
    # Extraire les données de la requête
    valeur = mesure.valeur
    id_capteur = mesure.id_capteur

    # Connexion à la base de données
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO Mesures (valeur, id_capteur) VALUES (?, ?)", (valeur, id_capteur))
        conn.commit()
        conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'insertion : {e}")

    return {"message": "Données ajoutées avec succès"}

@app.post("/ADDFactures/")
async def ajouter_types(typeFacture : str,DateFacture : str,montant :int, valeur_conso :int,id_logements:int):

    try:
        # Convertir la chaîne en objet datetime pour vérifier le format
        datetime.strptime(DateFacture, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="DateFacture must be in format YYYY-MM-DD")
    
    # Connexion à la base de données
    conn = get_db_connection()
    c = conn.cursor()

    try:
        # Ajout de la facture à la base de données
        c.execute(
            '''
            INSERT INTO Factures (typeFacture, DateFacture, montant, valeur_conso, id_logements) 
            VALUES (?, ?, ?, ?, ?)
            ''',
            (typeFacture, DateFacture, montant, valeur_conso, id_logements)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

    return {"message": "Facture ajoutée avec succès"}

@app.post("/ADDFacturesJson/")
async def ajouter_facture(facture: Facture):

    # Validation explicite de la date
    try:
        datetime.strptime(facture.DateFacture, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="DateFacture must be in format YYYY-MM-DD")

    # Connexion à la base de données
    conn = get_db_connection()
    c = conn.cursor()

    try:
        # Ajout de la facture à la base de données
        c.execute(
            '''
            INSERT INTO Factures (typeFacture, DateFacture, montant, valeur_conso, id_logements) 
            VALUES (?, ?, ?, ?, ?)
            ''',
            (facture.typeFacture, facture.DateFacture, facture.montant, facture.valeur_conso, facture.id_logements)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

    return {"message": "Facture ajoutée avec succès"}

from datetime import datetime, timedelta

@app.get("/Camem/{id_log}")
async def read_item(request: Request, id_log: int):
    conn = get_db_connection()
    c = conn.cursor()

    # Répartition actuelle
    montantElec = 0
    montantGaz = 0
    montantEau = 0
    montantAutre = 0
    for raw in c.execute("SELECT montant FROM Factures WHERE typeFacture = 'ELEC' AND id_logements = ?", (id_log,)):
        montantElec += raw["montant"]
    for raw in c.execute("SELECT montant FROM Factures WHERE typeFacture = 'GAZ' AND id_logements = ?", (id_log,)):
        montantGaz += raw["montant"]
    for raw in c.execute("SELECT montant FROM Factures WHERE typeFacture = 'EAU' AND id_logements = ?", (id_log,)):
        montantEau += raw["montant"]
    for raw in c.execute("SELECT montant FROM Factures WHERE typeFacture = 'AUTRE' AND id_logements = ?", (id_log,)):
        montantAutre += raw["montant"]

    # Factures des 3 derniers mois
    today = datetime.today()
    three_months_ago = today - timedelta(days=90)
    montantElecMois = c.execute(
        "SELECT SUM(montant) as montant FROM Factures WHERE typeFacture = 'ELEC' AND id_logements = ? AND DateFacture >= ?",
        (id_log, three_months_ago),
    ).fetchone()["montant"] or 0
    montantGazMois = c.execute(
        "SELECT SUM(montant) as montant FROM Factures WHERE typeFacture = 'GAZ' AND id_logements = ? AND DateFacture >= ?",
        (id_log, three_months_ago),
    ).fetchone()["montant"] or 0
    montantEauMois = c.execute(
        "SELECT SUM(montant) as montant FROM Factures WHERE typeFacture = 'EAU' AND id_logements = ? AND DateFacture >= ?",
        (id_log, three_months_ago),
    ).fetchone()["montant"] or 0
    montantAutreMois = c.execute(
        "SELECT SUM(montant) as montant FROM Factures WHERE typeFacture = 'AUTRE' AND id_logements = ? AND DateFacture >= ?",
        (id_log, three_months_ago),
    ).fetchone()["montant"] or 0

    # Factures des 2 dernières années
    current_year = today.year
    montantElecAnne = c.execute(
        "SELECT SUM(montant) as montant FROM Factures WHERE typeFacture = 'ELEC' AND id_logements = ? AND strftime('%Y', DateFacture) IN (?, ?)",
        (id_log, str(current_year - 1), str(current_year)),
    ).fetchone()["montant"] or 0
    montantGazAnne = c.execute(
        "SELECT SUM(montant) as montant FROM Factures WHERE typeFacture = 'GAZ' AND id_logements = ? AND strftime('%Y', DateFacture) IN (?, ?)",
        (id_log, str(current_year - 1), str(current_year)),
    ).fetchone()["montant"] or 0
    montantEauAnne = c.execute(
        "SELECT SUM(montant) as montant FROM Factures WHERE typeFacture = 'EAU' AND id_logements = ? AND strftime('%Y', DateFacture) IN (?, ?)",
        (id_log, str(current_year - 1), str(current_year)),
    ).fetchone()["montant"] or 0
    montantAutreAnne = c.execute(
        "SELECT SUM(montant) as montant FROM Factures WHERE typeFacture = 'AUTRE' AND id_logements = ? AND strftime('%Y', DateFacture) IN (?, ?)",
        (id_log, str(current_year - 1), str(current_year)),
    ).fetchone()["montant"] or 0

    conn.close()

    # Préparation des données pour les graphiques
    data = [
        {'ELEC': montantElec, 'GAZ': montantGaz, 'EAU': montantEau, 'AUTRE': montantAutre, 'id_log': id_log},
        {'ELECMOIS': montantElecMois, 'GAZMOIS': montantGazMois, 'EAUMOIS': montantEauMois, 'AUTREMOIS': montantAutreMois},
        {'ELECANNE': montantElecAnne, 'GAZANNE': montantGazAnne, 'EAUANNE': montantEauAnne, 'AUTREANNE': montantAutreAnne},
    ]

    print(data)

    return templates.TemplateResponse(
        request=request,
        name="camembert2.html",
        context={"data": data}
    )


@app.get("/meteo/{id_log}")
async def read_item(id_log):
    conn = get_db_connection()
    c = conn.cursor()

    params = {
        "q": c.execute("SELECT Ville FROM Logements WHERE id_logements = ?",id_log) ,
        "appid": API_KEY,
        "units": "metric",
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        conn.commit()
        conn.close()
        
        forecast = {}
        for item in data.get("list", []):
            date = item["dt_txt"].split(" ")[0]  
            if date not in forecast:
                forecast[date] = []
            forecast[date].append({
                "time": item["dt_txt"].split(" ")[1],
                "temperature": item["main"]["temp"],
                "description": item["weather"][0]["description"],
            })

        return {
            "city": data["city"]["name"],
            "country": data["city"]["country"],
            "forecast": forecast,
        }

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Error fetching weather data")
    except KeyError as e:
        raise HTTPException(status_code=404, detail="City not found or invalid response format")


@app.get("/accueil/")
async def read_item(request: Request):

    adresse_logements = get_adresses()

    return templates.TemplateResponse(
        "acccueil.html", {"request": request, "logements": adresse_logements}
    )

@app.get("/logement/{id_log}")
async def read_item(request: Request,id_log):

    affichage_piece = get_pieces(id_log)
    print(affichage_piece)

    return templates.TemplateResponse(
        "logement.html", {"request": request, "Pieces": affichage_piece}
    )

@app.get("/piece/{id_piece}")
async def read_item(request: Request,id_piece):

    affichage_capteurs = get_capteur(id_piece)
    print(affichage_capteurs)
    return templates.TemplateResponse(
        "capteurs.html", {"request": request, "Capteurs": affichage_capteurs}
    )

@app.get("/capteur/{id_capteur}")
async def read_item(request: Request,id_capteur):

    affichage_mesures = get_mesure(id_capteur)
    return templates.TemplateResponse(
        "graphe.html", {"request": request, "Mesures": affichage_mesures}
    )

@app.get("/ajouterfacture/{id_log}", response_class=HTMLResponse)
async def afficher_ajouter_facture(request: Request,id_log):
    return templates.TemplateResponse("ajoutFactures.html", {"request": request, "id_log":id_log })

@app.get("/ajouterCapteur/{id_piece}", response_class=HTMLResponse)
async def afficher_ajouter_facture(request: Request,id_piece):
    return templates.TemplateResponse("AjoutCapteur.html", {"request": request, "id_piece":id_piece})



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.1.210", port=8000)