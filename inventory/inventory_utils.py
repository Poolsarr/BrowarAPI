from pymongo import MongoClient
from bson import ObjectId
from flask import jsonify
from config import Config

client = MongoClient(Config.ATLAS_LOGIN)
db = client.Browar1
inventory = db.inventory

def get_all_inventory():
    all_inventory = list(inventory.find())
    for item in all_inventory:
        item["_id"] = str(item["_id"])
    return jsonify(all_inventory)

def create_inventory_item(request):
    data = request.json
    item = data.get('item')
    item_type = data.get('type')
    quantity = data.get('quantity')
    unit = data.get('unit')
    location = data.get('location')
    updated_at = data.get('updatedAt')

    inventory_item = {
        'item': item,
        'type': item_type,
        'quantity': quantity,
        'unit': unit,
        'location': location,
        'updatedAt': updated_at
    }
    result = inventory.insert_one(inventory_item)
    return jsonify({"message": "Inventory item created", "item_id": str(result.inserted_id)}), 201

def get_single_inventory_item(item_id):
    item = inventory.find_one({"_id": ObjectId(item_id)})
    if item:
        item["_id"] = str(item["_id"])
        return jsonify(item)
    return jsonify({"error": "Inventory item not found"}), 404

def update_inventory_item(item_id, request):
    data = request.json
    fields_to_update = ['item', 'type', 'quantity', 'unit', 'location', 'updatedAt']
    updated_item = {field: data[field] for field in fields_to_update if field in data}

    if updated_item:
        result = inventory.update_one(
            {"_id": ObjectId(item_id)}, 
            {"$set": updated_item}
        )
        if result.modified_count > 0:
            return jsonify({"message": "Inventory item updated"})
        return jsonify({"error": "No changes made"}), 400
    return jsonify({"error": "No data to update"}), 400

def delete_inventory_item(item_id):
        result = inventory.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count > 0:
            return jsonify({"message": "Inventory item deleted"})
        return jsonify({"error": "Inventory item not found"}), 404