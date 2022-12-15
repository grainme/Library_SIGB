from flask import Flask, render_template, request, redirect
from cs50 import SQL

app = Flask(__name__)


# Creating a connection to the database.
db = SQL("sqlite:///database.db")

Bibliothecaires = db.execute("SELECT * FROM Bibliothecaire")
    
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
# A list of the attributes of the table "Periodique"
periodique_attributes = ["ISSN", "VOLUME", "NUMERO", "ID DOCUMENT"]

@app.route("/")
def root():
    return render_template("home.html")


@app.route("/login_page", methods=["POST"])
def login_page():
    return render_template("login.html", biblio=biblio_attributes)

# Bilbiothecaire CODE
@app.route("/register", methods=["POST"])
def register():
    if request.form.get("entite") == "Bibliothecaire":
        return redirect("/registrants")
    return "Access Denied!"


@app.route("/login", methods=["GET","POST"])
def login():
    id_ = request.form.get("id")
    name_login = request.form.get("login_name")
    if not name_login or not id_ or int(id_) not in ids_bibliothecaire:
        return render_template("alert.html")
    imgs = ["avatar_1.png", "avatar_2.png", "avatar_3.png"]

    return render_template("index.html",
                           name = Bibliothecaires[int(id_)-1]["nom_bitc"],
                           prenom = Bibliothecaires[int(id_)-1]["prenom_bitc"],
                           age = Bibliothecaires[int(id_)-1]["age_bitc"],
                           grade = Bibliothecaires[int(id_)-1]["grade"],
                           img = imgs[int(id_)-1] )


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
        db.execute(f"UPDATE Bibliothecaire SET id_bitc = id_bitc - 1 WHERE id_bitc>{id}")

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

@app.route("/deregister_2", methods=["GET","POST"])
def deregister_2():    # sourcery skip: use-named-expression
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM Exemplaire WHERE id_ref = ?", id)
        db.execute("DELETE FROM Document WHERE id_ref = ?", id)
        db.execute(f"UPDATE Document SET id_ref = id_ref - 1 WHERE id_ref>{id}")

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

    db.execute("""INSERT INTO Emprunteur (id_emp, nom_emp, prenom_emp,
               tele_emp, email_emp, ville_emp, ctg_emp) VALUES(?, ?, ?, ?, ?, ?, ?)"""
               , id, nom, prenom, tele, mail, ville, cat)
    
    return  redirect("/Clients")

@app.route("/deregister_4", methods=["POST"])
def deregister_4():    
    id = request.form.get("id")
    query_x = f"DELETE FROM Emprunteur WHERE id_emp = {id}"
    print(query_x)
    if id:
        db.execute("DELETE FROM EMPRUNT WHERE id_emp = ?", id)
        db.execute(query_x)
        db.execute(f"UPDATE Emprunteur SET id_emp = id_emp - 1 WHERE id_emp>{id}")

    return redirect("/Clients")

@app.route("/querying_4", methods=["POST"])
def querying_4():
    query = request.form.get("query")
    query_x = db.execute(query)
    if query_x:
        return render_template("clients.html", clients=query_x)
    else:
        return render_template("clients.html", clients=[])

# CODE EMPRUNT

# A list of the attributes of the table "Emprunt"
emprunt_attributs = ["Date Debut", "Date Fin", "ID Exemplaire", "ID EMPRUNTEUR" ]

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

    # Inserting the values of the variables dt_debut, dt_fin, id_exemplaire, id_emprunteur into the
    # table EMPRUNT.
    db.execute("""INSERT INTO EMPRUNT (Date_debut, Date_fin, id_exemp, id_emp) VALUES(?, ?, ?, ?)""",
               dt_debut, dt_fin, id_exemplaire, id_emprunteur)
    
    db.execute("UPDATE EXEMPLAIRE SET pres_type='EN PRET' WHERE id_exemp = ?", id_exemplaire)
    
    return  redirect("/emprunts") 

@app.route("/deregister_5", methods=["POST"])
def deregister_5():
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM Emprunt WHERE Emprunt.id_exemp=?",id)
        db.execute("UPDATE EXEMPLAIRE SET pres_type='EN RAYON' WHERE id_exemp = ?", id)
        
    return redirect("/emprunts")

# CODE EXEMPLAIRE
vars = ["id", "n_ord", "dt_achat", "etat",  "id_rayon", "id_ref","pres_type"]
# A list of the attributes of the table "Exemplaire".
exemp_att = ["ID","Num Ordre", "Date Achat", "Etat", "ID Rayon", "ID Document", "TYPE PRESENCE"]

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

    db.execute("""INSERT INTO Exemplaire (id_exemp, num_ord, date_acht, etat_exemp,
               id_rayon, id_ref,pres_type) VALUES(?, ?, ?, ?, ?, ?, ?)""",
               vars[0], vars[1], vars[2], vars[3], vars[4], vars[5], vars[6])
    
    return  redirect("/exemplaires")

@app.route("/deregister_7", methods=["POST"])
def deregister_7():    # sourcery skip: use-named-expression
    id = request.form.get("id")
    if id: 
        db.execute("DELETE FROM Emprunt WHERE id_exemp = ?", id)
        db.execute("DELETE FROM Exemplaire WHERE id_exemp = ?", id)
        db.execute(f"UPDATE Exemplaire SET id_exemp = id_exemp - 1 WHERE id_exemp>{id}")
    return redirect("/exemplaires")

