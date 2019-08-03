import json

import spotipy
import spotipy.util as util

import secret

scope = 'user-top-read'


def gather_uri(content):
    uris = []

    for item in content['items']:
        uris.append(item['uri'])

    return uris


def get_recs(valence):
    token = util.prompt_for_user_token(secret.username, scope,
                                       secret.CLIENT_ID, secret.CLIENT_SECRET,
                                       secret.REDIRECT)
    sp = spotipy.Spotify(token)

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

    items = json.dumps(recommendations)
    return items
