import json
from baseui import BaseUI
from models import Track
from linkedlist import LinkedList


class LibraryUI(BaseUI):
    def __init__(self, library, playlists, albums):
        self.library = library
        self.playlists = playlists
        self.albums = albums
        

    def validate_duration(self, raw):
        while True:
            if raw.count(":") != 1:
                print("Invalid format. Use mm:ss.")
                raw = input("Enter duration: ")
                continue

            minutes_text, seconds_text = raw.split(":")

            if not minutes_text.isdigit():
                print("Minutes must be numbers.")
                raw = input("Enter duration: ")
                continue

            if not seconds_text.isdigit():
                print("Seconds must be numbers.")
                raw = input("Enter duration: ")
                continue

            minutes = int(minutes_text)
            seconds = int(seconds_text)

            if seconds >= 60:
                print("Seconds must be below 60.")
                raw = input("Enter duration: ")
                continue

            return f"{minutes:02d}:{seconds:02d}"

    def show_library(self):
        if self.library.head is None:
            print("Your library is empty.")
            return

        tracks = []
        node = self.library.head
        while node is not None:
            tracks.append(node.data)
            node = node.next

        def compare(a, b):
            if a.title.lower() < b.title.lower(): 
                return -1
            if a.title.lower() > b.title.lower():
                return 1

            if a.artist.lower() < b.artist.lower():
                return -1
            if a.artist.lower() > b.artist.lower():
                return 1

            if a.album.lower() < b.album.lower():
                return -1
            if a.album.lower() > b.album.lower():
                return 1

            if a.duration < b.duration:
                return -1
            if a.duration > b.duration:
                return 1

            return 0

        def merge(left, right):
            result = []
            i = 0
            j = 0

            while i < len(left) and j < len(right):
                if compare(left[i], right[j]) <= 0:
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1

            while i < len(left):
                result.append(left[i])
                i += 1

            while j < len(right):
                result.append(right[j])
                j += 1

            return result

        def mergee(arr):
            if len(arr) <= 1:
                return arr

            mid = len(arr) // 2
            left = mergee(arr[:mid])
            right = mergee(arr[mid:])

            return merge(left, right)

        sorted_tracks = mergee(tracks)

        print("\n--- MUSIC LIBRARY ---")

        index = 1
        for track in sorted_tracks:
            add_artists = track.adds.to_list()
            if len(add_artists) > 0:
                artist_string = track.artist + ", " + ", ".join(add_artists)
            else:
                artist_string = track.artist
                
            print(f"[{index}]")
            print(f"Title: {track.title}")
            print(f"Artist: {artist_string}")
            print(f"Album: {track.album}")
            print(f"Duration: {track.duration}\n")
            index += 1

    def add_track(self):
        add_artist = LinkedList()

        t = input("please add the name of your track: ")
        a = input("please add the artist of your track: ")
        ad = input("please add the additional artist of your track (optional, press s to skip): ")

        if ad.lower() != 's':
            temp = ""
            for char in ad:
                if char != ',':
                    temp += char
                else:
                    cleaned = temp.strip()
                    if cleaned != "":
                        add_artist.add(cleaned)
                    temp = ""
            cleaned = temp.strip()
            if cleaned != "":
                add_artist.add(cleaned)

        al = input("please add the album of your track: ")

        d = input("please add the duration of your track [mm:ss]: ")
        d = self.validate_duration(d)

        tr = Track(t, a, add_artist, al, d)
        self.library.add(tr)
        self.add_to_album(tr)
        self.save_library()


        print("\nTrack added!")
    
    def search_track(self):
        query = input("Enter track title to search: ").strip().lower()
        

        if not query:
            print("Search cancelled.")
            return

        exact_matches = []
        partial_matches = []

        node = self.library.head
        while node is not None:
            title_lower = node.data.title.lower()

            if title_lower == query:
                exact_matches.append(node.data)
            elif query in title_lower:
                partial_matches.append(node.data)

            node = node.next

        results = exact_matches + partial_matches

        if len(results) == 0:
            print("No matching tracks found.")
            return

        page = 1
        page_size = 10

        while True:
            page_items = self.paginate(results, page_size, page)

            print(f"\n--- Search Results (Page {page}) ---\n")

            index = (page - 1) * page_size + 1

            for track in page_items:
                add_artists = track.adds.to_list()
                if len(add_artists) > 0:
                    artist_string = track.artist + ", " + ", ".join(add_artists)
                else:
                    artist_string = track.artist

                print(f"[{index}]")
                print(f"Title: {track.title}")
                print(f"Artist: {artist_string}")
                print(f"Album: {track.album}")
                print(f"Duration: {track.duration}\n")

                index += 1

            print("[N] Next Page")
            print("[P] Previous Page")
            print("[E] Exit")

            choice = input("Choose: ").strip().lower()

            if choice == "n":
                if page * page_size < len(results):
                    page += 1
                else:
                    print("No more pages.")
            elif choice == "p":
                if page > 1:
                    page -= 1
                else:
                    print("Already at first page.")
            elif choice == "e":
                return
            else:
                print("Invalid option.")

    def add_to_album(self, track):
        node = self.albums.head
        while node is not None:
            if node.data.name.lower() == track.album.lower():
                node.data.tracks.add(track)
                return
            node = node.next

        from models import Album
        new_album = Album(track.album)
        new_album.tracks.add(track)
        self.albums.add(new_album)


    def import_tracks(self):
        filename = input("Enter JSON filename to import: ").strip()

        try:
            with open(filename, "r") as file:
                data = json.load(file)
        except:
            print("Failed to open JSON file.")
            return

        count = 0

        for item in data:
            t = item.get("title", "")
            a = item.get("artist", "")
            adds_list = item.get("additional_artists", [])
            al = item.get("album", "")
            d = item.get("duration", "")

            adds = LinkedList()
            for x in adds_list:
                adds.add(x)

            tr = Track(t, a, adds, al, d)
            self.library.add(tr)
            self.add_to_album(tr)
            count += 1

        print(f"{count} tracks imported successfully.")
    
    
    def save_library(self):
        data = {"library": [], "albums": []}

        node = self.library.head
        while node is not None:
            track = node.data
            add_artists = track.adds.to_list()

            data["library"].append({
                "title": track.title,
                "artist": track.artist,
                "additional_artists": add_artists,
                "album": track.album,
                "duration": track.duration
            })

            node = node.next

        album_node = self.albums.head
        while album_node is not None:
            album = album_node.data
            track_titles = []
            tnode = album.tracks.head
            while tnode is not None:
                track_titles.append(tnode.data.title)
                tnode = tnode.next

            data["albums"].append({
                "name": album.name,
                "tracks": track_titles
            })

            album_node = album_node.next

        with open("songs.json", "w") as file:
            json.dump(data, file)

    
        
    def load_library(self):
        try:
            with open("songs.json", "r") as file:
                data = json.load(file)
        except:
            return

        self.library.clear()
        self.albums.clear()



        for item in data.get("library", []):
            t = item["title"]
            a = item["artist"]
            adds_list = item["additional_artists"]
            al = item["album"]
            d = item["duration"]

            adds = LinkedList()
            for x in adds_list:
                adds.add(x)

            tr = Track(t, a, adds, al, d)
            self.library.add(tr)
            self.add_to_album(tr)


