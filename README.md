# Préparation de données et entraînement d'un modèle de recommandation

## Contexte
Un exercice de développement du pipeline d'entraînement d'un modèle de recommandation, à partir de fichiers `.json` contenant une liste d'utilisateurs et leurs avis à propos de différents films.

## Prérequis
Il faudra télécharger les fichiers `.json`, et installer/configurer MongoDB.

### Fichiers de données
- [Liste de films](http://camillepradel.fr/teaching/nosql/movielens_export/movielens_movies.json)
- [Liste des utilisateurs](http://camillepradel.fr/teaching/nosql/movielens_export/movielens_users.json)

### Installation de MongoDB
1 / Mise à jour du système
```bash
sudo apt update
sudo apt upgrade -y
```
2 / Import de la clé GPG MongoDB
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
```
3 / Création du repo MongoDB
```bash
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
```
Dans cette ligne de commande, remplacez `focal` par :
- `bionic` si vous utilisez Ubuntu 18.04
- `focal` pour Ubuntu 20.04
- `jammy` pour Ubuntu 22.04<br>

La commande ci-dessous vous permettra de connaître version Ubuntu que vous utilisez.
 ```bash
 lsb_release -a
```
4 / Mise à jour de la liste de packages
```bash
sudo apt update
```
5 / Installation de MongoDB
```bash
sudo apt install -y mongodb-org
```
6 / Démarrage de MongoDB
```bash
sudo systemctl start mongod
```

### Installation de MongoDB Compass (GUI)
Si vous souhaitez visualiser graphiquement votre base MongoDB, vous pouvez utiliser Compass. L'outil est téléchargeable [ici](https://www.mongodb.com/try/download/compass).

## Structure du projet
```bash
project/
│
├── functions/
│   ├── cleaning.py                 # Nettoyage, filtrage des données
│   ├── database.py                 # Connexion à Mongo, import des données
│   ├── evaluation.py               # Évaluation du modèle
│   └── model_processing.py         # Entraînement du modèle
│
├── .gitignore
├── notebook.ipynb                  # Pipeline complet, des données à l'évaluation
├── README.md
└── requirements.txt                # Dépendances à installer
```

## Procédure
0 / Installation des dépendances
```bash
pip install -r requirements.txt
```
1 / Démarrage de MongoDB
```bash
sudo systemctl start mongod
```
2 / Création de la database `Movielens`<br>

3 / Création des collections `Movies` et `Users`<br>

4 / Import des `.json` dans leur collection respective<br>

5 / Exécution du pipeline à travers le `notebook.ipynb`