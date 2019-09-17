from pyDatalog import pyDatalog
import mysql.connector

def getCaloriesPer100g(recipeName):
    calorieSum = 0
    calories = pyDatalog.ask("baseIngredientWithCalories('" + recipeName + "', X, Y)")
    if not calories == None:
        for c in calories.answers:
            calorieSum += c[1]
        return calorieSum * 100 / pyDatalog.ask("weightPerServing('" + recipeName + "', X)").answers[0][0]
    else:
        return 0

@pyDatalog.program()
def init_datalog():
    mydb = mysql.connector.connect(
        host="localhost",
        user="user",
        passwd="test",
        database="recipeDatabase"
    )
    if not mydb.is_connected():
        print("There is a problem with the Database")
        raise Exception("Database Error")
    mycursor = mydb.cursor()

    # create all Datalog terms
    pyDatalog.create_terms('hasCaloriesPer100g, containsGluten, containsLactose, containsMeat, containsAnimalProduct, hasID')
    pyDatalog.create_terms('recipeInstructions')
    pyDatalog.create_terms('containsIngredient, weightPerServing')

    # create facts for ingredient
    mycursor.execute("SELECT * FROM `Lebensmittel`")
    myresult = mycursor.fetchall()
    for x in myresult:
        pyDatalog.assert_fact('hasID', x[1], "ingredient", "ingredient" + str(x[0]))
        pyDatalog.assert_fact('hasCaloriesPer100g', x[1], x[2])
        if x[5] == 1:
            pyDatalog.assert_fact('containsGluten', x[1])
        if x[11] == 1:
            pyDatalog.assert_fact('containsLactose', x[1])
        if x[3] == 1:
            pyDatalog.assert_fact('containsMeat', x[1])
        if (x[4] == 1) | (x[3] == 1):
            pyDatalog.assert_fact('containsAnimalProduct', x[1])
        pyDatalog.assert_fact('weightPerServing', x[1], 1)

    mycursor.execute(
        "SELECT `Rezepte`.`Name` AS `Rezept`, `KomponentenRezept`.`Name` AS `KomponentenRezept`, `enthaeltRezept`.`Menge` AS `Menge` FROM `enthaeltRezept` INNER JOIN `Rezepte` ON `enthaeltRezept`.`RezeptId` = `Rezepte`.`RezeptId` INNER JOIN `Rezepte` `KomponentenRezept` ON `enthaeltRezept`.`KomponentenRezeptId` = `KomponentenRezept`.`RezeptId`")
    myresult = mycursor.fetchall()
    for x in myresult:
        pyDatalog.assert_fact('containsIngredient', x[0], x[1], x[2])

    # create facts for containsIngredient
    mycursor.execute(
        "SELECT `Rezepte`.`Name` AS `Rezept`, `Lebensmittel`.`Name` AS `Lebensmittel`, `enthaeltLebensmittel`.`Menge` AS `Menge` FROM `enthaeltLebensmittel` INNER JOIN `Rezepte` ON `enthaeltLebensmittel`.`RezeptId` = `Rezepte`.`RezeptId` INNER JOIN `Lebensmittel` ON `enthaeltLebensmittel`.`LebensmittelId` = `Lebensmittel`.`LebensmittelId`")
    myresult = mycursor.fetchall()
    for x in myresult:
        pyDatalog.assert_fact('containsIngredient', x[0], x[1], x[2])

    # create facts for recipes
    mycursor.execute("SELECT * FROM `Rezepte`")
    myresult = mycursor.fetchall()
    for x in myresult:
        pyDatalog.assert_fact('hasID', x[1], "recipe", "recipe" + str(x[0]))
        pyDatalog.assert_fact('recipeInstructions', x[1], x[2])
        ingredients = pyDatalog.ask("containsIngredient('" + x[1] + "', Y, Z)")
        weight = 0
        if not ingredients == None:
            for i in ingredients.answers:
                weight += i[1]
        pyDatalog.assert_fact('weightPerServing', x[1], weight)

    # resolve all ingredients from a recipe
    pyDatalog.create_terms('A, B, C, D, X, Y, Z, I, containsBaseIngredient')
    containsBaseIngredient(X, Y, Z) <= containsIngredient(X, Y, Z) & recipeInstructions(X, A) & hasCaloriesPer100g(Y, B)
    containsBaseIngredient(X, Y, Z) <= containsIngredient(X, A, B) & containsIngredient(A, Y, C) & weightPerServing(A, D) & (
                Z == C * B / D)

    # get calories per 100g for all recipes
    pyDatalog.create_terms('baseIngredientWithCalories')
    baseIngredientWithCalories(X, Y, Z) <= containsBaseIngredient(X, Y, B) & hasCaloriesPer100g(Y, C) & (
                Z == C / 100 * B)
    # hasCaloriesPer100g2(X, Y) <= baseIngredientWithCalories(X, A, B) & Y == sum(B, for_each=X))
    recipes = pyDatalog.ask('recipeInstructions(X, Y)')
    for r in recipes.answers:
        pyDatalog.assert_fact('hasCaloriesPer100g', r[0], getCaloriesPer100g(r[0]))

    # resolve allergens for recipes
    containsGluten(X) <= containsIngredient(X, A, B) & containsGluten(A)
    containsLactose(X) <= containsIngredient(X, A, B) & containsLactose(A)
    containsMeat(X) <= containsIngredient(X, A, B) & containsMeat(A)
    containsAnimalProduct(X) <= containsIngredient(X, A, B) & containsAnimalProduct(A)

    if mydb.is_connected():
        mycursor.close()
        mydb.close()

