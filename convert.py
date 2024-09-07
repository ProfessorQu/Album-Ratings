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
            }
            for song in result['tracks']['items']
        )
    return songs


def get_album_datum(input_datum, best_songs=None, headers=None):
    if best_songs is None:
        best_songs = []
    link = (
        "https://api.spotify.com/v1/albums/" +
        input_datum["album"].split("/")[-1].split("?")[0]
    )
    result = json.loads(requests.get(link, headers=headers).text)

    artists = [
        {"name": artist["name"], "link": artist["external_urls"]["spotify"]}
        for artist in result["artists"]
    ]
    this_songs = []
    for song in result['tracks']['items']:
        for best_song in best_songs:
            if song['id'] == best_song['id']:
                this_songs.append(best_song)
                break

    return {
        "name": result["name"],
        "image": result["images"][0]["url"],
        "link": result["external_urls"]["spotify"],

        "rating": input_datum["rating"],
        "recommended by": input_datum["recommended by"],
        "best songs": this_songs,
        "comment": input_datum["comment"],

        "artists": artists
    }


def get_playlist_datum(input_datum, best_songs=None, headers=None):
    if best_songs is None:
        best_songs = []
    link = (
        "https://api.spotify.com/v1/playlists/" +
        input_datum["playlist"].split("/")[-1].split("?")[0]
    )
    result = json.loads(requests.get(link, headers=headers).text)

    this_songs = []
    for song in result['tracks']['items']:
        for best_song in best_songs:
            if song['track']['id'] == best_song['id']:
                this_songs.append(best_song)
                break

    return {
        "name": result["name"],
        "image": result["images"][0]["url"],
        "link": result["external_urls"]["spotify"],

        "artists": input_datum["artists"],
        "rating": input_datum["rating"],
        "recommended by": input_datum["recommended by"],
        "best songs": this_songs,
        "comment": input_datum["comment"]
    }


def get_datum(input_datum, best_songs=None, headers=None):
    if best_songs is None:
        best_songs = []
    if "album" in input_datum:
        return get_album_datum(input_datum,
                               best_songs=best_songs,
                               headers=headers)
    elif "playlist" in input_datum:
        return get_playlist_datum(input_datum,
                                  best_songs=best_songs,
                                  headers=headers)


def main():
    input_data = []
    with open("data/input.json") as file:
        input_data = json.load(file)

    token = get_token()
    headers = {'Authorization': f'Bearer {token}'}

    best_songs = get_best_songs(headers=headers)

    data = [
        get_datum(input_datum, best_songs=best_songs, headers=headers)
        for input_datum in input_data
    ]
    with open("data/data.json", "w") as data_file:
        data_file.write(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
