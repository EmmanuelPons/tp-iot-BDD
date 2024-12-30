async function ajouterCapteur() {
    const id_piece = document.getElementById("id_piece").value;
    const typeCapteur = document.getElementById("typeCapteur").value;
    const refCom = document.getElementById("refCom").value;
    const refPiece = document.getElementById("refPiece").value;
    const portCom = document.getElementById("portCom").value;

    // Validation locale : vérifier que tous les champs requis sont remplis
    if (!id_piece || !typeCapteur || !refCom || !refPiece || !portCom) {
        alert("Veuillez remplir tous les champs avant de soumettre.");
        return;
    }

    // Préparer les données à envoyer
    const data = {
        id_piece: parseInt(id_piece),
        typeCapteur: parseInt(typeCapteur),
        RefCom: parseInt(refCom),
        RefPiece: parseInt(refPiece),
        portCom: parseInt(portCom)
    };

    console.log("Données envoyées :", data);

    try {
        const response = await fetch("http://192.168.1.210:8000/ADDCapteursActionneursJson/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert("Capteur ajouté avec succès!");
        } else {
            const errorData = await response.json();
            alert(`Erreur lors de l'ajout du capteur : ${JSON.stringify(errorData.detail)}`);
        }
    } catch (error) {
        console.error("Erreur réseau :", error);
        alert("Erreur réseau ou problème inattendu.");
    }
}
