import json
import requests


def get_token():
    with open("data/token.txt") as token_file:
        return token_file.read()


def main():
    input_data = []
    with open("data/input.json") as file:
        input_data = json.load(file)

    token = get_token()
    headers = {'Authorization': f'Bearer {token}'}

    data = []

    for input_datum in input_data:
        if "album" in input_datum:
            link = "https://api.spotify.com/v1/albums/" + input_datum["album"].split("/")[-1].split("?")[0]
            result = json.loads(requests.get(link, headers=headers).text)

            datum = {
                "name": result["name"],
                "image": result["images"][0]["url"],
                "link": result["external_urls"]["spotify"]
            }

            artists = []

            for artist in result["artists"]:
                artists.append({
                    "name": artist["name"],
                    "link": artist["external_urls"]["spotify"]
                })

            datum["artists"] = artists

            datum["rating"] = input_datum["rating"]
            datum["recommended by"] = input_datum["recommended by"]
            datum["best songs"] = input_datum["best songs"]
            datum["comment"] = input_datum["comment"]

            data.append(datum)
        elif "playlist" in input_datum:
            link = "https://api.spotify.com/v1/playlists/" + input_datum["playlist"].split("/")[-1].split("?")[0]
            result = json.loads(requests.get(link, headers=headers).text)

            datum = {
                "name": result["name"],
                "image": result["images"][0]["url"],
                "link": result["external_urls"]["spotify"]
            }

            datum["artists"] = input_datum["artists"]
            datum["rating"] = input_datum["rating"]
            datum["recommended by"] = input_datum["recommended by"]
            datum["best songs"] = input_datum["best songs"]
            datum["comment"] = input_datum["comment"]

            data.append(datum) 

    with open("data/data.json", "w") as data_file:
        data_file.write(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
