async function ajouterFacture() {
    const typeFacture = document.getElementById("typeFacture").value;
    const DateFacture = document.getElementById("DateFacture").value; // La date sera envoyée en tant que chaîne
    const montant = document.getElementById("montant").value;
    const valeur_conso = document.getElementById("valeur_conso").value;
    const id_logements = document.getElementById("id_logements").value;

    // Validation locale pour s'assurer que tous les champs sont remplis
    if (!typeFacture || !DateFacture || !montant || !valeur_conso || !id_logements) {
        alert("Veuillez remplir tous les champs avant de soumettre.");
        return;
    }

    // Préparer les données à envoyer
    const data = {
        typeFacture: typeFacture,
        DateFacture: DateFacture, 
        montant: parseInt(montant),
        valeur_conso: parseInt(valeur_conso),
        id_logements: parseInt(id_logements)
    };

    console.log("Données envoyées :", data);

    try {
        const response = await fetch("http://192.168.1.210:8000/ADDFacturesJson/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert("Facture ajoutée avec succès!");
        } else {
            const errorData = await response.json();
            alert(`Erreur lors de l'ajout de la facture : ${JSON.stringify(errorData.detail)}`);
        }
    } catch (error) {
        console.error("Erreur réseau :", error);
        alert("Erreur réseau ou problème inattendu.");
    }
}
