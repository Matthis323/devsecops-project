FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Variables d'environnement par défaut (seront surchargées par K8s)
ENV DB_HOST=postgres-service
ENV DB_PORT=5432
ENV DB_NAME=devsecops
ENV DB_USER=admin
ENV DB_PASSWORD=password123

EXPOSE 5001

CMD ["python", "app.py"]
