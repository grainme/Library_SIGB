from flask import Flask, render_template, request, redirect
import sqlite3
from cs50 import SQL

app = Flask(__name__)


# Creating a connection to the database.
db = SQL("sqlite:///database.db")

# Liste des Id de Bibliothecaires
ids_bibliothecaire=[]
for i in db.execute("SELECT id_bitc FROM bibliothecaire"):
    ids_bibliothecaire.append(*iter(i.values()))
    
    
# Liste des Id d' editeurs
ids_editeurs=[]
for i in db.execute("SELECT id_editeur FROM Editeur"):
    ids_editeurs.append(*iter(i.values()))

# Liste des Id d' editeurs
ids_documents=[]
for i in db.execute("SELECT id_ref FROM Document"):
    ids_documents.append(*iter(i.values()))
print(ids_documents)
    
ids_livres=[]
for i in db.execute("SELECT code_ISBN FROM Livre"):
    ids_documents.append(*iter(i.values()))

# Les Tables de la base de donnée
components = ["Bibliothecaire", "Stagiaire", "Clients", "Documents"]
# Les attributs de la table "Bibliothecaire".
biblio_attributes = ["ID", "NOM", "PRENOM", "AGE", "GRADE"]
# A list of the attributes of the table "Document"
docs_attributes = ["ID", "TITRE", "ANNEE_PUB", "EDITEUR", "NOMBRE EXEMPLAIRE"]

livre_attributes = ["ISBN", "ID DOCUMENT"]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/home")
def index():
    return render_template("index.html", component = components)


# Bilbiothecaire CODE

@app.route("/register", methods=["POST"])
def register():
    if request.form.get("entite") == "Bibliothecaire":
        return redirect("/registrants")
    return "Access Denied!"

@app.route("/login_page", methods=["POST"])
def login_page():
    return render_template("login.html", biblio=biblio_attributes)

@app.route("/login", methods=["POST"])
def login():
    id = request.form.get("id")
    name_login = request.form.get("login_name")
    try:
        if not name_login or not id:
            return render_template("alert.html")
        if int(id) in ids_bibliothecaire:
            return redirect("/home")
        else:
            # I NEED TO CREATE AN HTML FILE TO ALERT NON BIBLIOTHECAIRE
            return """    <script>
        alert("NAME or ID missing!")
    </script>"""
    except Exception:
        return """    <script>
        alert("NAME or ID missing!")
    </script>"""

@app.route("/register_2", methods=["POST"])
def register_2():
    
    ID = request.form.get("ID")
    if not ID:
        return render_template("error.html", message = "ID Missing")
    elif int(ID) in ids_bibliothecaire:
        return render_template("error.html", message = "ID already Exists")
    
    name = request.form.get("NOM")
    PRENOM = request.form.get("PRENOM")
    AGE = request.form.get("AGE")
    GRADE = request.form.get("GRADE")
    
    db.execute("""INSERT INTO Bibliothecaire (id_bitc, nom_bitc, prenom_bitc, age_bitc, grade) 
               VALUES(?, ?, ?, ?, ?)""", ID, name, PRENOM, AGE, GRADE)
    return  redirect("/home")


@app.route("/registrants")
def registrants():
    registrants = db.execute("SELECT * FROM Bibliothecaire")
    return render_template("registrants.html", registrants=registrants)

 
@app.route("/deregister", methods=["POST"])
def deregister():    # sourcery skip: use-named-expression
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM Bibliothecaire WHERE id_bitc = ?", id)
    return redirect("/registrants")

@app.route("/add_element", methods=["POST"])
def add_element():                                                               
    return redirect("/login_page")

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
    
# DOCUMENT CODE    
@app.route("/docs")
def documents():
    docs = db.execute("SELECT * FROM Document")
    return render_template("documents.html", dox = docs)

@app.route("/doc_reg", methods=["POST"])
def doc_reg():
    return render_template("docs_reg.html", docum=docs_attributes )

