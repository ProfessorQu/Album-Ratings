import json
import requests


def get_token():
    with open("data/token.txt") as token_file:
        return token_file.read()


def get_best_songs(headers=None):
    link = "https://api.spotify.com/v1/playlists/3xkh0VpL5iRLws4P04xmk1"

    result = json.loads(requests.get(link, headers=headers).text)
    songs = [
        {
            "link": song['track']['external_urls']['spotify'],
            "id": song['track']['id'],
            "name": song['track']['name'],
            "popularity": song['track']['popularity']
        }
        for song in result['tracks']['items']
    ]
    while 'next' in result:
        result = json.loads(requests.get(result['next'], headers=headers).text)
        songs.extend(
            {
                "link": song['track']['external_urls']['spotify'],
                "id": song['track']['id'],
                "name": song['track']['name'],
                "popularity": song['track']['popularity']
            }
            for song in result['tracks']['items']
        )

    return songs


if __name__ == '__main__':
    token = get_token()
    headers = {'Authorization': f'Bearer {token}'}

    best_songs = get_best_songs(headers=headers)
    best_songs.sort(key=lambda song: song['popularity'], reverse=True)

    for song in best_songs:
        print(song["name"], song["popularity"])
