
FROM python:3.9-slim

# Répertoire de travail
WORKDIR /app

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY app.py .

# Variables d'environnement par défaut
ENV BACKEND_URL=http://backend-service:5001
ENV LOG_LEVEL=DEBUG

# Exposer le port
EXPOSE 5000

# Lancement (en root — Phase 1 volontairement non durci)
CMD ["python", "app.py"]
