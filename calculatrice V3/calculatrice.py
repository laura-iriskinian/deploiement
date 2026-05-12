import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database=os.environ.get("DB_NAME", "calculatrice"),
        user=os.environ.get("DB_USER", "calc"),
        password=os.environ.get("DB_PASSWORD", "calc"),
    )

def init_db():
    conn = get_db()
    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id SERIAL PRIMARY KEY,
                    expression TEXT NOT NULL,
                    result DOUBLE PRECISION NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
    conn.close()

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Division par zéro impossible")
    return a / b

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    a = float(data["a"])
    op = data["op"]
    b = float(data["b"])

    if op == "+":
        result = add(a, b)
    elif op == "-":
        result = subtract(a, b)
    elif op == "*":
        result = multiply(a, b)
    elif op == "/":
        result = divide(a, b)
    else:
        return jsonify({"error": f"Opérateur inconnu : {op}"}), 400

    expression = f"{a} {op} {b}"
    conn = get_db()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO history (expression, result) VALUES (%s, %s)",
                (expression, result)
            )
    conn.close()

    return jsonify({"result": result})

@app.route("/history", methods=["GET"])
def get_history():
    conn = get_db()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT expression, result FROM history ORDER BY created_at ASC")
        rows = cur.fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/history", methods=["DELETE"])
def clear_history():
    conn = get_db()
    with conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM history")
    conn.close()
    return jsonify({"message": "Historique effacé"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=3000)
