from json import load


class SongInfo:
    def __init__(
        self,
        identifier=0,
        title="",
        lyrics="",
        artist="",
        album="",
        release_year="",
        image="",
        link="",
    ):
        self.identifier = identifier
        self.title = title
        self.lyrics = lyrics
        self.artist = artist
        self.album = album
        self.release_year = release_year
        self.image = image
        self.link = link
        self.alternative_titles = []

    def add_alternative_title(self, title: str):
        self.alternative_titles.append(title)


class SongList:
    def __init__(self):
        self.dict = {}
        self.filename = "songs.json"

    def add_song(self, song: SongInfo):
        self.dict[song.title] = song

    def get_song_by_name(self, name: str):
        if name in self.dict.keys():
            return self.dict[name]
        for song in self.dict.values():
            if name.lower() in song.alternative_titles:
                return song
        return None

    def get_song_by_id(self, identifer: int):
        for song in self.dict.values():
            if song.identifier == identifer:
                return song

    def load_from_json(self, filename: str = ""):
        if not filename:
            filename = self.filename
        with open("data/" + filename, "r", encoding="utf8") as read_file:
            song_data = load(read_file)
        for song_object in song_data["songs"]:
            song = SongInfo(
                song_object["id"],
                song_object["title"],
                song_object["lyrics"],
                song_object["artist"],
                song_object["album"],
                song_object["release_year"],
                song_object["image"],
                song_object["link"],
            )
            self.add_song(song)
            if "alternative_titles" in song_object:
                for title in song_object["alternative_titles"]:
                    song.add_alternative_title(title)
