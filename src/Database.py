import mysql.connector

def getRezeptId(rezeptName):
    sql = "SELECT `RezeptId` FROM `Rezepte` WHERE `Name` = %s"
    mycursor.execute(sql, (rezeptName,))
    id = mycursor.fetchone()[0]
    return id


def getLebensmittelId(lebensmittelName):
    sql = "SELECT `LebensmittelId` FROM `Lebensmittel` WHERE `Name` = %s"
    mycursor.execute(sql, (lebensmittelName,))
    id = mycursor.fetchone()[0]
    return id

# connect to database or create new one if no database exists
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="user",
        passwd="test",
        database="recipeDatabase"
    )
    mycursor = mydb.cursor()
except:
    mydb = mysql.connector.connect(
        host="localhost",
        user="user",
        passwd="test",
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE recipeDatabase")

mycursor.execute("SHOW DATABASES")
for x in mycursor:
    print(x)

# delete old tables
mycursor.execute("DROP TABLE IF EXISTS `enthaeltLebensmittel`")
mycursor.execute("DROP TABLE IF EXISTS `enthaeltRezept`")
mycursor.execute("DROP TABLE IF EXISTS `Lebensmittel`")
mycursor.execute("DROP TABLE IF EXISTS `Rezepte`")

# create tables
mycursor.execute(
    "CREATE TABLE `Lebensmittel` (`LebensmittelId` INT AUTO_INCREMENT PRIMARY KEY, `Name` VARCHAR(30), `KalorienPro100g` Integer, `Fleisch` Boolean, `Tierprodukt` Boolean, `Gluten` Boolean, `Krebstiere` Boolean, `Eier` Boolean, `Fisch` Boolean, `Erdnuesse` Boolean, `Sojabohnen` Boolean, `Milch` Boolean, `Schalenfruechte` Boolean, `Sellerie` Boolean, `Sesamsamen` Boolean, `Schwefeldioxid` Boolean, `Lupinien` Boolean, `Weichtiere` Boolean);")
mycursor.execute(
    "CREATE TABLE `Rezepte` (`RezeptId` INT AUTO_INCREMENT PRIMARY KEY, `Name` VARCHAR(30), `Anleitung` VARCHAR(1000));")
mycursor.execute(
    "CREATE TABLE `enthaeltLebensmittel` (`enthaeltLebensmittelId` INT AUTO_INCREMENT PRIMARY KEY, `RezeptId` Integer, `LebensmittelId` Integer, `Menge` Integer, FOREIGN KEY (`RezeptId`) REFERENCES `Rezepte`(`RezeptId`), FOREIGN KEY (`LebensmittelId`) REFERENCES `Lebensmittel`(`LebensmittelId`));")
mycursor.execute(
    "CREATE TABLE `enthaeltRezept` (`enthaeltRezeptId` INT AUTO_INCREMENT PRIMARY KEY, `RezeptId` Integer, `KomponentenRezeptId` Integer, `Menge` Integer, FOREIGN KEY (`RezeptId`) REFERENCES `Rezepte`(`RezeptId`), FOREIGN KEY (`KomponentenRezeptId`) REFERENCES `Rezepte`(`RezeptId`));")

mycursor.execute("SHOW TABLES")
for x in mycursor:
    print("created table:", x[0])

# add some sample data to table Lebensmittel
sqlLebensmittel = "INSERT INTO `Lebensmittel` (`Name`, `KalorienPro100g`, `Fleisch`, `Tierprodukt`, `Gluten`, `Krebstiere`, `Eier`, `Fisch`, `Erdnuesse`, `Sojabohnen`, `Milch`, `Schalenfruechte`, `Sellerie`, `Sesamsamen`, `Schwefeldioxid`, `Lupinien`, `Weichtiere`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
valLebensmittel = [
    ("Weizenmehl", 343, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Zucker", 405, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Eier", 155, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Milch", 68, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),
    ("Käse", 346, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),
    ("Sahne", 303, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),
    ("Butter", 741, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),
    ("Buttermilch", 40, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),
    ("Rapsöl", 884, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Kakaopulver", 339, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),
    ("Backpulver", 86, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Bananen", 90, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Äpfel", 52, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Tomaten", 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Karotten", 41, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Sellerie", 17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0),
    ("Tofu", 70, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0),
    ("Schweinefleisch", 136, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Rindfleisch", 190, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Putenfleisch", 107, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Lachs", 206, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Weißbrot", 247, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Wasser", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Olivenöl", 900, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Hefe", 83, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Salz", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Zwiebeln", 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Knoblauch", 149, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Mozzarella", 254, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0),
    ("Champignons", 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ("Thunfisch in Öl", 189, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
]
mycursor.executemany(sqlLebensmittel, valLebensmittel)
mydb.commit()
print(mycursor.rowcount, "rows were inserted in Lebensmittel.")

# add some sample data to table Rezepte
sqlRezepte = "INSERT INTO `Rezepte` (`Name`, `Anleitung`) VALUES (%s, %s)"
valRezepte = [
    ("Pizzateig",
     "Im lauwarmen Wasser und dem Olivenöl die Hefe mit dem Salz und Zucker auflösen. Dann das Mehl hinzufügen und einen glatten Teig kneten. Eine halbe Stunde an einem warmen Ort gehen lassen, zusammenkneten und abgedeckt im Kühlschrank 2 Tage ruhen lassen."),
    ("Tomatensoße",
     "Tomaten schälen. Dazu die Haut kreuzförmig einschneiden und kurz in kochendes Wasser legen, danach sofort in kaltes Wasser tauchen. Zwiebeln und Knoblauch klein schneiden und mit etwas Öl anbraten. Tomaten würfeln und dazu geben. Mit Salz abschmecken. Auf kleiner Flamme eine halbe Stunde köcheln lassen."),
    ("Thunfischpizza",
     "Den Ofen auf heißester Stufe vorheitzen. Den Pizzateig sehr dünn ausrollen. Tomatensoße darauf verteilen. Mit Thunfisch, Zwiebeln und Käse belegen. Im Ofen bachen, bis der Käse goldbraun ist. ")
]
mycursor.executemany(sqlRezepte, valRezepte)
mydb.commit()
print(mycursor.rowcount, "rows were inserted in Rezepte.")

# add some sample data to table enthaeltLebensmittel
sqlEnthaeltLebensmittel = "INSERT INTO `enthaeltLebensmittel` (`RezeptId`, `LebensmittelId`, `Menge`) VALUES (%s, %s, %s)"
valEnthaeltLebensmittel = [
    (getRezeptId("Pizzateig"), getLebensmittelId("Weizenmehl"), 925),
    (getRezeptId("Pizzateig"), getLebensmittelId("Wasser"), 500),
    (getRezeptId("Pizzateig"), getLebensmittelId("Hefe"), 40),
    (getRezeptId("Pizzateig"), getLebensmittelId("Salz"), 20),
    (getRezeptId("Pizzateig"), getLebensmittelId("Olivenöl"), 20),
    (getRezeptId("Pizzateig"), getLebensmittelId("Zucker"), 10),
    (getRezeptId("Tomatensoße"), getLebensmittelId("Tomaten"), 500),
    (getRezeptId("Tomatensoße"), getLebensmittelId("Salz"), 10),
    (getRezeptId("Tomatensoße"), getLebensmittelId("Zwiebeln"), 50),
    (getRezeptId("Tomatensoße"), getLebensmittelId("Knoblauch"), 10),
    (getRezeptId("Tomatensoße"), getLebensmittelId("Rapsöl"), 15),
    (getRezeptId("Thunfischpizza"), getLebensmittelId("Thunfisch in Öl"), 100),
    (getRezeptId("Thunfischpizza"), getLebensmittelId("Zwiebeln"), 50),
    (getRezeptId("Thunfischpizza"), getLebensmittelId("Käse"), 50)
]
mycursor.executemany(sqlEnthaeltLebensmittel, valEnthaeltLebensmittel)
mydb.commit()
print(mycursor.rowcount, "rows were inserted in enthaeltLebensmittel.")

mycursor.execute("SELECT `Rezepte`.`Name` AS `Rezept`, `Lebensmittel`.`Name` AS `Lebensmittel`, `enthaeltLebensmittel`.`Menge` AS `Menge` FROM `enthaeltLebensmittel` INNER JOIN `Rezepte` ON `enthaeltLebensmittel`.`RezeptId` = `Rezepte`.`RezeptId` INNER JOIN `Lebensmittel` ON `enthaeltLebensmittel`.`LebensmittelId` = `Lebensmittel`.`LebensmittelId`")
myresult = mycursor.fetchall()
for x in myresult:
    print(x)


# add some sample data to table enthaeltrezept
sqlEnthaeltrezept = "INSERT INTO `enthaeltRezept` (`RezeptId`, `KomponentenRezeptId`, `Menge`) VALUES (%s, %s, %s)"
valEnthaeltrezept = [
    (getRezeptId("Thunfischpizza"), getRezeptId("Pizzateig"), 300),
    (getRezeptId("Thunfischpizza"), getRezeptId("Tomatensoße"), 150)
]
mycursor.executemany(sqlEnthaeltrezept, valEnthaeltrezept)
mydb.commit()
print(mycursor.rowcount, "rows were inserted in enthaeltRezept.")

mycursor.execute("SELECT `Rezepte`.`Name` AS `Rezept`, `KomponentenRezept`.`Name` AS `KomponentenRezept`, `enthaeltRezept`.`Menge` AS `Menge` FROM `enthaeltRezept` INNER JOIN `Rezepte` ON `enthaeltRezept`.`RezeptId` = `Rezepte`.`RezeptId` INNER JOIN `Rezepte` `KomponentenRezept` ON `enthaeltRezept`.`KomponentenRezeptId` = `KomponentenRezept`.`RezeptId`")
myresult = mycursor.fetchall()
for x in myresult:
    print(x)


if mydb.is_connected():
    mycursor.close()
    mydb.close()
    print("MySQL connection is closed")
