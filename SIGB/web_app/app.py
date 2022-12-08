from flask import Flask, render_template, request, redirect
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
    
# A list of the ISBN of the books in the database.
ids_livres=[]
for i in db.execute("SELECT code_ISBN FROM Livre"):
    ids_livres.append(*iter(i.values()))
    
ids_clients=[]
for i in db.execute("SELECT id_emp FROM Emprunteur"):
    ids_clients.append(*iter(i.values()))


# Les Tables de la base de donnée
components = ["Bibliothecaire", "Stagiaire", "Clients", "Documents"]
# Les attributs de la table "Bibliothecaire".
biblio_attributes = ["ID", "NOM", "PRENOM", "AGE", "GRADE"]
# A list of the attributes of the table "Document"
docs_attributes = ["ID", "TITRE", "ANNEE_PUB", "EDITEUR", "NOMBRE EXEMPLAIRE"]
# A list of the attributes of the table "Livre"
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


    db.execute("INSERT INTO Document (id_ref, an_pub, titre_doc, id_editeur,nbr_exemp ) VALUES(?, ?, ?, ?, ?)", 
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
@app.route("/livre", methods=['POST', 'GET'])
def livre():
    livres = db.execute("SELECT * FROM Livre")
    return render_template("livre.html", books = livres)

@app.route("/livre_reg", methods=['POST', 'GET'])
def livre_reg():
    return render_template("livre_reg.html", livree=livre_attributes )

@app.route("/register_4", methods=['POST', 'GET'])
def register_4():
    ISBN = request.form.get("ISBN")
    ID_doc = request.form.get("ID DOCUMENT")
    if not ISBN:
        return render_template("error.html", message = "ID Missing")

    db.execute("INSERT INTO Livre (code_ISBN, id_ref) VALUES(?, ?)", ISBN,ID_doc)
    
    return render_template("livre.html")

@app.route("/deregister_3", methods=['POST', 'GET'])
def deregister_3():    # sourcery skip: use-named-expression
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM Livre WHERE code_ISBN = ?", id)
    return redirect("/livre")

@app.route("/querying_3", methods=['POST', 'GET'])
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

# CODE CLIENTS
clts_attributes = ["ID", "NOM", "PRENOM", "TELEPHONE", "EMAIL", "VILLE", "CATEGORIE"]

@app.route("/Clients")
def clients():
    clts_ = db.execute("SELECT * FROM Emprunteur")
    
    return render_template("clients.html", clients = clts_)

@app.route("/client_reg", methods=["POST"])
def client_reg():
    return render_template("clients_reg.html", clt_att=clts_attributes )

@app.route("/register_6", methods=["POST"])
def register_6():
    
    id = request.form.get("ID")
    nom = request.form.get("NOM")
    prenom = request.form.get("PRENOM")
    tele = request.form.get("TELEPHONE")
    mail = request.form.get("EMAIL")
    ville = request.form.get("VILLE")
    cat = request.form.get("CATEGORIE")
    
    if not id:
        return render_template("error.html", message = "ID Missing")

    db.execute("""INSERT INTO Emprunteur (id_emp, nom_emp, prenom_emp, tele_emp, email_emp,
               ville_emp, ctg_emp) VALUES(?, ?, ?, ?, ?, ?, ?)""",
               id, nom, prenom, tele, mail, ville, cat)
    
    return  redirect("/Clients")

@app.route("/deregister_4", methods=["POST"])
def deregister_4():    # sourcery skip: use-named-expression
    id = request.form.get("id")
    if id:
        db.execute("PRAGMA foreign_keys = OFF")
        db.execute("DELETE FROM Emprunteur WHERE id_emp = ?", id)
        db.execute(f"UPDATE Emprunteur SET id_emp = id_emp - 1 WHERE id_emp>{id}")
    return redirect("/Clients")

@app.route("/querying_4", methods=["POST"])
def querying_4():
    query = request.form.get("query")
    try:
        query_x = db.execute(query)
    except Exception:
        return render_template("clients.html", clients=[])
    if query_x:
        return render_template("clients.html", clients=query_x)
    else:
        return render_template("clients.html", clients=[])

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

# CODE EXEMPLAIRE
vars = ["id", "n_ord", "dt_achat", "etat", "id_emp", "id_rayon", "id_ref"]
# A list of the attributes of the table "Exemplaire".
exemp_att = ["ID","Num Ordre", "Date Achat", "Etat", "ID Emprunteur", "ID Rayon", "ID Document"]

@app.route("/exemplaires")
def exemplaires():
    exemps = db.execute("SELECT * FROM Exemplaire")
    return render_template("exemplaire.html", exemp = exemps)

@app.route("/exemp_reg", methods=["POST"])
def exemp_reg():
    return render_template("exemp_reg.html",exp_att = exemp_att)

@app.route("/register_7", methods=["POST"])
def register_7():
    for cnt in range(len(vars)):
        vars[cnt] =  request.form.get(exemp_att[cnt])
        
    if not id:
        return render_template("error.html", message = "ID Missing")

    db.execute("""INSERT INTO Exemplaire (id_exemp, num_ord, date_acht, etat_exemp, id_emp,
               id_rayon, id_ref) VALUES(?, ?, ?, ?, ?, ?, ?)""",
               vars[0], vars[1], vars[2], vars[3], vars[4], vars[5], vars[6])
    
    return  redirect("/exemplaires")


if __name__ == "__main__":
    app.run(debug=True)