@app.route("/querying_exemp", methods=['POST', 'GET'])
def querying_exemp():
    query = request.form.get("query")
    if "count" in query.lower():
        return render_template("exemplaire.html", exemp=[], counting=db.execute(query))
    try:
        query_x = db.execute(query)
    except Exception:
        return render_template("exemplaire.html", exemp=[])
    if query_x:
        return render_template("exemplaire.html", exemp=query_x)
    else:
        return render_template("exemplaire.html", exemp=[])
    
@app.route("/update_exemp", methods=["POST"])
def update():
    up_q = request.form.get("update_query").split(", ")
    if up_q:
        db.execute(f"UPDATE Exemplaire SET {up_q[1]} = '{up_q[2]}' WHERE id_exemp = {int(up_q[0])}")
    return redirect("/exemplaires")

# CODE STAGIAIRE

stagiaire_attributes = ["ID", "NOM", "PRENOM", "ID BIBLIOTHECAIRE"]
vars = ["id", "nom", "prenom", "bitc"]
@app.route("/stagiaire")
def stagiaire():
    stgs_ = db.execute("SELECT * FROM Stagiaire")
    
    return render_template("stagiaire.html", stagiaires = stgs_)

@app.route("/stagiaire_reg", methods=["POST"])
def stagiaire_reg():
    return render_template("stagiaire_reg.html", stg_att=stagiaire_attributes)

@app.route("/register_stg", methods=["POST"])
def register_stg():
    
    for i in range(len(stagiaire_attributes)):
        vars[i] = request.form.get(stagiaire_attributes[i])

    if not id:
        return render_template("error.html", message = "ID Missing")

    db.execute("""INSERT INTO Stagiaire (id_stg, nom_stg, prenom_stg, id_bitc) 
               VALUES(?, ?, ?, ?)""", vars[0], vars[1], vars[2], vars[3])
    
    return  redirect("/stagiaire")


# PERIODIQUE CODE
periodique_attributes = ["ISSN", "VOLUME", "NUMERO", "ID DOCUMENT"]

@app.route("/periodique", methods=['GET', 'POST'])
def periodique():
    periodique = db.execute("SELECT * FROM Periodique")
    return render_template("periodique.html", pdq = periodique)

@app.route("/periodique_reg", methods=['GET', 'POST'])
def periodique_reg():
    return render_template("periodique_reg.html", PDQ=periodique_attributes)

@app.route("/register_periodique", methods=['GET', 'POST'])
def register_periodique():
    issn = request.form.get("ISSN")
    vol = request.form.get("VOLUME")
    num = request.form.get("NUMERO")
    doc = request.form.get("ID DOCUMENT")
    db.execute("""INSERT INTO  Periodique VALUES(?, ?, ?, ?)""",issn, vol, num, doc)
    
    return redirect("/periodique")


@app.route("/deregister_8", methods=['POST'])
def deregister_8():    # sourcery skip: use-named-expression
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM Periodique WHERE code_ISSN = ?", id)

    return redirect("/periodique")

@app.route("/querying_9", methods=['POST'])
def querying_8():
    query = request.form.get("query")
    try:
        query_x = db.execute(query)
    except Exception:
        return render_template("periodique.html", PDQ=[])
    if query_x:
        return render_template("periodique.html", PDQ=query_x)
    else:
        return render_template("periodique.html", PDQ=[])

# Queries 
@app.route("/queries")
def queries():
    return render_template("queries.html")

@app.route("/clts_ctg", methods=["POST"])
def clts_ctg():
    ctgs = ["VIP", "OCCASIONNEL", "ABONNE"]
    x = request.form.get("list_option")
    s = db.execute(f"SELECT * FROM Emprunteur WHERE ctg_emp='{ctgs[int(x)-1]}'")
    return render_template("clients.html", clients = s)    
    

@app.route("/nom_rayon", methods=["POST"])
def nom_rayon():
    x = request.form.get("list_option")
    if x == "0":
        s = db.execute("""SELECT nom_rayon,titre_doc FROM Document 
	                    JOIN Exemplaire ON Exemplaire.id_ref = Document.id_ref
		                    JOIN Rayon ON Rayon.id_rayon = Exemplaire.id_rayon
   			                    GROUP BY Rayon.nom_rayon""")
    else:
        rayon_s = ["Anime", "Aventure", "Biographie", "Histoire", "divertissement"]
        s = db.execute(f"""SELECT nom_rayon,titre_doc FROM Document 
	                    JOIN Exemplaire ON Exemplaire.id_ref = Document.id_ref
		                    JOIN Rayon ON Rayon.id_rayon = Exemplaire.id_rayon
   			                    WHERE Rayon.nom_rayon = '{rayon_s[int(x)-1]}'
                          """)

    return list(s)

    
@app.route("/rayons", methods=["POST"])
def rayon():
    ray_x = db.execute("SELECT * FROM Rayon")
    return render_template("rayons.html", ray = ray_x)


@app.route("/count", methods=["GET", "POST"])
def count():
    entities_ = ["Exemplaire", "Emprunteur", "Document", "Stagiaire"]
    s = [db.execute(f"SELECT COUNT(*) FROM {i}") for i in entities_]
    return render_template("count.html", entities = s, list_ent = entities_)

if __name__ == "__main__":
    app.run(debug=True)