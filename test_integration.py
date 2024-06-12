import unittest
from unittest.mock import patch, mock_open
from app import app, get_db, init_db


class TestIntegracao(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        init_db()

    def tearDown(self):
        pass

    def test_register_missing_data(self):
        response = self.app.post(
            '/register', data=dict(), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Campo obrigat\xc3\xb3rio', response.data)

    def test_login_invalid_credentials(self):
        response = self.app.post('/login', data=dict(
            username='testuser', password='wrongpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'Credenciais inv\xc3\xa1lidas. Tente novamente.', response.data)

    def test_upload_file_without_login(self):
        response = self.app.post('/upload', data=dict(), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Por favor, fa\xc3\xa7a o login', response.data)


if __name__ == '__main__':
    unittest.main()

