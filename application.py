import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from design import Ui_MainWindow


cnx = mysql.connector.connect(
    user='monuser', 
    password='qwerty',
    host='localhost',
    database='TravailBd')

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.choix_livre.addItem("          ")
        self.arme1.addItem("          ")
        self.arme2.addItem("          ")
        self.descipline1.addItem("          ")
        self.descipline2.addItem("          ")
        self.descipline3.addItem("          ")
        self.descipline4.addItem("          ")
        self.descipline5.addItem("          ")
        self.charger_partie.addItem("          ")
        self.afficher_sauvegarde()
        self.afficher_option_livre()
        self.choix_livre.activated.connect(self.afficher_livre)
        self.aller.clicked.connect(self.afficher_suite)
        self.nouvelle_partie.clicked.connect(self.nouvellepartie)
        self.supprimer.clicked.connect(self.supprimer_partie)
        self.sauvegarder.clicked.connect(self.sauvegarder_partie)
        self.charger_partie.activated.connect(self.afficher_info_sauvegarde)
        self.afficher_option_armes()
        self.afficher_option_disciplines()


    def afficher_option_livre(self):
        requete = "SELECT titre FROM livre;"
        cursor = cnx.cursor()
        cursor.execute(requete)

        resultat = cursor.fetchall()

        if resultat:
            for title in resultat:
                self.choix_livre.addItem(title[0])
        else:
            self.resultat.setText("Aucun résultat trouvé")

        cursor.close()

    def afficher_option_armes(self):
        requete = "SELECT nom FROM armes;"
        cursor = cnx.cursor()
        cursor.execute(requete)

        resultat = cursor.fetchall()

        if resultat:
            for armes in resultat:
                self.arme1.addItem(armes[0])
                self.arme2.addItem(armes[0])

        cursor.close()
    
    def afficher_option_disciplines(self):
        requete = "SELECT nom FROM disciplines_Kai;"
        cursor = cnx.cursor()
        cursor.execute(requete)

        resultat = cursor.fetchall()

        if resultat:
            for disciplines in resultat:
                self.descipline1.addItem(disciplines[0])
                self.descipline2.addItem(disciplines[0])
                self.descipline3.addItem(disciplines[0])
                self.descipline4.addItem(disciplines[0])
                self.descipline5.addItem(disciplines[0])
        cursor.close()


    def afficher_livre(self):
        livre = self.choix_livre.currentText() 
        requete = "SELECT no_chapitre, texte, livre.titre, chapitre.id FROM chapitre JOIN livre ON chapitre.livre_id = livre.id WHERE livre.titre = %(livre)s AND ordre_insertion = 1"
        parametres = {'livre': livre}
        cursor = cnx.cursor()
        cursor.execute(requete, parametres)
        resultat = cursor.fetchone()
        cursor.close()
        if resultat:
            self.chapitre_titre.setText(resultat[0])
            self.zone_texte_chapitre.setText(resultat[1])
            self.zone_texte_chapitre.setAlignment(Qt.AlignJustify)
            self.titre_livre.setText(resultat[2])

        self.afficher_option_suite(resultat[3])

    def afficher_sauvegarde(self):
        requete = "SELECT nom FROM sauvegarde;"
        cursor = cnx.cursor()
        cursor.execute(requete)

        resultat = cursor.fetchall()
        
        cursor.close()  

        if resultat:
            for nom in resultat:
                self.charger_partie.addItem(nom[0])


    def afficher_option_suite(self, id_chapitre):
        requete = "SELECT chapitre.no_chapitre FROM chapitre JOIN lien_chapitre ON lien_chapitre.no_chapitre_destination_id = chapitre.id WHERE lien_chapitre.no_chapitre_origine_id = %(id_chapitre)s"
        parametres = {'id_chapitre': id_chapitre}

        cursor = cnx.cursor()
        cursor.execute(requete, parametres)

        resultat = cursor.fetchall()

        self.suite.clear()

        if resultat:
            for nom_chapitre in resultat:
                self.suite.addItem(nom_chapitre[0])

        cursor.close()

    def afficher_suite(self):
        no_chapitre = self.suite.currentText() 
        livre = self.choix_livre.currentText()
        requete = "SELECT no_chapitre, texte, chapitre.id FROM chapitre JOIN livre ON chapitre.livre_id = livre.id WHERE no_chapitre = %(no_chapitre)s AND livre.titre = %(livre)s"
        parametres = {'no_chapitre': no_chapitre, 'livre': livre}
        cursor = cnx.cursor()
        cursor.execute(requete, parametres)
        resultat = cursor.fetchone()
        cursor.close()

        if resultat:
            self.chapitre_titre.setText(resultat[0])
            self.zone_texte_chapitre.setText(resultat[1])
            self.zone_texte_chapitre.setAlignment(Qt.AlignJustify)

        self.afficher_option_suite(resultat[2])

    def nouvellepartie(self):
        nom = self.nom.text() 

        # Insert into fiche_personnage
        requete_fiche_personnage = "INSERT INTO fiche_personnage (object, repas, object_speciaux, bourse) VALUES (NULL, NULL, NULL, NULL);"
        cursor = cnx.cursor()
        cursor.execute(requete_fiche_personnage)
        fiche_id = cursor.lastrowid
        cnx.commit()
        cursor.close()

        # Insert into sauvegarde
        requete_sauvegarde = "INSERT INTO sauvegarde (nom, fiche_id) VALUES (%(nom)s, %(fiche_id)s);"
        parametres = {'nom': nom, 'fiche_id': fiche_id}
        cursor = cnx.cursor()
        cursor.execute(requete_sauvegarde, parametres)
        cnx.commit()
        cursor.close()

        self.charger_partie.clear()
        self.afficher_sauvegarde()
        self.nom.clear()



    def supprimer_partie(self):
        nom = self.charger_partie.currentText() 
        requete = "DELETE FROM sauvegarde WHERE nom = %(nom)s;"
        parametres = {'nom': nom}
        cursor = cnx.cursor()
        cursor.execute(requete, parametres)
        cnx.commit()
        id = cursor.lastrowid
        self.charger_partie.clear()
        self.afficher_sauvegarde()
        cursor.close()
        #supprimer la fiche
        requete = "DELETE FROM fiche_personnage WHERE id = %(id)s;"
        parametres = {'id': id}
        cursor = cnx.cursor()
        cursor.execute(requete, parametres)
        cnx.commit()
        self.charger_partie.clear()
        self.afficher_sauvegarde()
        cursor.close()

    def sauvegarder_partie(self):
        brs = self.bourse.value()
        object_spec = self.zone_texte_object_speciaux.toPlainText()
        if brs == "          ":
            brs = None
        repas = self.repas.toPlainText()
        if repas == "          ":
            repas = None
        obj = self.zone_texte_object.toPlainText()
        if obj == "          ":
            obj = None
        nom = self.charger_partie.currentText()
        livre_titre = self.titre_livre.text()
        requete = "SELECT livre.id FROM livre WHERE livre.titre = %(livre_titre)s"
        parametres = {'livre_titre': livre_titre}
        cursor = cnx.cursor()
        cursor.execute(requete, parametres)
        resultat = cursor.fetchone()
        if resultat:
            livre_id = resultat[0]
        else:
            livre_id = None
        cursor.close()

        requete_check_fiche = "SELECT fiche_id FROM sauvegarde WHERE nom = %(nom)s;"
        parametres_check_fiche = {'nom': nom}
        cursor = cnx.cursor()
        cursor.execute(requete_check_fiche, parametres_check_fiche)
        resultat_check_fiche = cursor.fetchone()
        cursor.close()
        id = resultat_check_fiche[0]

        # Savoir no_chapitre_id
        no_chapitre = self.chapitre_titre.text()
        requete3 = "SELECT chapitre.id FROM chapitre WHERE livre_id = %(livre_id)s AND no_chapitre = %(no_chapitre)s;"
        parametres3 = {'livre_id': livre_id, 'no_chapitre': no_chapitre}
        cursor = cnx.cursor()
        cursor.execute(requete3, parametres3)
        resultat = cursor.fetchone()
        no_chapitre_id = resultat[0]
        cursor.close()

        # update
        
        requete_update = "UPDATE fiche_personnage SET object = %(obj)s, repas = %(repas)s, object_speciaux = %(object_spec)s, bourse = %(brs)s WHERE id = %(id)s"
        parametres_update = {
            'obj': obj,
            'repas': repas,
            'object_spec': object_spec,
            'brs': brs,
            'id' : id
        }
        cursor = cnx.cursor()
        cursor.execute(requete_update, parametres_update)
        cnx.commit()
        cursor.close()

        requete_update2 = "UPDATE sauvegarde SET no_chapitre_id = %(no_chapitre_id)s, livre_id = %(livre_id)s WHERE fiche_id = %(id)s"
        parametres_updates = {
            'no_chapitre_id': no_chapitre_id,
            'livre_id': livre_id,
            'id': id,
        }
        cursor = cnx.cursor()
        cursor.execute(requete_update2, parametres_updates)
        cnx.commit()
        cursor.close()

        # armes
        noms_armes = [
            self.enleverespace(self.arme1.currentText()),
            self.enleverespace(self.arme2.currentText())
        ]

        # Boucle pour mettre à jour ou insérer les armes dans la table lien_armes
        for i, nom_arme in enumerate(noms_armes, start=1):
            # Récupérez l'ID de l'arme à partir de son nom
            requete_arme = "SELECT id FROM armes WHERE nom = %(nom_arme)s;"
            parametres_arme = {'nom_arme': nom_arme}
            cursor = cnx.cursor()
            cursor.execute(requete_arme, parametres_arme)
            resultat_arme = cursor.fetchone()
            cursor.close()

            # Si aucune arme n'est trouvée, attribuez None à armes_id
            armes_id = resultat_arme[0] if resultat_arme else None

            # Supprimez le lien existant s'il y en a un
            requete_delete_arme = """
                DELETE FROM lien_armes
                WHERE fiche_id = %(fiche_id)s AND numero_armes = %(numero_armes)s;
            """
            parametres_delete_arme = {'fiche_id': id, 'numero_armes': i}
            cursor = cnx.cursor()
            cursor.execute(requete_delete_arme, parametres_delete_arme)
            cnx.commit()
            cursor.close()

            if resultat_arme is not None and nom_arme is not None:  # Si l'arme n'est pas "      "
                # Insérez l'arme dans la table lien_armes
                requete_insert_arme = """
                    INSERT INTO lien_armes (fiche_id, armes_id, numero_armes)
                    VALUES (%(fiche_id)s, %(armes_id)s, %(numero_armes)s);
                """
                parametres_insert_arme = {'fiche_id': id, 'armes_id': armes_id, 'numero_armes': i}
                cursor = cnx.cursor()
                cursor.execute(requete_insert_arme, parametres_insert_arme)
                cnx.commit()
                cursor.close()

        # disciplines
        noms_disciplines = [
            self.enleverespace(self.descipline1.currentText()),
            self.enleverespace(self.descipline2.currentText()),
            self.enleverespace(self.descipline3.currentText()),
            self.enleverespace(self.descipline4.currentText()),
            self.enleverespace(self.descipline5.currentText()),
        ]

        # Boucle pour mettre à jour ou insérer les disciplines dans la table lien_disciplines_Kai
        for i, nom_discipline in enumerate(noms_disciplines, start=1):
            # Récupérez l'ID de la discipline à partir de son nom
            requete_discipline = "SELECT id FROM disciplines_Kai WHERE nom = %(nom_discipline)s;"
            parametres_discipline = {'nom_discipline': nom_discipline}
            cursor = cnx.cursor()
            cursor.execute(requete_discipline, parametres_discipline)
            resultat_discipline = cursor.fetchone()
            cursor.close()

            # Si aucune discipline n'est trouvée, attribuez None à discipline_id
            discipline_id = resultat_discipline[0] if resultat_discipline else None

            # Supprimez le lien existant s'il y en a un
            requete_delete_discipline = """
                DELETE FROM lien_disciplines_Kai
                WHERE fiche_id = %(fiche_id)s AND numero_disciplines = %(numero_disciplines)s;
            """
            parametres_delete_discipline = {'fiche_id': id, 'numero_disciplines': i}
            cursor = cnx.cursor()
            cursor.execute(requete_delete_discipline, parametres_delete_discipline)
            cnx.commit()
            cursor.close()

            if resultat_discipline is not None and nom_discipline is not None:  # Si la discipline n'est pas "      "
                # Insérez la discipline dans la table lien_disciplines_Kai
                requete_insert_discipline = """
                    INSERT INTO lien_disciplines_Kai (fiche_id, discipline_id, numero_disciplines)
                    VALUES (%(fiche_id)s, %(discipline_id)s, %(numero_disciplines)s);
                """
                parametres_insert_discipline = {'fiche_id': id, 'discipline_id': discipline_id, 'numero_disciplines': i}
                cursor = cnx.cursor()
                cursor.execute(requete_insert_discipline, parametres_insert_discipline)
                cnx.commit()
                cursor.close()


    def afficher_info_sauvegarde(self):

        self.zone_texte_object.clear()
        self.repas.clear()
        self.zone_texte_object_speciaux.clear()
        self.bourse.setValue(0)
        self.suite.clear()

        self.descipline1.setCurrentIndex(self.descipline1.findText("          "))
        self.descipline2.setCurrentIndex(self.descipline2.findText("          "))
        self.descipline3.setCurrentIndex(self.descipline3.findText("          "))
        self.descipline4.setCurrentIndex(self.descipline4.findText("          "))
        self.descipline5.setCurrentIndex(self.descipline5.findText("          "))
        self.arme1.setCurrentIndex(self.arme1.findText("          "))
        self.arme2.setCurrentIndex(self.arme2.findText("          "))
        self.chapitre_titre.setText("Chapitre 0")
        self.zone_texte_chapitre.clear()
        self.titre_livre.setText("Veuillez choisir un livre")

        ######
        nom = self.charger_partie.currentText()
        requete_info = "SELECT livre.titre, fiche_personnage.*, no_chapitre_id FROM sauvegarde \
                    LEFT JOIN livre ON sauvegarde.livre_id = livre.id \
                    LEFT JOIN fiche_personnage ON sauvegarde.fiche_id = fiche_personnage.id \
                    WHERE sauvegarde.nom = %(nom)s;"
        parametres_info = {'nom': nom}

        cursor = cnx.cursor(dictionary=True)
        cursor.execute(requete_info, parametres_info)
        resultat_info = cursor.fetchone() 
        cursor.close()
        ######

        if resultat_info['titre'] != None:
            if resultat_info['no_chapitre_id'] == None:
                resultat_info['no_chapitre_id'] = 1

            requete_info = "SELECT no_chapitre, texte FROM chapitre WHERE id = %(id)s;"
            parametres_info = {'id': resultat_info['no_chapitre_id']}

            cursor = cnx.cursor(dictionary=True)
            cursor.execute(requete_info, parametres_info)
            resultat_livre = cursor.fetchone() 
            cursor.close()


            self.chapitre_titre.setText(resultat_livre['no_chapitre'])
            self.zone_texte_chapitre.setText(resultat_livre['texte'])
            self.zone_texte_chapitre.setAlignment(Qt.AlignJustify)
            if resultat_info['no_chapitre_id'] != None:
                self.afficher_option_suite(resultat_info['no_chapitre_id'])

            if resultat_info:
                titre_livre = resultat_info['titre']
                index_livre = self.choix_livre.findText(titre_livre)
                self.titre_livre.setText(resultat_info['titre'])
            if index_livre != -1:
                self.choix_livre.setCurrentIndex(index_livre)


            if resultat_info['object']:
                self.zone_texte_object.setText(resultat_info['object'])
            else:
                self.zone_texte_object.clear()
            if resultat_info['repas']:
                self.repas.setPlainText(resultat_info['repas'])
            else:
                self.repas.clear()
            if resultat_info['object_speciaux']:
                self.zone_texte_object_speciaux.setPlainText(resultat_info['object_speciaux'])
            else:
                self.zone_texte_object_speciaux.clear()
            if resultat_info['bourse']:
                self.bourse.setValue(resultat_info['bourse'])
            else:
                self.bourse.setValue(0)

            id_fiche = resultat_info['id']

            requete_armes_disciplines = """
                                        SELECT disciplines_Kai.nom AS nom_discipline, lien_disciplines_Kai.numero_disciplines, 
                                            armes.nom AS nom_arme, lien_armes.numero_armes 
                                        FROM fiche_personnage
                                        LEFT JOIN lien_disciplines_Kai ON fiche_personnage.id = lien_disciplines_Kai.fiche_id
                                        LEFT JOIN disciplines_Kai ON lien_disciplines_Kai.discipline_id = disciplines_Kai.id
                                        LEFT JOIN lien_armes ON fiche_personnage.id = lien_armes.fiche_id
                                        LEFT JOIN armes ON lien_armes.armes_id = armes.id
                                        WHERE fiche_personnage.id = %(id_fiche)s;
                                        """

            parametres_armes_disciplines = {'id_fiche': id_fiche}
            cursor = cnx.cursor()
            cursor.execute(requete_armes_disciplines, parametres_armes_disciplines)
            resultat_armes_disciplines = cursor.fetchall()
            cursor.close()

            for resultat in resultat_armes_disciplines:
                nom_discipline = resultat[0]  # Utilisez les indices pour accéder aux éléments du tuple
                numero_discipline = resultat[1]
                nom_arme = resultat[2]
                numero_arme = resultat[3]

               # Remplir les combobox pour les disciplines
                if nom_discipline and numero_discipline:
                    combobox_discipline = getattr(self, f"descipline{numero_discipline}")
                    index_discipline = combobox_discipline.findText(nom_discipline)
                    if index_discipline != -1:
                        combobox_discipline.setCurrentIndex(index_discipline)
                    else:
                        combobox_discipline.setCurrentIndex(combobox_discipline.findText("          "))

                # Remplir les combobox pour les armes
                if nom_arme and numero_arme:
                    combobox_arme = getattr(self, f"arme{numero_arme}")
                    index_arme = combobox_arme.findText(nom_arme)-1
                    if index_arme != -1:
                        combobox_arme.setCurrentIndex(index_arme)
                    else:
                        combobox_arme.setCurrentIndex(combobox_arme.findText("          "))


    def enleverespace(self, obj):
        if obj == ("          "):
            return None
        else: 
            return obj




app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()