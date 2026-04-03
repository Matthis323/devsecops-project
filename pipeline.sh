cat << 'EOF' > pipeline.sh
#!/bin/bash
# Le paramètre -e est crucial en CI : il arrête le script à la moindre erreur
set -e 


echo "--- Étape 1 : BUILD DES IMAGES ---"
echo "Building Backend..."
docker build -t backend-app:latest ./backend/
echo "Building Frontend..."
docker build -t frontend-app:latest ./frontend/

# ---------------------------------------------------------
echo "--- Étape 2 : TESTS ---"
# Test basique : vérifier que l'image a bien été générée et est valide
if docker image inspect backend-app:latest > /dev/null 2>&1; then
    echo "Test Backend: OK (L'image est valide et inspectable)"
else
    echo "Échec du test Backend."
    exit 1
fi

if docker image inspect frontend-app:latest > /dev/null 2>&1; then
    echo "Test Frontend: OK (L'image est valide et inspectable)"
else
    echo "Échec du test Frontend."
    exit 1
fi

# ---------------------------------------------------------
echo "--- Étape 3 : PUSH VERS LE REGISTRY (K3S) ---"
# Comme on n'a pas de Docker Hub, notre "Push" consiste à sauvegarder 
# l'image et l'importer directement dans l'espace de K3s (containerd)
echo "Sauvegarde des images en .tar..."
docker save backend-app:latest > backend.tar
docker save frontend-app:latest > frontend.tar

echo "Importation dans K3s..."
sudo k3s ctr images import backend.tar
sudo k3s ctr images import frontend.tar

# Nettoyage des archives temporaires
rm backend.tar frontend.tar

echo "=== PIPELINE TERMINÉ AVEC SUCCÈS ==="z