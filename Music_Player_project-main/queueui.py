# queueui.py
import random
from baseui import BaseUI
from linkedlist import LinkedList

class QueueUI(BaseUI):
    def __init__(self, queue):
        self.queue = queue            # MusicQueue object

    def show_queue(self):
        while True:
            self.display_header("Now Playing")
            
            if self.queue.tracks.size == 0:
                print("The queue is empty. Load a playlist or add tracks first.")
                input("Press Enter to return...")
                return

            # Ensure current_node is set if queue exists
            if self.queue.current_node is None:
                self.queue.current_node = self.queue.tracks.head

            current_track = self.queue.current_node.data
            
            print(f"TRACK:  {current_track.title}")
            print(f"ARTIST: {current_track.artist}")
            print(f"ALBUM:  {current_track.album}")
            print(f"TIME:   {current_track.duration}")
            
            status = []
            if self.queue.shuffle: status.append("Shuffle: ON")
            else: status.append("Shuffle: OFF")
            
            if self.queue.repeat: status.append("Repeat: ON")
            else: status.append("Repeat: OFF")
            
            print(f"\nSTATUS: {' | '.join(status)}")
            
            print("\n[P] Play/Pause (Simulated)")
            print("[N] Next Track")
            print("[B] Previous Track")
            print("[S] Toggle Shuffle")
            print("[R] Toggle Repeat")
            print("[C] Clear Queue")
            print("[E] Exit Player")

            choice = input("Control: ").strip().lower()

            if choice == 'n':
                self.next_track()
            elif choice == 'b':
                self.previous_track()
            elif choice == 's':
                if self.queue.shuffle:
                    self.shuffle_off()
                else:
                    self.shuffle_on()
            elif choice == 'r':
                if self.queue.repeat:
                    self.repeat_off()
                else:
                    self.repeat_on()
            elif choice == 'c':
                self.clear_queue()
                return # Exit after clearing
            elif choice == 'e':
                break
            elif choice == 'p':
                print("...Playing...")
            else:
                print("Invalid key.")

    def next_track(self):
        if not self.queue.current_node:
            return

        if self.queue.current_node.next:
            self.queue.current_node = self.queue.current_node.next
        elif self.queue.repeat:
            print("Repeating queue...")
            self.queue.current_node = self.queue.tracks.head
        else:
            print("End of queue.")

    def previous_track(self):
        if not self.queue.current_node:
            return

        if self.queue.current_node.prev:
            self.queue.current_node = self.queue.current_node.prev
        else:
            print("Start of queue.")

    def shuffle_on(self):
        if self.queue.tracks.size < 2:
            print("Not enough tracks to shuffle.")
            return

        # 1. Save original order
        self.queue.original_order.from_list(self.queue.tracks.to_list())
        
        # 2. Shuffle
        items = self.queue.tracks.to_list()
        random.shuffle(items)
        
        # 3. Rebuild queue
        self.queue.tracks.from_list(items)
        self.queue.current_node = self.queue.tracks.head
        self.queue.shuffle = True
        print("Shuffle ON.")

    def shuffle_off(self):
        if not self.queue.shuffle:
            return

        # Restore original order
        self.queue.tracks.from_list(self.queue.original_order.to_list())
        self.queue.original_order.clear()
        
        self.queue.current_node = self.queue.tracks.head
        self.queue.shuffle = False
        print("Shuffle OFF.")

    def repeat_on(self):
        self.queue.repeat = True
        print("Repeat ON.")

    def repeat_off(self):
        self.queue.repeat = False
        print("Repeat OFF.")

    def clear_queue(self):
        self.queue.tracks.clear()
        self.queue.original_order.clear()
        self.queue.current_node = None
        self.queue.shuffle = False
        self.queue.repeat = False
        print("Queue cleared.")
