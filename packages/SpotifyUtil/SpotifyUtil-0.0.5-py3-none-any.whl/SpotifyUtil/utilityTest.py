from SpotifyUtil import SpotifyUtil

# from config import Config
# from file_reader import FileReader

SPOTIPY_CLIENT_ID="7214d90460af4f26a805e1132e1f8d9d"
SPOTIPY_CLIENT_SECRET="bc076ca4972c47fda59d3ff24e9d2e02"
SPOTIPY_REDIRECT_URI="http://127.0.0.1:5500/"

sp = SpotifyUtil(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)

def make_changes(main_url, source_url):
    tracks1 = sp.get_total_songs_length(main_url)
    tracks2 = sp.get_total_songs_length(source_url)
    if tracks1<tracks2:
        print("Adding songs")
        # sp.add_songs_to_playlist_from_file(playlist_url=main_url, file_path="G:\LeMusic\lemusic.txt", allow_duplicates=False)
        sp.add_songs_to_playlist(playlist_url=main_url, from_url=source_url, allow_duplicates=False)

def check_full(url):
    tracks = sp.get_tracks(url, verbose=True)
    print(tracks.detailed_list)

def get_diff(url1, url2):
    print(sp.get_different_tracks(url1, url2))

def clear_p(url):
    sp.clear_playlist(url)

def create_liked_songs_playlist(name, is_public):
    sp.add_liked_songs_to_playlist(name=name, is_public=is_public)

# main_url="https://open.spotify.com/playlist/269spiLROhagtO6WNUKHjP?si=f34822da6e6d43d5"
source_url="https://open.spotify.com/playlist/6Ujd4z9JhEhBR5Bwr7pvsi?si=83bf130895264580"

def test_test():
    print(sp.test())

test_test()

# make_changes(main_url, source_url)
# print("===============================================")
# get_diff(main_url, source_url)
# print("===============================================")
# # clear_p(main_url)
