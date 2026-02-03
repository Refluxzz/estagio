from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_components():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, id, name, price FROM components")
    data = cursor.fetchall()
    conn.close()

    components = {}
    for category, cid, name, price in data:
        components.setdefault(category, []).append({
            "id": cid,
            "name": name,
            "price": price
        })
    return components

@app.route("/")
def builder():
    components = get_components()
    return render_template("builder.html", components=components)

@app.route("/calculate", methods=["POST"])
def calculate():
    ids = request.json.get("ids", [])
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    total = 0
    for cid in ids:
        cursor.execute("SELECT price FROM components WHERE id = ?", (cid,))
        result = cursor.fetchone()
        if result:
            total += result[0]

    conn.close()
    return jsonify({"total": round(total, 2)})

if __name__ == "__main__":
    app.run(debug=True)