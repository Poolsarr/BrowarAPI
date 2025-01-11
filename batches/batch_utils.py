from pymongo import MongoClient
from bson import ObjectId
from flask import jsonify
from config import Config

client = MongoClient(Config.ATLAS_LOGIN)
db = client.Browar1
batches = db.batches
recipes = db.recipes

def get_all_batches():
    all_batches = list(batches.find())
    for batch in all_batches:
        batch["_id"] = str(batch["_id"])
    return jsonify(all_batches)

def create_batch(request):
    data = request.json
    recipe_id = data.get('recipeId')
    start_date = data.get('startDate')
    end_date = data.get('endDate')
    status = data.get('status')
    volume = data.get('volume')
    notes = data.get('notes')

    batch = {
        'recipeId': recipe_id,
        'startDate': start_date,
        'endDate': end_date,
        'status': status,
        'volume': volume,
        'notes': notes
    }
    result = batches.insert_one(batch)
    return jsonify({"message": "Batch created", "batch_id": str(result.inserted_id)}), 201

def get_single_batch(batch_id):
    batch = batches.find_one({"_id": ObjectId(batch_id)})
    if batch:
        batch["_id"] = str(batch["_id"]) 
        return jsonify(batch)
    return jsonify({"error": "Batch not found"}), 404

def update_batch(batch_id, request):
    data = request.json
    fields_to_update = ['recipeId', 'startDate', 'endDate', 'status', 'volume', 'notes']
    updated_batch = {field: data[field] for field in fields_to_update if field in data}

    if updated_batch:
        result = batches.update_one(
            {"_id": ObjectId(batch_id)}, 
            {"$set": updated_batch}
        )
        if result.modified_count > 0:
            return jsonify({"message": "Batch updated"})
        return jsonify({"error": "No changes made"}), 400
    return jsonify({"error": "No data to update"}), 400

def delete_batch(batch_id):
    result = batches.delete_one({"_id": ObjectId(batch_id)})
    if result.deleted_count > 0:
        return jsonify({"message": "Batch deleted"})
    return jsonify({"error": "Batch not found"}), 404

def get_batch_with_recipe(batch_id):
    try:
        print("Batch id:", batch_id)
        batch = batches.find_one({"_id": ObjectId(batch_id)})
        if not batch:
              print("Nie znaleziono batcha o id", batch_id)
              return jsonify({"error": "Batch not found"}), 404
        print ("Znaleziono batch", batch)

        batch = batches.aggregate([
            {
                "$match": {
                    "_id": ObjectId(batch_id)
                }
            },
            {
                "$lookup": {
                    "from": "recipes",
                    "localField": "recipeId",
                    "foreignField": "_id",
                    "as": "recipe"
                }
            },
            {
                "$unwind": "$recipe"
            }
        ])
       
        batch = list(batch)
        if not batch:
             return jsonify({"error": "Batch not found"}), 404

        batch_data = batch[0]
        batch_data["_id"] = str(batch_data["_id"])
        batch_data["recipe"]["_id"] = str(batch_data["recipe"]["_id"])
        return jsonify(batch_data), 200
    except Exception as e:
          print("Błąd:", str(e))
          return jsonify({"error": str(e)}), 500