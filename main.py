import creds
import Spotify.Core


if __name__ == '__main__':
    try:
        spotify = Spotify.Core.GetSpotifyCreds()
        library_playlist_id = Spotify.Core.GetLibraryPlaylistId(spotify)

        playlist_tracks = Spotify.Core.GetAllPlaylistTrackIds(spotify)
        liked_tracks = Spotify.Core.GetLikedTrackIds(spotify)

        unique_tracks = set(playlist_tracks + liked_tracks)

        pause = 0

        t1 = list(unique_tracks)

        spotify.playlist_add_items(library_playlist_id, t1[10])

        pause = 0

    except BaseException as err:
        print('Some error')
        e = err

