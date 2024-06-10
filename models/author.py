from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self._id = id
        self.name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        if not isinstance(id, int):
            raise TypeError("id must be of type int")
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be of type str")
        if len(name) == 0:
            raise ValueError("name must be longer than 0 characters")
        if hasattr(self, '_name'):
            raise AttributeError("name cannot be changed once set")
        self._name = name

    @property
    def articles(self):
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.id, a.title, a.content, a.author_id, a.magazine_id
            FROM articles a
            JOIN authors au ON a.author_id = au.id
            WHERE au.id = ?
        ''', (self.id,))
        article_info = cursor.fetchall()
        conn.close()
        if article_info:
            return [Article(article["id"], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in article_info]
        else:
            return []

    @property
    def magazines(self):
        from models.magazine import Magazine
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT m.id, m.name, m.category
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        ''', (self.id,))
        magazine_info = cursor.fetchall()
        conn.close()
        if magazine_info:
            return [Magazine(magazine["id"], magazine['name'], magazine['category']) for magazine in magazine_info]
        else:
            return []

    def __repr__(self):
        article_titles = ", ".join([article.title for article in self.articles]) if self.articles else "None"
        magazine_titles = ", ".join([magazine.name for magazine in self.magazines]) if self.magazines else "None"
        return f'<Author: {self.name} | id: {self.id} | MAGAZINES:{magazine_titles} | ARTICLES:{article_titles}>'