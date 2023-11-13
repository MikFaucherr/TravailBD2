USE TravailBd;


# Trigger pour rajouter l'ordre d'insertion pour les chapitres dans un meme livre
DELIMITER //

CREATE TRIGGER avant_chapitre
BEFORE INSERT ON chapitre
FOR EACH ROW
BEGIN
    DECLARE max_ordre_insertion INT;
    
    SELECT COALESCE(MAX(ordre_insertion), 0) INTO max_ordre_insertion
    FROM chapitre
    WHERE livre_id = NEW.livre_id;

    SET NEW.ordre_insertion = max_ordre_insertion + 1;
END //

DROP TRIGGER before_insert_sauvegarde;
DELIMITER //

CREATE TRIGGER before_insert_sauvegarde
BEFORE INSERT ON sauvegarde
FOR EACH ROW
BEGIN

    SET @nomexiste = (SELECT COUNT(*) FROM sauvegarde WHERE nom LIKE CONCAT(New.nom,'%'));

    IF @nomexiste > 0 THEN 
        SET NEW.nom = CONCAT(NEW.nom, '_', @nomexiste);
    END IF;

END //

DELIMITER ;



