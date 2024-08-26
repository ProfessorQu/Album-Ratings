from flask import Flask, render_template
import json

app = Flask(__name__)

albums = []
with open("data/data.json") as data_file:
    albums = json.load(data_file)


@app.route("/album/<index>")
def album(index: int):
    album = albums[int(index)]
    return render_template("album.html", album=album,
                           artists_len=len(album['artists']),
                           songs_len=len(album['best songs']))


@app.route("/")
def home():
    return render_template("index.html", albums=albums, albums_len=len(albums))
