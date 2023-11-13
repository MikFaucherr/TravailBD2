DROP DATABASE IF EXISTS TravailBd;
CREATE DATABASE IF NOT EXISTS TravailBd;

USE TravailBd;

CREATE TABLE IF NOT EXISTS livre (
    id INT PRIMARY KEY AUTO_INCREMENT,
    titre VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS chapitre (
	id INT PRIMARY KEY AUTO_INCREMENT,
    no_chapitre VARCHAR(255),
    texte TEXT,
    livre_id INT,
    ordre_insertion INT, 
    FOREIGN KEY (livre_id) REFERENCES livre(id)
);

CREATE TABLE IF NOT EXISTS fiche_personnage (
    id INT PRIMARY KEY AUTO_INCREMENT,
    object VARCHAR(255),
    repas VARCHAR(255),
    object_speciaux VARCHAR(255),
    bourse INT
);

CREATE TABLE IF NOT EXISTS lien_chapitre (
    id INT PRIMARY KEY AUTO_INCREMENT,
    no_chapitre_origine_id INT,
    no_chapitre_destination_id INT,
    FOREIGN KEY (no_chapitre_origine_id) REFERENCES chapitre(id),
    FOREIGN KEY (no_chapitre_destination_id) REFERENCES chapitre(id)
);


CREATE TABLE IF NOT EXISTS disciplines_Kai (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255),
    description VARCHAR(2000)
);

CREATE TABLE IF NOT EXISTS lien_disciplines_Kai (
    fiche_id INT,
    discipline_id INT,
    numero_disciplines INT,
    PRIMARY KEY (fiche_id, discipline_id),
    FOREIGN KEY (fiche_id) REFERENCES fiche_personnage(id) ON DELETE CASCADE,
    FOREIGN KEY (discipline_id) REFERENCES disciplines_Kai(id),
    UNIQUE KEY unique_fiche_numerod (fiche_id, numero_disciplines) 
);

CREATE TABLE IF NOT EXISTS armes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS lien_armes  (
    fiche_id INT,
    armes_id INT,
    numero_armes INT,
    PRIMARY KEY (fiche_id,armes_id),
    FOREIGN KEY (fiche_id) REFERENCES fiche_personnage(id) ON DELETE CASCADE,
    FOREIGN KEY (armes_id) REFERENCES armes(id),
    UNIQUE KEY unique_fiche_numeroa (fiche_id, numero_armes) 
);

CREATE TABLE IF NOT EXISTS sauvegarde (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(255),
    no_chapitre_id INT,
    fiche_id INT UNIQUE,
    livre_id INT,
    FOREIGN KEY (livre_id) REFERENCES livre(id),
    FOREIGN KEY (no_chapitre_id) REFERENCES chapitre(id),
    UNIQUE KEY unique_fiche_id (id, fiche_id),
    FOREIGN KEY (fiche_id) REFERENCES fiche_personnage(id) ON DELETE CASCADE
    
);

CREATE USER 'monuser'@'localhost' IDENTIFIED BY 'qwerty';

GRANT SELECT ON TravailBd.armes TO 'monuser'@'localhost';
GRANT SELECT ON TravailBd.disciplines_Kai TO 'monuser'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON TravailBd.fiche_personnage TO 'monuser'@'localhost';
GRANT SELECT ON TravailBd.lien_chapitre TO 'monuser'@'localhost';
GRANT SELECT, INSERT, DELETE ON TravailBd.lien_armes TO 'monuser'@'localhost';
GRANT SELECT, INSERT, DELETE ON TravailBd.lien_disciplines_Kai TO 'monuser'@'localhost';
GRANT SELECT ON TravailBd.livre TO 'monuser'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON TravailBd.sauvegarde TO 'monuser'@'localhost';
GRANT SELECT ON TravailBd.chapitre TO 'monuser'@'localhost';







