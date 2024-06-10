# 1. Teste de Cadastro de Usuário

import unittest

class TestRegistration(unittest.TestCase):
    def setUp(self):
        self.users = {}

    def test_user_registration(self):
        username = "testuser"
        password = "testpassword"
        self.register_user(username, password)
        self.assertIn(username, self.users)
        self.assertEqual(self.users[username], password)

    def register_user(self, username, password):
        self.users[username] = password

if __name__ == '__main__':
    unittest.main()

# 2 Teste de Cadastro com Senhas Diferentes

class TestRegistration(unittest.TestCase):
    def setUp(self):
        self.users = {}

    def test_registration_with_different_passwords(self):
        username = "testuser"
        password1 = "password1"
        password2 = "password2"
        self.register_user(username, password1, password2)
        self.assertNotIn(username, self.users)

    def register_user(self, username, password1, password2):
        if password1 == password2:
            self.users[username] = password1

if __name__ == '__main__':
    unittest.main()

# 3. Teste de Login de Usuário

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.logged_in_user = None

    def test_user_login(self):
        username = "testuser"
        password = "testpassword"
        self.login_user(username, password)
        self.assertEqual(self.logged_in_user, username)

    def login_user(self, username, password):
        if password == "testpassword":  # Simulação de verificação da senha
            self.logged_in_user = username

if __name__ == '__main__':
    unittest.main()

# 4. Teste de Login com Senha Incorreta

class TestLogin(unittest.TestCase):
    def setUp(self):
        self.logged_in_user = None

    def test_login_with_incorrect_password(self):
        username = "testuser"
        password = "wrongpassword"
        self.login_user(username, password)
        self.assertIsNone(self.logged_in_user)

    def login_user(self, username, password):
        if password == "testpassword":  # Simulação de verificação da senha
            self.logged_in_user = username

if __name__ == '__main__':
    unittest.main()

# 5 Teste de Upload e Download com Criptografia

import io
from encrypt_decrypt import encrypt_file, decrypt_file

class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db = get_db()
            db.execute("DELETE FROM users")
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       ("testuser", generate_password_hash("testpassword")))
            db.commit()

    def test_upload_and_download_file_with_encryption(self):
        # Login do usuário
        with self.app.session_transaction() as sess:
            sess['username'] = 'testuser'

        # Upload do arquivo
        response = self.app.post('/upload', content_type='multipart/form-data', data=dict(
            file=(io.BytesIO(b"this is a test"), "test.txt")
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # Download do arquivo
        response = self.app.get('/download/test.txt', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Descriptografa o conteúdo do arquivo baixado para verificação
        decrypted_content = decrypt_file(io.BytesIO(response.data))
        self.assertEqual(decrypted_content, b"this is a test")  # Supondo que o conteúdo do arquivo esteja correto

if __name__ == '__main__':
    unittest.main()

