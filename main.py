from flask import Flask, render_template, request, flash
from dataclasses import dataclass
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = b'oxabadidea'


@app.get("/")
def index_page():
    con = sqlite3.connect("points.db")
    cur = con.cursor()
    return render_template("index.html", coords=fetch_markers(cur))


@app.post("/")
def receive_notification():
    data = request.form
    con = sqlite3.connect("points.db")
    cur = con.cursor()

    try:
        longitude = float(data["longitude"])
        latitude = float(data["latitude"])
        title = data["title"]
        description = data["description"]
    except:
        print("Invalid data received")
        flash("Invalid data types")
        markers = fetch_markers(cur)

        return render_template("index.html", coords=markers), 400

    cur.execute(
        "INSERT INTO markers (longitude, latitude, title, description) VALUES (?, ?, ?, ?)",
        (longitude, latitude, title, description),
    )
    con.commit()

    markers = fetch_markers(cur)
    return render_template("index.html", coords=markers)


def fetch_markers(cur):
    markers = cur.execute("SELECT * FROM markers").fetchall()
    return [DataPoint(m[1], m[2], m[3], m[4]) for m in markers]


@dataclass
class DataPoint:
    longitude: float
    latitude: float
    title: str
    description: str

