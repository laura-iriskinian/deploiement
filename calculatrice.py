from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

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

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
