import spotipy
import spotipy.util as util

import secret

scope = '''user-top-read
           playlist-read-collaborative
           playlist-modify-private
           playlist-modify-public
           playlist-read-private
        '''


def gather_uri(content, key='items'):
    uris = []

    for item in content[key]:
        uris.append(item['uri'])

    return uris


def get_recs(valence):
    token = util.prompt_for_user_token('', scope,
                                       secret.CLIENT_ID, secret.CLIENT_SECRET,
                                       secret.REDIRECT)
    sp = spotipy.Spotify(token)

    user = sp.current_user()
    user_id = user['id']

    user_artists = sp.current_user_top_artists(limit=1,
                                               time_range='short_term')
    user_tracks = sp.current_user_top_tracks(limit=1,
                                             time_range='short_term')

    seed_artists = gather_uri(user_artists)
    seed_tracks = gather_uri(user_tracks)

    recommendations = sp.recommendations(seed_artists=seed_artists,
                                         seed_tracks=seed_tracks,
                                         limit=5,
                                         target_valence=valence)

    recommendation_uris = gather_uri(recommendations, key='tracks')

    playlist_name = "SONAR_ID"
    get_last_playlist = lambda: sp.user_playlists(user_id, limit=1)['items'][0]

    curr_last_playlist = get_last_playlist()

    if curr_last_playlist['name'] == playlist_name:
        sp.user_playlist_replace_tracks(user_id, curr_last_playlist['id'],
                                        recommendation_uris)
    else:
        sp.user_playlist_create(user_id, playlist_name)
        sp.user_playlist_add_tracks(user_id, curr_last_playlist['id'],
                                    recommendation_uris)

    new_last_playlist = get_last_playlist()

    return new_last_playlist
