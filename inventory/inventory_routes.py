from flask import Blueprint, request, jsonify
from inventory.inventory_utils import get_all_inventory, create_inventory_item, get_single_inventory_item, update_inventory_item, delete_inventory_item
from flask_jwt_extended import jwt_required

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route("", methods=["GET", "POST"])
@jwt_required()
def inventory_route():
    if request.method == "GET":
        return get_all_inventory()
    if request.method == "POST":
        return create_inventory_item(request)

@inventory_bp.route("/<item_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def single_inventory(item_id):
    if request.method == "GET":
        return get_single_inventory_item(item_id)
    if request.method == "PUT":
        return update_inventory_item(item_id, request)
    if request.method == "DELETE":
        return delete_inventory_item(item_id)