import creds
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials


LIBRARY_PLAYLIST_NAME = 'Archive'


def GetSpotifyCreds():
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(scope='user-library-read,playlist-modify-public',
                                  username=creds.username,
                                  client_id=creds.client_id,
                                  client_secret=creds.client_secret,
                                  redirect_uri='http://localhost:8888/callback/')
    )


def FormatTracks(liked_tracks, playlist_tracks):
    pause = 0
    return None


def GetLikedTrackIds(spotify):
    all_tracks = []
    liked_tracks = spotify.current_user_saved_tracks()['items']
    offset = 0

    while len(liked_tracks) > 0:
        all_tracks.extend(liked_tracks)
        offset += 20
        liked_tracks = spotify.current_user_saved_tracks(offset=offset)['items']

    tracks = [track['track'] for track in all_tracks]
    return [track['id'] for track in tracks]


def GetAllTracksInPlaylist(spotify, playlistId):
    all_tracks = []
    playlist_tracks = spotify.playlist_items(playlistId)['items']
    offset = 0

    pause = 0

    while len(playlist_tracks) > 0:
        offset += 100 # default limit for playlist tracks grabbed at once
        all_tracks.extend(playlist_tracks)
        playlist_tracks = spotify.playlist_items(playlistId,
                                                 offset=offset)['items']
    return all_tracks


def GetAllPlaylistTrackIds(spotify):
    all_playlists = spotify.user_playlists(creds.username)
    all_tracks = []

    for playlist in spotify.user_playlists(creds.username)['items']:
        playlist_tracks = GetAllTracksInPlaylist(spotify, playlist['id'])
        all_tracks.extend(playlist_tracks)

    tracks = [track['track'] for track in all_tracks]
    return [track['id'] for track in tracks]


def chunker(seq, size):
    return list(seq[pos:pos + size] for pos in range(0, len(seq), size))


def WriteToLibrary(spotify, library_id, track_list):
    # Ensure tracks are unique
    track_list = list(set(track_list))
    chunks = chunker(track_list, 100)

    # Empty playlist
    for chunk in chunks:
        spotify.playlist_remove_all_occurrences_of_items(library_id, chunk)

    # Re-fill playlist
    for chunk in chunks:
        spotify.playlist_add_items(library_id, chunk)


def GetLibraryPlaylistId(spotify):
    all_playlists = spotify.user_playlists(creds.username)['items']
    return [playlist['id'] for playlist in all_playlists if playlist['name'] == LIBRARY_PLAYLIST_NAME][0]
