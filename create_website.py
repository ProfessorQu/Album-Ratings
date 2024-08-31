from yattag import Doc, indent
import json


def create_index(albums):
    doc, tag, text = Doc().tagtext()

    doc.asis("<!DOCTYPE html>")
    with tag("html"):
        with tag("head"):
            doc.line("title", "Album Ratings")
            doc.stag("link", rel="icon", href="assets/icon.png")
            doc.stag("link", rel="stylesheet", href="static/stylesheet.css")
            with tag("script", src="script.js"):
                pass

        with tag("body"):
            with tag("ul", klass="navbar"):
                with tag("li"):
                    with tag("a", href="index.html"):
                        text("Home")

                with tag("li"):
                    with tag("a", href="list.html"):
                        text("List")

            with tag("div", klass="album-list"):
                for album in albums:
                    klass = f"cover-image {album['recommended by'].lower()}"
                    with tag("a",
                             href=f"albums/{album['name']}.html",
                             klass=klass):
                        doc.stag("img", src=album['image'])

    index_content = indent(doc.getvalue())

    with open("index.html", "w") as index_file:
        index_file.write(index_content)


def create_list(albums):
    doc, tag, text = Doc().tagtext()

    doc.asis("<!DOCTYPE html>")
    with tag("html"):
        with tag("head"):
            doc.line("title", "List")
            doc.stag("link", rel="icon", href="assets/icon.png")
            doc.stag("link", rel="stylesheet", href="static/stylesheet.css")

        with tag("body"):
            with tag("ul", klass="navbar"):
                with tag("li"):
                    with tag("a", href="index.html"):
                        text("Home")

                with tag("li"):
                    with tag("a", href="list.html"):
                        text("List")

            with tag("table"):
                with tag("tr"):
                    with tag("th"):
                        text("Image")
                    with tag("th"):
                        text("Name")
                    with tag("th"):
                        text("Artists")
                    with tag("th"):
                        text("Recommended by")
                    with tag("th"):
                        text("Rating")

                albums.sort(key=lambda x: x['rating'], reverse=True)

                for album in albums:
                    with tag("tr", klass=album['recommended by'].lower()):
                        with tag("td"):
                            with tag("a",
                                     href=f"albums/{album['name']}.html"):
                                doc.stag("img", src=album['image'],
                                         style="width: 5em;")

                        with tag("td"):
                            with tag("a", href=album['link']):
                                text(album['name'])

                        with tag("td"):
                            for i, artist in enumerate(album['artists']):
                                with tag("a", href=artist['link'],
                                         target="_blank"):
                                    text(artist['name'])

                                if i < len(album['artists']) - 1:
                                    text(" & ")

                        with tag("td", klass="text"):
                            text(album['recommended by'])

                        with tag("td"):
                            text(f"{album['rating']} / 10")

    index_content = indent(doc.getvalue())

    with open("list.html", "w") as index_file:
        index_file.write(index_content)


def create_album(album):
    doc, tag, text = Doc().tagtext()

    doc.asis("<!DOCTYPE html>")
    with tag("html"):
        with tag("head"):
            doc.line("title", f"Ratings - {album['name']}")
            doc.stag("link", rel="icon", href=album['image'])
            doc.stag("link", rel="stylesheet", href="../static/stylesheet.css")

        with tag("body"):
            with tag("ul", klass="navbar"):
                with tag("li"):
                    with tag("a", href="../index.html"):
                        text("Home")

                with tag("li"):
                    with tag("a", href="../list.html"):
                        text("List")

            with tag("h1"):
                with tag("a", href=album['link'], target="_blank"):
                    text(album['name'])

            with tag("h2"):
                for i, artist in enumerate(album['artists']):
                    with tag("a", href=artist['link'], target="_blank"):
                        text(artist['name'])

                    if i < len(album['artists']) - 1:
                        text(" & ")

            with tag("div",
                     klass=f"content {album['recommended by'].lower()}"):
                with tag("a", href=album['link'], target="_blank"):
                    doc.stag("img", src=album['image'])

                with tag("div", klass="text"):
                    _create_content(tag, text, album, doc)
    album_content = indent(doc.getvalue())

    with open(f"albums/{album['name']}.html", "w") as album_file:
        album_file.write(album_content)


def _create_content(tag, text, album, doc):
    with tag("b"):
        text("Recommended by ")
    text(album['recommended by'])

    doc.stag("br")
    with tag("b"):
        text("Rating ")
    text(f"{album['rating']} / 10")

    doc.stag("br")
    with tag("b"):
        text("Best Songs ")
    with tag("ul"):
        for song in album['best songs']:
            with tag("li"):
                with tag("a", href=song['link'],
                         target="_blank"):
                    text(song['name'])

    doc.stag("br")
    with tag("b"):
        text("Comment ")
    text(album['comment'])


def create_albums(albums):
    for album in albums:
        create_album(album)


if __name__ == "__main__":
    albums = []
    with open("data/data.json") as data_file:
        albums = json.load(data_file)

    create_index(albums)
    create_list(albums)
    create_albums(albums)
