from flask import Flask, render_template, request, redirect
import sqlite3
from cs50 import SQL

app = Flask(__name__)

db = SQL("sqlite:///database.db")

# Liste des Id 
L=[]
for i in db.execute("SELECT id_bitc FROM bibliothecaire"):
    L.append(*iter(i.values()))

# Les Tables de la base de donnée
components = ["Bibliothecaire", "Stagiaire", "Clients", "Documents"]
# Les attributs de la table "Bibliothecaire".
x = ["ID", "NOM", "PRENOM", "AGE", "QUALIFICATION"]

@app.route("/")
def index():
    return render_template("index.html", component = components)


@app.route("/register", methods=["POST"])
def register():
    if request.form.get("entite") == "Bibliothecaire":
        return redirect("/login_page")
    return "Access Denied!"

@app.route("/login_page")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    id = request.form.get("id")
    name_login = request.form.get("login_name")
    try:
        if not name_login or not id:
            return render_template("alert.html")
        if int(id) in L:
            return redirect("/registrants")
        else:
            # I NEED TO CREATE AN HTML FILE TO ALERT NON BIBLIOTHECAIRE
            return render_template("alert.html")
    except Exception:
        return render_template("alert.html")


@app.route("/bibliothecaire")
def bibliothecaire():
    return render_template("Bibliothecaire.html", biblio=x)

@app.route("/register_2", methods=["POST"])
def register_2():
    # Check Name
    ID = request.form.get("ID")
    if not ID:
        return render_template("error.html", message = "ID Missing")
    elif int(ID) in L:
        return render_template("error.html", message = "ID already Exists")
    
    # Check sport
    name = request.form.get("NOM")
    PRENOM = request.form.get("PRENOM")
    AGE = request.form.get("AGE")
    QUALIF = request.form.get("QUALIFICATION")
    
    # Registrants[name] = sport
    db.execute("INSERT INTO Bibliothecaire (id_bitc, nom_bitc, prenom_bitc, age_bitc, qualif_bitc) VALUES(?, ?, ?, ?, ?)", ID, name, PRENOM, AGE, QUALIF)
    
    return  redirect("/registrants")


@app.route("/registrants")
def registrants():
    registrants = db.execute("SELECT * FROM Bibliothecaire")
    return render_template("registrants.html", registrants=registrants)
    
 
@app.route("/deregister", methods=["POST"])
def deregister():  
    # sourcery skip: use-named-expression
    # Forget registrant
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM Bibliothecaire WHERE id_bitc = ?", id)
    return redirect("/registrants")


@app.route("/querying", methods=["POST"])
def querying():
    query = request.form.get("query")
    try:
        query_x = db.execute(query)
    except Exception:
        return render_template("registrants.html", registrants=[])
    if query_x:
        return render_template("registrants.html", registrants=query_x)
    else:
        return render_template("registrants.html", registrants=[])

if __name__ == "__main__":
    app.run()