import time
from baseui import BaseUI
from linkedlist import LinkedList
from models import Playlist

class PlaylistUI(BaseUI):
    def __init__(self, playlists, library, queue=None):
        self.playlists = playlists    # LinkedList of Playlist objects
        self.library = library        # LinkedList of Track objects
        self.queue = queue            # MusicQueue object

    def calculate_duration(self, tracks_list):
        total_seconds = 0
        current = tracks_list.head
        while current:
            try:
                parts = current.data.duration.split(":")
                minutes = int(parts[0])
                seconds = int(parts[1])
                total_seconds += (minutes * 60) + seconds
            except:
                pass # skip invalid durations
            current = current.next
        
        m, s = divmod(total_seconds, 60)
        return f"{m:02d}:{s:02d}"

    def create_playlist(self):
        self.display_header("Create Playlist")
        name = input("Enter playlist name: ").strip()
        
        if not name:
            print("Name cannot be empty.")
            return

        # Check for duplicates
        current = self.playlists.head
        while current:
            if current.data.name.lower() == name.lower():
                print("A playlist with this name already exists.")
                return
            current = current.next

        new_playlist = Playlist(name)
        self.playlists.add(new_playlist)
        print(f"Playlist '{name}' created!")

    def show_playlists(self):
        if self.playlists.size == 0:
            print("\nNo playlists created yet.")
            return

        all_playlists = self.playlists.to_list()
        page = 1
        page_size = 5

        while True:
            self.display_header(f"Playlists (Page {page})")
            
            items = self.paginate(all_playlists, page_size, page)
            index = (page - 1) * page_size + 1

            for plist in items:
                print(f"[{index}] {plist.name} (Tracks: {plist.tracks.size}, Duration: {plist.total_duration})")
                index += 1

            print("\n[N] Next Page | [P] Previous Page | [S] Select Playlist | [E] Exit")
            choice = input("Choice: ").strip().lower()

            if choice == 'n':
                if page * page_size < len(all_playlists):
                    page += 1
                else:
                    print("No more pages.")
            elif choice == 'p':
                if page > 1:
                    page -= 1
                else:
                    print("Already on first page.")
            elif choice == 's':
                self.select_playlist(all_playlists)
                # Refresh list (in case duration/counts changed)
                all_playlists = self.playlists.to_list() 
            elif choice == 'e':
                break
            else:
                print("Invalid choice.")

    def select_playlist(self, all_playlists):
        try:
            sel_index = int(input("Enter playlist number to select: ")) - 1
            if 0 <= sel_index < len(all_playlists):
                selected_playlist = all_playlists[sel_index]
                self.playlist_details(selected_playlist)
            else:
                print("Invalid index.")
        except ValueError:
            print("Please enter a number.")

    def playlist_details(self, plist):
        while True:
            self.display_header(f"Playlist: {plist.name}")
            print(f"Total Duration: {plist.total_duration}")
            print(f"Total Tracks: {plist.tracks.size}")
            print("-" * 20)
            
            # Show first 5 tracks as preview
            current = plist.tracks.head
            count = 0
            while current and count < 5:
                print(f"{count + 1}. {current.data.title} - {current.data.artist}")
                current = current.next
                count += 1
            if plist.tracks.size > 5:
                print("... (select 'View/Remove Tracks' to see all)")

            print("\n1. Play Playlist (Load to Queue)")
            print("2. View/Remove Tracks")
            print("3. Add Track")
            print("4. Back")

            choice = input("Enter choice: ")

            if choice == "1":
                self.play_playlist(plist)
            elif choice == "2":
                self.manage_tracks(plist)
            elif choice == "3":
                self.add_track_to_playlist(plist)
            elif choice == "4":
                break
            else:
                print("Invalid choice.")

    def play_playlist(self, plist):
        if not self.queue:
            print("Error: Queue system not connected (Check main.py).")
            return

        if plist.tracks.size == 0:
            print("Playlist is empty.")
            return

        # Clear queue and add all tracks
        self.queue.tracks.clear()
        self.queue.original_order.clear()
        self.queue.repeat = False
        self.queue.shuffle = False
        self.queue.current_node = None

        current = plist.tracks.head
        while current:
            self.queue.tracks.add(current.data)
            current = current.next
        
        # Set to start
        self.queue.current_node = self.queue.tracks.head
        print(f"Loaded '{plist.name}' into queue! Go to Main Menu -> Play Queue to listen.")

    def add_track_to_playlist(self, plist):
        # 1. Convert library to list for easy indexing
        all_tracks = self.library.to_list()
        
        if not all_tracks:
            print("Library is empty. Go add tracks in the Main Menu first.")
            return

        page = 1
        page_size = 10 

        while True:
            self.display_header(f"Add Tracks to '{plist.name}' (Page {page})")
            
            # 2. Get items for current page
            items = self.paginate(all_tracks, page_size, page)
            
            # Calculate display index (e.g. 1, 11, 21...)
            start_index = (page - 1) * page_size + 1
            
            for i, track in enumerate(items):
                print(f"[{start_index + i}] {track.title} - {track.artist} ({track.duration})")

            print("\nCOMMANDS:")
            print(" - Enter numbers to add (e.g., '1, 3, 5')")
            print(" - [N] Next Page")
            print(" - [P] Previous Page")
            print(" - [B] Back to Playlist")

            raw_input = input("Select: ").strip().lower()

            if raw_input == 'b':
                break
            elif raw_input == 'n':
                if page * page_size < len(all_tracks):
                    page += 1
                else:
                    print("No more pages.")
            elif raw_input == 'p':
                if page > 1:
                    page -= 1
                else:
                    print("Already on first page.")
            else:
                # 3. Handle Number Input (e.g., "1,2")
                try:
                    # Split by comma to allow multiple adds
                    choices = raw_input.split(',')
                    added_count = 0
                    
                    for choice in choices:
                        choice = choice.strip()
                        if not choice.isdigit(): 
                            continue
                            
                        idx = int(choice) - 1 # Convert 1-based to 0-based index
                        
                        if 0 <= idx < len(all_tracks):
                            track_to_add = all_tracks[idx]
                            plist.tracks.add(track_to_add)
                            added_count += 1
                        else:
                            print(f"Skipping invalid number: {choice}")

                    if added_count > 0:
                        print(f"Successfully added {added_count} track(s)!")
                        # Recalculate duration immediately
                        plist.total_duration = self.calculate_duration(plist.tracks)
                    else:
                        print("No valid tracks selected.")

                except Exception as e:
                    print(f"Error: {e}")

    def manage_tracks(self, plist):
        if plist.tracks.size == 0:
            print("No tracks to manage.")
            return

        while True:
            tracks_list = plist.tracks.to_list()
            self.display_header(f"Tracks in {plist.name}")
            
            for i, track in enumerate(tracks_list):
                print(f"[{i+1}] {track.title} - {track.duration}")

            print("\nEnter number to remove, or 'B' to back.")
            choice = input("Choice: ").strip().lower()

            if choice == 'b':
                break
            
            try:
                idx = int(choice) - 1
                if plist.tracks.remove_at(idx):
                    print("Track removed.")
                    plist.total_duration = self.calculate_duration(plist.tracks)
                else:
                    print("Invalid index.")
            except ValueError:
                print("Invalid input.")