@app.route("/register_3", methods=["POST"])
def register_3():
    ID = request.form.get("ID")
    titre = request.form.get("TITRE")
    an_pub = request.form.get("ANNEE_PUB")
    editeur = request.form.get("EDITEUR")
    nbr_exemp = request.form.get("NOMBRE EXEMPLAIRE")
    if not ID:
        return render_template("error.html", message = "ID Missing")
    elif int(ID) in ids_documents:
        return render_template("error.html", message = "ID already Exists")

    db.execute("INSERT INTO Document (id_ref, an_pub, titre_doc, id_editeur,nbr_exemp ) VALUES(?, ?, ?, ?)", 
               ID , an_pub, titre, editeur, nbr_exemp)
    
    return  redirect("/docs")

@app.route("/deregister_2", methods=["POST"])
def deregister_2():    # sourcery skip: use-named-expression
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM Document WHERE id_ref = ?", id)
    return redirect("/docs")

@app.route("/querying_2", methods=["POST"])
def querying_2():
    query = request.form.get("query")
    try:
        query_x = db.execute(query)
    except Exception:
        return render_template("documents.html", dox=[])
    if query_x:
        return render_template("documents.html", dox=query_x)
    else:
        return render_template("documents.html", dox=[])

# LIVRE CODE    
@app.route("/livre", methods=["POST"])
def livre():
    livres = db.execute("SELECT * FROM Livre")
    return render_template("livre.html", books = livres)

@app.route("/livre_reg", methods=["POST"])
def livre_reg():
    return render_template("livre_reg.html", livree=livre_attributes )

@app.route("/register_4", methods=["POST"])
def register_4():
    ISBN = request.form.get("ISBN")
    ID_doc = request.form.get("ID DOCUMENT")
    if not ISBN:
        return render_template("error.html", message = "ID Missing")
    elif int(ISBN) in ids_livres:
        return render_template("error.html", message = "ID already Exists")

    db.execute("INSERT INTO Livre (code_ISBN, id_ref) VALUES(?, ?)", ISBN,ID_doc)
    
    return  redirect("/livre")

@app.route("/deregister_3", methods=["POST"])
def deregister_3():    # sourcery skip: use-named-expression
    id = request.form.get("ISBN")
    if id:
        db.execute("DELETE FROM Livre WHERE code_ISBN = ?", id)
    return redirect("/livre")

@app.route("/querying_3", methods=["POST"])
def querying_3():
    query = request.form.get("query")
    try:
        query_x = db.execute(query)
    except Exception:
        return render_template("livre.html", books=[])
    if query_x:
        return render_template("livre.html", books=query_x)
    else:
        return render_template("livre.html", books=[])

# CODE EMPRUNT

# A list of the attributes of the table "Emprunt"
emprunt_attributs = ["Date Debut", "Date Fin", "ID Exemplaire", "ID EMPRUNTEUR"]

@app.route("/emprunts")
def emprunt():
    emprunts_ = db.execute("SELECT * FROM EMPRUNT")
    return render_template("emprunts.html",emp_att = emprunt_attributs, emp_vals = emprunts_)

@app.route("/emprunt_reg", methods=["POST"])
def emprunt_reg():
    return render_template("emprunt_reg.html", empp=emprunt_attributs )

@app.route("/register_5", methods=["POST"])
def register_5():
    dt_debut = request.form.get("Date Debut")
    dt_fin = request.form.get("Date Fin")
    id_exemplaire = request.form.get("ID Exemplaire")
    id_emprunteur = request.form.get("ID EMPRUNTEUR")

    db.execute("""INSERT INTO EMPRUNT (Date_debut, Date_fin, id_exemp, id_emp) 
               VALUES(?, ?, ?, ?)""", dt_debut, dt_fin, id_exemplaire, id_emprunteur)
    
    return  redirect("/emprunts")

if __name__ == "__main__":
    app.run(debug=True)