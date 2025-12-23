from flask import Flask, request, jsonify, render_template
import sqlite3

print("APP FILE STARTED")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/convert")
def convert():
    from_cur = request.args.get("from")
    to_cur = request.args.get("to")
    amount = float(request.args.get("amount"))

    conn = sqlite3.connect("currency.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT rate FROM exchange_rates WHERE from_currency=? AND to_currency=?",
        (from_cur, to_cur)
    )
    row = cur.fetchone()
    conn.close()

    if row:
        rate = row [0]
        return jsonify({"converted_amount": amount * rate})
    else:
        return jsonify({"error": "Rate not found"})

if __name__ == "__main__":
    app.run(debug=True)