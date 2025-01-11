from flask import Blueprint, request, jsonify
from recipes.recipe_utils import get_all_recipes, create_recipe, get_single_recipe, update_recipe, delete_recipe
from flask_jwt_extended import jwt_required

recipe_bp = Blueprint('recipes', __name__, url_prefix='/recipes')

@recipe_bp.route("", methods=["GET", "POST"])
@jwt_required()
def recipes_route():
    if request.method == "GET":
        return get_all_recipes()
    if request.method == "POST":
        return create_recipe(request)

@recipe_bp.route("/<recipe_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def single_recipe(recipe_id):
    if request.method == "GET":
        return get_single_recipe(recipe_id)
    if request.method == "PUT":
        return update_recipe(recipe_id, request)
    if request.method == "DELETE":
        return delete_recipe(recipe_id)