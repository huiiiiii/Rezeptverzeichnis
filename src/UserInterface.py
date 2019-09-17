import sys

from src.DatalogLogic import getRecipesOrIngredients, getRecipeDetails, isValidId, addRecipe

shouldExit = False

def printRecipeList(glutenFree, lactoseFree, vegan, vegetarian, lowCalorie):
    print(getRecipesOrIngredients("recipe", glutenFree, lactoseFree, vegan, vegetarian, lowCalorie))

def printAllIngredients():
    print("\nVerfügbare Zutaten sind:")
    print(getRecipesOrIngredients("ingredient", False, False, False, False, False))

def printRecipe(id):
    if isValidId(id) == None:
        print("This is no valid ID")
    print(getRecipeDetails(id))


print("Willkommen im Rezeptverzeichnis.")
print("Hier können alle Rezepte angezeigt werden. Die Auswahl der Rezepte kann durch verschiedene Kriterien eingeschränkt werden. \nFolgende Kriterien können ausgewählt werden: glutenfrei, lactosefrei, vegetarisch, vegan und kalorienarm. \nMit dem Befehl exit kann das Programm beendet werden.")
while not shouldExit:
    i = input("\nWelche Kriterien sollen die Rezepte erfüllen? ")
    if "exit" in i:
        shouldExit = True
        sys.exit(0)
    printRecipeList("glutenfrei" in i, "lactosefrei" in i, "vegan" in i, "vegetarisch" in i, "kalorienarm" in i)

    rezeptAnzeigen = input("\nSoll ein Rezept angezeigt weden (ja / nein) ?")
    if "exit" in rezeptAnzeigen:
        shouldExit = True
        sys.exit(0)
    while "ja" in rezeptAnzeigen:
        id = input("\nBitte geben Sie die ID des Rezepts ein (z.B. recipe1): ")
        printRecipe(id)
        rezeptAnzeigen = input("\nSoll ein weiteres Rezept angezeigt weden (ja / nein)?  ")
        if "exit" in rezeptAnzeigen:
            shouldExit = True
            sys.exit(0)

    rezeptAnlegen = input("\nSoll ein Rezept neu angelegt werden (ja / nein) ? ")
    if "exit" in rezeptAnlegen:
        shouldExit = True
        sys.exit(0)
    while "ja" in rezeptAnlegen:
        name = input("\nBitte geben Sie den Namen des Rezepts ein: ")
        ingredients = []
        printAllIngredients()
        zutatHinzufuegen = input("\nSoll eine Zutat hinzugefuegt werden (ja / nein) ? ")
        while "ja" in zutatHinzufuegen:
            zutatId = input("\nBitte geben Sie die id der Zutat ein (z.B. ingredient1): ")
            if isValidId(zutatId):
                zutatMenge = float(input("\nBitte geben Sie die Menge der Zutat in Gramm ein (z.B. 40): "))
                ingredients.append((zutatId, zutatMenge))
            else:
                print(zutatId + " + ist keine mögliche ID")
            zutatHinzufuegen = input("\nSoll eine Zutat hinzugefuegt werden (ja / nein) ? ")
        instructions = input("\nBitte geben Sie eine Anleitung für das Rezept ein: ")
        id = addRecipe(name, ingredients, instructions)
        print("\nRezept wurde gespeichert: ")
        printRecipe(id)
        rezeptAnlegen = input("\nSoll ein weiteres Rezept angelegt werden (ja / nein)? ")
        if "exit" in rezeptAnlegen:
            shouldExit = True
            sys.exit(0)
