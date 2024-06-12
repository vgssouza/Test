import unittest
from unittest.mock import patch, mock_open
from app import app, get_db, init_db


class TestUnitarios(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        init_db()

    def tearDown(self):
        pass

    def test_get_db(self):
        with app.app_context():
            db = get_db()
            self.assertIsNotNone(db)

    def test_init_db(self):
        with app.app_context():
            init_db()
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users')
            result = cursor.fetchall()
            self.assertEqual(len(result), 0)

    def test_register_success(self):
        response = self.app.post('/register', data=dict(
            username='testuser', password='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registro realizado com sucesso!', response.data)

    def test_register_existing_user(self):
        response = self.app.post('/register', data=dict(
            username='testuser', password='testpassword'
        ), follow_redirects=True)
        response = self.app.post('/register', data=dict(
            username='testuser', password='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Nome de usu\xc3\xa1rio j\xc3\xa1 existe. Escolha outro nome.', response.data)

    def test_login_success(self):
        self.app.post('/register', data=dict(
            username='testuser', password='testpassword'
        ), follow_redirects=True)
        response = self.app.post('/login', data=dict(
            username='testuser', password='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Arquivos dispon\xc3\xadveis para download', response.data)


if __name__ == '__main__':
    unittest.main()
