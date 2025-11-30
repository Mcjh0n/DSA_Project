import os
print("RUNNING FROM:", os.getcwd())

from models import Track, Playlist, MusicQueue
from linkedlist import LinkedList
from library import LibraryUI
from playlistui import PlaylistUI
from queueui import QueueUI

class Ui:
    def __init__(self):
        # 1. Initialize Data Structures
        self.library = LinkedList()      # LinkedList of Track objects
        self.playlists = LinkedList()    # LinkedList of Playlist objects
        self.queue = MusicQueue()        # The main Queue object
        self.albums = LinkedList()

        # 2. Initialize UI Managers
        self.library_ui = LibraryUI(self.library, self.playlists, self.albums)
        self.library_ui.load_library()
        
        # UPDATE: Pass self.queue here so we can load playlists into the queue
        self.playlist_ui = PlaylistUI(self.playlists, self.library, self.queue)
        
        self.queue_ui = QueueUI(self.queue)

    def mainmenu(self):
        while True:
            print("\n--- Music Player ---")
            print("1. View Music Library")
            print("2. Add Track")
            print("3. Create Playlist")
            print("4. View Playlists")
            print("5. Play Queue")
            print("6. Search Track")
            print("7. Import Tracks")
            print("8. Exit")

            choice = input("Enter choice: ")

            if choice == "1":
                self.library_ui.show_library()
            elif choice == "2":
                self.library_ui.add_track()
            elif choice == "3":
                self.playlist_ui.create_playlist()
            elif choice == "4":
                self.playlist_ui.show_playlists()
            elif choice == "5":
                self.queue_ui.show_queue()
            elif choice ==  "6":
                self.library_ui.search_track()
            elif choice == "7":
                self.library_ui.import_tracks()
            elif choice == "8":
                print("Exiting...")
                break
            else:
                print("Invalid input!")
                continue

ui = Ui()
ui.mainmenu()
