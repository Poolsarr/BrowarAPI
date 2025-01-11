from flask import Blueprint, request, jsonify
from batches import batch_utils
from flask_jwt_extended import jwt_required

batch_bp = Blueprint('batches', __name__, url_prefix='/batches')

@batch_bp.route("", methods=["GET", "POST"])
@jwt_required()
def batches_route():
    if request.method == "GET":
        return batch_utils.get_all_batches()
    if request.method == "POST":
        return batch_utils.create_batch(request)

@batch_bp.route("/<batch_id>", methods=["GET", "PUT", "DELETE"])
@jwt_required()
def single_batch(batch_id):
    if request.method == "GET":
        return batch_utils.get_single_batch(batch_id)
    if request.method == "PUT":
        return batch_utils.update_batch(batch_id, request)
    if request.method == "DELETE":
        return batch_utils.delete_batch(batch_id)

@batch_bp.route("/<batch_id>/recipe", methods=["GET"])
@jwt_required()
def get_batch_with_recipe(batch_id):
    return batch_utils.get_batch_with_recipe(batch_id)