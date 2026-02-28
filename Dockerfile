FROM python:3.11-slim

WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code source
COPY . .

# Exposer le port pour le serveur de santé (utilisé par Koyeb pour vérifier que le bot tourne)
EXPOSE 8080

# Lancer le bot (assure-toi que ton fichier principal s'appelle bien bot.py)
CMD ["python", "bot.py"]
