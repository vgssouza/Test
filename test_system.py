import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from app import app, get_db, init_db

# Define a classe de testes de sistema que herda de unittest.TestCase
class TestSistema(unittest.TestCase):

    # Método setUp é executado antes de cada teste
    def setUp(self):
        # Cria uma instância do WebDriver para o Chrome
        self.driver = webdriver.Chrome()
        # Navega para a URL da aplicação local
        self.driver.get('http://localhost:5000')
        # Inicializa o banco de dados
        init_db()

    # Método tearDown é executado após cada teste
    def tearDown(self):
        # Fecha o navegador
        self.driver.quit()

    # Teste para registrar um usuário e fazer login
    def test_register_and_login(self):
        driver = self.driver
        # Clica no link para registro
        driver.find_element_by_link_text('Registre-se aqui').click()
        # Encontra os campos de username e password
        username = driver.find_element_by_name('username')
        password = driver.find_element_by_name('password')
        # Preenche os campos de username e password
        username.send_keys('testuser')
        password.send_keys('testpassword')
        # Envia o formulário
        password.send_keys(Keys.RETURN)
        # Verifica se a mensagem de sucesso está na página
        assert 'Arquivos disponíveis para download' in driver.page_source

    # Teste para fazer upload de um arquivo
    def test_upload_file(self):
        driver = self.driver
        # Registra um usuário como no teste anterior
        driver.find_element_by_link_text('Registre-se aqui').click()
        username = driver.find_element_by_name('username')
        password = driver.find_element_by_name('password')
        username.send_keys('testuser')
        password.send_keys('testpassword')
        password.send_keys(Keys.RETURN)
        # Encontra o campo de upload de arquivo e envia um arquivo
        driver.find_element_by_name('file').send_keys('path_to_file')
        # Clica no botão de upload
        driver.find_element_by_xpath("//button[contains(text(),'Upload')]").click()
        # Verifica se a mensagem de sucesso está na página
        assert 'File uploaded to Azure' in driver.page_source

    # Teste para fazer download de um arquivo
    def test_download_file(self):
        driver = self.driver
        # Registra um usuário como no teste anterior
        driver.find_element_by_link_text('Registre-se aqui').click()
        username = driver.find_element_by_name('username')
        password = driver.find_element_by_name('password')
        username.send_keys('testuser')
        password.send_keys('testpassword')
        password.send_keys(Keys.RETURN)
        # Clica no link para fazer download do arquivo
        driver.find_element_by_link_text('file_name').click()
        # Verifica se a mensagem de sucesso está na página
        assert 'File downloaded successfully' in driver.page_source

# Permite que o script de teste seja executado diretamente
if __name__ == '__main__':
    unittest.main()
