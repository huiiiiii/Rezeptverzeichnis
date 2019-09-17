from pyDatalog import pyDatalog
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# define a base class with SQLAlchemy and pyDatalog capabilities
Base = declarative_base(cls=pyDatalog.Mixin, metaclass=pyDatalog.sqlMetaMixin)
engine = create_engine('mysql://user:test@localhost/recipeDatabase')
# open a session on a database, then associate it to the Base class
Session = sessionmaker(bind=engine)
session = Session()
Base.session = session
Base.metadata.bind = engine

class Recipe(Base):
    __tablename__ = 'Rezepte'
    __table_args__ = {'autoload':True}
    def __repr__(self):
        return self.Name

class Ingredient(Base):
    __tablename__ = 'Lebensmittel'
    __table_args__ = {'autoload':True}
    def __repr__(self):
        return self.Name

class containRecipe(Base):
    __tablename__ = 'enthaeltRezept'
    __table_args__ = {'autoload':True}

class containIngredient(Base):
    __tablename__ = 'enthaeltLebensmittel'
    __table_args__ = {'autoload':True}

pyDatalog.create_terms('I, A, X, Y, Z, N')

# get all ingredients of an recipe
pyDatalog.create_terms('hasIngredient, recipeIngredients')
hasIngredient(X, Y, Z) <= (containIngredient.RezeptId[A] == X) & (containIngredient.LebensmittelId[A] == Y) & (containIngredient.Menge[A] == Z)
Recipe.recipeIngredients(X, Y) <= (containRecipe.RezeptId[A] == X) & (containRecipe.KomponentenRezeptId[A] == Z) & (Recipe.hasIngredient(Z, Y))
# get weight of recipe
pyDatalog.create_terms('weight')
#weight(X) <=

# get Calories of Recipes
pyDatalog.create_terms('calorie')
#calorie(X) <=



Y = pyDatalog.Variable()
Ingredient.Fleisch[Y] == 0
print(Y)

X = pyDatalog.Variable()
Recipe.Name[X] == "Pizzateig"
print(X)

result = pyDatalog.ask('hasIngredient(X, Y, Z)')
print(result)






pyDatalog.create_terms('ingredient, contains')
pyDatalog.create_terms('allergenList, freeFrom')

pyDatalog.assert_fact('ingredient', 'Mehl')
pyDatalog.assert_fact('ingredient', 'Nudeln')
pyDatalog.assert_fact('contains', 'Mehl', 'Gluten')
pyDatalog.assert_fact('contains', 'Nudeln', 'Mehl')

contains(I, A) <= contains(I, X) & contains(X, A)

print(pyDatalog.ask('contains(I, A)'))

#freeFrom(allergenList[N]) <= not(contains(I, allergenList[N])) & freeFrom(allergenList[N-1])