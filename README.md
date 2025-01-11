# 🍺 Browar API

API stworzone przy użyciu **Python (Flask)** i **MongoDB** służące do zarządzania browarem. Umożliwia zarządzanie użytkownikami, partiami produkcyjnymi, stanem magazynowym oraz recepturami piwa.

## **Instalacja i uruchomienie**

1.  **Skonfiguruj środowisko:**
    *   Zainstaluj wymagane biblioteki:
        ```bash
        pip install -r requirements.txt
        ```
    *   Utwórz plik `.env` w głównym katalogu z następującymi zmiennymi:
        ```
        atlas_login=<TWÓJ_ADRES_MONGODB>
        jwt_key=<TWÓJ_SEKRET_JWT>
        ```
        *   `atlas_login` - adres połączenia z bazą danych MongoDB.
        *   `jwt_key` - sekretny klucz do generowania tokenów JWT.

2.  **Uruchom API:**
    *   Uruchom serwer za pomocą polecenia:
        ```bash
        python server.py
        ```

## Podstawowe Endpointy API

**Lista podstawowych endpointów:**

| Endpoint        | Opis                                                   |
| --------------- | ------------------------------------------------------ |
| `POST /register` | Rejestracja nowego użytkownika.                       |
| `POST /login`    | Logowanie użytkownika i uzyskanie tokena JWT.         |
| `GET /batches`   | Pobranie listy partii produkcyjnych.                |
|`GET /recipes`| Pobranie listy receptur.|
|`GET /inventory` | Pobranie listy przedmiotów w magazynie.|

Wszystkie endpointy są szczegółowo opisane poniżej:

