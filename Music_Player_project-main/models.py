from linkedlist import LinkedList

class Track:
    def __init__(self, title, artist, adds, album, duration):
        self.title = title
        self.artist = artist
        self.adds = adds
        self.album = album
        self.duration = duration

class Playlist:
    def __init__(self, name):
        self.name = name
        self.tracks = LinkedList()         
        self.total_duration = "00:00"

class MusicQueue:
    def __init__(self):
        self.tracks = LinkedList()
        self.current_node = None
        self.repeat = False
        self.shuffle = False
        self.original_order = LinkedList()
        
class Album:
    def __init__(self, name):
        self.name = name
        self.tracks = LinkedList()

