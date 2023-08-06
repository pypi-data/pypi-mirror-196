from typing import Dict
from audiodotturn.view_tools.artists import Artist

DATASET = {
    'Eminem': {
        'tracks': [
            {
                'title': 'Lose Yourself',
                'artist': 'Eminem',
                'features': '',
                'misc': 'from the movie "8 Mile"',
                'youtube_id': 'bkfBgq6AheE',
                'filetype': 'mp3'
            },
            {
                'title': 'Rap God',
                'artist': 'Eminem',
                'features': '',
                'misc': '',
                'youtube_id': 'XbGs_qK2PQA',
                'filetype': 'mp3'
            },
            {
                'title': 'The Real Slim Shady',
                'artist': 'Eminem',
                'features': '',
                'misc': '',
                'youtube_id': 'eJO5HU_7_1w',
                'filetype': 'mp3'
            },
        ]
    },
    'Drake': {
        'tracks': [
            {
                'title': 'Laugh Now Cry Later ft. Lil Durk',
                'artist': 'Drake',
                'features': 'Lil Durk',
                'misc': '',
                'youtube_id': 'JFm7YDVlqnI',
                'filetype': 'mp3'
            },
            {
                'title': 'One Dance',
                'artist': 'Drake',
                'features': 'Wizkid, Kyla',
                'misc': '',
                'youtube_id': 'RUw6cNWYE1s',
                'filetype': 'mp3'
            },
            {
                'title': 'In My Feelings',
                'artist': 'Drake',
                'features': '',
                'misc': '',
                'youtube_id': 'DRS_PpOrUZ4',
                'filetype': 'mp3'
            },
        ]
    },
    'Post Malone': {
        'tracks': [
            {
                'title': 'rockstar ft. 21 Savage',
                'artist': 'Post Malone',
                'features': '21 Savage',
                'misc': '',
                'youtube_id': 'UceaB4D0jpo',
                'filetype': 'mp3'
            },
            {
                'title': 'Circles',
                'artist': 'Post Malone',
                'features': '',
                'misc': '',
                'youtube_id': 'wXhTHyIgQ_U',
                'filetype': 'mp3'
            },
            {
                'title': 'Better Now',
                'artist': 'Post Malone',
                'features': '',
                'misc': '',
                'youtube_id': 'UYwF-jdcVjY',
                'filetype': 'mp3'
            },
        ]
    }
}

# Test get_artists() method
def test_get_artists():
    artist = Artist(dataset=DATASET)
    artists = artist.get_artists()
    assert len(artists) == 3
    assert "Eminem" in artists
    assert "Drake" in artists
    assert "Post Malone" in artists

def test_get_tracks():
    art = Artist(dataset=DATASET)
    tracks = art.get_tracks()
    assert isinstance(tracks, Dict)
    assert len(tracks) == 3
    assert tracks['Eminem'][0]['title'] == 'Lose Yourself'
    assert tracks['Eminem'][0]['artist'] == 'Eminem'
    assert tracks['Eminem'][0]['features'] == ''
    assert tracks['Eminem'][0]['misc'] == 'from the movie "8 Mile"'
    assert tracks['Eminem'][0]['youtube_id'] == 'bkfBgq6AheE'
    assert tracks['Eminem'][0]['filetype'] == 'mp3'
    assert tracks['Eminem'][1]['title'] == 'Rap God'
    assert tracks['Eminem'][1]['artist'] == 'Eminem'
    assert tracks['Eminem'][1]['features'] == ''
    assert tracks['Eminem'][1]['misc'] == ''
    assert tracks['Eminem'][1]['youtube_id'] == 'XbGs_qK2PQA'
    assert tracks['Eminem'][1]['filetype'] == 'mp3'
    assert tracks['Eminem'][2]['title'] == 'The Real Slim Shady'
    assert tracks['Eminem'][2]['artist'] == 'Eminem'
    assert tracks['Eminem'][2]['features'] == ''
    assert tracks['Eminem'][2]['misc'] == ''
    assert tracks['Eminem'][2]['youtube_id'] == 'eJO5HU_7_1w'
    assert tracks['Eminem'][2]['filetype'] == 'mp3'
    assert tracks['Drake'][0]['title'] == 'Laugh Now Cry Later ft. Lil Durk'
    assert tracks['Drake'][0]['artist'] == 'Drake'
    assert tracks['Drake'][0]['features'] == 'Lil Durk'
    assert tracks['Drake'][0]['misc'] == ''
    assert tracks['Drake'][0]['youtube_id'] == 'JFm7YDVlqnI'
    assert tracks['Drake'][0]['filetype'] == 'mp3'
    assert tracks['Drake'][1]['title'] == 'One Dance'
    assert tracks['Drake'][1]['artist'] == 'Drake'
    assert tracks['Drake'][1]['features'] == 'Wizkid, Kyla'
    assert tracks['Drake'][1]['misc'] == ''
    assert tracks['Drake'][1]['youtube_id'] == 'RUw6cNWYE1s'
    assert tracks['Drake'][1]['filetype'] == 'mp3'
    assert tracks['Drake'][2]['title'] == 'In My Feelings'
    assert tracks['Drake'][2]['artist'] == 'Drake'
    assert tracks['Drake'][2]['features'] == ''
    assert tracks['Drake'][2]['misc'] == ''
    assert tracks['Drake'][2]['youtube_id'] == 'DRS_PpOrUZ4'
    assert tracks['Drake'][2]['filetype'] == 'mp3'
    assert tracks['Post Malone'][0]['title'] == 'rockstar ft. 21 Savage'
    assert tracks['Post Malone'][0]['artist'] == 'Post Malone'
    assert tracks['Post Malone'][0]['features'] == '21 Savage'
    assert tracks['Post Malone'][0]['misc'] == ''
    assert tracks['Post Malone'][0]['youtube_id'] == 'UceaB4D0jpo'
    assert tracks['Post Malone'][0]['filetype'] == 'mp3'
    assert tracks['Post Malone'][1]['title'] == 'Circles'
    assert tracks['Post Malone'][1]['artist'] == 'Post Malone'
    assert tracks['Post Malone'][1]['features'] == ''
    assert tracks['Post Malone'][1]['misc'] == ''
    assert tracks['Post Malone'][1]['youtube_id'] == 'wXhTHyIgQ_U'
    assert tracks['Post Malone'][1]['filetype'] == 'mp3'
    assert tracks['Post Malone'][2]['title'] == 'Better Now'
    assert tracks['Post Malone'][2]['artist'] == 'Post Malone'
    assert tracks['Post Malone'][2]['features'] == ''
    assert tracks['Post Malone'][2]['misc'] == ''
    assert tracks['Post Malone'][2]['youtube_id'] == 'UYwF-jdcVjY'
    assert tracks['Post Malone'][2]['filetype'] == 'mp3'
