-- SQL queries pour le SIGB 

--  Extraire les clients dont le prenom se termine par 'i'
SELECT prenom_emp FROM Emprunteur WHERE prenom_emp LIKE '%I'

-- -- Nombre Etat Exemplaire
SELECT etat_exemp,COUNT(*) FROM Exemplaire
    GROUP BY etat_exemp

-- Chaque emprunteur et son emprunt 
SELECT nom_emp, titre_doc FROM Emprunteur
    JOIN Emprunt ON Emprunteur.id_emp = Emprunt.id_emp
        JOIN Exemplaire ON Emprunt.id_exemp = Exemplaire.id_exemp
            JOIN Document ON Document.id_ref = Exemplaire.id_ref;

-- Affichage nom_emprunteur ainsi que son doc, date_debut, date_fin
SELECT prenom_emp, titre_doc, Date_debut, Date_fin FROM Exemplaire
    JOIN Emprunteur ON Emprunteur.id_emp = Emprunt.id_emp
        JOIN Emprunt ON Exemplaire.id_exemp = Emprunt.id_exemp
            JOIN Document ON Document.id_ref = Exemplaire.id_ref;

-- Affichage nbt_exemplaire ainsi que le nom de document, d'une maniére ordonnée
SELECT nbr_exemp , titre_doc FROM Document
        ORDER BY Document.nbr_exemp DESC,titre_doc ASC;

-- Tirer le nom du livre à partir de son code_ISBN (en utilisant un clé etrangère)
SELECT titre_doc FROM Document
    JOIN Livre ON Livre.id_ref = Document.id_ref
        WHERE code_ISBN = '0-5920-1424-X';

-- 
SELECT nom_edit, titre_doc FROM Editeur
    JOIN Document ON Document.id_editeur = Editeur.id_editeur;