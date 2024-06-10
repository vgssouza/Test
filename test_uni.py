import unittest
from app import app, get_db
from werkzeug.security import generate_password_hash

# 1. Teste de Registro de Usuário

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        # Configura o cliente de teste e limpa o banco de dados antes de cada teste
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db = get_db()
            db.execute("DELETE FROM users")
            db.commit()

    def test_register_user(self):
        # Envia um POST request para a rota de registro com dados de usuário
        response = self.app.post('/register', data=dict(
            username="testuser",
            password="testpassword"
        ), follow_redirects=True)
        
        # Verifica se o registro foi bem-sucedido
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registro realizado com sucesso!', response.data)

if __name__ == '__main__':
    unittest.main()

# 2. Teste de Login de Usuário

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        # Configura o cliente de teste e adiciona um usuário no banco de dados antes de cada teste
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db = get_db()
            db.execute("DELETE FROM users")
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       ("testuser", generate_password_hash("testpassword")))
            db.commit()

    def test_login_user(self):
        # Envia um POST request para a rota de login com credenciais do usuário
        response = self.app.post('/login', data=dict(
            username="testuser",
            password="testpassword"
        ), follow_redirects=True)
        
        # Verifica se o login foi bem-sucedido e se o usuário foi redirecionado para a página inicial
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'index', response.data)  # suposição de que a página inicial contém a palavra "index"

if __name__ == '__main__':
    unittest.main()

#3. Teste de Upload de Arquivo

import io

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        # Configura o cliente de teste e adiciona um usuário no banco de dados antes de cada teste
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db = get_db()
            db.execute("DELETE FROM users")
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       ("testuser", generate_password_hash("testpassword")))
            db.commit()

    def test_upload_file(self):
        # Simula uma sessão de usuário logado
        with self.app.session_transaction() as sess:
            sess['username'] = 'testuser'
        
        # Envia um POST request para a rota de upload com um arquivo de teste
        response = self.app.post('/upload', content_type='multipart/form-data', data=dict(
            file=(io.BytesIO(b"this is a test"), "test.txt")
        ), follow_redirects=True)
        
        # Verifica se o upload foi bem-sucedido
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

#4. Teste de Download de Arquivo

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        # Configura o cliente de teste e adiciona um usuário no banco de dados antes de cada teste
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db = get_db()
            db.execute("DELETE FROM users")
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       ("testuser", generate_password_hash("testpassword")))
            db.commit()

    def test_download_file(self):
        # Simula uma sessão de usuário logado
        with self.app.session_transaction() as sess:
            sess['username'] = 'testuser'
        
        # Primeiro, faz o upload do arquivo de teste
        self.app.post('/upload', content_type='multipart/form-data', data=dict(
            file=(io.BytesIO(b"this is a test"), "test.txt")
        ), follow_redirects=True)
        
        # Em seguida, faz o download do arquivo
        response = self.app.get('/download/test.txt', follow_redirects=True)
        
        # Verifica se o download foi bem-sucedido e se o conteúdo do arquivo está correto
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"this is a test")  # Supondo que não haja criptografia para este teste

if __name__ == '__main__':
    unittest.main()

#5. Teste de Rota Protegida

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        # Configura o cliente de teste
        self.app = app.test_client()
        self.app.testing = True

    def test_protected_route(self):
        # Tenta acessar a rota inicial sem estar autenticado
        response = self.app.get('/', follow_redirects=True)
        
        # Verifica se o usuário foi redirecionado para a página de login
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)  # Supondo que a página de login contém a palavra "Login"

if __name__ == '__main__':
    unittest.main()

