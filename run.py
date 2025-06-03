from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

DB_CONFIG = {
    "host":     "localhost",
    "database": "bankdb",
    "user":     "mhz351",
    "password": "Magnum99"
}

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (%s) RETURNING id, name, balance;", (name,))
    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": user[0], "name": user[1], "balance": float(user[2])}), 201

@app.route("/users", methods=["GET"])
def list_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, balance FROM users;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    users = [{"id": r[0], "name": r[1], "balance": float(r[2])} for r in rows]
    return jsonify(users), 200

@app.route("/deposit", methods=["POST"])
def deposit():
    data = request.get_json()
    user_id = data.get("user_id")
    amount = data.get("amount")
    if not user_id or not amount:
        return jsonify({"error": "user_id and amount are required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET balance = balance + %s WHERE id = %s RETURNING balance;", (amount, user_id))
    result = cur.fetchone()
    if result is None:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"error": "User not found"}), 404

    new_balance = result[0]
    # Optionally record the transaction:
    cur.execute(
        "INSERT INTO transactions (user_id, amount, type) VALUES (%s, %s, %s);",
        (user_id, amount, "deposit")
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": user_id, "new_balance": float(new_balance)}), 200

@app.route("/", methods=["GET"])
def index():
    return "Bank App API is running. Use /users and /deposit endpoints.", 200


if __name__ == "__main__":
    app.run(debug=True)

