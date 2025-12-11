from flask import Flask, render_template, request
from functions import get_access_token, get_song_genre, map_music_to_game, videgames, get_game_data, get_relevant_data
from keys import RAWG_KEY

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main_page.html')

@app.route('/results', methods=['POST'])
def results():
    song = request.form['song']
    artist = request.form['artist']

    access_token = get_access_token()

    music_genre = get_song_genre(song, artist, access_token)

    if not music_genre:
        return render_template('results.html', error="Song not found. Please try again.")

    game_genre = map_music_to_game(music_genre)

    videogames = videgames(game_genre, RAWG_KEY)

    games = [game['name'] for game in videogames]
    all_data = []

    for game_title in games:
        data = get_game_data(game_title)
        if data:
            relevant_data = get_relevant_data(data)
            all_data.extend(relevant_data)

    return render_template('results.html',
                           song=song,
                           artist=artist,
                           music_genre=music_genre,
                           game_genre=game_genre,
                           videogames=videogames,
                           deals=all_data)
