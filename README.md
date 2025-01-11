# 🍺 BrowarAPI

This API, built using **Python (Flask)** and **MongoDB**, is designed for managing a brewery. It allows for the management of users, production batches, inventory, and beer recipes.

## **Installation and Setup**

1.  **Configure Environment:**
    *   Install required libraries:
        ```bash
        pip install -r requirements.txt
        ```
    *   Create a `.env` file in the root directory with the following variables:
        ```
        atlas_login=<YOUR_MONGODB_ADDRESS>
        jwt_key=<YOUR_JWT_SECRET>
        ```
        *   `atlas_login` - The connection address to your MongoDB database.
        *   `jwt_key` - The secret key for generating JWT tokens.

2.  **Run the API:**
    *   Start the server using the command:
        ```bash
        python server.py
        ```

## Basic API Endpoints

**List of Basic Endpoints:**

| Endpoint        | Description                                        |
| --------------- | -------------------------------------------------- |
| `POST /register` | Register a new user.                              |
| `POST /login`    | Log in a user and obtain a JWT token.              |
| `GET /batches`   | Get a list of production batches.                  |
|`GET /recipes`| Get a list of recipes.|
|`GET /inventory` | Get a list of inventory items.|

All endpoints are described in detail below:

-   [**Authentication**](#authentication-/)
    -   [Registration](#registration-)
    -   [Login](#login-)
-   [**Production Batches**](#production-batches-)
    -   [Get All Batches](#get-all-batches-)
    -   [Create Batch](#create-batch-)
    -   [Get Batch](#get-batch-)
    -   [Update Batch](#update-batch-)
    -   [Delete Batch](#delete-batch-)
    -    [Get Batch with Recipe](#get-batch-with-recipe-)
-   [**Inventory**](#inventory-)
    -   [Get All Items](#get-all-items-)
    -   [Create Item](#create-item-)
    -   [Get Item](#get-item-)
    -   [Update Item](#update-item-)
    -   [Delete Item](#delete-item-)
-   [**Recipes**](#recipes-)
    -   [Get All Recipes](#get-all-recipes-)
    -   [Create Recipe](#create-recipe-)
    -   [Get Recipe](#get-recipe-)
    -   [Update Recipe](#update-recipe-)
    -   [Delete Recipe](#delete-recipe-)
-   [**Users**](#users-)
     - [Get All Users](#get-all-users-)

## API Details

### Authentication (`/`) <a name="authentication-/"></a>

#### `POST /register` <a name="registration-"></a>

*   **Description:** Registers a new user.
*   **Request Body (JSON):**
    ```json
    {
      "login": "username",
      "password": "user_password"
    }
    ```
*   **Response (201 Created):**
    ```json
    {
      "message": "User <username> has been registered"
    }
    ```
*   **Response (400 Bad Request):**
    ```json
    {
      "error": "Please provide login and password"
    }
    ```
    ```json
    {
      "error": "User with provided login already exists"
    }
    ```

#### `POST /login` <a name="login-"></a>

*   **Description:** Logs in a user and returns a JWT token.
*   **Request Body (JSON):**
    ```json
    {
      "login": "username",
      "password": "user_password"
    }
    ```
*   **Response (200 OK):**
    ```json
    {
      "message": "Logged in successfully!",
      "access_token": "jwt_token"
    }
    ```
*   **Response (400 Bad Request):**
    ```json
    {
      "error": "Please provide login and password"
    }
    ```
*   **Response (401 Unauthorized):**
    ```json
    {
      "error": "Invalid login or password"
    }
    ```

### Production Batches (`/batches`) <a name="production-batches-/"></a>

#### `GET /batches` <a name="get-all-batches-"></a>

*   **Description:** Retrieves a list of all production batches.
*   **Headers:** `Authorization: Bearer <token>`
*   **Response (200 OK):**

    ```json
    [
        {
            "_id": "batch_id_1",
            "recipeId": "recipe_id_1",
            "startDate": "start_date",
            "endDate": "end_date",
            "status": "batch_status",
            "volume": "batch_volume",
            "notes": "notes"
        },
        {
            "_id": "batch_id_2",
            "recipeId": "recipe_id_2",
            "startDate": "start_date",
            "endDate": "end_date",
            "status": "batch_status",
            "volume": "batch_volume",
            "notes": "notes"
        }
    ]
    ```

#### `POST /batches` <a name="create-batch-"></a>

*   **Description:** Creates a new production batch.
*   **Headers:** `Authorization: Bearer <token>`
*   **Request Body (JSON):**

    ```json
    {
        "recipeId": "recipe_id",
        "startDate": "start_date",
        "endDate": "end_date",
        "status": "batch_status",
        "volume": "batch_volume",
        "notes": "notes"
    }
    ```

*   **Response (201 Created):**
    ```json
    {
        "message": "Batch created",
        "batch_id": "new_batch_id"
    }
    ```

#### `GET /batches/<batch_id>` <a name="get-batch-"></a>

*   **Description:** Retrieves data for a specific production batch.
*   **Headers:** `Authorization: Bearer <token>`
*   **Response (200 OK):**

    ```json
    {
        "_id": "batch_id",
        "recipeId": "recipe_id",
        "startDate": "start_date",
        "endDate": "end_date",
        "status": "batch_status",
        "volume": "batch_volume",
        "notes": "notes"
    }
    ```

*   **Response (404 Not Found):**

    ```json
    {
        "error": "Batch not found"
    }
    ```

#### `PUT /batches/<batch_id>` <a name="update-batch-"></a>

*   **Description:** Updates data for a specific production batch.
*  **Headers:** `Authorization: Bearer <token>`
*   **Request Body (JSON):**

    ```json
    {
        "recipeId": "recipe_id",
        "startDate": "start_date",
        "endDate": "end_date",
        "status": "batch_status",
        "volume": "batch_volume",
        "notes": "notes"
    }
    ```

*   **Response (200 OK):**
    ```json
    {
        "message": "Batch updated"
    }
    ```

*   **Response (400 Bad Request):**

    ```json
    {
        "error": "No changes were made"
    }
    ```
    ```json
    {
      "error": "No data for update"
    }
    ```

#### `DELETE /batches/<batch_id>` <a name="delete-batch-"></a>

*   **Description:** Deletes a specific production batch.
*  **Headers:** `Authorization: Bearer <token>`
*   **Response (200 OK):**
    ```json
    {
        "message": "Batch deleted"
    }
    ```
*   **Response (404 Not Found):**
    ```json
    {
        "error": "Batch not found"
    }
    ```

#### `GET /batches/<batch_id>/recipe` <a name="get-batch-with-recipe-"></a>

*   **Description:** Retrieves a specific production batch with recipe data.
*   **Headers:** `Authorization: Bearer <token>`
*    **Response (200 OK):**
        ```json
          {
            "_id": "batch_id",
            "recipeId": "recipe_id",
            "startDate": "start_date",
            "endDate": "end_date",
            "status": "batch_status",
            "volume": "batch_volume",
            "notes": "notes",
            "recipe": {
                  "_id": "recipe_id",
                  "name": "recipe_name",
                  "style": "beer_style",
                   "ingredients": "ingredients",
                   "process": "brewing_process",
                   "createdAt": "created_at_date",
                   "updatedAt": "updated_at_date"
            }
         }
        ```
*   **Response (404 Not Found):**
    ```json
    {
        "error": "Batch not found"
    }
    ```

### Inventory (`/inventory`) <a name="inventory-/"></a>

#### `GET /inventory` <a name="get-all-items-"></a>

*   **Description:** Retrieves a list of all items in the inventory.
*  **Headers:** `Authorization: Bearer <token>`
*   **Response (200 OK):**

    ```json
    [
      {
        "_id": "item_id_1",
        "item": "item_name_1",
        "type": "item_type_1",
        "quantity": "quantity_1",
        "unit": "unit_1",
        "location": "location_1",
        "updatedAt": "updated_at_date"
      },
      {
        "_id": "item_id_2",
        "item": "item_name_2",
        "type": "item_type_2",
        "quantity": "quantity_2",
        "unit": "unit_2",
        "location": "location_2",
        "updatedAt": "updated_at_date"
      }
    ]
    ```

#### `POST /inventory` <a name="create-item-"></a>

*   **Description:** Creates a new item in the inventory.
*  **Headers:** `Authorization: Bearer <token>`
*   **Request Body (JSON):**

    ```json
    {
      "item": "item_name",
      "type": "item_type",
      "quantity": "quantity",
      "unit": "unit",
      "location": "location",
      "updatedAt": "updated_at_date"
    }
    ```

*   **Response (201 Created):**
    ```json
    {
      "message": "Inventory item created",
      "item_id": "new_item_id"
    }
    ```

#### `GET /inventory/<item_id>` <a name="get-item-"></a>

*   **Description:** Retrieves data for a specific item in the inventory.
*  **Headers:** `Authorization: Bearer <token>`
*   **Response (200 OK):**

    ```json
    {
      "_id": "item_id",
      "item": "item_name",
      "type": "item_type",
      "quantity": "quantity",
      "unit": "unit",
      "location": "location",
      "updatedAt": "updated_at_date"
    }
    ```

*   **Response (404 Not Found):**
    ```json
    {
       "error": "Item not found"
    }
    ```

#### `PUT /inventory/<item_id>` <a name="update-item-"></a>

*   **Description:** Updates data for a specific item in the inventory.
*  **Headers:** `Authorization: Bearer <token>`
*   **Request Body (JSON):**

    ```json
    {
      "item": "item_name",
      "type": "item_type",
      "quantity": "quantity",
      "unit": "unit",
      "location": "location",
      "updatedAt": "updated_at_date"
    }
    ```

*   **Response (200 OK):**
    ```json
    {
      "message": "Inventory item updated"
    }
    ```

*   **Response (400 Bad Request):**
    ```json
    {
        "error": "No changes were made"
    }
    ```
    ```json
    {
        "error": "No data for update"
    }
    ```

#### `DELETE /inventory/<item_id>` <a name="delete-item-"></a>

*   **Description:** Deletes a specific item from the inventory.
*  **Headers:** `Authorization: Bearer <token>`
*   **Response (200 OK):**
    ```json
    {
      "message": "Inventory item deleted"
    }
    ```

*   **Response (404 Not Found):**
    ```json
    {
        "error": "Item not found"
    }
    ```

### Recipes (`/recipes`) <a name="recipes-/"></a>

#### `GET /recipes` <a name="get-all-recipes-"></a>

*   **Description:** Retrieves a list of all recipes.
*  **Headers:** `Authorization: Bearer <token>`
*   **Response (200 OK):**

    ```json
    [
        {
          "_id": "recipe_id_1",
          "name": "recipe_name_1",
          "style": "beer_style_1",
          "ingredients": "ingredients_1",
          "process": "brewing_process_1",
          "createdAt": "created_at_date_1",
          "updatedAt": "updated_at_date_1"
        },
        {
          "_id": "recipe_id_2",
          "name": "recipe_name_2",
          "style": "beer_style_2",
          "ingredients": "ingredients_2",
          "process": "brewing_process_2",
          "createdAt": "created_at_date_2",
          "updatedAt": "updated_at_date_2"
        }
    ]
    ```

#### `POST /recipes` <a name="create-recipe-"></a>

*   **Description:** Creates a new recipe.
*  **Headers:** `Authorization: Bearer <token>`
*   **Request Body (JSON):**

    ```json
    {
       "_id": "recipe_id(5 digits)",
       "name": "recipe_name",
        "style": "beer_style",
        "ingredients": "ingredients",
       "process": "brewing_process",
        "createdAt": "created_at_date",
        "updatedAt": "updated_at_date"
    }
    ```

*   **Response (201 Created):**
    ```json
    {
      "message": "Recipe created",
      "recipe_id": "new_recipe_id"
    }
    ```
*   **Response (400 Bad Request):**
     ```json
    {
      "error": "ID must be a 5-digit number"
    }
    ```
    ```json
    {
       "error": "Recipe with the provided ID already exists"
    }
    ```

#### `GET /recipes/<recipe_id>` <a name="get-recipe-"></a>

*   **Description:** Retrieves data for a specific recipe.
*  **Headers:** `Authorization: Bearer <token>`
*   **Response (200 OK):**

    ```json
    {
      "_id": "recipe_id",
      "name": "recipe_name",
      "style": "beer_style",
      "ingredients": "ingredients",
      "process": "brewing_process",
      "createdAt": "created_at_date",
      "updatedAt": "updated_at_date"
    }
    ```

*   **Response (404 Not Found):**
    ```json
    {
        "error": "Recipe not found"
    }
    ```

#### `PUT /recipes/<recipe_id>` <a name="update-recipe-"></a>

*   **Description:** Updates data for a specific recipe.
*  **Headers:** `Authorization: Bearer <token>`
*   **Request Body (JSON):**

    ```json
    {
      "name": "recipe_name",
      "style": "beer_style",
      "ingredients": "ingredients",
      "process": "brewing_process",
      "updatedAt": "updated_at_date"
    }
    ```

*   **Response (200 OK):**
    ```json
    {
      "message": "Recipe updated"
    }
    ```

*   **Response (400 Bad Request):**
    ```json
    {
        "error": "No changes were made"
    }
    ```
    ```json
    {
        "error": "No data for update"
    }
    ```

#### `DELETE /recipes/<recipe_id>` <a name="delete-recipe-"></a>

*   **Description:** Deletes a specific recipe.
*  **Headers:** `Authorization: Bearer <token>`
*   **Response (200 OK):**
    ```json
    {
      "message": "Recipe deleted"
    }
    ```

*   **Response (404 Not Found):**
    ```json
    {
        "error": "Recipe not found"
    }
    ```

### Users (`/users`) <a name="users-/"></a>
  #### `GET /users` <a name="get-all-users-"></a>

*   **Description:** Retrieves a list of all registered users.
*   **Headers:** `Authorization: Bearer <token>`
*   **Response (200 OK):**
       ```json
            [
              {
                "_id": "user_id_1",
                 "login": "user_login_1"
              },
             {
                "_id": "user_id_2",
                "login": "user_login_2"
             }
            ]
       ```
## API Security

-   Most endpoints require authentication using a JWT token.
-   Secrets are stored in a `.env` file.
-   The JWT token is obtained after logging in (`POST /login`).

## Technologies

*   Python
*   Flask
*   MongoDB
*   Flask-JWT-Extended
*   Bcrypt
