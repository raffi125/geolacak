import os, sqlite3, json, math
from flask import Flask, request, jsonify, render_template, g

BASE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE, "tracker.db")
app = Flask(__name__, template_folder="templates", static_folder="static")

def db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(_):
    d = g.pop("db", None)
    if d: d.close()

def init_db():
    with sqlite3.connect(DB) as c:
        c.execute("""CREATE TABLE IF NOT EXISTS visits(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT, ua TEXT, lat REAL, lon REAL, acc REAL,
            status TEXT, ts TEXT)""")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/location", methods=["POST"])
def api_location():
    init_db()
    d = request.get_json(silent=True) or {}
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent","")
    status = d.get("status","allowed")
    if status not in ("allowed", "denied"):
        return jsonify({"ok": False, "error": "invalid status"}), 400
    if status == "denied":
        lat = None
        lon = None
        acc = None
    else:
        lat = d.get("lat")
        lon = d.get("lon")
        acc = d.get("accuracy")
        def valid_number(value):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return False
            return math.isfinite(value)
        if not (valid_number(lat) and valid_number(lon)):
            return jsonify({"ok": False, "error": "lat and lon must be numbers"}), 400
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return jsonify({"ok": False, "error": "invalid coordinates"}), 400
        if acc is not None:
            if not valid_number(acc) or acc < 0:
                return jsonify({"ok": False, "error": "accuracy must be a non-negative number in meters"}), 400
    ts = d.get("ts","")
    cur = db().execute(
        "INSERT INTO visits(ip,ua,lat,lon,acc,status,ts) VALUES(?,?,?,?,?,?,?)",
        (ip,ua,lat,lon,acc,status,ts))
    db().commit()
    return jsonify({"ok": True, "id": cur.lastrowid}), 201

@app.route("/api/visits")
def api_visits():
    init_db()
    rows = db().execute("SELECT * FROM visits ORDER BY id DESC").fetchall()
    return jsonify([dict(r) for r in rows])

if __name__ == "__main__":
    init_db()
    host=os.environ.get("HOST","0.0.0.0")
    port=int(os.environ.get("PORT","5000"))
    app.run(host=host, port=port, debug=False)
