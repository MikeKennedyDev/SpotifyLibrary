import creds
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

LIBRARY_PLAYLIST = 'Archive'


def GetSpotifyCreds():
    USERNAME = creds.username
    CLIENT_ID = creds.client_id
    CLIENT_SECRET = creds.client_secret

    auth_manager = SpotifyOAuth(scope='playlist-modify-public')

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=creds.client_id,
                                                                                  client_secret=creds.client_secret))

    sp = spotipy.Spotify(auth_manager=auth_manager)

    print(f'spotify: {spotify}')
    print(f'auth_manager: {auth_manager}')

    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(scope='playlist-modify-public',
                                  username=USERNAME,
                                  client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET,
                                  redirect_uri='http://localhost:8888/callback/')
    )


def RemoveDuplicates(sp, playlist):
    # print('Checking for duplicates in playlist: ' + str({playlist['name']}))
    tracks = GetAllPlaylistTracks(sp, playlist['name'])
    if len(tracks) == 0:
        return
    duplicateTracks = [item for item in tracks if tracks.count(item) > 1]
    duplicateTracks = list(dict.fromkeys(duplicateTracks))  # remove duplicate tracks
    # print(f"{len(duplicateTracks)} duplicates found in {playlist['name']}")
    if len(duplicateTracks) > 0:
        sp.playlist_remove_all_occurrences_of_items(playlist['id'], duplicateTracks)
        sp.playlist_add_items(playlist['id'], duplicateTracks)
    return


def GetAllPlaylistTracks(sp, playlistName):
    # print(f'Getting all tracks for playlist {playlistName}')
    playlist = [p for p in sp.user_playlists(creds.username)['items'] if p['name'] == playlistName]
    library_id = playlist[0]['id']
    results = sp.playlist_items(library_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return [t['track']['id'] for t in tracks]  # returns track ids


def GetAllTracks(spotify):
    all_tracks = []

    # Get tracks from user playlists
    for playlist in spotify.user_playlists(creds.username)['items']:
        RemoveDuplicates(spotify, playlist)
        tracks = GetAllPlaylistTracks(spotify, playlist['name'])
        all_tracks.extend(tracks)

    # Get tracks from user liked songs
    print('Looking for liked songs')
    for track in spotify.current_user_saved_tracks():
        print(track)

    return list(dict.fromkeys(all_tracks))  # Remove duplicate entries


if __name__ == '__main__':
    spotify = GetSpotifyCreds()

    # Get tracks from user liked songs
    print('Looking for liked songs')
    print(spotify.current_user_saved_tracks()['items'])

    # for idx, item in enumerate(spotify.current_user_saved_tracks()['items']):
    #     track = item['track']
    #     print(track)

    # for track in spotify.current_user_saved_tracks()['items']:
    #     print(track)

    library_tracks = GetAllPlaylistTracks(spotify, LIBRARY_PLAYLIST)
    print(f'num tracks in {LIBRARY_PLAYLIST}: {len(library_tracks)}')

    all_tracks = GetAllTracks(spotify)
    print(f'num total tracks {len(all_tracks)}')

    tracks_to_add = [track for track in all_tracks if track not in library_tracks]
    print(f'{len(tracks_to_add)} new tracks to add to {LIBRARY_PLAYLIST}')

    library_playlist = [p for p in spotify.user_playlists(creds.username)['items'] if p['name'] == LIBRARY_PLAYLIST]

    RemoveDuplicates(spotify, library_playlist[0])

    for i in range(0, len(tracks_to_add), 100):
        spotify.playlist_add_items(library_playlist[0]['id'], tracks_to_add[i:i + 100])
