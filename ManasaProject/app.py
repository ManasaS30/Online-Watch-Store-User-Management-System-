from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# SQLite database
DATABASE = os.path.join(os.path.dirname(__file__), "users.db")

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# CREATE - Add user
@app.route('/users', methods=['POST'])
def add_users():
    data = request.get_json()
    name = data['name']
    email = data['email']
    contact = data['contact']
    address = data['address']
    city = data['city']
    state = data['state']
   
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO users(name, email, contact,address,city,state) VALUES (?,?,?,?,?,?)",
        (name, email, contact,address,city,state)
    )
    conn.commit()
    conn.close()
    return jsonify({
        "message": "User added successfully"
    }), 201

# READ - Get All users
@app.route('/users', methods=['GET'])
def get_users():
    conn = get_db_connection()
    users = conn.execute(
        "SELECT * FROM users"
    ).fetchall()
    conn.close()
    result = []
    for user in users:
        result.append({
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "contact": user["contact"],
            "address": user["address"],
            "city": user["city"],
            "state": user["state"],
        })
    return jsonify(result), 200

# UPDATE - Update User
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    name = data['name']
    email = data['email']
    contact = data['contact']
    address = data['address']
    city = data['city']
    state = data['state']
   
    conn = get_db_connection()
    conn.execute(
        """UPDATE users
           SET name = ?, email = ?, contact = ?,address = ?,city = ?,state=?
           WHERE id = ?""",
        (name, email, contact,address,city,state,id)
    )
    conn.commit()
    conn.close()
    return jsonify({
        "message": "User updated successfully"
    }), 200

# DELETE - Delete user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = get_db_connection()
    conn.execute(
        "DELETE FROM users WHERE id = ?",
        (id,)
    )
    conn.commit()
    conn.close()
    return jsonify({
        "message": "Users deleted successfully"
    }), 200

if __name__ == '__main__':
    app.run(debug=True)

