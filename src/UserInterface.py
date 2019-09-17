from src.DatalogLogic import getRecipesOrIngredients, getRecipeDetails, isValidId

shouldExit = False

def getRecipeListAsJson(glutenFree, lactoseFree, vegan, vegetarian, lowCalorie):
    return getRecipesOrIngredients("recipe", glutenFree, lactoseFree, vegan, vegetarian, lowCalorie)

def getRecipeAsJson(id):
    if isValidId(id) == None:
        return "This is no valid ID"
    return getRecipeDetails(id)


print("Willkommen im Rezeptverzeichnis.")
print("Hier können alle Rezepte angezeigt werden. Die Auswahl der Rezepte kann durch verschiedene Kriterien eingeschränkt werden. \nFolgende Kriterien können ausgewählt werden: glutenfrei, lactosefrei, vegetarisch, vegan und kalorienarm. \nMit dem Befehl exit kann das Programm beendet werden.")
while not shouldExit:
    i = input("\nWelche Kriterien sollen die Rezepte erfüllen? ")
    if "exit" in i:
        shouldExit = True
        break
    print(getRecipeListAsJson("glutenfrei" in i, "lactosefrei" in i, "vegan" in i, "vegetarisch" in i, "kalorienarm" in i))
    i = input("\nSoll ein Rezept angezeigt weden (ja / nein) ?")
    while "ja" in i:
        id = input("\nBitte geben Sie die ID des Rezepts ein: ")
        print(getRecipeAsJson(id))
        i = input("\nSoll ein weiteres Rezept angezeigt weden (ja / nein)? ")