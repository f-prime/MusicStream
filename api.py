from flask import jsonify, Flask 
import time
import thread
from id3reader import Reader
import hashlib
import random
import os

app = Flask(__name__)
songs = {}

@app.route("/getAllMusic")
def getAllMusic():
    songs_ = []
    for x in songs:
        songs_.append(songs[x])
    return jsonify({"data":songs_})

@app.route("/getMusicByArtist/<artist>")
def getMusicByArtist(artist):
    songs_ = []
    for x in songs:
        if songs[x]['artist'].lower() == artist.lower():
            songs_.append(songs[x])

    return jsonify({"data":songs_})

@app.route("/getMusicByGenre/<genre>")
def getMusicByGenre(genre):
    songs_ = []
    for x in songs:
        if songs[x]['genre'].lower() == genre.lower():
            songs_.append(songs[x])
    
    return jsonify({"data":songs_})

@app.route("/getRandomSong")
def getRandomSong():
    return jsonify(random.choice([songs[x] for x in songs]))

@app.route("/streamSong/<_id>")
def streamSong(_id):
    return open(songs[_id]['directory']).read()


def songManager():
    while True:
        for x in os.listdir("songs"):
            id_ = hashlib.md5(open("songs/"+x).read()).hexdigest()
            if id_ not in songs:
                data = Reader("songs/"+x)
                songs[id_] = {"artist":data.getValue("performer"), "title":data.getValue("title"), "year":data.getValue("year"), "directory":"songs/"+x, "id":id_, "genre":data.getValue("genre")}
        time.sleep(15)

if __name__ == "__main__":
    thread.start_new_thread(songManager, ())
    app.run(debug=True)
