import unittest
from .models import db, Post
from .database_config import DATABASE_URI

class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Konfigurasi basis data untuk pengujian
        self.app = Warmindo()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
        db.init_app(self.app)

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        with self.app.app_context():
            post = Post(title='Test Post', content='This is a test post.')
            db.session.add(post)
            db.session.commit()

            saved_post = Post.query.filter_by(title='Test Post').first()
            self.assertIsNotNone(saved_post)
            self.assertEqual(saved_post.title, 'Test Post')
            self.assertEqual(saved_post.content, 'This is a test post.')

if __name__ == '__main__':
    unittest.main()