from flask import Flask, render_template, request, g
from dataclasses import dataclass
from uuid import uuid4

app = Flask(__name__)

database = {}


@app.get("/")
def index_page():
    return render_template("index.html", coords=database)


@app.post("/")
def receive_notification():
    data = request.form

    longitude = data["longitude"]
    latitude = data["latitude"]
    title = data["title"]
    description = data["description"]
    point = DataPoint(longitude, latitude, title, description)

    uuid = uuid4()
    database[uuid] = point

    return render_template("index.html", coords=database)


@dataclass
class DataPoint:
    longitude: str
    latitude: str
    title: str
    description: str