-   [**Autoryzacja**](#autoryzacja-/)
    -   [Rejestracja](#rejestracja-)
    -   [Logowanie](#logowanie-)
-   [**Partie Produkcyjne**](#partie-produkcyjne-)
    -   [Pobierz Wszystkie Partie](#pobierz-wszystkie-partie-)
    -   [Utwórz Partię](#utwórz-partię-)
    -   [Pobierz Partię](#pobierz-partię-)
    -   [Aktualizuj Partię](#aktualizuj-partię-)
    -   [Usuń Partię](#usuń-partię-)
    -   [Pobierz Partię z Recepturą](#pobierz-partię-z-recepturą-)
-   [**Magazyn**](#magazyn-)
    -   [Pobierz Wszystkie Przedmioty](#pobierz-wszystkie-przedmioty-)
    -   [Utwórz Przedmiot](#utwórz-przedmiot-)
    -   [Pobierz Przedmiot](#pobierz-przedmiot-)
    -   [Aktualizuj Przedmiot](#aktualizuj-przedmiot-)
    -   [Usuń Przedmiot](#usuń-przedmiot-)
-   [**Receptury**](#receptury-)
    -   [Pobierz Wszystkie Receptury](#pobierz-wszystkie-receptury-)
    -   [Utwórz Recepturę](#utwórz-recepturę-)
    -   [Pobierz Recepturę](#pobierz-recepturę-)
    -   [Aktualizuj Recepturę](#aktualizuj-recepturę-)
    -   [Usuń Recepturę](#usuń-recepturę-)
-   [**Użytkownicy**](#użytkownicy-)
    -   [Pobierz Wszystkich Użytkowników](#pobierz-wszystkich-użytkowników-)

## Szczegóły API

### Autoryzacja (`/`) <a name="autoryzacja-/"></a>

#### `POST /register` <a name="rejestracja-"></a>

*   **Opis:** Rejestruje nowego użytkownika.
*   **Treść żądania (JSON):**
    ```json
    {
      "login": "nazwa_użytkownika",
      "password": "hasło_użytkownika"
    }
    ```
*   **Odpowiedź (201 Created):**
    ```json
    {
      "message": "Użytkownik <nazwa_użytkownika> został zarejestrowany"
    }
    ```
*   **Odpowiedź (400 Bad Request):**
    ```json
    {
      "error": "Podaj login i hasło"
    }
    ```
    ```json
    {
      "error": "Użytkownik o podanym loginie już istnieje"
    }
    ```

#### `POST /login` <a name="logowanie-"></a>

*   **Opis:** Loguje użytkownika i zwraca token JWT.
*   **Treść żądania (JSON):**
    ```json
    {
      "login": "nazwa_użytkownika",
      "password": "hasło_użytkownika"
    }
    ```
*   **Odpowiedź (200 OK):**
    ```json
    {
      "message": "Zalogowano pomyślnie!",
      "access_token": "token_jwt"
    }
    ```
*   **Odpowiedź (400 Bad Request):**
    ```json
    {
      "error": "Podaj login i hasło"
    }
    ```
*   **Odpowiedź (401 Unauthorized):**
    ```json
    {
      "error": "Nieprawidłowy login lub hasło"
    }
    ```

### Partie Produkcyjne (`/batches`) <a name="partie-produkcyjne-/"></a>

#### `GET /batches` <a name="pobierz-wszystkie-partie-"></a>

*   **Opis:** Pobiera listę wszystkich partii produkcyjnych.
*   **Nagłówki:** `Authorization: Bearer <token>`
*   **Odpowiedź (200 OK):**

    ```json
    [
        {
            "_id": "id_partii_1",
            "recipeId": "id_receptury_1",
            "startDate": "data_rozpoczęcia",
            "endDate": "data_zakończenia",
            "status": "status_partii",
            "volume": "objętość_partii",
            "notes": "notatki"
        },
        {
            "_id": "id_partii_2",
            "recipeId": "id_receptury_2",
            "startDate": "data_rozpoczęcia",
            "endDate": "data_zakończenia",
            "status": "status_partii",
            "volume": "objętość_partii",
            "notes": "notatki"
        }
    ]
    ```

#### `POST /batches` <a name="utwórz-partię-"></a>

*   **Opis:** Tworzy nową partię produkcyjną.
*   **Nagłówki:** `Authorization: Bearer <token>`
*   **Treść żądania (JSON):**

    ```json
    {
        "recipeId": "id_receptury",
        "startDate": "data_rozpoczęcia",
        "endDate": "data_zakończenia",
        "status": "status_partii",
        "volume": "objętość_partii",
        "notes": "notatki"
    }
    ```

*   **Odpowiedź (201 Created):**
    ```json
    {
        "message": "Partia utworzona",
        "batch_id": "id_nowej_partii"
    }
    ```

#### `GET /batches/<batch_id>` <a name="pobierz-partię-"></a>

*   **Opis:** Pobiera dane konkretnej partii produkcyjnej.
*   **Nagłówki:** `Authorization: Bearer <token>`
*   **Odpowiedź (200 OK):**

    ```json
    {
        "_id": "id_partii",
        "recipeId": "id_receptury",
        "startDate": "data_rozpoczęcia",
        "endDate": "data_zakończenia",
        "status": "status_partii",
        "volume": "objętość_partii",
        "notes": "notatki"
    }
    ```

*   **Odpowiedź (404 Not Found):**

    ```json
    {
        "error": "Nie znaleziono partii"
    }
    ```

#### `PUT /batches/<batch_id>` <a name="aktualizuj-partię-"></a>

*   **Opis:** Aktualizuje dane konkretnej partii produkcyjnej.
*   **Nagłówki:** `Authorization: Bearer <token>`
*   **Treść żądania (JSON):**

    ```json
    {
        "recipeId": "id_receptury",
        "startDate": "data_rozpoczęcia",
        "endDate": "data_zakończenia",
        "status": "status_partii",
        "volume": "objętość_partii",
        "notes": "notatki"
    }
    ```

*   **Odpowiedź (200 OK):**
    ```json
    {
        "message": "Partia zaktualizowana"
    }
    ```

*   **Odpowiedź (400 Bad Request):**

    ```json
    {
        "error": "Nie wprowadzono żadnych zmian"
    }
    ```
    ```json
    {
        "error": "Brak danych do aktualizacji"
    }
    ```

#### `DELETE /batches/<batch_id>` <a name="usuń-partię-"></a>

*   **Opis:** Usuwa konkretną partię produkcyjną.
*   **Nagłówki:** `Authorization: Bearer <token>`
*   **Odpowiedź (200 OK):**
    ```json
    {
        "message": "Partia usunięta"
    }
    ```
*   **Odpowiedź (404 Not Found):**
    ```json
    {
        "error": "Nie znaleziono partii"
    }
    ```
  
#### `GET /batches/<batch_id>/recipe` <a name="pobierz-partię-z-recepturą-"></a>

*   **Opis:** Pobiera dane konkretnej partii produkcyjnej wraz z danymi receptury.
*   **Nagłówki:** `Authorization: Bearer <token>`
*    **Odpowiedź (200 OK):**
        ```json
          {
            "_id": "id_partii",
            "recipeId": "id_receptury",
            "startDate": "data_rozpoczęcia",
            "endDate": "data_zakończenia",
            "status": "status_partii",
            "volume": "objętość_partii",
            "notes": "notatki",
            "recipe": {
                  "_id": "id_receptury",
                  "name": "nazwa_receptury",
                  "style": "styl_piwa",
                   "ingredients": "składniki",
                   "process": "proces_warzenia",
                   "createdAt": "data_utworzenia",
                   "updatedAt": "data_aktualizacji"
            }
         }
        ```
*   **Odpowiedź (404 Not Found):**
    ```json
    {
        "error": "Nie znaleziono partii"
    }
    ```

### Magazyn (`/inventory`) <a name="magazyn-/"></a>

#### `GET /inventory` <a name="pobierz-wszystkie-przedmioty-"></a>

*   **Opis:** Pobiera listę wszystkich przedmiotów w magazynie.
*  **Nagłówki:** `Authorization: Bearer <token>`
*   **Odpowiedź (200 OK):**

    ```json
    [
      {
        "_id": "id_pozycji_1",
        "item": "nazwa_przedmiotu_1",
        "type": "typ_przedmiotu_1",
        "quantity": "ilość_1",
        "unit": "jednostka_1",
        "location": "lokalizacja_1",
        "updatedAt": "data_aktualizacji"
      },
      {
        "_id": "id_pozycji_2",
        "item": "nazwa_przedmiotu_2",
        "type": "typ_przedmiotu_2",
        "quantity": "ilość_2",
        "unit": "jednostka_2",
        "location": "lokalizacja_2",
        "updatedAt": "data_aktualizacji"
      }
    ]
    ```

#### `POST /inventory` <a name="utwórz-przedmiot-"></a>

*   **Opis:** Tworzy nowy przedmiot w magazynie.
*  **Nagłówki:** `Authorization: Bearer <token>`
*   **Treść żądania (JSON):**

    ```json
    {
      "item": "nazwa_przedmiotu",
      "type": "typ_przedmiotu",
      "quantity": "ilość",
      "unit": "jednostka",
      "location": "lokalizacja",
      "updatedAt": "data_aktualizacji"
    }
    ```

*   **Odpowiedź (201 Created):**
    ```json
    {
      "message": "Przedmiot magazynowy utworzony",
      "item_id": "id_nowej_pozycji"
    }
    ```

#### `GET /inventory/<item_id>` <a name="pobierz-przedmiot-"></a>

*   **Opis:** Pobiera dane konkretnego przedmiotu w magazynie.
*  **Nagłówki:** `Authorization: Bearer <token>`
*   **Odpowiedź (200 OK):**

    ```json
    {
      "_id": "id_pozycji",
      "item": "nazwa_przedmiotu",
      "type": "typ_przedmiotu",
      "quantity": "ilość",
      "unit": "jednostka",
      "location": "lokalizacja",
      "updatedAt": "data_aktualizacji"
    }
    ```

*   **Odpowiedź (404 Not Found):**
    ```json
    {
       "error": "Nie znaleziono przedmiotu"
    }
    ```

#### `PUT /inventory/<item_id>` <a name="aktualizuj-przedmiot-"></a>

*   **Opis:** Aktualizuje dane konkretnego przedmiotu w magazynie.
*  **Nagłówki:** `Authorization: Bearer <token>`
*   **Treść żądania (JSON):**

    ```json
    {
      "item": "nazwa_przedmiotu",
      "type": "typ_przedmiotu",
      "quantity": "ilość",
      "unit": "jednostka",
      "location": "lokalizacja",
      "updatedAt": "data_aktualizacji"
    }
    ```

*   **Odpowiedź (200 OK):**
    ```json
    {
      "message": "Przedmiot magazynowy zaktualizowany"
    }
    ```

*   **Odpowiedź (400 Bad Request):**
    ```json
    {
        "error": "Nie wprowadzono żadnych zmian"
    }
    ```
    ```json
    {
        "error": "Brak danych do aktualizacji"
    }
    ```

#### `DELETE /inventory/<item_id>` <a name="usuń-przedmiot-"></a>

*   **Opis:** Usuwa konkretny przedmiot z magazynu.
*  **Nagłówki:** `Authorization: Bearer <token>`
*   **Odpowiedź (200 OK):**
    ```json
    {
      "message": "Przedmiot magazynowy usunięty"
    }
    ```

*   **Odpowiedź (404 Not Found):**
    ```json
    {
        "error": "Nie znaleziono przedmiotu"
    }
    ```

### Receptury (`/recipes`) <a name="receptury-/"></a>

#### `GET /recipes` <a name="pobierz-wszystkie-receptury-"></a>

*   **Opis:** Pobiera listę wszystkich receptur.
*  **Nagłówki:** `Authorization: Bearer <token>`
*   **Odpowiedź (200 OK):**

    ```json
    [
        {
          "_id": "id_receptury_1",
          "name": "nazwa_receptury_1",
          "style": "styl_piwa_1",
          "ingredients": "składniki_1",
          "process": "proces_warzenia_1",
          "createdAt": "data_utworzenia_1",
          "updatedAt": "data_aktualizacji_1"
        },
        {
          "_id": "id_receptury_2",
          "name": "nazwa_receptury_2",
          "style": "styl_piwa_2",
          "ingredients": "składniki_2",
          "process": "proces_warzenia_2",
          "createdAt": "data_utworzenia_2",
          "updatedAt": "data_aktualizacji_2"
        }
    ]
    ```

#### `POST /recipes` <a name="utwórz-recepturę-"></a>

*   **Opis:** Tworzy nową recepturę.
*  **Nagłówki:** `Authorization: Bearer <token>`
*   **Treść żądania (JSON):**

    ```json
    {
       "_id": "id_receptury(5 cyfr)",
       "name": "nazwa_receptury",
        "style": "styl_piwa",
        "ingredients": "składniki",
       "process": "proces_warzenia",
        "createdAt": "data_utworzenia",
        "updatedAt": "data_aktualizacji"
    }
    ```

*   **Odpowiedź (201 Created):**
    ```json
    {
      "message": "Receptura utworzona",
      "recipe_id": "id_nowej_receptury"
    }
    ```
*   **Odpowiedź (400 Bad Request):**
    ```json
    {
      "error": "ID musi być 5-cyfrowym numerem"
    }
    ```
    ```json
    {
       "error": "Receptura o podanym ID już istnieje"
    }
    ```

#### `GET /recipes/<recipe_id>` <a name="pobierz-recepturę-"></a>

*   **Opis:** Pobiera dane konkretnej receptury.
*  **Nagłówki:** `Authorization: Bearer <token>`
*   **Odpowiedź (200 OK):**

    ```json
    {
      "_id": "id_receptury",
      "name": "nazwa_receptury",
      "style": "styl_piwa",
      "ingredients": "składniki",
      "process": "proces_warzenia",
      "createdAt": "data_utworzenia",
      "updatedAt": "data_aktualizacji"
    }
    ```

*   **Odpowiedź (404 Not Found):**
    ```json
    {
        "error": "Nie znaleziono receptury"
    }
    ```

#### `PUT /recipes/<recipe_id>` <a name="aktualizuj-recepturę-"></a>

*   **Opis:** Aktualizuje dane konkretnej receptury.
*  **Nagłówki:** `Authorization: Bearer <token>`
*   **Treść żądania (JSON):**

    ```json
    {
      "name": "nazwa_receptury",
      "style": "styl_piwa",
      "ingredients": "składniki",
      "process": "proces_warzenia",
      "updatedAt": "data_aktualizacji"
    }
    ```

*   **Odpowiedź (200 OK):**
    ```json
    {
      "message": "Receptura zaktualizowana"
    }
    ```

*   **Odpowiedź (400 Bad Request):**
    ```json
    {
        "error": "Nie wprowadzono żadnych zmian"
    }
    ```
    ```json
    {
        "error": "Brak danych do aktualizacji"
    }
    ```

#### `DELETE /recipes/<recipe_id>` <a name="usuń-recepturę-"></a>

*   **Opis:** Usuwa konkretną recepturę.
*  **Nagłówki:** `Authorization: Bearer <token>`
*   **Odpowiedź (200 OK):**
    ```json
    {
      "message": "Receptura usunięta"
    }
    ```

*   **Odpowiedź (404 Not Found):**
    ```json
    {
        "error": "Nie znaleziono receptury"
    }
    ```

### Użytkownicy (`/users`) <a name="użytkownicy-/"></a>
  #### `GET /users` <a name="pobierz-wszystkich-użytkowników-"></a>

*   **Opis:** Pobiera listę wszystkich zarejestrowanych użytkowników.
*   **Nagłówki:** `Authorization: Bearer <token>`
*   **Odpowiedź (200 OK):**
       ```json
            [
              {
                "_id": "id_uzytkownika_1",
                 "login": "login_uzytkownika_1"
              },
             {
                "_id": "id_uzytkownika_2",
                "login": "login_uzytkownika_2"
             }
            ]
       ```
## Bezpieczeństwo API

-   Większość endpointów wymaga uwierzytelnienia za pomocą tokenu JWT.
-   Sekrety przechowywane są w pliku `.env`.
-   Token JWT jest uzyskiwany po zalogowaniu (`POST /login`).

## Technologie

*   Python
*   Flask
*   MongoDB
*   Flask-JWT-Extended
*   Bcrypt
