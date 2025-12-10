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
            "genres": genre
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

        return videogames_list
    
    except Exception as e:
        print(f"Error: {e}")
        return []

# i have to iterate trhough each dictonary (theres one per deal) and take out the normal price the slae price and the sale id
def get_relevant_data(game_data):
    relevant_data = []
    for deal in game_data:
        data = {'Title': deal['title'], 'Normal Price' : deal['normalPrice'], 'Sale Price' : deal['salePrice'],
                'Deal ID' : deal['dealID']}
        relevant_data.append(data)

    return relevant_data

def display_game_data(relevant_data):
    with open("game_deals.html", "w") as f:
        f.write("<html><body>\n")
        f.write("<h1>Game Deals</h1>\n")
        for deal in relevant_data:
            f.write(f"<p>Title: {deal['Title']}</p>\n")
            f.write(f"<p>Normal Price: ${deal['Normal Price']}</p>\n")
            f.write(f"<p>Sale Price: ${deal['Sale Price']}</p>\n")
            f.write(f"<p>Deal ID: {deal['Deal ID']}</p>\n")
            f.write("<hr>\n")

        f.write("</body></html>\n")

games = ["The Last of US", "Minecraft", "Red Dead Redemption"]
all_data = []

for game_title in games:
    data = get_game_data(game_title)
    if data:
        relevant_data = get_relevant_data(data)
        all_data.extend(relevant_data)

display_game_data(all_data)

# access_token = get_access_token()
# result = get_song_genre('Last Christmas', 'Ariana Grande', access_token)
# videgames(result, RAWG_KEY)
# print(result)
#
# map_music_to_game(result)

access_token = get_access_token()
result = get_song_genre('Last Christmas', 'Ariana Grande', access_token)
print(f"Music genres: {result}")

# Pass only the first genre
game_genres = map_music_to_game(result)
print(f"Game genres: {game_genres}")













