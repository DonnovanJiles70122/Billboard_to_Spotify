import datetime, requests, spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

CURRENT_YEAR = 2023
now = datetime.datetime.now()
today = str(now).split(' ')
user_date = input("Which year do you want to travel to? Type the data in this format YYYY-MM-DD \n")
date_format = '%Y-%m-%d'
check_date = user_date.split('-')


# Validating user date data
if int(check_date[0]) < 2000 or int(check_date[0]) > CURRENT_YEAR or user_date > today[0]:
    print('The date that was entered is invalid')

try:
    date_obj = datetime.datetime.strptime(user_date, date_format)
except ValueError:
    print("Incorrect data format, should be YYYY-MM-DD")

# web scrape data from billboard 
response = requests.get(f'https://www.billboard.com/charts/hot-100/{user_date}')
contents = response.text

soup = BeautifulSoup(contents, "html.parser")


titles = soup.find_all(name="h3", class_="a-no-trucate")
artists = soup.find_all(name='span', class_="a-no-trucate")

top_songs = [title.getText().strip() for title in titles]
top_artist = [artist.getText().strip() for artist in artists]

id = 'YOUR CIENT ID'
secret = 'YOUR CLIENT SECRET'

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=id,
        client_secret=secret,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

year = user_date.split('-')[0]

song_uri = []

for i in range(len(top_songs)):
    result = sp.search(q=f'track:{top_songs[i]} year:{year}', type='track')
    try:
        uri = result['tracks']['items'][0]["uri"]
        song_uri.append(uri)
    except IndexError:
        print(f'{top_songs[i]} does not exist in Spotify' )

playlist = sp.user_playlist_create(user=user_id, name=f'{year} Top songs', public=False)

sp.playlist_add_items(playlist_id=playlist['id'], items=song_uri)

print("Playlist is complete check Spotify")