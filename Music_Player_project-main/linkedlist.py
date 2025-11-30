

class Node:
    def __init__(self, data):
        self.data = data        # track or playlist object
        self.next = None
        self.prev = None        # doubly linked list for easy backwards navigation


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0      



    # ADD NODE AT END 
    # this method adds a new node with the given data at the end of the linked list.
    # -------------------------------------------------------
    def add(self, data):
        new_node = Node(data)


        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node     # current tail -> new
            new_node.prev = self.tail     # new prev -> old tail
            self.tail = new_node          # update tail

        self.size += 1



    # REMOVE BY INDEX
    # THis method removes a node at a specific index in the linked list.
    # -----------------------------------------------------------
    
    def remove_at(self, index):
        if index < 0 or index >= self.size:
            return False

        current = self.head
        for _ in range(index):
            current = current.next

        # unlink current node
        if current.prev:     # middle or tail
            current.prev.next = current.next
        else:
            self.head = current.next      # removing head

        if current.next:     # middle or head
            current.next.prev = current.prev
        else:
            self.tail = current.prev      # removing tail

        self.size -= 1
        return True



    # GET DATA BY INDEX
    # This method retrieves the data at a specific index in the linked list.
    # -----------------------------------------------------------
    
    def get(self, index):
        if index < 0 or index >= self.size:
            return None

        current = self.head
        for _ in range(index):
            current = current.next

        return current.data



    # ITERATOR (HOW YOU LOOP OVER IT)
    # This method allows you to iterate over the linked list using a for loop.
    # -----------------------------------------------------------
    
    def iter(self):
        current = self.head
        while current:
            yield current.data
            current = current.next



    # FIND INDEX OF A DATA OBJECT
    # This method returns the index of the first occurrence of the specified data in the linked list.
    # ------------------------------------------------------------
    
    def index_of(self, data):
        current = self.head
        idx = 0
        while current:
            if current.data == data:
                return idx
            current = current.next
            idx += 1
        return -1


    # CLEAR THE LINKED LIST
    # This method clears the linked list by setting head, tail, and size to their initial values.
    # -----------------------------------------------------------
    
    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0


    
    # CONVERT TO PYTHON LIST (ONLY FOR JSON USE)
    # Allowed because JSON saving is exempt from the rule.
    # ------------------------------------------------------------

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result



    # REBUILD LINKED LIST FROM PYTHON LIST (for loading JSON)
    # This method clears the current list and appends each item from the provided list. 
    # -----------------------------------------------------------
    
    def from_list(self, items):
        self.clear()    
        for item in items:
            self.add(item)
            
    
    # CLEAR THE LINKED LIST
    # This method clears the linked list by setting head to None.
    # -----------------------------------------------------------        
    def clear(self):
        self.head = None

