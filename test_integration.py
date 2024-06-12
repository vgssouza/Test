import unittest
from unittest.mock import patch, mock_open
from app import app, get_db, init_db

# Define a classe de testes de integração que herda de unittest.TestCase
class TestIntegracao(unittest.TestCase):

    # Método setUp é executado antes de cada teste
    def setUp(self):
        # Cria um cliente de teste para a aplicação Flask
        self.app = app.test_client()
        # Inicializa o banco de dados
        init_db()

    # Método tearDown é executado após cada teste
    def tearDown(self):
        pass  # Não faz nada atualmente, mas pode ser usado para limpar recursos

    # Teste para verificar se o registro falha quando dados obrigatórios estão ausentes
    def test_register_missing_data(self):
        response = self.app.post(
            '/register', data=dict(), follow_redirects=True)
        # Verifica se a resposta HTTP é 200 OK
        self.assertEqual(response.status_code, 200)
        # Verifica se a mensagem de campo obrigatório ausente está na resposta
        self.assertIn(b'Campo obrigat\xc3\xb3rio', response.data)

    # Teste para verificar se o login falha com credenciais inválidas
    def test_login_invalid_credentials(self):
        response = self.app.post('/login', data=dict(
            username='testuser', password='wrongpassword'
        ), follow_redirects=True)
        # Verifica se a resposta HTTP é 200 OK
        self.assertEqual(response.status_code, 200)
        # Verifica se a mensagem de credenciais inválidas está na resposta
        self.assertIn(
            b'Credenciais inv\xc3\xa1lidas. Tente novamente.', response.data)

    # Teste para verificar se o upload de arquivos falha sem estar logado
    def test_upload_file_without_login(self):
        response = self.app.post('/upload', data=dict(), follow_redirects=True)
        # Verifica se a resposta HTTP é 200 OK
        self.assertEqual(response.status_code, 200)
        # Verifica se a mensagem de login necessário está na resposta
        self.assertIn(b'Por favor, fa\xc3\xa7a o login', response.data)

# Permite que o script de teste seja executado diretamente
if __name__ == '__main__':
    unittest.main()
