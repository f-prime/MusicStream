import pygame
import urllib
import StringIO
import json
import time

pygame.mixer.init()
songs = []
while True:
    while True:
        data = urllib.urlopen("http://localhost:5000/getRandomSong").read()
        x = json.loads(data)
        if x['id'] not in songs:
            break
    songs.append(x['id'])
    stream = urllib.urlopen("http://localhost:5000/streamSong/{0}".format(x['id'])).read()
    data = StringIO.StringIO(stream)
    print "Playing: {0}, {1}, {2}".format(x['title'], x['artist'], x['year'])
    pygame.mixer.music.load(data)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy(): time.sleep(1)

