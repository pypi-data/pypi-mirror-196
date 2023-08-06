from audiodotturn.view_tools.songs import Song

# create a dataset
dataset = {
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

def test_search_by_artist():
    songs = Song(dataset, 'post')
    assert songs.search_by_artist() == [
               {'artist': 'Post Malone', 'title': 'rockstar ft. 21 Savage', 'features': '21 Savage', 'misc': '', 'youtube_id': 'UceaB4D0jpo', 'filetype': 'mp3'}, 
               {'artist': 'Post Malone', 'title': 'Circles', 'features': '', 'misc': '', 'youtube_id': 'wXhTHyIgQ_U', 'filetype': 'mp3'}, 
               {'artist': 'Post Malone', 'title': 'Better Now', 'features': '', 'misc': '', 'youtube_id': 'UYwF-jdcVjY', 'filetype': 'mp3'}
    ]

def test_search_by_title():
    songs = Song(dataset, 'lose')
    assert songs.search_by_title() == [{'artist': 'Eminem', 'title': 'Lose Yourself', 'features': '', 'misc': 'from the movie "8 Mile"', 'youtube_id': 'bkfBgq6AheE', 'filetype': 'mp3'}]

def test_search_by_features():
    songs = Song(dataset, '21')
    assert songs.search_by_features() == [{'artist': 'Post Malone', 'title': 'rockstar ft. 21 Savage', 'features': '21 Savage', 'misc': '', 'youtube_id': 'UceaB4D0jpo', 'filetype': 'mp3'}]
