import sqlite3

class Author:
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("Name must be of type str")
        if len(name) == 0:
            raise ValueError("Name must be longer than 0 characters")
        
        self._name = name
        self._id = None
        self.save()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def save(self):
        conn = sqlite3.connect('authors.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS authors (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
        ''')
        
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (self._name,))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()

# Example of creating a new author
new_author = Author("John Doe")
print(new_author.id)   # Outputs the id of the new author
print(new_author.name) # Outputs "John Doe"
