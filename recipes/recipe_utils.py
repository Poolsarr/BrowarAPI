from pymongo import MongoClient
from flask import jsonify
from config import Config

client = MongoClient(Config.ATLAS_LOGIN)
db = client.Browar1
recipes = db.recipes

def get_all_recipes():
    all_recipes = list(recipes.find())
    for recipe in all_recipes:
        recipe["_id"] = str(recipe["_id"])
    return jsonify(all_recipes)

def create_recipe(request):
    data = request.json
    recipe_id = data.get('_id')
    name = data.get('name')
    style = data.get('style')
    ingredients = data.get('ingredients')
    process = data.get('process')
    created_at = data.get('createdAt')
    updated_at = data.get('updatedAt')

    # Walidacja ID (musi być 5 cyfr)
    if not recipe_id or not recipe_id.isdigit() or len(recipe_id) != 5:
        return jsonify({"error": "ID musi być 5-cyfrowym numerem"}), 400

    if recipes.find_one({"_id": recipe_id}):
        return jsonify({"error": "Receptura o podanym ID już istnieje"}), 400

    # Dodanie nowej receptury
    recipe = {
        "_id": recipe_id,
        "name": name,
        "style": style,
        "ingredients": ingredients,
        "process": process,
        "createdAt": created_at,
        "updatedAt": updated_at
    }
    recipes.insert_one(recipe)
    return jsonify({"message": "Recipe created", "recipe_id": recipe_id}), 201

def get_single_recipe(recipe_id):
    recipe = recipes.find_one({"_id": recipe_id})
    if recipe:
        recipe["_id"] = str(recipe["_id"])
        return jsonify(recipe)
    return jsonify({"error": "Recipe not found"}), 404

def update_recipe(recipe_id, request):
    data = request.json
    fields_to_update = ['name', 'style', 'ingredients', 'process', 'updatedAt']
    updated_recipe = {field: data[field] for field in fields_to_update if field in data}

    if updated_recipe:
        result = recipes.update_one(
            {"_id": recipe_id}, 
            {"$set": updated_recipe}
        )
        if result.modified_count > 0:
            return jsonify({"message": "Recipe updated"})
        return jsonify({"error": "No changes made"}), 400
    return jsonify({"error": "No data to update"}), 400

def delete_recipe(recipe_id):
    result = recipes.delete_one({"_id": recipe_id})
    if result.deleted_count > 0:
        return jsonify({"message": "Recipe deleted"})
    return jsonify({"error": "Recipe not found"}), 404