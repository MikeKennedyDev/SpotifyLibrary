import Spotify.Core


if __name__ == '__main__':
    try:
        spotify = Spotify.Core.GetSpotifyCreds()
        library_playlist_id = Spotify.Core.GetLibraryPlaylistId(spotify)

        playlist_tracks = Spotify.Core.GetAllPlaylistTrackIds(spotify)
        liked_tracks = Spotify.Core.GetLikedTrackIds(spotify)

        Spotify.Core.WriteToLibrary(spotify, library_playlist_id, (playlist_tracks + liked_tracks))

    except BaseException as err:
        print('Some error')
        e = err

