import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import Config
import pprint

ARTIST_URI = 'spotify:artist:5wVJpXzuKV6Xj7Yhsf2uYx'

def load_basic_info(CLIENT_ID, CLIENT_SECRET):
    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    artist_info = sp.artist(ARTIST_URI)

    artist_name = artist_info['name']
    followers = artist_info['followers']['total']
    popularity = artist_info['popularity']

    return {"Name": artist_name, "Followers": followers, "Popularity": popularity}

def _count_tracks(CLIENT_ID, CLIENT_SECRET):
    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    artist_name = sp.artist(ARTIST_URI)['name']
    print(f"'{artist_name}' 아티스트의 총 곡 수 계산을 시작합니다. (시간이 오래 걸릴 수 있습니다...)")

    unique_track_ids = set()

    offset = 0
    limit = 50
    total_releases_checked = 0

    while True:
        releases = sp.artist_albums(
            ARTIST_URI,
            album_type='album,single,appears_on,compilation',
            limit=limit,
            offset=offset,
        )

        album_items = releases.get('items', [])
        if not album_items:
            break

        total_releases_checked += len(album_items)

        for album in album_items:
            album_id = album['id']

            track_offset = 0
            while True:
                tracks_response = sp.album_tracks(album_id, limit=50, offset=track_offset, market='KR')
                track_items = tracks_response.get('items', [])

                if not track_items:
                    break

                for track in track_items:
                    is_artist_in_track = False
                    for artist in track.get('artists', []):
                        if artist['uri'] == ARTIST_URI:
                            is_artist_in_track = True
                            break

                    if is_artist_in_track:
                        unique_track_ids.add(track['id'])

                track_offset += 50

        offset += limit
    return len(unique_track_ids)

def load_tracks(CLIENT_ID, CLIENT_SECRET):
    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    query = "artist:HANRORO"
    search_result = sp.search(q=query, type='track', limit=40)

    result = []

    for track in search_result['tracks']['items']:
        track_id = track['id']
        track_name = track['name']
        track_details = sp.track(track_id)
        popularity_score = track_details['popularity']
        result.append((track_name, popularity_score))

    result.sort(key=lambda x: x[1], reverse=True)

    return result

def load_playlist(CLIENT_ID, CLIENT_SECRET):
    auth_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    MELON_HOT_100_ID = "4cRo44TavIHN54w46OqRVc"
    search_result = sp.playlist(MELON_HOT_100_ID)['tracks']['items']

    result = []

    ranking = 1
    for track in search_result:
        artist_name = track['track']['artists'][0]['name']
        if artist_name == 'HANRORO':
            result.append({'name': artist_name, 'rank': ranking})
        ranking += 1

    return result

load_playlist(Config.CLIENT_ID, Config.CLIENT_SECRET)