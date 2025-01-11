from flask import Flask
from config import Config
from auth.auth_routes import auth_bp
from batches.batch_routes import batch_bp
from inventory.inventory_routes import inventory_bp
from recipes.recipe_routes import recipe_bp
from users.user_routes import user_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

# Rejestracja blueprintów
app.register_blueprint(auth_bp)
app.register_blueprint(batch_bp)
app.register_blueprint(inventory_bp)
app.register_blueprint(recipe_bp)
app.register_blueprint(user_bp)


if __name__ == "__main__":
    app.run(debug=True)