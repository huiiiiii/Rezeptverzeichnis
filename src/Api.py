from flask import Flask, jsonify
from flask_restful import Api, Resource

from src.DatalogLogic import getRecipesOrIngredients, donothing

app = Flask(__name__)
api = Api(app)

def getRecipeListAsJson():
    print(getRecipesOrIngredients("recipe", True, True, True, True, True))
    return 0


class Recipes(Resource):
    def get(self):
        getRecipeListAsJson()
        result = [
            {
                "id": "id0",
                "name": "rezeptname"
            },
            {
                "id": "id1",
                "name": "rezeptname1"
            },
            {
                "id": "id2",
                "name": "rezeptname2"
            }
        ]
        return jsonify(result)

    def post(self):
        recipe_id_new = 1
        return recipe_id_new, 201


class Recipes_Detail(Resource):
    def get(self, recipe_id):
        result = {
            "id": recipe_id,
            "name": "rezeptname",
            "ingredients": [
                {
                    "id": "id1",
                    "name": "zutatenname",
                    "amount": "45",
                    "unit": "gramm"
                },
                {
                    "id": "id2",
                    "name": "zutatenname2",
                    "amount": "10",
                    "unit": "gramm"
                }
            ],
            "instruction": "tue dies und das",
            "caloriePer100g":"200",
            "allergens": [
                "Gluten", "Tierprodukt"
            ]
        }
        return jsonify(result)


api.add_resource(Recipes, '/recipes')
api.add_resource(Recipes_Detail, '/recipes/<recipe_id>')
getRecipeListAsJson()

if __name__ == '__main__':
    app.run(port='5002')
