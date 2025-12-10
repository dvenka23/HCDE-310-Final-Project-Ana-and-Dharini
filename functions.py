import urllib.request
import urllib.parse
import json
from keys import CLIENT_ID, CLIENT_SECRET, RAWG_KEY


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

    artist_url = f'https://api.spotify.com/v1/artists/{artist_id}'

    artist_request = urllib.request.Request(artist_url)
    artist_request.add_header('Authorization', f'Bearer {access_token}')

    with urllib.request.urlopen(artist_request) as response:
        artist_data = json.loads(response.read().decode('utf-8'))

    genre = artist_data['genres']

    if genre:
        genre = genre[0]
    else:
        genre = 'No genre information available'

    return genre


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


def map_music_to_game(genre):
    genre_map = {
        'pop': ['casual', 'simulation', 'family'],
        'rock': ['action', 'shooter', 'racing'],
        'metal': ['action', 'shooter', 'fighting'],
        'edm': ['arcade', 'racing', 'sports'],
        'electronic': ['arcade', 'puzzle', 'platformer'],
        'hip hop': ['action', 'sports', 'racing'],
        'classical': ['strategy', 'puzzle', 'adventure'],
        'jazz': ['puzzle', 'casual', 'indie'],
        'indie': ['indie', 'adventure', 'platformer'],
        'country': ['adventure', 'simulation', 'casual'],
        'r&b': ['casual', 'adventure', 'simulation'],
    }

    genre_lower = genre.strip().lower()

    for key in genre_map:
        if key in genre_lower:
            return str(genre_map[key][0])

    return 'adventure'


def videgames(genre, RAWG_KEY):
    videogames_list = []
    base_url = "https://api.rawg.io/api/games"
    try:
        params = {
            "key": RAWG_KEY,
            "genres": genre,
            "page_size": 20,
        }
        videogame_url = base_url + '?' + urllib.parse.urlencode(params)
        video_request = urllib.request.Request(videogame_url)

        with urllib.request.urlopen(video_request) as response:
            video_data = json.loads(response.read().decode('utf-8'))

        if not video_data.get('results'):
            print(f"Sorry, I couldn't find anything for {genre}.")
            return []

        for game in video_data['results']:
            videogames_list.append(game)

        return videogames_list[:10]

    except Exception as e:
        print(f"Error: {e}")
        return []

def get_game_data(title):
    base_url = 'https://www.cheapshark.com/api/1.0/deals'

    params = {"title": title}

    paramstr = urllib.parse.urlencode(params)
    game_request = base_url + '?' + paramstr

    try:
        with urllib.request.urlopen(game_request) as response:
            game_response_str = response.read().decode()
        game_data = json.loads(game_response_str)
        return game_data
    except urllib.error.HTTPError as e:
        print("Error trying to retrieve data. Error code:", e.code)
        return None
    except urllib.error.URLError as e:
        print("Error trying to retrieve data.")
        print("Failure to reach server. Reason: ", e.reason)
        return None

def get_relevant_data(game_data):
    relevant_data = []
    for deal in game_data:
        data = {'Title': deal['title'], 'Normal Price': deal['normalPrice'], 'Sale Price': deal['salePrice'],
                'Deal ID': deal['dealID']}
        relevant_data.append(data)

    return relevant_data


















