from flask import Flask, render_template, request, jsonify, session
from matching import get_recommendation
from database import get_connection, initialize_database, seed_stores
import os

app = Flask(__name__)
app.secret_key = "grocery_tracker_secret_key"
from scheduler import start_scheduler
scheduler = start_scheduler()

@app.route('/')
def home():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.id, s.name, us.selected
        FROM stores s
        JOIN user_stores us ON s.id = us.store_id
    ''')
    stores = cursor.fetchall()
    conn.close()
    return render_template('index.html', stores=stores)

@app.route('/update-stores', methods=['POST'])
def update_stores():
    selected_stores = request.form.getlist('stores')
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE user_stores SET selected = 0")
    for store_id in selected_stores:
        cursor.execute(
            "UPDATE user_stores SET selected = 1 WHERE store_id = ?",
            (store_id,)
        )
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

@app.route('/list')
def grocery_list():
    return render_template('list.html')

@app.route('/results', methods=['POST'])
def results():
    raw_input = request.form.get('grocery_list', '')
    items = [item.strip() for item in raw_input.split(',') if item.strip()]
    
    if not items:
        return render_template('list.html', error="Please enter at least one item!")
    
    recommendation = get_recommendation(items)
    
    return render_template('results.html', 
                         recommendation=recommendation,
                         grocery_items=items)

if __name__ == '__main__':
    initialize_database()
    seed_stores()
    app.run(debug=True)