from database.connection import get_db_connection
from models.magazine import Magazine
from models.author import Author

class Article:
    def __init__(self, article_id, title, content, author_id, magazine_id):
        self.id = article_id
        self._title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        if self.id is None:
            self.create_db_entry()

    @property
    def author(self):
        author_info = self.get_author_info_by_id(self.author_id)
        if author_info:
            return Author(author_info["id"], author_info['name'])
        else:
            return None

    @property
    def magazine(self):
        magazine_info = self.get_magazine_info_by_id(self.magazine_id)
        if magazine_info:
            return Magazine(magazine_info["id"], magazine_info['name'], magazine_info['category'])
        else:
            return None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        if not hasattr(self, '_title'):
            if isinstance(new_title, str) and 5 <= len(new_title) <= 50:
                self._title = new_title
            else:
                raise TypeError("Title must be a string with length between 5 and 50 characters")
        else:
            raise AttributeError("Title cannot be changed")

    def create_db_entry(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)', 
                       (self.title, self.content, self.author_id, self.magazine_id))
        self.id = cursor.lastrowid
        conn.commit()
        conn.close()

    @staticmethod
    def get_author_info_by_id(author_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (author_id,))
        author_info = cursor.fetchone()
        conn.close()
        return author_info

    @staticmethod
    def get_magazine_info_by_id(magazine_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (magazine_id,))
        magazine_info = cursor.fetchone()
        conn.close()
        return magazine_info

    def __repr__(self):
        author_info = self.get_author_info_by_id(self.author_id)
        author_name = author_info['name'] if author_info else "None"
        magazine_info = self.get_magazine_info_by_id(self.magazine_id)
        magazine_name = magazine_info['name'] if magazine_info else "None"
        return f'<Article: {self.title} | Author: {author_name} | Magazine: {magazine_name}>'