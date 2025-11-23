import os
import json

JSON_FILE = "playlist_data.json"


def time_to_seconds(duration: str) -> int:
    minutes, seconds = map(int, duration.split(":"))
    return minutes * 60 + seconds


def seconds_to_time(total_seconds: int) -> str:
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d}"


class Song:
    def __init__(self, title, artist, duration, album):
        self.title = title
        self.artist = artist
        self.duration = duration
        self.album = album

    def __str__(self):
        return f"{self.title} - {self.artist} ({self.duration}) [{self.album}]"

    def to_dict(self):
        return {
            "title": self.title,
            "artist": self.artist,
            "duration": self.duration,
            "album": self.album
        }


class Playlist:
    def __init__(self):
        self.songs = []
        self.current_index = 0
        self.load_json()

    def load_json(self):
        if not os.path.exists(JSON_FILE):
            return

        with open(JSON_FILE, "r") as f:
            try:
                data = json.load(f)
                for item in data:
                    self.songs.append(Song(
                        item["title"],
                        item["artist"],
                        item["duration"],
                        item["album"]
                    ))
            except json.JSONDecodeError:
                print("⚠ JSON file corrupted. Starting fresh.")

    def save_json(self):
        with open(JSON_FILE, "w") as f:
            json.dump([song.to_dict() for song in self.songs], f, indent=4)

    # ADD SONG
    def add_song(self, title, artist, duration, album):
        self.songs.append(Song(title, artist, duration, album))
        self.save_json()
        print("✔ Song added successfully!")

    # DELETE A SONG BY TITLE
    def delete_song_by_title(self, title):
        removed_any = False
        self.songs = [song for song in self.songs if not (song.title.lower() == title.lower())]
        self.save_json()
        print(f"✔ Deleted all songs with title: {title}")

    # ORIGINAL REMOVE BY INDEX
    def remove_song(self, index):
        if 0 <= index < len(self.songs):
            removed = self.songs.pop(index)
            self.save_json()
            print(f"✔ Removed: {removed}")
        else:
            print("❌ Invalid index")

    # VIEW
    def view_playlist(self):
        if not self.songs:
            print("Playlist is empty.")
            return

        print("\n--- PLAYLIST ---")
        for i, song in enumerate(self.songs):
            marker = " <--- current" if i == self.current_index else ""
            print(f"{i}. {song}{marker}")
        print("-----------------\n")

    # NEXT SONG
    def next_song(self):
        if not self.songs:
            print("Playlist empty.")
            return

        self.current_index = (self.current_index + 1) % len(self.songs)
        print(f"▶ Now playing: {self.songs[self.current_index]}")

    # PREVIOUS SONG
    def previous_song(self):
        if not self.songs:
            print("Playlist empty.")
            return

        self.current_index = (self.current_index - 1) % len(self.songs)
        print(f"▶ Now playing: {self.songs[self.current_index]}")

    # SORTING
    def sort_by_title(self):
        self.songs.sort(key=lambda s: s.title.lower())
        self.save_json()
        print("✔ Sorted by title")

    def sort_by_artist(self):
        self.songs.sort(key=lambda s: s.artist.lower())
        self.save_json()
        print("✔ Sorted by artist")

    def sort_by_album(self):
        self.songs.sort(key=lambda s: s.album.lower())
        self.save_json()
        print("✔ Sorted by album")

    # TOTAL DURATION
    def total_playlist_duration(self):
        total = sum(time_to_seconds(song.duration) for song in self.songs)
        return seconds_to_time(total)

    def total_album_duration(self, album_name):
        total = sum(
            time_to_seconds(song.duration)
            for song in self.songs
            if song.album.lower() == album_name.lower()
        )
        return seconds_to_time(total) if total > 0 else None


# MENU

def menu():
    playlist = Playlist()

    while True:
        print("""
===== MUSIC PLAYLIST (JSON STORAGE) =====
1. View playlist
2. Add song
3. Remove song by index
4. Next song
5. Previous song
6. Sort by title
7. Sort by artist
8. Sort by album
9. Total playlist duration
10. Total duration of an album
11. Delete songs by title
0. Exit
=========================================
""")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            playlist.view_playlist()

        elif choice == "2":
            title = input("Song title: ")
            artist = input("Artist: ")
            duration = input("Duration (mm:ss): ")
            album = input("Album: ")
            playlist.add_song(title, artist, duration, album)

        elif choice == "3":
            playlist.view_playlist()
            try:
                idx = int(input("Enter index to remove: "))
                playlist.remove_song(idx)
            except ValueError:
                print("❌ Invalid input")

        elif choice == "4":
            playlist.next_song()

        elif choice == "5":
            playlist.previous_song()

        elif choice == "6":
            playlist.sort_by_title()

        elif choice == "7":
            playlist.sort_by_artist()

        elif choice == "8":
            playlist.sort_by_album()

        elif choice == "9":
            total = playlist.total_playlist_duration()
            print(f"\n⏳ Total playlist duration: {total}\n")

        elif choice == "10":
            album = input("Enter album name: ")
            result = playlist.total_album_duration(album)
            if result:
                print(f"\n⏳ Total duration of '{album}': {result}\n")
            else:
                print(f"\n❌ Album '{album}' not found.\n")

        elif choice == "11":
            title = input("Enter song title to delete: ")
            playlist.delete_song_by_title(title)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("❌ Invalid option")


menu()
