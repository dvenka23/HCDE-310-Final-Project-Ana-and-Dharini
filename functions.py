import urllib.request
import urllib.parse
import json
from keys import CLIENT_ID, CLIENT_SECRET, RAWG_KEY
from PyDictionary import PyDictionary

dictionary = PyDictionary()

def get_song_genre(title, artist, access_token):

    base_url = 'https://api.spotify.com/v1/search'

    params = {
        'q': f'track:{title} artist:{artist}',
        'type': 'track',
        'limit': 1
    }

    search_url = base_url + '?' + urllib.parse.urlencode(params)

    search_request = urllib.request.Request(search_url)
    search_request.add_header('Authorization', f'Bearer {access_token}')

    with urllib.request.urlopen(search_request) as response:
        search_data = json.loads(response.read().decode('utf-8'))

    if not search_data['tracks']['items']:
        print(f"Sorry, I couldn't find anything for {title} by {artist}.")
        return None

    track = search_data['tracks']['items'][0]
    artist_id = track['artists'][0]['id']
    artist_name = track['artists'][0]['name']

    artist_url = f'https://api.spotify.com/v1/artists/{artist_id}'

    artist_request = urllib.request.Request(artist_url)
    artist_request.add_header('Authorization', f'Bearer {access_token}')

    with urllib.request.urlopen(artist_request) as response:
        artist_data = json.loads(response.read().decode('utf-8'))

    genre = artist_data['genres']

    if genre:
        genre_list = genre
    else:
        genre_list = ['No genre information available']

    return genre_list

def get_access_token():
    base_url = 'https://accounts.spotify.com/api/token'

    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    data_encoded = urllib.parse.urlencode(data).encode('utf-8')
    req = urllib.request.Request(base_url, data=data_encoded, method='POST')
    req.add_header('Content-Type', 'application/x-www-form-urlencoded')

    with urllib.request.urlopen(req) as response:
        access_token = json.loads(response.read().decode('utf-8'))['access_token']
        return access_token


# def synonym():
#     genre = get_song_genre('Spotify', '', get_access_token())
#     synonyms = dictionary.synonyms(genre)
#     return synonyms


def videgames(genre, RAWG_KEY):
    videogames_list = []
    try:
        genre = str(genre)
        params = {
            "key":RAWG_KEY,
            "genre": genre
        }
        videogame_url = base_url + '?' + urllib.parse.urlencode(params)
        video_request = urllib.request.Request(videogame_url)

        with urllib.request.urlopen(video_request) as response:
            video_data = json.loads(response.read().decode('utf-8'))
            
        for game in video_data['results']:
            videogames_list.append(game)

        return videogames_list
        
    except: 
        videogames_list = []

        base_url = "https://api.rawg.io/api/games"
        genre_list = dictionary.synonym(genre)

        params = {
            "key": RAWG_KEY,
            "genre": genre_list,
        }
        videogame_url = base_url + '?' + urllib.parse.urlencode(params)
        video_request = urllib.request.Request(videogame_url)

        with urllib.request.urlopen(video_request) as response:
            video_data = json.loads(response.read().decode('utf-8'))

        if not video_data.get('results'):
            print(f"Sorry, I couldn't find anything for {genre}.")
            return None

        for game in video_data['results']:
            videogames_list.append(game)

        return videogames_list







