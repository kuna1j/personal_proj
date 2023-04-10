import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd

CLIENT_ID = 'CLIENT_ID'
CLIENT_SECRET_KEY = 'CLIENT_SECRET_KEY'
REDIRECT_URI = 'https://developer.spotify.com/dashboard/applications/1f7291a56f9d4823a96e583a46e3d12b'

scope = "user-read-currently-playing"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET_KEY, 
                                redirect_uri=REDIRECT_URI, scope=scope))

data_dict1 = {'Playlist Name': [], 'No. of Songs': [], 'Playlist ID': []}

results = sp.current_user_playlists(limit=10)
print(results)
for playlist in results['items']:
    data_dict1['Playlist Name'].append(playlist['name'])
    data_dict1['No. of Songs'].append(playlist['tracks']['total'])
    data_dict1['Playlist ID'].append(playlist['id'])
    
df1 = pd.DataFrame(data_dict1) 
print(df1)


def func(p_id, p_name):
    xd = []
    artist_names = [[]]
    data_dict2 = {'Track Names': [], 'Artist Names': []}

    items = sp.playlist_items(playlist_id=p_id)

    for i in items['items']:
        data_dict2['Track Names'].append(i['track']['name'])
        for j in i['track']['artists']:
            xd.append(j['name'])
        data_dict2['Artist Names'].append(xd)
        xd=[]
    del artist_names[0]

    df2 = pd.DataFrame(data_dict2)
    df2 = df2.replace({'Artist Names': {'\'':''}})
    df2.to_csv(f'{p_name}.csv', index=False)
    
    data = ""
    with open(f"{p_name}.csv",'r') as file:
        data = file.read().replace("[", "").replace("]", "").replace("\'", "")
    with open(f"{p_name}.csv", 'w') as file:
        file.write(data)



for pid in data_dict1['Playlist ID']:
    pname = sp.playlist(pid)['name']
    func(pid, pname)
