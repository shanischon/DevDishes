from flask import Flask, request, jsonify
import os
import psycopg2

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
        content TEXT NOT NULL,
        image TEXT
    )''')
    conn.commit()
    c.close()
    conn.close()

@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.get_json()
    name = data.get('name')
    content = data.get('content')
    image = data.get('image')
    if not all([name, content]):
        return jsonify({'error': 'Missing fields'}), 400
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO recipes (name, content, image) VALUES (%s, %s, %s) RETURNING id',
              (name, content, image))
    recipe_id = c.fetchone()[0]
    conn.commit()
    c.close()
    conn.close()
    return jsonify({'message': 'Recipe added successfully', 'id': recipe_id}), 201

@app.route('/recipes', methods=['GET'])
def get_recipes():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id, name, content, image FROM recipes')
    rows = c.fetchall()
    c.close()
    conn.close()
    recipes = []
    for row in rows:
        recipes.append({
            'id': row[0],
            'name': row[1],
            'content': row[2],
            'image': row[3]
        })
    return jsonify(recipes)

@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT id, name, content, image FROM recipes WHERE id = %s', (recipe_id,))
    row = c.fetchone()
    c.close()
    conn.close()
    if not row:
        return jsonify({'error': 'Recipe not found'}), 404
    recipe = {
        'id': row[0],
        'name': row[1],
        'content': row[2],
        'image': row[3]
    }
    return jsonify(recipe)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000) 