import unittest
from models.author import Author
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author = Author("John Doe")
        self.assertIsInstance(author.id, int)
        self.assertEqual(author.name, "John Doe")

    def test_magazine_creation(self):
        magazine = Magazine("Tech Today", "Technology")
        self.assertIsInstance(magazine.id, int)
        self.assertEqual(magazine.name, "Tech Today")
        self.assertEqual(magazine.category, "Technology")

if __name__ == '__main__':
    unittest.main()
