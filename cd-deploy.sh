#!/bin/bash
set -e

echo "=== 🚀 DÉMARRAGE DU DÉPLOIEMENT CONTINU (CD) ==="

# 1. On s'assure d'avoir la dernière version des manifests depuis Git
echo "📥 Récupération des dernières configurations (Git Pull)..."
git pull origin main

# 2. Application des manifests Kubernetes
echo "🔄 Mise à jour du cluster K3s..."
sudo kubectl apply -f k8s/postgres-deployment.yaml
sudo kubectl apply -f k8s/backend-deployment.yaml
sudo kubectl apply -f k8s/frontend-deployment.yaml

echo "✅ Déploiement terminé. Vérification de l'état des Pods :"
sudo kubectl get pods