def getRecipesOrIngredients(recipeOrIngredient, glutenFree, lactoseFree, vegan, vegetarian, lowCalorie):
    query = "hasID(X,'"+ recipeOrIngredient + "', I)" + ("& ~containsGluten(X)" if glutenFree else "") + (
        "& ~containsLactose(X)" if lactoseFree else "") + ("& ~containsMeat(X)" if vegetarian else "") + (
                "& ~containsAnimalProduct(X)" if vegan else "") + ("& hasCaloriesPer100g(X, A) & (A < 100)" if lowCalorie else "")
    recipes = pyDatalog.ask(query)
    return recipes

def getRecipeDetails(recipeID):
    recipeInstructions = pyDatalog.ask("hasID(X, 'recipe', '" + recipeID + "') & recipeInstructions(X, Y)")
    recipeIngredients = pyDatalog.ask("containsIngredient('" + recipeInstructions.answers[0][0] + "', Y, Z)")
    recipeIngredientsReturnValue = []
    if not recipeIngredients == None:
        recipeIngredientsReturnValue = recipeIngredients.answers
    return recipeInstructions.answers + recipeIngredientsReturnValue

def isValidId(id):
    return pyDatalog.ask("hasID(X, Y, '" + id + "')")

def addRecipe(name, ingredients, instructions):
    isAlreadyDefined = pyDatalog.ask("hasID('" + name + "', 'recipe', Z)")
    if (not isAlreadyDefined == None):
        print("This recipe is already defined")
        return isAlreadyDefined.answers[0][0]

    # insert recipe in database
    mydb = mysql.connector.connect(
        host="localhost",
        user="user",
        passwd="test",
        database="recipeDatabase"
    )
    mycursor = mydb.cursor()

    sqlRezepte = "INSERT INTO `Rezepte` (`Name`, `Anleitung`) VALUES (%s, %s)"
    valRezepte = [(name, instructions)]
    mycursor.executemany(sqlRezepte, valRezepte)
    mydb.commit()
    recipeNumber = mycursor.lastrowid
    id = "recipe" + str(recipeNumber)

    # add recipe to datalog
    pyDatalog.assert_fact('hasID', name, "recipe", id)
    pyDatalog.assert_fact('recipeInstructions', name, instructions)

    # insert ingredients in database
    for i in ingredients:
        if isValidId(i[0]):
            if "ingredient" in i[0]:
                sqlEnthaeltLebensmittel = "INSERT INTO `enthaeltLebensmittel` (`RezeptId`, `LebensmittelId`, `Menge`) VALUES (%s, %s, %s)"
                valEnthaeltLebensmittel = [
                    (recipeNumber, int(i[0][10:11]), i[1])
                ]
                mycursor.executemany(sqlEnthaeltLebensmittel, valEnthaeltLebensmittel)
                mydb.commit()
            if "recipe" in i[0]:
                sqlEnthaeltrezept = "INSERT INTO `enthaeltRezept` (`RezeptId`, `KomponentenRezeptId`, `Menge`) VALUES (%s, %s, %s)"
                valEnthaeltrezept = [
                    (recipeNumber, int(i[0][6:7]), i[1])
                ]
                mycursor.executemany(sqlEnthaeltrezept, valEnthaeltrezept)
                mydb.commit()

            # add ingredient to datalog
            ingredient = pyDatalog.ask(("hasID(X, Y, '" + i[0] + "')"))
            pyDatalog.assert_fact('containsIngredient', name, ingredient.answers[0][0], i[1])
        else:
            print(i[0] + " is no valid id")

    # add weight to datalog
    ingredients = pyDatalog.ask("containsIngredient('" + name + "', Y, Z)")
    weight = 0
    if not ingredients == None:
        for i in ingredients.answers:
            weight += i[1]
    pyDatalog.assert_fact('weightPerServing', name, weight)
    pyDatalog.assert_fact('hasCaloriesPer100g', name, getCaloriesPer100g(name))

    if mydb.is_connected():
        mycursor.close()
        mydb.close()
    return id

#print(getRecipesOrIngredients("ingredient", True, True, True, True, True))
#print(getRecipeDetails("recipe1"))

#print(addRecipe("RecipeName", [("ingredient1", 100), ("ingredient5", 20), ("recipe1", 200)], "Instruction"))
#print(getRecipesOrIngredients("recipe", False, False, False, False, False))
#print(getRecipeDetails("recipe4"))
#print(pyDatalog.ask("hasCaloriesPer100g(Y, Z)"))
#print(pyDatalog.ask("containsGluten(Y)"))
