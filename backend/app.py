from flask import Flask, request, jsonify
import os
import psycopg2
import json

app = Flask(__name__)
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = os.environ.get('DB_PORT', '5432')
DB_NAME = os.environ.get('DB_NAME', 'devdishes')
DB_USER = os.environ.get('DB_USER', 'devuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'supersecret')

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS recipes (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        ingredients TEXT NOT NULL,
        instructions TEXT NOT NULL
    )''')
    conn.commit()
    c.close()
    conn.close()

@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.get_json()
    name = data.get('name')
    ingredients = data.get('ingredients')
    instructions = data.get('instructions')
    if not all([name, ingredients, instructions]):
        return jsonify({'error': 'Missing fields'}), 400
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO recipes (name, ingredients, instructions) VALUES (%s, %s, %s)',
              (name, ingredients, instructions))
    conn.commit()
    c.close()
    conn.close()
    return jsonify({'message': 'Recipe added successfully'}), 201

@app.route('/recipes', methods=['GET'])
def get_recipes():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id, name, ingredients, instructions FROM recipes')
    rows = c.fetchall()
    c.close()
    conn.close()
    recipes = []
    for row in rows:
        try:
            ingredients = json.loads(row[2])
        except Exception:
            ingredients = row[2]
        try:
            instructions = json.loads(row[3])
        except Exception:
            instructions = row[3]
        recipes.append({
            'id': row[0],
            'name': row[1],
            'ingredients': ingredients,
            'instructions': instructions
        })
    return jsonify(recipes)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000) 